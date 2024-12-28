def get_prosec_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[0] == "":
            continue

        ra = row[0]
        snils = row[1]
        fio = row[2] + " " + row[3] + " " + row[4]
        birth_date = row[5]
        num_of_doc = row[6]
        date_of_doc = row[7]
        name_of_doc = row[8]
        type_of_doc = row[9]
        month_proc = row[10]
        month_sum = row[11]
        date_of_start = row[12]
        date_of_end = row[13]
        min_type = row[14]
        type_gos = row[15]
        type_pens = row[16]

        data.append((ra, snils, fio, birth_date, num_of_doc, date_of_doc, name_of_doc, type_of_doc, month_proc, month_sum, date_of_start, date_of_end, min_type, type_gos, type_pens))
    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    except Exception as e:
        print(e)

def get_spisok_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[2] == "":
            continue

        snils = row[2]
        re = row[8]
        ra = row[9]
        punkt = row[10]
        ul = row[11]
        dom = row[12]
        korp = row[13]
        kv = row[14]

        data.append((snils, re, ra, punkt, ul, dom, korp, kv))
    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)
    except Exception as e:
        print(e)