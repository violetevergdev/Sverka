from modules.Common.read_main_dir import read_main_dir
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.FSS.sverka_FSS.get_FSS_XLSX_data import get_FSS_XLSX_data
from modules.Common.readers.csv_reader import csv_reader
from modules.FSS.sverka_FSS.get_FSS_matches import get_FSS_matches
from modules.Common.create_db import create_db

def start_FSS(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        xlsx_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # =============== Чтение XLSX файлов по ФСС ==================

        progress_status.set('Чтение файлов ФСС')

        # Уст. имя БД
        db_xlsx_name = 'fss_base'

        # Уст. имена столбцов
        col_names = ['Имя_Файла', 'ФИО', 'СНИЛС']

        # Создание таблицы в БД
        create_db(db_curs, db_xlsx_name, col_names)

        err = xlsx_reader(xlsx_dir, db_conn, db_curs, db_name=db_xlsx_name,
                          skiprows=4, processing_data_func=get_FSS_XLSX_data)
        if err:
            raise Exception(err)

        progress_value.set(30 + progress_value.get())

        # =============== Чтение csv файлов из VIB ==================

        progress_status.set('Чтение выборки')

        # Уст. имя БД
        db_vib_name = 'vib_base'

        # Задаем название столбцам
        col_names = ['dsm', 'npers', 'pw', 'ra', 're']

        # Создание таблицы в БД для файлов из VIB
        create_db(db_curs, db_vib_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        err = csv_reader(db_vib_name, db_conn, dir=vib_dir, names=col_names,
                             usecols=col)
        if err:
            raise Exception(err)

        progress_value.set(30 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_FSS_matches(db_curs, fss_db=db_xlsx_name, vib_db=db_vib_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        err = e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_xlsx_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_vib_name}")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err


