
def create_mits_db(db_curs, db_name):
    db_curs.execute(f'''
            CREATE TABLE IF NOT EXISTS {db_name} (
              'СНИЛС получателя',
              'ФИО получателя' ,
              'СНИЛС л-о',
              'ФИО л-о',
              'Дата смерти получателя',
              'Дата смерти л-о'
            )
            ''')

def create_msp_db(db_curs, db_name):
    db_curs.execute(f'''
            CREATE TABLE IF NOT EXISTS {db_name} (
              'СНИЛС',
              'Район',
              'pw'
            )
            ''')