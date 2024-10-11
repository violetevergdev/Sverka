import os

def read_main_dir(folder_path):
    for file in os.listdir(folder_path):
        if file.startswith("выплатной реестр"):
            vip = os.path.join(folder_path, file)
        else:
            if file.startswith("реестр заявлений"):
                zayav = os.path.join(folder_path, file)
            return vip, zayav





