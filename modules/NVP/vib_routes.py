from selenium.webdriver.common.by import By

from modules.viborka.select_DB import select_database
from modules.viborka.select_table import select_table
from modules.viborka.select_fields import select_fields
from modules.viborka.filling_fields import filling_fields
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def vib_routes(driver, config_data):
    vib_fields = config_data["vib-fields"]
    useful_btn = config_data["useful-btn"]
    filling_data = config_data["filling-data"]

    # Выбор БД - 1й шаг
    select_database(driver, vib_fields['database'], useful_btn)

    # Выбор таблиц БД - 2й шаг
    select_table(driver, vib_fields['table'], useful_btn)

    # Выбор полей таблиц - 3й шаг
    select_fields(driver, vib_fields['field'], useful_btn)

    # Заполнение полей - 4й шаг
    filling_fields(driver, filling_data)

    # Выполнение запроса
    run_query_btn = driver.find_element(By.ID, useful_btn["run_query_btn"])
    run_query_btn.click()

    # Сохранение запроса
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.ID, 'form1:text1')))

    save_btn = driver.find_element(By.ID, useful_btn["save_btn"])
    save_btn.click()

