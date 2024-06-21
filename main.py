from modules.read_main_dir import read_main_dir
from modules.xml_reader import xml_reader
from modules.xlsx_reader import xlxs_reader
from modules.csv_reader import csv_reader
from modules.db_connection import db_connection
from modules.get_matches import get_matches


def main(folder_path):
    try:
        conn, c = db_connection()

        xml_file, xlsx_dir_path, csv_dir_path = read_main_dir(folder_path)

        # Обрабатываем поступающие данные
        xml_reader(conn, c, xml_file)
        xlxs_reader(conn, c, xlsx_dir_path)
        csv_reader(conn, c, csv_dir_path)

        # Обрабатываем БД
        get_matches(c, folder_path)

        # Чистим БД на выходе
        try:
            c.execute("DROP TABLE xml_base")
            c.execute("DROP TABLE pfr_base")
            c.execute("DROP TABLE nvp_base")
        except Exception as e:
            print(e)

        conn.close()
    except Exception as e:
        return e


if __name__ == '__main__':
    main('input/задача по РПВ')
