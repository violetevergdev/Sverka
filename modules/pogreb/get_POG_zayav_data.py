
def get_POG_zayav_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[0] == "":
            continue

        snils_z = row[0]
        fio_z = row[1]
        snils_y = row[2]
        fio_y = row[3]

        data.append((snils_z, fio_z, snils_y, fio_y))

    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?)', data)
    except Exception as e:
        print(e)