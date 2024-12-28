from modules.Common.read_main_dir import read_main_dir
from modules.Common.create_db import create_db
from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.SEP_ADDR.get_ADDR_data import get_prosec_data, get_spisok_data
from modules.SEP_ADDR.get_ADDR_matches import get_ADDR_matches


# Запуск сценария обработки документов по опекунам
def start_ADDR(in_path, type_of_sver, db_conn, db_curs, progress_value, progress_status):
    err = None
    try:
        # Чтение рабочей директории
        prosec_dir, vib_dir = read_main_dir(in_path, type_of_sver)

        # ============= Чтение входящих csv файлов по опекунам ================

        # Задаем название БД
        db_prosec_name = 'prosec_base'

        # Задаем название столбцам
        col_names = ['Район', 'СНИЛС', 'ФИО',
                     'Дата рождения', 'Номер исп. документа', 'Дата выдачи документа', 'Название испол. документа', 'Вид взыскания', 'Ежемес. % удерж', 'Ежемес. сумма удерж', 'Дата начала выплат', 'Дата окончания удержания', 'Огр. до прожиточного мин.', 'Вид госпенсии-1', 'Вид трудовой пенсии']

        # Создаем таблицу в БД
        create_db(db_conn, db_prosec_name, col_names)

        err = xlsx_reader(prosec_dir, db_conn, db_curs, db_name=db_prosec_name, skiprows=0, processing_data_func=get_prosec_data)
        if err:
            raise Exception(err)


        # # =============== Чтение xlsx файла SPISOK  ==================

        # Задаем название БД
        db_vib_name = 'spis_base'

        # Задаем название столбцам
        col_names = ['Снилс', 'Регион', 'Район', 'Населеный пункт', 'Улица', 'Дом', 'Корпус', 'Квартира' ]

        # Создаем таблицу в БД для файлов из VIB
        create_db(db_curs, db_vib_name, col_names)

        err = xlsx_reader(vib_dir, db_conn, db_curs, db_name=db_vib_name, skiprows=2, processing_data_func=get_spisok_data)
        if err:
            raise Exception(err)

        db_curs.execute(f'CREATE INDEX snils_ind ON {db_vib_name} (Снилс)')


        # =============== Обработка БД и выгрузка результата ==================

        get_ADDR_matches(db_curs, prosec_db=db_prosec_name, spisok_db=db_vib_name)


    except Exception as e:
        err = e
    finally:
        # Чистка БД на выходе
        try:
            db_curs.execute(f"DROP TABLE IF EXISTS {db_prosec_name}")
            db_curs.execute(f"DROP TABLE IF EXISTS {db_vib_name}")
        except Exception as e:
            if err is None:
                return "Невозможно удалить БД: " + str(e)

        if err:
            return err
