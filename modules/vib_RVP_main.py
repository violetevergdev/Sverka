from modules.Common.browser_init import browser
from modules.Common.start_vib import start_to_vib
import os

def vib_RVP(server, out_dir):
    # Запуск браузера
    driver = browser(out_dir)

    if server == "M":
        # Запуск выборки по Москве
        start_to_vib(driver, server, "РВП", out_dir)
    else:
        # Запуск выборки по Области
        start_to_vib(driver, server, "РВП", out_dir)


def vib_RVP_main(out_path):
    vib_RVP("M", out_path)
    vib_RVP("MO", out_path)

if __name__ == '__main__':
    vib_RVP_main()