
from datetime import datetime

import pytest

from sverka_main import sver_main
import tkinter as tk
class TestSverkaMain():
    @pytest.fixture
    def fake_gui(self):
        root = tk.Tk()
        root.withdraw()

        progress_value = tk.IntVar()
        progress_status = tk.StringVar()

        yield {"root": root, "progress_value": progress_value, "progress_status": progress_status}

        root.destroy()

    @pytest.fixture
    def runtime_tracking(self):
        def _runtime_tracking(func, time_limit, *args, **kwargs):
            start_time = datetime.now()
            print(f'\nНачало работы функции - {args[0]}')

            result = func(*args, **kwargs)

            end_time = datetime.now()
            time_taken = (end_time - start_time).total_seconds()
            print(f'Конец работы функции {args[0]}. Время выполнения - {time_taken} сек.')

            assert time_taken <= time_limit, f"Время выполнения {time_taken} превысило {time_limit} секунд."

            return result

        return _runtime_tracking

    def test_RVP_time_of_work(self, fake_gui, runtime_tracking):
        make_fake_gui = fake_gui
        progress_value = make_fake_gui["progress_value"]
        progress_status = make_fake_gui["progress_status"]

        res = runtime_tracking(sver_main, 3, "РПВ", False, progress_value, progress_status)

        assert res is None

    def test_MITS_time_of_work(self, fake_gui, runtime_tracking):
        make_fake_gui = fake_gui
        progress_value = make_fake_gui["progress_value"]
        progress_status = make_fake_gui["progress_status"]

        res = runtime_tracking(sver_main, 3, "МСП", False, progress_value, progress_status)

        assert res is None

    def test_FSS_time_of_work(self, fake_gui, runtime_tracking):
        make_fake_gui = fake_gui
        progress_value = make_fake_gui["progress_value"]
        progress_status = make_fake_gui["progress_status"]

        res = runtime_tracking(sver_main, 30, "ФСС", False, progress_value, progress_status)

        assert res is None

    def test_FSS_BASE_time_of_work(self, fake_gui, runtime_tracking):
        make_fake_gui = fake_gui
        progress_value = make_fake_gui["progress_value"]
        progress_status = make_fake_gui["progress_status"]

        res = runtime_tracking(sver_main, 30, "ФСС-БАЗА", False, progress_value, progress_status)

        assert res is None


    def test_NAKOP_time_of_work(self, fake_gui, runtime_tracking):
        make_fake_gui = fake_gui
        progress_value = make_fake_gui["progress_value"]
        progress_status = make_fake_gui["progress_status"]

        res = runtime_tracking(sver_main, 60, "НАКОП", False, progress_value, progress_status)

        assert res is None

