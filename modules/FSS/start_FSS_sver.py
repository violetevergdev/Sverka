from modules.Common.read_main_dir import read_main_dir
from modules.FSS.sverka_FSS.create_fss_db import create_fss_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.FSS.sverka_FSS.get_FSS_XLSX_data import get_FSS_XLSX_data
from modules.FSS.sverka_FSS.create_fss_db import create_vib_db
from modules.Common.readers.csv_reader import csv_reader
from modules.FSS.sverka_FSS.get_FSS_matches import get_FSS_matches

def start_FSS(in_path, type_of_sver, db_conn, db_curs):
    try:
        # Чтение рабочей директории
        xlsx_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # =============== Чтение XLSX файлов по ФСС ==================

        # Создание таблицы в БД для файлов из XLSX (картотека) РПВ
        db_xlsx_name = 'fss_base'
        create_fss_db(db_curs, db_xlsx_name)

        err = xlsx_reader(xlsx_dir, db_conn, db_curs, db_name=db_xlsx_name,
                          skiprows=4, processing_data_func=get_FSS_XLSX_data)
        if err:
            return err

        # =============== Чтение csv файлов из VIB ==================

        # Создание таблицы в БД для файлов из VIB
        db_vib_name = 'vib_base'
        create_vib_db(db_curs, db_vib_name)

        # Задаем название столбцам
        col_names = ['dsm', 'npers', 'pw', 'ra', 're']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        err = csv_reader(db_vib_name, db_conn, dir=vib_dir, names=col_names,
                             usecols=col)
        if err:
            return err

        # =============== Обработка БД и выгрузка результата ==================

        get_FSS_matches(db_curs, fss_db=db_xlsx_name, vib_db=db_vib_name)

    except Exception as e:
        return e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_xlsx_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_vib_name}")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err


