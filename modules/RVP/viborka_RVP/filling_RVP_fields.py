from datetime import datetime

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def filling_RVP_fields(driver, filling_data):
    dsm_type_select = Select(driver.find_element(By.ID, filling_data["dsm"]["dsm_type_select"]))
    dsm_type_select.select_by_index(filling_data["dsm"]["dsm_type_option"])

    dsm_type_set_ot = driver.find_element(By.ID, filling_data["dsm"]["dsm_type_set_ot"])
    dsm_type_set_ot.send_keys(filling_data["dsm"]["dsm_type_set_ot_keys"])

    dsm_type_set_do = driver.find_element(By.ID, filling_data["dsm"]["dsm_type_set_do"])
    dsm_type_set_do.send_keys(datetime.today().strftime('%Y-%m-%d'))

    npers_type_select = Select(driver.find_element(By.ID, filling_data["npers"]["npers_type_select"]))
    npers_type_select.select_by_index(filling_data["npers"]["npers_type_option"])

    ra_type_select = Select(driver.find_element(By.ID, filling_data["ra"]["ra_type_select"]))
    ra_type_select.select_by_index(filling_data["ra"]["ra_type_option"])

    ra_type_set = driver.find_element(By.ID, filling_data["ra"]["ra_type_set"])
    ra_type_set.send_keys(filling_data["ra"]["ra_type_set_keys"])

    pw_type_select = Select(driver.find_element(By.ID, filling_data["pw"]["pw_type_select"]))
    pw_type_select.select_by_index(filling_data["pw"]["pw_type_option"])

    pw_type_set = driver.find_element(By.ID, filling_data["pw"]["pw_type_set"])
    pw_type_set.send_keys(filling_data["pw"]["pw_type_set_keys"])
