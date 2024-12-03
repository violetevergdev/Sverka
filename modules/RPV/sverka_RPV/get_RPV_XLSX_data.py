

def get_RPV_XLSX_data(df, db_curs, db_name, file=None):
    data = []
    for _, row in df.iterrows():
        # Не пушим пустые записи
        if row[1] == "":
            continue
        # Получаем данные из таблицы
        temp_data = {
            'Вид_выплаты_pfr': row[2],
            'СНИЛС_pfr': row[3].replace('\n\t\t', ""),
            'Фамилия_pfr': row[4].split(",")[0].split()[0],
            'Имя_pfr': row[4].split(",")[0].split()[1],
            'Отчество_pfr': if_patronymic_exist(row),
            'Дата_рождения_pfr': format_date(row[4].split(",")[1]),
            'Сумма_pfr': row[5],
            'Район_pfr': file.replace('.xls', ''),
        }
        data.append(temp_data)

    db_curs.executemany(
        f'INSERT INTO {db_name} VALUES (:Вид_выплаты_pfr, :СНИЛС_pfr, :Фамилия_pfr, :Имя_pfr, :Отчество_pfr, :Дата_рождения_pfr, :Сумма_pfr, :Район_pfr)',
        data)

# Проверка на наличие отчества
def if_patronymic_exist(row):
    try:
        return row[4].split(",")[0].split()[2]
    except Exception:
        name = row[4].split(",")[0].split()[1]
        surname = row[4].split(",")[0].split()[0]
        print(surname, name, ': Отчество отсутсвует')


# Приводим даты в единый формат
def format_date(date):
    s = date.lstrip().replace('\n\t\t', "").split('.')
    new_date = s[2] + '-' + s[1] + '-' + s[0]
    return new_date
