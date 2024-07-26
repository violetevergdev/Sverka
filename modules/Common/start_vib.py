import os
import time

from modules.Common.customization.browser_init import browser
from modules.Common.viborka.configurations.get_vib_configs import get_vib_config
from modules.Common.viborka.nvp_routes.open_nvp import open_nvp
from modules.Common.viborka.nvp_routes.authentication import authentication
from modules.Common.viborka.nvp_routes.open_vib_url import open_vib_url

from modules.Common.vib_routes import vib_routes


def start_to_vib(server, type_of_vib, out_path):
    try:
        # Запуск браузера
        driver = browser(out_path)

        # Получаем конфигурационые данные
        routes_config, login_config, config_data = get_vib_config(type_of_vib)

        # Запуск VIB в Firefox
        err = open_nvp(server, type_of_vib, driver, routes_config)
        if err:
            return err

        # Логинимся
        err = authentication(driver, login_config)
        if err:
            return err

        # Переход на страницу выборок
        err = open_vib_url(server, type_of_vib, driver, routes_config)
        if err:
            return err

        # Осуществление выборки
        vib_routes(driver, config_data, server, type_of_vib)

        # Переименование
        old_name = os.path.join(out_path, 'results.csv')
        new_name = old_name.replace('.csv', '_' + server + '.csv')
        os.rename(old_name, new_name)

    except Exception as e:
        return e
    finally:
        driver.close()
