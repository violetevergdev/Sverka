import json
import os
import time

from modules.NVP.authentication import authentication
from modules.NVP.vib_routes import vib_routes


def start_to_vib(driver, server, out_path):
    # Получаем конфигурационные данные
    if server == "M":
        configuration_file = open("C:/For_programs/VIB_Config/rvp_conf_М.json", "r")
        config_data = json.load(configuration_file)
    else:
        configuration_file = open("C:/For_programs/VIB_Config/rvp_conf_МO.json", "r")
        config_data = json.load(configuration_file)

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
    vib_routes(driver, config_data)

    time.sleep(2)

    driver.close()

    old_name = os.path.join(out_path, 'results.csv')
    new_name = old_name.replace('.csv','_' + server + '.csv')
    os.rename(old_name, new_name)
