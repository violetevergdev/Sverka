from modules.Common.refactor_data import format_snils_with_fill_zero, format_date_from_dot_to_dash


def refactor_opek_data(df):
    df.fillna('', inplace=True)
    df['СНИЛС взрослого'] = df['СНИЛС взрослого'].apply(format_snils_with_fill_zero)
    if df['СНИЛС ребенка'].empty:
        pass
    else:
        df['СНИЛС ребенка'] = df['СНИЛС ребенка'].apply(format_snils_with_fill_zero)
