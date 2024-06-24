from modules.NVP.browser_init import browser
from modules.NVP.start_vib import start_to_vib


def vib(out_dir, server):
    # Запуск браузера
    driver = browser(out_dir)

    if server == "M":
        # Запуск выборки по Москве
        start_to_vib(driver, server, out_dir)
    else:
        # Запуск выборки по Области
        start_to_vib(driver, server, out_dir)


def vib_main(out_dir):
    vib(out_dir, "M")
    vib(out_dir, "MO")