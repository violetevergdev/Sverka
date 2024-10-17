from modules.Common.read_main_dir import read_main_dir
from modules.Common.readers.csv_reader import csv_reader

from modules.svo.create_SVO_db import create_svo_db, create_vib_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.svo.get_SVO_data import get_SVO_data
from modules.svo.get_SVO_matches import get_SVO_matches

def start_SVO_sver(in_path, db_conn, db_curs):
    try:
        # Чтение рабочей директории
        xlsx, vib = read_main_dir(in_path)

        # =============== Чтение файла xlsx ==================

        # Создание таблицы в БД для файлов из XLSX
        db_svo_name = 'svo_base'
        create_svo_db(db_curs, db_svo_name)

        err = xlsx_reader(xlsx, db_conn, db_curs, db_name=db_svo_name, skiprows=2, processing_data_func=get_SVO_data)
        if err:
            return err

        # =============== Чтение csv файлов  ==================

        # Создание таблицы в БД для файлов из МиЦ
        db_prf_name = 'pfr_base'
        create_vib_db(db_curs, db_prf_name)

        # Задаем название столбцам
        col_names = ['DPW', 'GSP', 'NPERS', 'PE', 'PW', 'RA', 'RE']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4, 5, 6]

        err = csv_reader(db_prf_name, db_conn, dir=vib, names=col_names, usecols=col, encoding='windows-1251')
        if err:
            return err

        # =============== Обработка БД и выгрузка результата ==================

        get_SVO_matches(db_curs, svo_db=db_svo_name, pfr_db=db_prf_name)

    except Exception as e:
        return e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE {db_svo_name}")
            db_curs.execute(f"DROP TABLE {db_prf_name}")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err