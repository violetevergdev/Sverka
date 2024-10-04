
def get_FSS_BASE_XLSX_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():

        if row[1] == "":
            continue

        fio = row[0]
        snils = format_snils(row[1])
        type_of_vpl = row[2]
        sum = row[4]
        id = row[5]
        bank = row[6]
        num_of_decision = row[7]
        date_of_decision = row[8]
        pay_up_to = row[9]
        payment_day = row[10]
        state = row[11]
        errors = row[12]


        data.append((fio, snils, type_of_vpl, sum, id, bank, num_of_decision, date_of_decision, pay_up_to, payment_day, state, errors))

    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?)', data)
    except Exception as e:
        print(e)


def format_snils(unvalid_snils):
    s = list(unvalid_snils)

    s.insert(3, '-')
    s.insert(7, '-')
    s.insert(11, ' ')
    return "".join(s)
