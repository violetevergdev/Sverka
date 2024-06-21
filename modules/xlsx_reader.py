import os
import pandas as pd

def xlxs_reader(conn, c, xlxs_dir):
    # Создааем таблицу в БД
    c.execute('''
    CREATE TABLE IF NOT EXISTS pfr_base (
      'Вид выплаты_pfr',
      'СНИЛС_pfr',
      'Фамилия_pfr',
      'Имя_pfr',
      'Отчество_pfr',
      'Дата рождения_pfr',
      'Сумма_pfr'
    )
    ''')

    # Читаем картотеку
    for file in os.listdir(xlxs_dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            try:
                file_path = os.path.join(xlxs_dir, file)
                # Читаем файл, пропускаем первые 6 строк
                df = pd.read_excel(file_path, skiprows=6, na_filter=False)

                for _, row in df.iterrows():
                    # Не пушим пустые записи
                    if row[1] == "":
                        continue
                    # Получаем данные из таблицы
                    data = {
                        'Вид_выплаты_pfr': row[2],
                        'СНИЛС_pfr': row[3].replace('\n\t\t', ""),
                        'Фамилия_pfr': row[4].split(",")[0].split()[0],
                        'Имя_pfr': row[4].split(",")[0].split()[1],
                        'Отчество_pfr': if_patronymic_exist(row),
                        'Дата_рождения_pfr': format_date(row[4].split(",")[1]),
                        'Сумма_pfr': row[5]
                    }

                    c.execute(
                        'INSERT INTO pfr_base VALUES (:Вид_выплаты_pfr, :СНИЛС_pfr, :Фамилия_pfr, :Имя_pfr, :Отчество_pfr, :Дата_рождения_pfr, :Сумма_pfr)',
                        data)
                    conn.commit()

            except Exception as e:
                print(e)


# Проверка на наличие отчества
def if_patronymic_exist(row):
    try:
        return row[4].split(",")[0].split()[2]
    except Exception:
        name = row[4].split(",")[0].split()[1]
        surname = row[4].split(",")[0].split()[0]
        print(f'{surname, name}: Отчество отсутсвует')


# Приводим даты в единый формат
def format_date(date):
    s = date.lstrip().replace('\n\t\t', "").split('.')
    return f'{s[2]}-{s[1]}-{s[0]}'