
def create_fss_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'Имя_Файла',
          'ФИО',
          'СНИЛС'
        )
        ''')

def create_vib_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'dsm',
        'npers',
        'pw',
        'ra',
        're'
        )
        ''')