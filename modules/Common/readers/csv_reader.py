import os
import pandas as pd


def csv_reader(db_name: str, db_conn, dir: str, names: list, usecols: list, skiprows: int = 0, encoding: str = None, opt=None):
    """
                        Функция для обработки csv файлов в БД

        :param db_name: имя БД в которую пушить данные
        :param db_conn: объект connection БД
        :param dir: директория расположения csv файлов
        :param names: наименование столбцов
        :param usecols: идентификаторы используемых столбцов
        :param skiprows: (опционально) пропуск первых строк
        :param encoding: (опционально) кодировка документа
        :param opt: (опционально) функция для дополнительной обработки данных
    """
    try:
        for file in os.listdir(dir):
            if file.endswith(".csv"):
                file_path = os.path.join(dir, file)

                # Чтение файла по частям
                for chunk in pd.read_csv(file_path, sep=";", header=None, names=names, usecols=usecols,
                                         skiprows=skiprows, encoding=encoding, chunksize=10000):
                    # Опционально обрабатываем данные
                    if opt:
                        opt(chunk)

                    # Записываем данные в БД
                    chunk.to_sql(db_name, db_conn, if_exists='append', index=False)
                    db_conn.commit()
    except Exception as e:
        e = __name__, e
        return e