
def open_vib_url(server, type_of_vib, driver, routes_config):
    try:
        if server == "M":
            if type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["vib_M"])
            else:
                driver.get(routes_config["url_PFR"]["vib_M"])
        else:
            if type_of_vib == "МСП":
                driver.get(routes_config["url_MSP"]["vib_MO"])
            else:
                driver.get(routes_config["url_PFR"]["vib_MO"])
    except Exception as e:
        err = str(e) + "Неверный URL для выборок"
        return err