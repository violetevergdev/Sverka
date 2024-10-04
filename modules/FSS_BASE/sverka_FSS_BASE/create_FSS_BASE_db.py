
def create_fss_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'ФИО',
          'СНИЛС',
          'Вид выплаты/компенсации',
          'Сумма начисления',
          'Идентификатор начисления',
          'Способ получения',
          'Решение номер',
          'Решение дата',
          'Выплатить до',
          'Дата оплаты',
          'Статус',
          'Ошибка загрузки вв ФБ'
        )
        ''')

def create_vib_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'dpw',
        'dsm',
        'fa',
        'im',
        'npers',
        'ot',
        'ra',
        're'
        )
        ''')