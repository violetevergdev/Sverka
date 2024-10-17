def create_svo_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
          'Регион',
          'Район',
          'СНИЛС',
          'ФИО',
          'Дата рождения',
          'Пол',
          'Адрес: места рождения',
          'Адрес: места жительства (прописка)',
          'Адрес: фактического проживания',
          'Паспорт: серия',
          'Паспорт: номер',
          'Паспорт: выдавш. орган',
          'Код изменения',
          'Льгота: L1',
          'Льгота: L2',
          'Признак получения: НСУ1',
          'Признак получения: НСУ2',
          'Признак получения: НСУ3',
          'Заявление на получение: НСУ1',
          'Заявление на получение: НСУ2',
          'Заявление на получение: НСУ3',
          'Дата: вкл. в ФР',
          'Дата: вкл. в сегмент',
          'Дата: искл. из ФР',
          'Дата: искл. из сегмента',
          'Док. на льготу: серия и номер',
          'Док. на льготу: кем и когда выдан',
          'Док. на льготу: дата начала действ.',
          'Док. на льготу: дата окончания действ.',
          'Зарег. в регион/район двойник в регион/район',
          'Выплачено по',
          'Выплаченная сумма',
          'Признак'
        )
        ''')

def create_vib_db(db_curs, db_name):
    db_curs.execute(f'''
        CREATE TABLE IF NOT EXISTS {db_name} (
        'DPW',
        'GSP',
        'NPERS',
        'PE',
        'PW',
        'RA',
        'RE'
        )
        ''')