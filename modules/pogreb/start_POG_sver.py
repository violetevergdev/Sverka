from modules.Common.read_main_dir import read_main_dir

from modules.pogreb.create_POG_db import create_vip_db, create_zayav_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.pogreb.get_POG_vip_data import get_POG_vip_data
from modules.pogreb.get_POG_zayav_data import get_POG_zayav_data
from modules.pogreb.get_POG_matches import get_POG_matches

def start_POG_sver(in_path, db_conn, db_curs):
    try:
        # Чтение рабочей директории
        vip, zayav = read_main_dir(in_path)

        # =============== Чтение файла выплатные реестры ==================

        # Создание таблицы в БД для файлов из XLSX (картотека) РВП
        db_vip_name = 'vip_base'
        create_vip_db(db_curs, db_vip_name)

        err = xlsx_reader(vip, db_conn, db_curs, db_name=db_vip_name, processing_data_func=get_POG_vip_data)
        if err:
            return err

        # =============== Чтение файла реестры заявлений ==================

        # Создание таблицы в БД для файлов из XLSX (картотека) РВП
        db_zauav_name = 'zayav_base'
        create_zayav_db(db_curs, db_zauav_name)

        err = xlsx_reader(zayav, db_conn, db_curs, db_name=db_zauav_name, processing_data_func=get_POG_zayav_data)
        if err:
            return err

        # =============== Обработка БД и выгрузка результата ==================

        get_POG_matches(db_curs, vip_db=db_vip_name, zayav_db=db_zauav_name)

    except Exception as e:
        return e
    # finally:
    #     # Чистим БД на выходе
    #     try:
    #         db_curs.execute(f"DROP TABLE {db_vip_name}")
    #         db_curs.execute(f"DROP TABLE {db_zauav_name}")
    #     except Exception as e:
    #         err = "Невозможно удалить БД" + str(e)
    #         return err