import os

from modules.Common.read_main_dir import read_main_dir
from modules.Common.create_db import create_db
from modules.OPEK.refactor_opek_data import refactor_opek_data
from modules.Common.readers.csv_reader import csv_reader
from modules.OPEK.get_OPEK_matches import get_OPEK_matches

# Запуск сценария обработки документов по опекунам
def start_OPEK(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        opek_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # ============= Чтение входящих csv файлов по опекунам ================

        progress_status.set('Чтение файлов по опекунам')

        # Задаем название БД
        db_opek_name = 'opek_base'

        # Задаем название столбцам
        col_names = ['СНИЛС взрослого', 'СНИЛС ребенка', 'ФИО взрослого',
                     'ФИО ребенка', 'Реестр', 'Код типа событий', 'Дата вступления в силу', 'Серия документа', 'Номер документа', 'Орган выдавший документ', 'Дата документа', 'Код ПИ']

        # Создаем таблицу в БД для файлов по опекунам
        create_db(db_conn, db_opek_name, col_names)

        # Задаем индексы используемых столбцов
        col = [i for i in range(0, len(col_names))]

        err = csv_reader(db_opek_name, db_conn, dir=opek_dir, names=col_names, usecols=col,
                   skiprows=1, encoding='windows-1251', opt=refactor_opek_data)
        if err:
            print(err)
            raise Exception(err)

        progress_value.set(5 + progress_value.get())

        # =============== Чтение csv файлов OID ==================

        progress_status.set('Чтение выборки OID')

        # Задаем название БД
        db_oid_name = 'vib_oid_base'

        # Задаем название столбцам
        col_names = ['OID_MAN_ID', 'OID_MAN_NPERS', 'OID_MAN_OID', 'OID_MAN_PW', 'OID_MAN_RA', 'OID_MAN_RE']

        # Создаем таблицу в БД для файлов из VIB
        create_db(db_curs, db_oid_name, col_names)

        # Задаем индексы используемых столбцов
        col = [i for i in range(0, len(col_names))]

        oid_dir = os.path.join(vib_dir, 'OID_MAN')

        err = csv_reader(db_oid_name, db_conn, dir=oid_dir, names=col_names,
                         usecols=col, encoding='windows-1251')
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        progress_status.set('Индексация СНИЛС и OID из выборки OID')

        db_curs.execute(f'CREATE INDEX snils_oid_ind ON {db_oid_name} (OID_MAN_NPERS)')
        db_curs.execute(f'CREATE INDEX oid_oid_ind ON {db_oid_name} (OID_MAN_OID)')

        progress_value.set(5 + progress_value.get())

        # =============== Чтение csv файлов ID ==================

        progress_status.set('Чтение выборки ID')

        # Задаем название БД
        db_id_name = 'vib_id_base'

        # Задаем название столбцам
        col_names = ['ID_MAN_FA', 'ID_MAN_ID', 'ID_MAN_IM', 'ID_MAN_NPERS', 'ID_MAN_OT', 'ID_MAN_PW', 'ID_MAN_RA', 'ID_MAN_RE']

        # Создаем таблицу в БД для файлов из VIB
        create_db(db_curs, db_id_name, col_names)

        # Задаем индексы используемых столбцов
        col = [i for i in range(0, len(col_names))]

        id_dir = os.path.join(vib_dir, 'ID_MAN')

        err = csv_reader(db_id_name, db_conn, dir=id_dir, names=col_names,
                         usecols=col, encoding='windows-1251')
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        progress_status.set('Индексация СНИЛС и ID из выборки ID')

        db_curs.execute(f'CREATE INDEX snils_id_ind ON {db_id_name} (ID_MAN_NPERS)')
        db_curs.execute(f'CREATE INDEX id_id_ind ON {db_id_name} (ID_MAN_ID)')

        progress_value.set(7 + progress_value.get())

        # =============== Чтение csv файлов VPL ==================

        progress_status.set('Чтение выборки VPL')

        # Задаем название БД
        db_vpl_name = 'vib_vpl_base'

        # Задаем название столбцам
        col_names = ['PO_NPERS', 'PO_RA', 'PO_RE', 'POPEN_NP', 'POPEN_PEN_B', 'POPEN_SROKS']

        # Создаем таблицу в БД для файлов из VIB
        create_db(db_curs, db_vpl_name, col_names)

        # Задаем индексы используемых столбцов
        col = [i for i in range(0, len(col_names))]

        vpl_dir = os.path.join(vib_dir, 'VPL')

        err = csv_reader(db_vpl_name, db_conn, dir=vpl_dir, names=col_names,
                         usecols=col, encoding='windows-1251')
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        progress_status.set('Индексация СНИЛС из выборки VPL')

        db_curs.execute(f'CREATE INDEX snils_vpl_ind ON {db_vpl_name} (PO_NPERS)')

        progress_value.set(5 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_OPEK_matches(db_curs, opek_db=db_opek_name, oid_db=db_oid_name, id_db=db_id_name, vpl_db=db_vpl_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        err = e
    finally:
        # Чистка БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_opek_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_oid_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_id_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_vpl_name}")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err

