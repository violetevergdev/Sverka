import os
import xml.etree.ElementTree as ET


def xml_reader(db_name: str, db_conn, db_curs, dir: str, depth: list, data_extract_func=None, inserting_data_func=None):
    """
                        Функция для обработки XML файлов в БД

        :param db_name: имя БД в которую пушить данные
        :param db_conn: объект connection БД
        :param db_curs: объект cursor БД
        :param dir: директория расположения XML файлов
        :param depth: глубина основного массива данных
        :param data_extract_func: функция для извлечения данных из XML
        :param inserting_data_func: функция для записи данных в БД
    """
    for file in os.listdir(dir):
        if file.endswith(".xml") or file.endswith(".XML"):
            try:
                # Парсим XML данные
                tree = ET.parse(os.path.join(dir, file))
                root = tree.getroot()

                lst = root
                for i in depth:
                    lst = lst[i]

                data = []
                for item in lst:
                    row_data = data_extract_func(item)
                    if row_data == 'BREAK':
                        break

                    data.append(row_data)

                inserting_data_func(db_curs, db_name, data)

                db_conn.commit()
            except Exception as e:
                e = __name__, e
                return e
