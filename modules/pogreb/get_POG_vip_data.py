
def get_POG_vip_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():
        if row[0] == "":
            continue

        fio = row[0]
        snils = format_snils(row[1])
        sum = row[2]

        data.append((fio, snils, sum))

    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?)', data)
    except Exception as e:
        print(e)


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