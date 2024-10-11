def create_vip_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'ФИО получателя',
          'СНИЛС получателя',
          'Сумма к доставке, руб.'
        )
        ''')

def create_zayav_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'СНИЛС заявителя',
        'ФИО заявителя',
        'СНИЛС умершего',
        'ФИО умершего'
        )
        ''')