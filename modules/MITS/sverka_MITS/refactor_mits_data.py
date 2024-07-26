def refactor_mits_data(df):
    # Форматируем СНИЛС
    df.fillna("", inplace=True)
    df['СНИЛС получателя'] = df['СНИЛС получателя'].apply(format_snils)
    df['ФИО получателя'] = df['ФИО получателя'].str.upper()
    df['СНИЛС л-о'] = df['СНИЛС л-о'].apply(format_snils)
    df['ФИО л-о'] = df['ФИО л-о'].str.upper()

    df['Дата смерти получателя'] = df['Дата смерти получателя'].apply(format_date)
    df['Дата смерти л-о'] = df['Дата смерти л-о'].apply(format_date)


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