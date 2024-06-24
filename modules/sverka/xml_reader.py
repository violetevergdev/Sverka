import xml.etree.ElementTree as ET


def xml_reader(conn, c, xml_file):
    # Создаем таблицу БД
    c.execute('''
    CREATE TABLE IF NOT EXISTS xml_base (
      'СНИЛС',
      'Фамилия',
      'Имя',
      'Отчество',
      'Дата рождения',
      'Код валюты',
      'Сумма выплаты РФ'
    )
    ''')

    try:
        # Парсим XML данные
        tree = ET.parse(xml_file)
        root = tree.getroot()
        lst = root[0][5]

        for item in lst:
            # Обрабатываем конец записей получателей
            if item[0].tag.endswith("ПенсияВВ"):
                break
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

            c.execute(
                'INSERT INTO xml_base VALUES (:СНИЛС, :Фамилия, :Имя, :Отчество, :Дата_рождения, :Код_валюты, :Сумма_выплаты_РФ)',
                data)
            conn.commit()
    except Exception as e:
        print(e)


