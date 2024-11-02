import pytest
from contextlib import nullcontext as does_not_raise

from modules.sverka_main import sver_main

class TestSverkaMain():
    @pytest.mark.parametrize(
        'type_op, sec, exp',
        [
            ('РПВ', 3, does_not_raise()),
            ('МСП', 3, does_not_raise()),
            ('ФСС', 12, does_not_raise()),
            ('ФСС', 5, pytest.raises(TimeoutError)),
            ('ФСС-БАЗА', 23, does_not_raise()),
            ('НАКОП', 60, does_not_raise())
        ]
    )
    def test_main_time_of_work(self, fake_gui, runtime_tracking, type_op, sec, exp):
        with exp:
            make_fake_gui = fake_gui
            progress_value = make_fake_gui["progress_value"]
            progress_status = make_fake_gui["progress_status"]

            res = runtime_tracking(sver_main, sec, type_op, False, progress_value, progress_status)

            assert res is None

