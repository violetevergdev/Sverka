def create_osfr_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'Код Района',
          'ИНН',
          'Вариант Решения',
          'СНИЛС',
          'ФИО',
          'Дата Рождения',
          'Сумма ЕВ',
          'Дата Решения',
          'Сумма расходов на оплату услуг',
          'Примечание'
        )
        ''')

def create_man_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'MAN_ID',
        'MAN_NPERS',
        'MAN_PE',
        'MAN_PW',
        'MAN_RA',
        'MAN_RE'
        )
        ''')

def create_popay_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'POPAY_AMOUNT',
        'POPAY_ID',
        'POPAY_NP',
        'POPAY_NVP',
        'POPAY_SPOSOB'
        )
        ''')

def create_wpr_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'WPR_KOD',
        'WPR_NAME',
        'WPR_NUS',
        'WPR_RA'
        )
        ''')

def create_loc_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'СНИЛС',
          'Район'
        )
        ''')