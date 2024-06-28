from modules.Common.browser_init import browser
from modules.Common.start_vib import start_to_vib


def vib_MITS(server, out_dir):
    # Запуск браузера
    driver = browser(out_dir)

    if server == "M":
        # Запуск выборки по Москве
        start_to_vib(driver, server, "МиЦ", out_dir)
    else:
        # Запуск выборки по Области
        start_to_vib(driver, server, "МиЦ", out_dir)


def vib_MITS_main(out_dir):
    vib_MITS("M", out_dir)
    vib_MITS("MO", out_dir)


if __name__ == '__main__':
    vib_MITS_main()