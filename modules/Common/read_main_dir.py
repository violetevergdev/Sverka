import os


def read_main_dir(folder_path, type_sver):
    if type_sver == 'РВП':
        for file in os.listdir(folder_path):
            if file.endswith(".xml") or file.endswith(".XML"):
                xml_file = os.path.join(folder_path, file)
            elif file == "КАРТОТЕКА РАЗОВОЙ":
                xlsx_dir_path = os.path.join(folder_path, file)
            elif file == "НВП":
                csv_dir_path = os.path.join(folder_path, file)

        return xml_file, xlsx_dir_path, csv_dir_path
    elif type_sver == 'МиЦ':
        for file in os.listdir(folder_path):
            if file == 'MITS':
                mits_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)

        return mits_dir, vib_dir


