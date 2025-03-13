import os

from modules.CHAES.get_CHAES_matches import get_CHAES_matches
from modules.Common.create_db import create_db
from modules.Common.read_main_dir import read_main_dir
from modules.Common.readers.csv_reader import csv_reader
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.CHAES.get_CHAES_XLSX_data import get_CHAES_XLSX_data

def start_CHAES(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        xlsx_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # =============== Чтение XLSX файлов ==================

        progress_status.set('Чтение XLSX')

        # Задаем наименование БД
        db_xlsx_name = 'xlsx_base'

        # Задаем наименование столбцов таблицы БД
        col_names = ['СНИЛС', 'Фамилия', 'Имя', 'Отчество']

        # Создание таблицы в БД для файлов из XLSX
        create_db(db_curs, db_xlsx_name, col_names)

        err = xlsx_reader(xlsx_dir, db_conn, db_curs, db_name=db_xlsx_name,
                          skiprows=2, processing_data_func=get_CHAES_XLSX_data)
        if err:
            raise Exception(err)

        progress_value.set(15 + progress_value.get())

        # =============== Чтение csv файлов из VIB - POPAY==================

        progress_status.set('Чтение выборки POPAY')

        # Задаем наименование БД
        db_popay_name = 'popay_base'

        # Задаем название столбцам
        col_names = ['NPERS', 'RA', 'DPW', 'NVP', 'PW', 'SCHET']

        # Создание таблицы в БД для файлов из VIB
        create_db(db_curs, db_popay_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4, 5]

        popay_dir = os.path.join(vib_dir, 'POPAY')

        err = csv_reader(db_popay_name, db_conn, dir=popay_dir, names=col_names,
                             usecols=col, encoding='ANSI')
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        progress_status.set('Индексация СНИЛС из выборки POPAY')

        db_curs.execute(f'CREATE INDEX snils_chaes_popay_2_ind ON {db_popay_name} (NPERS)')

        progress_value.set(15 + progress_value.get())

        # =============== Чтение csv файлов из VIB - WPR==================

        progress_status.set('Чтение выборки WPR')

        # Задаем наименование БД
        db_wpr_name = 'wpr_base'

        # Задаем название столбцам
        col_names = ['BIK', 'KOD', 'NAME', 'NUS', 'RA']

        # Создание таблицы в БД для файлов из VIB
        create_db(db_curs, db_wpr_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        wpr_dir = os.path.join(vib_dir, 'WPR')

        err = csv_reader(db_wpr_name, db_conn, dir=wpr_dir, names=col_names, encoding='ANSI', usecols=col)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_CHAES_matches(db_curs, xlsx_db=db_xlsx_name,popay_db=db_popay_name, wpr_db=db_wpr_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        print(e)
        err = e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_xlsx_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_popay_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_wpr_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS pn")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)
        if err:
            return err