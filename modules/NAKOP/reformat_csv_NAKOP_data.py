
def reformat_popay_data(df):
    df['POPAY_NVP'] = df['POPAY_NVP'].apply(reformat_num_types)


def reformat_wpr_data(df):
    df['WPR_KOD'] = df['WPR_KOD'].apply(reformat_num_types)
    df['WPR_NUS'] = df['WPR_NUS'].apply(reformat_num_types)


def reformat_num_types(num):
    if type(num) == str:
        return num

    s = str(num)
    if '.' in s:
        return s.split('.')[0]
    return s


