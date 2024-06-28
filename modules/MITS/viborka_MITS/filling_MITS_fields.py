from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def filling_MITS_fields(driver, filling_data):
    ra_type_select = Select(driver.find_element(By.ID, filling_data["ra"]["ra_type_select"]))
    ra_type_select.select_by_index(filling_data["ra"]["ra_type_option"])

    ra_type_set = driver.find_element(By.ID, filling_data["ra"]["ra_type_set"])
    ra_type_set.send_keys(filling_data["ra"]["ra_type_set_keys"])

    pw_type_select = Select(driver.find_element(By.ID, filling_data["pw"]["pw_type_select"]))
    pw_type_select.select_by_index(filling_data["pw"]["pw_type_option"])

    pw_type_set = driver.find_element(By.ID, filling_data["pw"]["pw_type_set"])
    pw_type_set.send_keys(filling_data["pw"]["pw_type_set_keys"])