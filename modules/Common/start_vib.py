import json
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
        # Получаем конфигурационые данные
        routes_config, login_config, conf_list = get_vib_config(type_of_vib)

        for type_config in conf_list:
            if type_config:
                with open(type_config, "r") as f:
                    config_data = json.load(f)

            try:
                if "out_path" in config_data:
                    new_out_path = os.path.join(out_path, config_data["out_path"])
                else:
                    new_out_path = out_path

                # Запуск браузера
                driver = browser(new_out_path)

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

                if server == 'M':
                    while len(os.listdir(new_out_path)) == 0:
                        time.sleep(1)
                    while any(file.endswith('.part') for file in os.listdir(new_out_path)):
                        time.sleep(1)
                else:
                    while len(os.listdir(new_out_path)) < 2:
                        time.sleep(1)
                    while any(file.endswith('.part') for file in os.listdir(new_out_path)):
                        time.sleep(1)

                # Переименование
                old_name = os.path.join(new_out_path, 'results.csv')
                new_name = old_name.replace('.csv', '_' + server + '.csv')
                os.rename(old_name, new_name)
            except Exception as e:
                return e
            finally:
                driver.close()

    except Exception as e:
        return e
