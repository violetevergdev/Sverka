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

    # Считываем все CSV-файлы в один DataFrame
    df = pd.concat([pd.read_csv(os.path.join(csv_dir, file), sep=";", header=None,
                    names=['Дата смерти', 'СНИЛС', 'Район', 'Регион', 'pw'],
                    usecols=[0, 1, 2, 3, 4]) for file in os.listdir(csv_dir) if
                    file.endswith(".csv")])

    # Записываем DataFrame в БД
    df.to_sql('nvp_base', conn, if_exists='append', index=False)
    conn.commit()