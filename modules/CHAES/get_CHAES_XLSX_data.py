def get_CHAES_XLSX_data(df, db_curs, db_name, file=None):
    data = []
    for _, row in df.iterrows():
        # Не пушим пустые записи
        if row[1] == "":
            continue
        # Получаем данные из таблицы
        temp_data = {
            'СНИЛС_out': str(row[0]).strip(),
            'Фамилия_out': row[1],
            'Имя_out': row[2],
            'Отчество_out': row[3],
        }
        data.append(temp_data)

    db_curs.executemany(
        f'INSERT INTO {db_name} VALUES (:СНИЛС_out, :Фамилия_out, :Имя_out, :Отчество_out)',
        data)