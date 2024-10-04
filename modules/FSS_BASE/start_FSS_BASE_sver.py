from modules.Common.read_main_dir import read_main_dir
from modules.FSS_BASE.sverka_FSS_BASE.create_FSS_BASE_db import create_fss_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.FSS_BASE.sverka_FSS_BASE.get_FSS_BASE_XLSX_data import get_FSS_BASE_XLSX_data
from modules.FSS_BASE.sverka_FSS_BASE.create_FSS_BASE_db import create_vib_db
from modules.Common.readers.csv_reader import csv_reader
from modules.FSS_BASE.sverka_FSS_BASE.get_FSS_BASE_matches import get_FSS_BASE_matches


def start_FSS_BASE(in_path, type_of_sver, db_conn, db_curs):
    try:
        # Чтение рабочей директории
        xlsx_dir, vib_dir = read_main_dir(in_path, type_of_sver)


        # =============== Чтение XLSX файлов по ФСС ==================

        # Создание таблицы в БД для файлов из XLSX (картотека) РВП
        db_xlsx_name = 'fss_base'
        create_fss_db(db_curs, db_xlsx_name)

        err = xlsx_reader(xlsx_dir, db_conn, db_curs, db_name=db_xlsx_name, processing_data_func=get_FSS_BASE_XLSX_data)
        if err:
            return err

        # =============== Чтение csv файлов из VIB ==================

        # Создание таблицы в БД для файлов из VIB
        db_vib_name = 'vib_base'
        create_vib_db(db_curs, db_vib_name)

        # Задаем название столбцам
        col_names = ['dpw', 'dsm', 'fa', 'im', 'npers', 'ot', 'ra', 're']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4, 5, 6, 7]

        err = csv_reader(db_vib_name, db_conn, dir=vib_dir, names=col_names,
                         usecols=col, encoding='ansi')
        if err:
            return err

        # =============== Обработка БД и выгрузка результата ==================

        get_FSS_BASE_matches(db_curs, fss_db=db_xlsx_name, vib_db=db_vib_name)

    except Exception as e:
        return e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE {db_xlsx_name}")
            db_curs.execute(f"DROP TABLE {db_vib_name}")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err