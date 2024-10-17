
def get_SVO_data(df, db_curs, db_name, file):
    data = []
    for _, row in df.iterrows():

        if row[4] == "":
            continue

        re = row[2]
        ra = row[3]
        snils = row[4]
        fio = row[5] + " " + row[6] + " " + row[7]
        birth_day = row[8]
        sex = row[9]
        homeland = row[10]
        residence = row[11]
        true_living_place = row[12]
        seria_of_passport = row[13]
        number_of_passport = row[14]
        vidavshi_organ = row[15]
        kod_of_change = row[16]
        benefit_l1 = row[17]
        benefit_l2 = row[18]
        attr_of_get_ns1 = row[19]
        attr_of_get_ns2 = row[20]
        attr_of_get_ns3 = row[21]
        decl_of_get_ns1 = row[22]
        decl_of_get_ns2 = row[23]
        decl_of_get_ns3 = row[24]
        date_in_fr = row[25]
        date_in_seg = row[26]
        date_out_fr = row[27]
        date_out_seg = row[28]
        doc_on_ben_ser_and_num = row[29]
        doc_on_ben_who_and_when = row[30]
        doc_on_ben_start = row[31]
        doc_on_ben_end = row[32]
        zareg_ra_re = row[33]
        rest_payment_day = row[34]
        rest_payment_sum = row[35]
        attr = row[36]

        data.append((re, ra, snils, fio, birth_day, sex, homeland, residence, true_living_place, seria_of_passport,
                     number_of_passport, vidavshi_organ, kod_of_change, benefit_l1, benefit_l2, attr_of_get_ns1,
                     attr_of_get_ns2, attr_of_get_ns3, decl_of_get_ns1, decl_of_get_ns2, decl_of_get_ns3, date_in_fr,
                     date_in_seg, date_out_fr, date_out_seg, doc_on_ben_ser_and_num, doc_on_ben_who_and_when,
                     doc_on_ben_start, doc_on_ben_end, zareg_ra_re, rest_payment_day, rest_payment_sum, attr))
#
    try:
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '
            f'?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    except Exception as e:
        print(e)
