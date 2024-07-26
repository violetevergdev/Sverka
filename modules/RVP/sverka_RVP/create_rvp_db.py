def create_vib_db(db_curs, db_name):
    db_curs.execute(f'''
    CREATE TABLE IF NOT EXISTS {db_name} (
       'Дата смерти',
        'СНИЛС',
        'Район',
        'Регион',
        'pw'
    )
    ''')

def create_xlsx_db(db_curs, db_name):
    db_curs.execute(f'''
    CREATE TABLE IF NOT EXISTS {db_name} (
      'Вид выплаты_pfr',
      'СНИЛС_pfr',
      'Фамилия_pfr',
      'Имя_pfr',
      'Отчество_pfr',
      'Дата рождения_pfr',
      'Сумма_pfr'
    )
    ''')

def create_xml_db(db_curs, db_name):
    db_curs.execute(f'''
    CREATE TABLE IF NOT EXISTS {db_name} (
      'СНИЛС',
      'Фамилия',
      'Имя',
      'Отчество',
      'Дата рождения',
      'Код валюты',
      'Сумма выплаты РФ'
    )
    ''')