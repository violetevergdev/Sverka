import os

from modules.Common.read_main_dir import read_main_dir
from modules.RPV.sverka_RPV.create_rpv_db import create_xml_db, create_adv_db
from modules.Common.readers.xml_reader import xml_reader
from modules.RPV.sverka_RPV.get_RPV_XML_data import get_RPV_XML_data
from modules.RPV.sverka_RPV.get_RPV_XML_data import insert_RVP_XML_data
from modules.RPV.sverka_RPV.create_rpv_db import create_xlsx_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.RPV.sverka_RPV.get_RPV_XLSX_data import get_RPV_XLSX_data
from modules.RPV.sverka_RPV.create_rpv_db import create_man_db
from modules.Common.readers.csv_reader import csv_reader
from modules.RPV.sverka_RPV.get_RPV_matches import get_RPV_matches


def start_RPV(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        xml_dir, xlsx_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # =============== Чтение XML файлов по РПВ ==================

        progress_status.set('Чтение XML')

        # Создание таблицы в БД для файлов из XML РПВ
        db_xml_name = 'xml_base'
        create_xml_db(db_curs, db_xml_name)

        err = xml_reader(db_xml_name, db_conn, db_curs, xml_dir, depth=[0, 5],
                         data_extract_func=get_RPV_XML_data,
                         inserting_data_func=insert_RVP_XML_data)
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        # =============== Чтение XLSX файлов по РПВ ==================

        progress_status.set('Чтение Картотеки')

        # Создание таблицы в БД для файлов из XLSX (картотека) РПВ
        db_xlsx_name = 'xlsx_base'
        create_xlsx_db(db_curs, db_xlsx_name)

        err = xlsx_reader(xlsx_dir, db_conn, db_curs, db_name=db_xlsx_name,
                          skiprows=6, processing_data_func=get_RPV_XLSX_data)
        if err:
            raise Exception(err)

        progress_value.set(10 + progress_value.get())

        # =============== Чтение csv файлов из VIB - MAN==================

        progress_status.set('Чтение выборки MAN')

        # Создание таблицы в БД для файлов из VIB
        db_man_name = 'man_base'
        create_man_db(db_curs, db_man_name)

        # Задаем название столбцам
        col_names = ['Дата смерти', 'СНИЛС', 'Район', 'Регион', 'pw']

        # Задаем индексы используемых столбцов
        col = [0, 1, 2, 3, 4]

        man_dir = os.path.join(vib_dir, 'MAN')

        err = csv_reader(db_man_name, db_conn, dir=man_dir, names=col_names,
                             usecols=col)
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        progress_status.set('Индексация СНИЛС из выборки MAN')

        db_curs.execute(f'CREATE INDEX snils_rvp_man_ind ON {db_man_name} (СНИЛС)')

        progress_value.set(10 + progress_value.get())

        # =============== Чтение csv файлов из VIB - ADV8==================

        progress_status.set('Чтение выборки ADV8')

        # Создание таблицы в БД для файлов из VIB
        db_adv8_name = 'adv8_base'
        create_adv_db(db_curs, db_adv8_name)

        # Задаем название столбцам
        col_names = ['Дата создания', 'СНИЛС', 'Дата смерти', 'Дата записи акта', 'Номер акта о смерти', 'Орган ЗАГС']

        # Задаем индексы используемых столбцов
        col = [0, 2, 3, 4, 5, 6]

        adv_dir = os.path.join(vib_dir, 'ADV8')

        err = csv_reader(db_adv8_name, db_conn, dir=adv_dir, names=col_names, encoding='windows-1251', usecols=col)
        if err:
            raise Exception(err)

        progress_value.set(20 + progress_value.get())

        progress_status.set('Индексация СНИЛС из выборки ADV8')

        db_curs.execute(f'CREATE INDEX snils_rvp_adv8_ind ON {db_adv8_name} (СНИЛС)')

        progress_value.set(10 + progress_value.get())

        # =============== Обработка БД и выгрузка результата ==================

        progress_status.set('Обработка БД')

        get_RPV_matches(db_curs, xml_db=db_xml_name, xlsx_db=db_xlsx_name, man_db=db_man_name, adv8_db=db_adv8_name)

        progress_value.set(200 - progress_value.get())

    except Exception as e:
        err = e
    finally:
        # Чистим БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_xml_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_xlsx_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_man_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_adv8_name}")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err
