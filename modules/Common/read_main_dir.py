import os

def read_main_dir(folder_path):
    for file in os.listdir(folder_path):
        if file == 'XLSX':
            xlsx_dir = os.path.join(folder_path, file)
        elif file == 'VIB':
            vib_dir = os.path.join(folder_path, file)
    return xlsx_dir, vib_dir





