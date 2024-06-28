import os
import pandas as pd


def vib_reader(conn, c, vib_dir):
    # Создаем таблицу в БД
    c.execute('''
        CREATE TABLE IF NOT EXISTS vib_msp_base (
          'СНИЛС',
          'Район',
          'pw'
        )
        ''')

    # Считываем все CSV-файлы в один DataFrame
    df = pd.concat([pd.read_csv(os.path.join(vib_dir, file), sep=";", header=None,
                                names=['СНИЛС', 'Район', 'pw'],
                                usecols=[0, 1, 3]) for file in os.listdir(vib_dir) if
                    file.endswith(".csv")])

    # Записываем DataFrame в БД
    df.to_sql('vib_msp_base', conn, if_exists='append', index=False)
    conn.commit()