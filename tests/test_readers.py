import os

import pytest

from settings.config import settings as conf
from modules.Common.readers.csv_reader import csv_reader
from modules.Common.refactor_data import format_snils_with_fill_zero

def mock_opt(df):
    df['npers'] = df['npers'].apply(format_snils_with_fill_zero)

class TestReaders:
    @pytest.mark.parametrize(
        'dir_name, col_names, use_cols, skiprows, opt, exp',
        [
            (os.path.join(conf.test_in_path, 'CSV/validSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 0, None, None),
            (os.path.join(conf.test_in_path, 'CSV/validSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 4], 0, None, pytest.raises(Exception)),
            (os.path.join(conf.test_in_path, 'CSV/invalidSNILS'),
             ['npers', 'ra', 'pw'], [0, 1, 3], 0, mock_opt, None),

        ]
    )
    def test_csv(self, setup_test_reader, dir_name,col_names, use_cols, skiprows, opt, exp):
        run = setup_test_reader
        if exp:
            with exp:
                err = run(csv_reader, 'test_csv_db', dir_name, col_names, use_cols, skiprows, opt)
                assert err is exp
        else:
            err = run(csv_reader, 'test_csv_db', dir_name, col_names, use_cols, skiprows, opt)
            assert err is None







