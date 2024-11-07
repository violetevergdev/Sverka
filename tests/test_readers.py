import os

import pytest
from contextlib import nullcontext as does_not_raise

from modules.Common.readers.xlsx_reader import xlsx_reader
from modules.Common.readers.xml_reader import xml_reader
from settings.config import settings as conf
from modules.Common.readers.csv_reader import csv_reader
from modules.Common.refactor_data import format_snils_with_fill_zero
from tests.custom_errors import *


class MockDatas:
    @staticmethod
    def opt(df):
        df['npers'] = df['npers'].apply(format_snils_with_fill_zero)

    @staticmethod
    def xlsx_col_names():
        return ['Вид_выплаты_pfr', 'СНИЛС_pfr', 'Фамилия_pfr', 'Имя_pfr', 'Отчество_pfr', 'Дата_рождения_pfr',
                'Сумма_pfr', 'Район_pfr']

    @staticmethod
    def process_func_for_xlsx(df, db_curs, db_name, file=None):
        data = []
        for _, row in df.iterrows():
            if row[1] == "":
                continue

            try:
                ot = row[4].split(",")[0].split()[2]
            except IndexError:
                ot = 'None'

            temp_data = {
                'Вид_выплаты_pfr': row[2],
                'СНИЛС_pfr': row[3].replace('\n\t\t', ""),
                'Фамилия_pfr': row[4].split(",")[0].split()[0],
                'Имя_pfr': row[4].split(",")[0].split()[1],
                'Отчество_pfr': ot,
                'Дата_рождения_pfr': row[4].split(",")[1],
                'Сумма_pfr': row[5],
                'Район_pfr': file.replace('.xls', ''),
            }
            data.append(temp_data)

        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (:Вид_выплаты_pfr, :СНИЛС_pfr, :Фамилия_pfr, :Имя_pfr, :Отчество_pfr, :Дата_рождения_pfr, :Сумма_pfr, :Район_pfr)',
            data)

    @staticmethod
    def xml_col_names():
        return ['СНИЛС', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Код валюты', 'Сумма выплаты РФ']

    @staticmethod
    def extract_xml(item):
        if item[0].tag.endswith("ПенсияВВ"):
            return 'BREAK'
            # Обрабатываем записи без СНИЛСОВ
        if not item[0][0].tag.endswith("СНИЛС"):
            data = {
                'СНИЛС': None,
                'Фамилия': item[0][0][0].text,
                'Имя': item[0][0][1].text,
                'Отчество': item[0][0][2].text,
                'Дата_рождения': item[0][2].text,
                'Код_валюты': item[1].text,
                'Сумма_выплаты_РФ': item[6].text
            }
            return data
        else:
            # Обрабатываем корректные записи
            data = {
                'СНИЛС': item[0][0].text,
                'Фамилия': item[0][1][0].text,
                'Имя': item[0][1][1].text,
                'Отчество': item[0][1][2].text,
                'Дата_рождения': item[0][3].text,
                'Код_валюты': item[1].text,
                'Сумма_выплаты_РФ': item[6].text
            }
            return data

    @staticmethod
    def insert_xml(db_curs, db_name, data):
        db_curs.executemany(
            f'INSERT INTO {db_name} VALUES (:СНИЛС, :Фамилия, :Имя, :Отчество, :Дата_рождения, :Код_валюты, :Сумма_выплаты_РФ)', data)


class TestReaders:
    @pytest.mark.parametrize(
        'dir_name, col_names, use_cols, skiprows, opt, exp_len, exp',
        [
            (os.path.join(conf.test_in_path, 'CSV/validSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 0, None, 1000, does_not_raise()),
            (os.path.join(conf.test_in_path, 'CSV/validSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 3, None, 997, does_not_raise()),
            (os.path.join(conf.test_in_path, 'CSV/validSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 4], 0, None, 0, pytest.raises(GetFailedAttr)),
            (os.path.join(conf.test_in_path, 'CSV/invalidSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 0, MockDatas.opt, 1000, does_not_raise()),
            (os.path.join(conf.test_in_path, 'CSV/invalidSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 0, MockDatas.opt, 100, pytest.raises(FailedExpectedLen)),
        ]
    )
    def test_csv(self, setup_test_reader, teardown_test_reader, dir_name, col_names, use_cols, skiprows, opt, exp_len,
                 exp):
        conn = setup_test_reader('test_csv_db', col_names)
        c = conn.cursor()

        try:
            with exp:
                err = csv_reader('test_csv_db', conn, dir_name, col_names, use_cols, skiprows, opt=opt)
                if err is not None:
                    raise GetFailedAttr(err)

                res = teardown_test_reader(c, 'test_csv_db')

                if len(res) != exp_len:
                    raise FailedExpectedLen()

        finally:
            conn.close()

    @pytest.mark.parametrize(
        'dir_name, skiprows, process_func, exp_len, exp',
        [
            (os.path.join(conf.test_in_path, 'XLSX/validSNILS'),
             6, None, 0, pytest.raises(GetFailedAttr)),
            (os.path.join(conf.test_in_path, 'XLSX/validSNILS'),
             6, MockDatas.process_func_for_xlsx, 2003, does_not_raise()),
            (os.path.join(conf.test_in_path, 'XLSX/validSNILS'),
             6, MockDatas.process_func_for_xlsx, 2000, pytest.raises(FailedExpectedLen)),
        ]
    )
    def test_xlsx(self, setup_test_reader, teardown_test_reader, dir_name, skiprows, process_func, exp_len, exp):
        conn = setup_test_reader('test_xlsx_db', col_names=MockDatas.xlsx_col_names())
        c = conn.cursor()

        try:
            with exp:
                err = xlsx_reader(dir_name, conn, c, 'test_xlsx_db', skiprows, process_func)
                if err is not None:
                    raise GetFailedAttr(err)

                res = teardown_test_reader(c, 'test_xlsx_db')
                if len(res) != exp_len:
                    raise FailedExpectedLen()
        finally:
            conn.close()

    @pytest.mark.parametrize(
        'dir_name, depth, extract_func, insert_func, exp_len, exp',
        [
            (os.path.join(conf.test_in_path, 'XML'), [0, 5],
             MockDatas.extract_xml, MockDatas.insert_xml, 50, does_not_raise()),
            (os.path.join(conf.test_in_path, 'XML'), [1, 6],
             MockDatas.extract_xml, MockDatas.insert_xml, 50, pytest.raises(GetFailedAttr)),
            (os.path.join(conf.test_in_path, 'XML'), [0, 5],
             MockDatas.extract_xml, MockDatas.insert_xml, 55, pytest.raises(FailedExpectedLen)),
            (os.path.join(conf.test_in_path, 'XML'), [0, 5],
             MockDatas.extract_xml, None, 50, pytest.raises(GetFailedAttr)),
        ]
    )
    def test_xml(self, setup_test_reader, teardown_test_reader, dir_name, depth, extract_func, insert_func, exp_len,
                 exp):
        conn = setup_test_reader('test_xml_db', col_names=MockDatas.xml_col_names())
        c = conn.cursor()

        try:
            with exp:
                err = xml_reader('test_xml_db', conn, c, dir_name, depth, extract_func, insert_func)
                if err is not None:
                    raise GetFailedAttr(err)

                res = teardown_test_reader(c, 'test_xml_db')
                if len(res) != exp_len:
                    raise FailedExpectedLen()
        finally:
            conn.close()
