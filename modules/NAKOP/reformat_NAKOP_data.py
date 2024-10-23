from modules.Common.refactor_data import to_str_type

def reformat_popay_data(df):
    df['POPAY_NVP'] = df['POPAY_NVP'].apply(to_str_type)


def reformat_wpr_data(df):
    df['WPR_KOD'] = df['WPR_KOD'].apply(to_str_type)
    df['WPR_NUS'] = df['WPR_NUS'].apply(to_str_type)




