from modules.Common.refactor_data import format_snils_with_fill_zero, format_date_from_dot_to_dash

def refactor_mits_data(df):
    # Форматируем СНИЛС
    df.fillna("", inplace=True)
    df['СНИЛС получателя'] = df['СНИЛС получателя'].apply(format_snils_with_fill_zero)
    df['ФИО получателя'] = df['ФИО получателя'].str.upper()
    df['СНИЛС л-о'] = df['СНИЛС л-о'].apply(format_snils_with_fill_zero)
    df['ФИО л-о'] = df['ФИО л-о'].str.upper()

    df['Дата смерти получателя'] = df['Дата смерти получателя'].apply(format_date_from_dot_to_dash)
    df['Дата смерти л-о'] = df['Дата смерти л-о'].apply(format_date_from_dot_to_dash)
