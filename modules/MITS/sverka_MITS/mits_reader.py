import os
import pandas as pd


def mits_reader(conn, c, mits_dir):
    # Создаем таблицу в БД
    c.execute('''
        CREATE TABLE IF NOT EXISTS mits_base (
          'СНИЛС получателя',
          'ФИО получателя' ,
          'СНИЛС л-о',
          'ФИО л-о',
          'Дата смерти получателя',
          'Дата смерти л-о'
        )
        ''')

    # Считываем все CSV-файлы в один DataFrame
    df = pd.concat([pd.read_csv(os.path.join(mits_dir, file), sep=";", skiprows=1, encoding='windows-1251', header=None,
                                names=['СНИЛС получателя', 'ФИО получателя', 'СНИЛС л-о', 'ФИО л-о',
                                       'Дата смерти получателя', 'Дата смерти л-о'],
                                usecols=[6, 7, 8, 9, 10, 11]) for file in os.listdir(mits_dir) if
                    file.endswith(".csv")])

    # Форматируем СНИЛС
    df.fillna("", inplace=True)
    df['СНИЛС получателя'] = df['СНИЛС получателя'].apply(format_snils)
    df['ФИО получателя'] = df['ФИО получателя'].str.upper()
    df['СНИЛС л-о'] = df['СНИЛС л-о'].apply(format_snils)
    df['ФИО л-о'] = df['ФИО л-о'].str.upper()

    df['Дата смерти получателя'] = df['Дата смерти получателя'].apply(format_date)
    df['Дата смерти л-о'] = df['Дата смерти л-о'].apply(format_date)

    # Записываем DataFrame в БД
    df.to_sql('mits_base', conn, if_exists='append', index=False)
    conn.commit()


def format_snils(unvalid_snils):
    if unvalid_snils == "":
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


def format_date(date):
    if "-" in date or date == "":
        return date
    else:
        s = date.split('.')
        new_date = s[2] + '-' + s[1] + '-' + s[0]
        return new_date