import json
import os
import time

from modules.Common.authentication import authentication
from modules.Common.vib_routes import vib_routes


def start_to_vib(driver, server, type_of_vib, out_path):
    # Получаем конфигурационные данные
    server_config = {
        "M": {
            "РВП": "config/RVP_CONF/rvp_conf_М.json",
            "МиЦ": "config/MITS_CONF/mits_conf_M.json",
        },
        "MO": {
            "РВП": "config/RVP_CONF/rvp_conf_МO.json",
            "МиЦ": "config/MITS_CONF/mits_conf_MO.json",
        },
    }

    configuration_file = server_config.get(server).get(type_of_vib)
    if configuration_file:
        with open(configuration_file, "r") as f:
            config_data = json.load(f)

    # Запуск НВП в Firefox
    try:
        if server == "M":
            driver.get(config_data["url"]["login_M"])
        else:
            driver.get(config_data["url"]["login_MO"])
    except Exception as e:
        err = str(e) + "Неверный URL адрес для аутентификации"
        return err

    # Логинимся
    authentication(driver, config_data)

    # Переход на страницу выборок
    try:
        if server == "M":
            driver.get(config_data["url"]["vib_M"])
        else:
            driver.get(config_data["url"]["vib_MO"])
    except Exception as e:
        err = str(e) + "Неверный URL для выборок"
        return err

    # Осуществление выборки:
    vib_routes(driver, config_data, type_of_vib)

    time.sleep(2)

    driver.close()

    old_name = os.path.join(out_path, 'results.csv')
    new_name = old_name.replace('.csv', '_' + server + '.csv')
    os.rename(old_name, new_name)
