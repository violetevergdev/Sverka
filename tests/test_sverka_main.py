import pytest
from contextlib import nullcontext as does_not_raise

from modules.sverka_main import sver_main


class TestSverkaMain():
    @pytest.mark.parametrize(
        'type_op, sec, exp',
        [
            ('РПВ', 3, does_not_raise()),  # 1.353138 сек.
            ('МСП', 3, does_not_raise()),  # 2.686599 сек.
            ('ФСС', 12, does_not_raise()),  # 10.301286 сек.
            ('ФСС', 5, pytest.raises(TimeoutError)),  # 9.866683 сек.
            ('ФСС-БАЗА', 23, does_not_raise()),  # 19.237339 сек.
            ('НАКОП', 60, does_not_raise())  # 57.387759 сек.
        ]
    )
    def test_main_time_of_work(self, fake_gui, runtime_tracking, type_op, sec, exp):
        with exp:
            make_fake_gui = fake_gui
            progress_value = make_fake_gui["progress_value"]
            progress_status = make_fake_gui["progress_status"]

            res = runtime_tracking(sver_main, sec, type_op, False, progress_value, progress_status)

            assert res is None
