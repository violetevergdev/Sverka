import pytest

from modules.Common.refactor_data import *


class TestRefactorData:
    @pytest.mark.parametrize(
        'unvalid_snils, exp',
        [
            (int(12312312312), '123-123-123 12'),
            (float(123123123), '001-231-231 23'),
            ('', None),
            (float(1237231231.00), '012-372-312 31'),
            ('98998982', '000-989-989 82'),
            ('| 9893+98982', '009-893-989 82'),
            (float(), None),
            (int(), None),

        ]
    )
    def test_format_snils(self, unvalid_snils, exp):
        snils = format_snils_with_fill_zero(unvalid_snils)
        assert snils == exp


    @pytest.mark.parametrize(
        'unvalid_data, exp',
        [
            ('12.12.1212', '1212-12-12'),
            ('1.12.1212', '1212-12-1'),
        ]
    )
    def test_format_data(self, unvalid_data, exp):
        date = format_date_from_dot_to_dash(unvalid_data)
        assert date == exp


    @pytest.mark.parametrize(
        'unvalid_str, exp',
        [
            (float(123.4), '123'),
            (123, '123'),
            ('123.4', '123'),
        ]
    )
    def test_to_str(self, unvalid_str, exp):
        s = to_str_type(unvalid_str)
        assert s == exp