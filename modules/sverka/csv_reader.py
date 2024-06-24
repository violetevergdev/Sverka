import os
import pandas as pd


def csv_reader(conn, c, csv_dir):
    # Создаем таблицу в БД
    c.execute('''
        CREATE TABLE IF NOT EXISTS nvp_base (
          'Дата смерти',
          'СНИЛС',
          'Район',
          'Регион',
          'pw'
        )
        ''')

    # Проходимся по дир-и НВП и добавляем данные из файлов
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            try:
                file_path = os.path.join(csv_dir, file)
                df = pd.read_csv(file_path, sep=";", header=None, names=['Дата смерти', 'СНИЛС', 'Район', 'Регион', 'pw'], usecols=[0, 1, 2, 3, 4])
                df.to_sql('nvp_base', conn, if_exists='append', index=False)
                conn.commit()
            except Exception as e:
                print(e)
