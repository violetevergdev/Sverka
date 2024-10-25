import os

from modules.Common.read_main_dir import read_main_dir
from modules.Common.readers.csv_reader import csv_reader
from modules.NAKOP.check_is_loc_data_valid import is_loc_data_valid

from modules.NAKOP.create_NAKOP_db import *
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.NAKOP.get_NAKOP_data import get_osfr_data, get_loc_data
from modules.NAKOP.get_NAKOP_matches import get_NAKOP_matches
from modules.NAKOP.reformat_NAKOP_data import reformat_popay_data, reformat_wpr_data


def start_NAKOP(in_path, type_of_sver, db_conn, db_curs):
    err = None
    try:
        # Чтение рабочей директории
        xlsx, vib, loc = read_main_dir(in_path, type_of_sver)

        is_continue, failed_files = is_loc_data_valid(loc, skiprows=2)

        if is_continue is False:
            err = 'В следующих файлах отсутствует СНИЛС: ' + str(failed_files)
            raise Exception(err)

        # =============== Чтение файла xlsx OSFR ==================

        # Создание таблицы в БД для файлов из XLSX
        db_osfr_name = 'osfr_base'
        create_osfr_db(db_curs, db_osfr_name)

        err = xlsx_reader(xlsx, db_conn, db_curs, db_name=db_osfr_name, processing_data_func=get_osfr_data)
        if err:
            raise Exception(err)

        # =============== Чтение файла xlsx LOC ==================

        # Создание таблицы в БД для файлов из XLSX
        db_loc_name = 'loc_base'
        create_loc_db(db_curs, db_loc_name)

        err = xlsx_reader(loc, db_conn, db_curs, db_name=db_loc_name, skiprows=2, processing_data_func=get_loc_data)
        if err:
            raise Exception(err)

        # =============== Чтение csv файлов MAN ==================

        # Создание таблицы в БД для файлов из МиЦ
        db_man_name = 'man_base'
        create_man_db(db_curs, db_man_name)

        # Задаем название столбцам
        col_names = ['MAN_ID', 'MAN_NPERS', 'MAN_PE', 'MAN_PW', 'MAN_RA', 'MAN_RE']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4, 5]

        man_dir = os.path.join(vib, 'MAN')

        err = csv_reader(db_man_name, db_conn, dir=man_dir, names=col_names, usecols=col, encoding='windows-1251')
        if err:
            raise Exception(err)

        # =============== Чтение csv файлов POPAY ==================

        # Создание таблицы в БД для файлов из МиЦ
        db_popay_name = 'popay_base'
        create_popay_db(db_curs, db_popay_name)

        # Задаем название столбцам
        col_names = ['POPAY_AMOUNT', 'POPAY_ID', 'POPAY_NP', 'POPAY_NVP', 'POPAY_SPOSOB']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        popay_dir = os.path.join(vib, 'POPAY')

        err = csv_reader(db_popay_name, db_conn, dir=popay_dir, names=col_names, usecols=col, encoding='windows-1251', opt=reformat_popay_data)
        if err:
            raise Exception(err)

        # =============== Чтение csv файлов WPR ==================

        # Создание таблицы в БД для файлов из МиЦ
        db_wpr_name = 'wpr_base'
        create_wpr_db(db_curs, db_wpr_name)

        # Задаем название столбцам
        col_names = ['WPR_KOD', 'WPR_NAME', 'WPR_NUS', 'WPR_RA']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3]

        wpr_dir = os.path.join(vib, 'WPR')

        err = csv_reader(db_wpr_name, db_conn, dir=wpr_dir, names=col_names, usecols=col, encoding='windows-1251', opt=reformat_wpr_data)
        if err:
            raise Exception(err)

        # =============== Обработка БД и выгрузка результата ==================

        get_NAKOP_matches(db_curs, osfr_db=db_osfr_name, loc_db=db_loc_name, man_db=db_man_name, popay_db=db_popay_name, wpr_db=db_wpr_name)

    except Exception as e:
        err = e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_osfr_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_loc_name}")
            # db_curs.execute(f"DROP TABLE IF EXISTS {db_man_name}")
            # db_curs.execute(f"DROP TABLE IF EXISTS {db_popay_name}")
            # db_curs.execute(f"DROP TABLE IF EXISTS {db_wpr_name}")
            # db_curs.execute(f"DROP TABLE IF EXISTS res")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err