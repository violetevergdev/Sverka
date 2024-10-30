import os
from datetime import datetime

from modules.NAKOP.start_NAKOP_sver import start_NAKOP
from modules.vib_main import start_vib_main
from modules.Common.customization.db_connection import db_connection
from modules.MITS.start_MITS_sver import start_MITS
from modules.RVP.start_RVP_sver import start_RVP
from modules.FSS.start_FSS_sver import start_FSS
from modules.FSS_BASE.start_FSS_BASE_sver import start_FSS_BASE


# Запуск скриптов в зависимости от типа сверки и условия выборки
def sver_main(type_of_sver, vib_state, progress_value, progress_status):
    # Задаем пути рабочих директорий
    in_path = os.path.join('IN', type_of_sver)
    out_vib_dir = os.path.join(os.getcwd(), in_path, 'VIB')

    if os.getenv('ENV_FOR_DYNACONF') == 'test':
        in_path = os.path.join('C:\Violet\DEV_PROJ\WORKING\Sverka\IN', type_of_sver)

    # Запуск выборки при наличии условия
    if vib_state is True:
        try:
            progress_status.set("Выполняется выборка")
            start_vib_main(type_of_sver, out_vib_dir)
            progress_value.set(20)
        except Exception as e:
            err = 'Ошибка выборки: ' + str(e)
            return err

    try:
        # Подключение к БД
        conn, c = db_connection()

        if type_of_sver == 'МСП':
            err = start_MITS(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err
        elif type_of_sver == 'РПВ':
            err = start_RVP(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err
        elif type_of_sver == 'ФСС':
            err = start_FSS(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err
        elif type_of_sver == 'ФСС-БАЗА':
            err = start_FSS_BASE(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err
        elif type_of_sver == 'НАКОП':
            err = start_NAKOP(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err

    except Exception as e:
        err = 'Ошибка сверки: ' + str(e)
        return err
    finally:
        conn.close()


if __name__ == '__main__':
    sver_main('ФСС-БАЗА', False)
