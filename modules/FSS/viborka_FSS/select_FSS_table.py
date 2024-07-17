from selenium.webdriver.common.by import By


def select_FSS_table(driver, vib_fields, useful_btn):
    pf_man = driver.find_element(By.ID, vib_fields["pf_man"])
    pf_man.click()

    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()