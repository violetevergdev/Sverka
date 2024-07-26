
def get_FSS_XLSX_data(df, db_curs, db_name, file):
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

    db_curs.executemany(
        f'INSERT INTO {db_name} VALUES (:Имя_Файла, :ФИО, :СНИЛС)',
        data)

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