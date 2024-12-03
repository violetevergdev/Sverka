import os

from modules.Common.read_main_dir import read_main_dir
from modules.Common.readers.csv_reader import csv_reader
from modules.NAKOP.check_is_loc_data_valid import is_loc_data_valid
from modules.Common.create_db import create_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.NAKOP.get_NAKOP_data import get_osfr_data, get_loc_data
from modules.NAKOP.get_NAKOP_matches import get_NAKOP_matches
from modules.NAKOP.reformat_NAKOP_data import reformat_popay_data, reformat_wpr_data


def start_NAKOP(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        xlsx, vib, loc = read_main_dir(in_path, type_of_sver)

        progress_status.set('Проверка файлов DONT_LOC')

        is_continue, failed_files = is_loc_data_valid(loc, skiprows=2)

        if is_continue is False:
            err = 'В следующих файлах отсутствует СНИЛС: ' + str(failed_files)
            raise Exception(err)

        progress_value.set(5 + progress_value.get())

        # =============== Чтение файла xlsx OSFR ==================

        progress_status.set('Чтение файла ОСФР')

        # Уст. имя БД
        db_osfr_name = 'osfr_base'

        # Уст. имена столбцов
        col_names = ['Код Района', 'ИНН', 'Вариант Решения', 'СНИЛС', 'ФИО', 'Дата Рождения', 'Сумма ЕВ',
                     'Дата Решения', 'Сумма расходов на оплату услуг', 'Примечание']

        # Создание таблицы в БД для файлов из XLSX
        create_db(db_curs, db_osfr_name, col_names)

        err = xlsx_reader(xlsx, db_conn, db_curs, db_name=db_osfr_name, processing_data_func=get_osfr_data)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        # =============== Чтение файла xlsx LOC ==================

        progress_status.set('Чтение файлов DONT LOC')

        # Уст. имя БД
        db_loc_name = 'loc_base'

        # Уст. имена столбцов
        col_names = ['СНИЛС', 'Район']

        # Создание таблицы в БД для файлов из XLSX
        create_db(db_curs, db_loc_name, col_names)

        err = xlsx_reader(loc, db_conn, db_curs, db_name=db_loc_name, skiprows=2, processing_data_func=get_loc_data)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        progress_status.set('Индексация СНИЛС из DONT LOC')

        db_curs.execute(f'CREATE INDEX snils_dtloc_ind ON {db_loc_name} (СНИЛС)')

        progress_value.set(7 + progress_value.get())

        # =============== Чтение csv файлов MAN =================

        progress_status.set('Чтение файлов  MAN')

        # Уст. имя БД
        db_man_name = 'man_base'

        # Задаем название столбцам
        col_names = ['MAN_ID', 'MAN_NPERS', 'MAN_PE', 'MAN_PW', 'MAN_RA', 'MAN_RE']

        # Создание таблицы в БД для файлов из МиЦ
        create_db(db_curs, db_man_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4, 5]

        man_dir = os.path.join(vib, 'MAN')

        err = csv_reader(db_man_name, db_conn, dir=man_dir, names=col_names, usecols=col, encoding='windows-1251')
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        progress_status.set('Индексация СНИЛС из MAN')

        db_curs.execute(f'CREATE INDEX snils_ind ON {db_man_name} (MAN_NPERS)')

        progress_value.set(7 + progress_value.get())

        # =============== Чтение csv файлов POPAY ==================

        progress_status.set('Чтение файлов POPAY')

        # Уст. имя БД
        db_popay_name = 'popay_base'

        # Задаем название столбцам
        col_names = ['POPAY_AMOUNT', 'POPAY_ID', 'POPAY_NP', 'POPAY_NVP', 'POPAY_SPOSOB']

        # Создание таблицы в БД для файлов из МиЦ
        create_db(db_curs, db_popay_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        popay_dir = os.path.join(vib, 'POPAY')

        err = csv_reader(db_popay_name, db_conn, dir=popay_dir, names=col_names, usecols=col, encoding='windows-1251', opt=reformat_popay_data)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        # =============== Чтение csv файлов WPR ==================

        progress_status.set('Чтение файлов WPR')

        db_wpr_name = 'wpr_base'

        # Задаем название столбцам
        col_names = ['WPR_KOD', 'WPR_NAME', 'WPR_NUS', 'WPR_RA']

        create_db(db_curs, db_wpr_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3]

        wpr_dir = os.path.join(vib, 'WPR')

        err = csv_reader(db_wpr_name, db_conn, dir=wpr_dir, names=col_names, usecols=col, encoding='windows-1251', opt=reformat_wpr_data)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_NAKOP_matches(db_curs, osfr_db=db_osfr_name, loc_db=db_loc_name, man_db=db_man_name, popay_db=db_popay_name, wpr_db=db_wpr_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        err = e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_osfr_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_loc_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_man_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_popay_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_wpr_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS res")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err