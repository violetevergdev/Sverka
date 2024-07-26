import json


def get_vib_config(type_of_vib):
        # Получаем маршруты из конфига
        with open('config/Common/routes.json', 'r') as f:
            routes_json = json.load(f)

        # Получаем конфиг для авторизации
        with open('config/Common/login.json', 'r') as f:
            login_json = json.load(f)

        # Получаем конфигурационные данные для выборок
        type_config = {
            "РВП": "config/Other/rvp_conf.json",
            "МСП": "config/Other/mits_conf.json",
            "ФСС": "config/Other/fss_conf.json",
        }

        configuration_file = type_config.get(type_of_vib)

        if configuration_file:
            with open(configuration_file, "r") as f:
                config_json = json.load(f)

        return routes_json, login_json, config_json

