
def open_vib_url(server, type_of_vib, driver, routes_config):
    try:
        if server == "M":
            if type_of_vib in ("РВП", "ФСС", "ФСС-БАЗА"):
                driver.get(routes_config["url_PFR"]["vib_M"])
            elif type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["vib_M"])
        else:
            if type_of_vib in ("РВП", "ФСС", "ФСС-БАЗА"):
                driver.get(routes_config["url_PFR"]["vib_MO"])
            elif type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["vib_MO"])
    except Exception as e:
        err = str(e) + "Неверный URL для выборок"
        return err