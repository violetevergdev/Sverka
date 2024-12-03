from modules.Common.read_main_dir import read_main_dir
from modules.Common.create_db import create_db
from modules.MITS.sverka_MITS.refactor_mits_data import refactor_mits_data
from modules.Common.readers.csv_reader import csv_reader
from modules.MITS.sverka_MITS.get_MITS_matches import get_MITS_matches


# Запуск сценария обработки документов МиЦ
def start_MITS(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        mits_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # =============== Чтение csv файлов из МиЦ ==================

        progress_status.set('Чтение файлов МиЦ')

        # Задаем название БД
        db_mits_name = 'mits_base'

        # Задаем название столбцам
        col_names = ['СНИЛС получателя', 'ФИО получателя', 'СНИЛС л-о',
                     'ФИО л-о', 'Дата смерти получателя', 'Дата смерти л-о', 'Смерть мобил']

        # Создаем таблицу в БД для файлов из МиЦ
        create_db(db_conn, db_mits_name, col_names)

        # Задаем индексы используемых столбцов
        col = [6, 7, 8, 9, 10, 11, 12]

        err = csv_reader(db_mits_name, db_conn, dir=mits_dir, names=col_names, usecols=col,
                   skiprows=1, encoding='windows-1251', opt=refactor_mits_data)
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        # =============== Чтение csv файлов из VIB ==================

        progress_status.set('Чтение выборки')

        # Задаем название БД
        db_msp_name = 'vib_msp_base'

        # Задаем название столбцам
        col_names = ['СНИЛС', 'Район', 'pw']

        # Создаем таблицу в БД для файлов из VIB
        create_db(db_curs, db_msp_name, col_names)

        # Задаем индексы используемых столбцов
        col = [0, 1, 3]

        err = csv_reader(db_msp_name, db_conn, dir=vib_dir, names=col_names,
                         usecols=col)
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_MITS_matches(db_curs, mits_db=db_mits_name, vib_db=db_msp_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        err = e
    finally:
        # Чистка БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_mits_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_msp_name}")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err

