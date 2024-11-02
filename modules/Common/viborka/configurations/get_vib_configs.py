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
            "РПВ": ["config/Other/rvp_conf.json"],
            "МСП": ["config/Other/mits_conf.json"],
            "ФСС": ["config/Other/fss_conf.json"],
            "ФСС-БАЗА": ["config/Other/fss_base_conf.json"],
            "НАКОП": ["config/Other/nakop_conf/nakop_man_conf.json", "config/Other/nakop_conf/nakop_popay_conf.json",
                      "config/Other/nakop_conf/nakop_wpr_conf.json"],
        }

        configuration_list = type_config.get(type_of_vib)


        return routes_json, login_json, configuration_list
