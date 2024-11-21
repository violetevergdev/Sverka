
def get_RPV_XML_data(item):
    # Обрабатываем конец записей получателей
    if item[0].tag.endswith("ПенсияВВ"):
        return 'BREAK'
        # Обрабатываем записи без СНИЛСОВ
    if not item[0][0].tag.endswith("СНИЛС"):
        data = {
            'СНИЛС': None,
            'Фамилия': item[0][0][0].text,
            'Имя': item[0][0][1].text,
            'Отчество': item[0][0][2].text,
            'Дата_рождения': item[0][2].text,
            'Код_валюты': item[1].text,
            'Сумма_выплаты_РФ': item[6].text
        }
        return data
    else:
        # Обрабатываем корректные записи
        data = {
            'СНИЛС': item[0][0].text,
            'Фамилия': item[0][1][0].text,
            'Имя': item[0][1][1].text,
            'Отчество': item[0][1][2].text,
            'Дата_рождения': item[0][3].text,
            'Код_валюты': item[1].text,
            'Сумма_выплаты_РФ': item[6].text
        }
        return data


def insert_RVP_XML_data(db_curs, db_name, data):
    db_curs.executemany(
        f'INSERT INTO {db_name} VALUES (:СНИЛС, :Фамилия, :Имя, :Отчество, :Дата_рождения, :Код_валюты, :Сумма_выплаты_РФ)',
        data)
