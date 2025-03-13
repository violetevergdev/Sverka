import os


def read_main_dir(folder_path, type_sver):
    if type_sver == 'РПВ':
        for file in os.listdir(folder_path):
            if file == 'XML':
                xml_dir = os.path.join(folder_path, file)
            elif file == "КАРТОТЕКА РАЗОВОЙ":
                xlsx_dir = os.path.join(folder_path, file)
            elif file == "VIB":
                vib_dir = os.path.join(folder_path, file)
        return xml_dir, xlsx_dir, vib_dir
    elif type_sver == 'МСП':
        for file in os.listdir(folder_path):
            if file == 'MITS':
                mits_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)
        return mits_dir, vib_dir
    elif type_sver in ('ФСС', 'ФСС-БАЗА'):
        for file in os.listdir(folder_path):
            if file == 'XLSX':
                xlsx_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)
        return xlsx_dir, vib_dir
    elif type_sver == 'НАКОП':
        for file in os.listdir(folder_path):
            if file == 'XLSX':
                xlsx_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)
            elif file == 'DONT_LOC':
                loc_dir = os.path.join(folder_path, file)
        return xlsx_dir, vib_dir, loc_dir
    elif type_sver == 'ОПЕКУНЫ':
        for file in os.listdir(folder_path):
            if file == 'CSV':
                opek_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)
        return opek_dir, vib_dir
    elif type_sver == 'ЧАЭС':
        for file in os.listdir(folder_path):
            if file == 'XLSX':
                xlsx_dir = os.path.join(folder_path, file)
            elif file == 'VIB':
                vib_dir = os.path.join(folder_path, file)
        return xlsx_dir, vib_dir




