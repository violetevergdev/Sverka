from selenium.webdriver.common.by import By


def select_FSS_database(driver, vib_fields, useful_btn):
    db = driver.find_element(By.ID, vib_fields["pf"])
    db.click()

    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()