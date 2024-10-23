from modules.Common.refactor_data import format_snils_with_fill_zero


def get_FSS_XLSX_data(df, db_curs, db_name, file):
    df.fillna("", inplace=True)

    data = []
    for _, row in df.iterrows():

        # Не пушим пустые записи
        if type(row[2]) is float or row[2] == 'Общая сумма начислений в реестре:':
            continue
        # Получаем данные из таблицы
        npers = format_snils_with_fill_zero(row[3])
        if npers is None:
            continue
        else:
            data.append((file, row[2], npers))

    db_curs.executemany(
        f'INSERT INTO {db_name} VALUES (:Имя_Файла, :ФИО, :СНИЛС)',
        data)
