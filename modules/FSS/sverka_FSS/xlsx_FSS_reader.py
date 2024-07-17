import os
import pandas as pd

def xlsx_reader(conn, c, xlxs_dir):
    # Создааем таблицу в БД
    c.execute('''
    CREATE TABLE IF NOT EXISTS fss_base (
      'Имя_Файла',
      'ФИО',
      'СНИЛС'
    )
    ''')

    # Читаем картотеку
    for file in os.listdir(xlxs_dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            try:
                file_path = os.path.join(xlxs_dir, file)
                # Читаем файл, пропускаем первые 6 строк
                df = pd.read_excel(file_path, skiprows=4)
                df.fillna("", inplace=True)

                data = []
                for _, row in df.iterrows():

                    # Не пушим пустые записи
                    if type(row[2]) is float or row[2] == 'Общая сумма начислений в реестре:':
                        continue
                    # Получаем данные из таблицы
                    npers = format_snils(row[3])
                    if npers is None:
                        continue
                    else:
                        data.append((file, row[2], npers))

                c.executemany(
                    'INSERT INTO fss_base VALUES (:Имя_Файла, :ФИО, :СНИЛС)',
                    data)
                conn.commit()

            except Exception as e:
                print(e)

def format_snils(unvalid_snils):
    if unvalid_snils == '':
        return None

    snils_str = str(unvalid_snils)

    if '.' in snils_str:
        s = list(snils_str[:-2])
    else:
        s = list(snils_str)

    while len(s) != 11:
        s.insert(0, '0')

    s.insert(3, '-')
    s.insert(7, '-')
    s.insert(11, ' ')
    return "".join(s)