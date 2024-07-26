
def open_nvp(server, type_of_vib, driver, routes_config):
    try:
        if server == "M":
            if type_of_vib == "РВП" or type_of_vib == "ФСС":
                driver.get(routes_config["url_PFR"]["login_M"])
            elif type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["login_M"])
        else:
            if type_of_vib == "РВП" or type_of_vib == "ФСС":
                driver.get(routes_config["url_PFR"]["login_MO"])
            elif type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["login_MO"])
    except Exception as e:
        err = str(e) + "Неверный URL адрес для аутентификации"
        return err
    