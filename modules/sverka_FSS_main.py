from modules.FSS.sverka_FSS.xlsx_FSS_reader import xlsx_reader
from modules.Common.db_connection import db_connection
from modules.Common.read_main_dir import read_main_dir
from modules.FSS.sverka_FSS.vib_FSS_reader import vib_reader
from modules.FSS.sverka_FSS.get_FSS_matches import get_FSS_matches

def sverka_FSS_main():
    try:
        conn, c = db_connection()

        in_path = 'IN/ФСС'
        out_path = 'OUT'

        xlsx_dir, vib_dir = read_main_dir(in_path, 'ФСС')

        # Обрабатываем поступающие данные
        xlsx_reader(conn, c, xlsx_dir)
        vib_reader(conn, c, vib_dir)

        # Обрабатываем БД
        get_FSS_matches(c, out_path)

        # Чистим БД на выходе
        try:
            c.execute("DROP TABLE fss_base")
            c.execute("DROP TABLE vib_fss_base")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err

        conn.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    sverka_FSS_main()