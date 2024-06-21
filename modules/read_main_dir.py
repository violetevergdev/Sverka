import os


def read_main_dir(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".xml") or file.endswith(".XML"):
            xml_file = os.path.join(folder_path, file)
        elif file == "КАРТОТЕКА РАЗОВОЙ":
            xlsx_dir_path = os.path.join(folder_path, file)
        elif file == "НВП":
            csv_dir_path = os.path.join(folder_path, file)


    return xml_file, xlsx_dir_path, csv_dir_path