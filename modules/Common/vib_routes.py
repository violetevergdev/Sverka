import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.Common.viborka.select_DB import select_database
from modules.Common.viborka.select_table import select_table
from modules.RVP.viborka_RVP.filling_RVP_fields import filling_RVP_fields

from modules.FSS.viborka_FSS.select_FSS_table import select_FSS_table
from modules.FSS.viborka_FSS.select_FSS_database import select_FSS_database
from modules.FSS.viborka_FSS.select_FSS_fields import select_FSS_fields
from modules.FSS.viborka_FSS.filling_FSS_fields import filling_FSS_fields


from modules.MITS.viborka_MITS.filling_MITS_fields import filling_MITS_fields
from modules.RVP.viborka_RVP.select_RVP_fields import select_RVP_fields
from modules.MITS.viborka_MITS.select_MITS_fields import select_MITS_fields


def vib_routes(driver, config_data, type_of_op):
    with open('config/Common/vib/btn.json', 'r') as f:
        btn = json.load(f)

    vib_fields = config_data["vib-fields"]
    useful_btn = btn["useful-btn"]
    filling_data = config_data["filling-data"]

    # Выбор БД - 1й шаг
    if type_of_op == 'РВП' or type_of_op =='МиЦ':
        select_database(driver, vib_fields['database'], useful_btn)
    elif type_of_op == 'ФСС':
        select_FSS_database(driver, vib_fields['database'], useful_btn)

    # Выбор таблиц БД - 2й шаг
    if type_of_op == 'РВП' or type_of_op =='МиЦ':
        select_table(driver, vib_fields['table'], useful_btn)
    elif type_of_op == 'ФСС':
        select_FSS_table(driver, vib_fields['table'], useful_btn)

    # Выбор полей таблиц - 3й шаг
    if type_of_op == 'РВП':
        select_RVP_fields(driver, vib_fields['field'], useful_btn)
        # Заполнение полей - 4й шаг
        filling_RVP_fields(driver, filling_data)
    elif type_of_op == 'МиЦ':
        select_MITS_fields(driver, vib_fields['field'], useful_btn)
        # Заполнение полей - 4й шаг
        filling_MITS_fields(driver, filling_data)
    elif type_of_op == 'ФСС':
        select_FSS_fields(driver, vib_fields['field'], useful_btn)
        # Заполнение полей - 4й шаг
        filling_FSS_fields(driver, filling_data)


    # Выполнение запроса
    run_query_btn = driver.find_element(By.ID, useful_btn["run_query_btn"])
    run_query_btn.click()

    # Сохранение запроса
    WebDriverWait(driver, 360).until(EC.presence_of_element_located((By.ID, 'form1:text1')))

    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, useful_btn["save_btn"])))

    try:
        save_btn = driver.find_element(By.ID, useful_btn["save_btn"])
        save_btn.click()
    except Exception as e:
        return e
