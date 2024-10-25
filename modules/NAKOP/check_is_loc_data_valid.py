import os
import pandas as pd
from tkinter import messagebox as mbox


def check_loc_data_on_failed_files(loc_dir, skiprows=0):
    failed_files = []
    for file in os.listdir(loc_dir):
        if file.endswith(".xls") or file.endswith(".xlsx"):

                file_path = os.path.join(loc_dir, file)

                df = pd.read_excel(file_path, skiprows=skiprows, na_filter=False)

                for _, row in df.iterrows():
                    print(row[0], file, loc_dir)
                    if row[1] in ("", " ", None):
                        continue

                    if row[0] in ("", " ", None):
                        if file in failed_files:
                            continue
                        else:
                            failed_files.append(file)

    return failed_files

def is_loc_data_valid(loc_dir, skiprows=0):
    try:
        result = None
        failed_files = check_loc_data_on_failed_files(loc_dir, skiprows=skiprows)

        if len(failed_files) > 0:
            result = mbox.askyesno("Подтверждение", "В файлах DONT_LOC имеются ошибки, продолжить сверку?")

        return result, failed_files


    except Exception as e:
        e = __name__, e
        return e