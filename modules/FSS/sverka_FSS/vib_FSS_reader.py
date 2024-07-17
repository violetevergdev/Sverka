import os
import pandas as pd


def vib_reader(conn, c, vib_dir):
    # Создаем таблицу в БД
    c.execute('''
        CREATE TABLE IF NOT EXISTS vib_fss_base (
        'dsm',
        'npers',
        'pw',
        'ra',
        're'
        )
        ''')

    # Считываем все CSV-файлы в один DataFrame
    df = pd.concat([pd.read_csv(os.path.join(vib_dir, file), sep=";", header=None,
                                names=['dsm', 'npers', 'pw', 'ra', 're'], usecols=[0, 1, 2, 3, 4]) for file in os.listdir(vib_dir) if
                    file.endswith(".csv")])

    # Записываем DataFrame в БД
    df.to_sql('vib_fss_base', conn, if_exists='append', index=False)
    conn.commit()