from selenium.webdriver.common.by import By


def select_database(driver, vib_fields, useful_btn):
    vpl = driver.find_element(By.ID, vib_fields["vpl"])
    vpl.click()

    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()
