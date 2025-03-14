import os

from modules.CHAES.start_CHAES_sver import start_CHAES
from modules.NAKOP.start_NAKOP_sver import start_NAKOP
from modules.vib_main import start_vib_main
from modules.Common.customization.db_connection import db_connection
from modules.MITS.start_MITS_sver import start_MITS
from modules.RPV.start_RPV_sver import start_RPV
from modules.FSS.start_FSS_sver import start_FSS
from modules.FSS_BASE.start_FSS_BASE_sver import start_FSS_BASE
from modules.OPEK.start_OPEK_sver import start_OPEK

from settings.config import settings as conf


# Запуск скриптов в зависимости от типа сверки и условия выборки
def sver_main(type_of_sver, vib_state, progress_value, progress_status):
    # Задаем пути рабочих директорий
    in_path = os.path.join(conf.in_path, type_of_sver)
    out_vib_dir = os.path.join(os.getcwd(), in_path, 'VIB')

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
            err = start_RPV(in_path, type_of_sver, conn, c, progress_value, progress_status)
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
        elif type_of_sver == 'ОПЕКУНЫ':
            err = start_OPEK(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err
        elif type_of_sver == 'ЧАЭС':
            err = start_CHAES(in_path, type_of_sver, conn, c, progress_value, progress_status)
            if err:
                return err

    except Exception as e:
        err = 'Ошибка сверки: ' + str(e)
        return err
    finally:
        conn.close()


if __name__ == '__main__':
    sver_main('ОПЕКУНЫ', False, None, None)
