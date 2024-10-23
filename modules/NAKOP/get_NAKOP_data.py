import re


def get_osfr_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[3] == "":
            continue

        ra = row[0]
        inn = row[1]
        var_deci = row[2]
        snils = row[3]
        fio = row[4] + " " + row[5] + " " + row[6]
        birth_date = row[7]
        sum_ev = row[8]
        date_deci = row[9]
        sum_of_exp = row[10]
        note = row[11]

        data.append((ra, inn, var_deci, snils, fio, birth_date, sum_ev, date_deci, sum_of_exp, note))
    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    except Exception as e:
        print(e)


def get_loc_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[1] == "":
            continue

        pattern = r"^\d{3}-\d{3}-\d{3} \d{2}$"
        if not re.match(pattern, row[0]):
            raise ValueError("СНИЛС указан неверно! Файл -" + str(file))

        data.append((row[0], str(file).split('.')[0]))
    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?)', data)
    except Exception as e:
        print(e)
