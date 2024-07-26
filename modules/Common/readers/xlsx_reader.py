import os
import pandas as pd


def xlsx_reader(dir: str, db_conn, db_curs, db_name: str, skiprows: int = 0, processing_data_func=None):
    """
                        Функция для обработки XLSX файлов в БД

        :param dir: директория расположения XML файлов
        :param db_conn: объект connection БД
        :param db_curs: объект cursor БД
        :param db_name: имя БД для записи данных
        :param skiprows: (опционально) пропуск первых строк
        :param processing_data_func: функция для изьятия и записи данных из XLSX в БД

    """
    for file in os.listdir(dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):
            try:
                file_path = os.path.join(dir, file)

                df = pd.read_excel(file_path, skiprows=skiprows, na_filter=False)

                processing_data_func(df, db_curs, db_name, file)

                db_conn.commit()

            except Exception as e:
                e = __name__, e
                return e


