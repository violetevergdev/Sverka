from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime


def filling_fields(driver, filling_data, difference, server):
    for k, v in filling_data.items():
        for options in v:
            if options == "select":
                select = Select(driver.find_element(By.ID, filling_data[k][options]))
                select.select_by_index(filling_data[k]["option"])

            elif options == "set":
                set_val = driver.find_element(By.ID, filling_data[k][options])

                if "set_keys" not in v and difference is True:
                    set_val.send_keys(filling_data[k]["set_keys_" + server])
                else:
                    set_val.send_keys(filling_data[k]["set_keys"])

            elif options == "set_ot":
                set_ot = driver.find_element(By.ID, filling_data[k][options])
                set_ot.send_keys(filling_data[k]["set_ot_keys"])

            elif options == "set_do":
                if "set_do_keys" in v:
                    set_do = driver.find_element(By.ID, filling_data[k]["set_do"])
                    set_do.send_keys(filling_data[k]["set_do_keys"])
                else:
                    set_do = driver.find_element(By.ID, filling_data[k]["set_do"])
                    set_do.send_keys(datetime.today().strftime('%Y-%m-%d'))

