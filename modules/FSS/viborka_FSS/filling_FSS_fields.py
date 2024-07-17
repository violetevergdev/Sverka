from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def filling_FSS_fields(driver, filling_data):
    dsm_type_select = Select(driver.find_element(By.ID, filling_data["dsm"]["dsm_type_select"]))
    dsm_type_select.select_by_index(filling_data["dsm"]["dsm_type_option"])

    npers_type_select = Select(driver.find_element(By.ID, filling_data["npers"]["npers_type_select"]))
    npers_type_select.select_by_index(filling_data["npers"]["npers_type_option"])
    npers_type_set = driver.find_element(By.ID, filling_data["npers"]["npers_type_set"])
    npers_type_set.send_keys(filling_data["npers"]["npers_type_set_keys"])

    pw_type_select = Select(driver.find_element(By.ID, filling_data["pw"]["pw_type_select"]))
    pw_type_select.select_by_index(filling_data["pw"]["pw_type_option"])
    pw_type_set = driver.find_element(By.ID, filling_data["pw"]["pw_type_set"])
    pw_type_set.send_keys(filling_data["pw"]["pw_type_set_keys"])