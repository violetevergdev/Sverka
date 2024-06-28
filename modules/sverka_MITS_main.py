from modules.MITS.sverka_MITS.mits_reader import mits_reader
from modules.Common.db_connection import db_connection
from modules.Common.read_main_dir import read_main_dir
from modules.MITS.sverka_MITS.vib_MITS_reader import vib_reader
from modules.MITS.sverka_MITS.get_MITS_matches import get_MITS_matches
from tkinter import filedialog

def sverka_MITS_main():
    try:
        conn, c = db_connection()

        in_path = 'IN/МСП'
        out_path = 'OUT'

        mits_dir, vib_dir = read_main_dir(in_path, 'МиЦ')

        # Обрабатываем поступающие данные
        mits_reader(conn, c, mits_dir)
        vib_reader(conn, c, vib_dir)

        # Обрабатываем БД
        get_MITS_matches(c, out_path)

        # Чистим БД на выходе
        try:
            c.execute("DROP TABLE mits_base")
            c.execute("DROP TABLE vib_msp_base")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err

        conn.close()

    except Exception as e:
        return e


if __name__ == '__main__':
    sverka_MITS_main()
