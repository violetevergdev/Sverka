import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.Common.viborka.selecting_fields.select_DB import select_database
from modules.Common.viborka.selecting_fields.select_table import select_table
from modules.Common.viborka.selecting_fields.select_fields import select_fields
from modules.Common.viborka.selecting_fields.filling_fields import filling_fields



def vib_routes(driver, config_data, server, type_of_op):
    # Проверка на наличие разницы в filling_data в зависимости от сервера
    difference = False
    if type_of_op in ("МСП", "ФСС-БАЗА", "НАКОП", "ОПЕКУНЫ"):
        difference = True

    try:
        with open('config/Common/vib/btn.json', 'r') as f:
            btn = json.load(f)

        vib_fields = config_data["vib-fields"]
        useful_btn = btn["useful-btn"]
        filling_data = config_data["filling-data"]

        # Выбор БД - 1й шаг
        select_database(driver, vib_fields['database'], useful_btn)

        # Выбор таблиц БД - 2й шаг
        select_table(driver, vib_fields['tables'], useful_btn)

        # Выбор полей таблиц - 3й шаг
        select_fields(driver, vib_fields['fields'], useful_btn)

         # Заполнение полей - 4й шаг
        filling_fields(driver, filling_data, difference, server)

        # Выполнение запроса
        run_query_btn = driver.find_element(By.ID, useful_btn["run_query_btn"])
        run_query_btn.click()

        # Сохранение запроса
        WebDriverWait(driver, 580).until(EC.presence_of_element_located((By.ID, 'form1:text1')))

        WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.ID, useful_btn["save_btn"])))

        if driver.find_element(By.ID, 'form1:text1').text in ('-1', '0'):
            raise AssertionError('Проблемы с сервером, получено строк: -1 ')

        save_btn = driver.find_element(By.ID, useful_btn["save_btn"])
        save_btn.click()

    except Exception as e:
        err = 'Ошибка осуществления выборки: ', e
        return err
