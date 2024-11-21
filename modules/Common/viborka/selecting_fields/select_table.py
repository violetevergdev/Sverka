from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def select_table(driver, vib_fields, useful_btn):
    # Ожидаем прогрузку таблицы
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'form1:table1')))

    rows = driver.find_elements(By.CLASS_NAME, 'table-row')
    ind = 0

    start_iteration = True
    page = 1
    last_row_in_page = 29

    while start_iteration:
        for el in vib_fields:
            names = el.split("~")
            db_name = names[0]
            table_name = names[1]

            not_found = True

            for _ in rows:
                while not_found:
                    db_val = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text2')
                    table_val = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':text9')

                    if db_val.text == db_name and table_val.text == table_name:
                        db = driver.find_element(By.ID, 'form1:table1:' + str(ind) + ':rowSelect1__input_sel')
                        db.click()
                        not_found = False
                        break

                    if ind == last_row_in_page:
                        next_page = driver.find_element(By.ID, 'form1:table1:web1__pagerWeb__' + str(page))
                        next_page.click()
                        page += 1
                        last_row_in_page += 30

                    ind += 1
        start_iteration = False


    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()
