from modules.RVP.sverka_RVP.vib_RVP_reader import csv_reader
from modules.Common.db_connection import db_connection
from modules.RVP.sverka_RVP.get_RVP_matches import get_matches
from modules.Common.read_main_dir import read_main_dir
from modules.RVP.sverka_RVP.xlsx_reader import xlxs_reader
from modules.RVP.sverka_RVP.xml_reader import xml_reader

def sverka_RVP_main():
    try:
        conn, c = db_connection()

        in_path = 'IN/РВП'
        out_path = 'OUT'

        xml_file, xlsx_dir_path, csv_dir_path = read_main_dir(in_path, "РВП")

        # Обрабатываем поступающие данные
        xml_reader(conn, c, xml_file)
        xlxs_reader(conn, c, xlsx_dir_path)
        csv_reader(conn, c, csv_dir_path)

        # Обрабатываем БД
        get_matches(c, out_path)

        # Чистим БД на выходе
        try:
            c.execute("DROP TABLE xml_base")
            c.execute("DROP TABLE pfr_base")
            c.execute("DROP TABLE nvp_base")
        except Exception as e:
            err = "Невозможно удалить БД" + str(e)
            return err

        conn.close()
    except Exception as e:
        return e


if __name__ == '__main__':
    sverka_RVP_main()
