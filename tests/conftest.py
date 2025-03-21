import pytest
import tkinter as tk
from datetime import datetime

from modules.Common.customization.db_connection import db_connection


@pytest.fixture(scope='class')
def fake_gui():
    root = tk.Tk()
    root.withdraw()

    progress_value = tk.IntVar()
    progress_status = tk.StringVar()

    yield {"progress_value": progress_value, "progress_status": progress_status}

    root.destroy()


@pytest.fixture
def runtime_tracking():
    def _runtime_tracking(func, time_limit, *args):
        start_time = datetime.now()
        print(f'\nНачало работы функции - {args[0]}')

        result = func(*args)

        end_time = datetime.now()
        time_taken = (end_time - start_time).total_seconds()
        print(f'Конец работы функции {args[0]}. Время выполнения - {time_taken} сек.')

        if time_taken > time_limit:
            raise TimeoutError

        return result

    return _runtime_tracking


@pytest.fixture()
def setup_test_reader():
    def _setup(db_name, col_names):
        conn, c = db_connection()
        c.execute(f'DROP TABLE IF EXISTS {db_name}')

        sql_col = ','.join(col_names)
        c.execute(f"""CREATE TABLE IF NOT EXISTS {db_name} ({sql_col})""")

        return conn

    yield _setup


@pytest.fixture()
def teardown_test_reader():
    def _teardown(c, db_name):
        res = c.execute(f"SELECT * FROM {db_name}").fetchall()
        return res

    return _teardown
