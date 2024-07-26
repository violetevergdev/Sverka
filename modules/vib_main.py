
from modules.Common.start_vib import start_to_vib


def start_vib_main(type_of_sver, out_dir):
    try:
        # Запуск выборки по Москве
        start_to_vib('M', type_of_sver, out_dir)

        # Запуск выборки по Области
        start_to_vib('MO', type_of_sver, out_dir)
    except Exception as e:
        return e
