from selenium.webdriver.common.by import By


def select_FSS_fields(driver, vib_fields, useful_btn):
    page2 = driver.find_element(By.ID, useful_btn["page2"])
    page2.click()

    man_dsm = driver.find_element(By.ID, vib_fields["man_dsm"])
    man_dsm.click()

    page4 = driver.find_element(By.ID, useful_btn["page4"])
    page4.click()

    man_npers = driver.find_element(By.ID, vib_fields["man_npers"])
    man_npers.click()

    page5 = driver.find_element(By.ID, useful_btn["page5"])
    page5.click()

    man_pw = driver.find_element(By.ID, vib_fields["man_pw"])
    man_pw.click()

    man_ra = driver.find_element(By.ID, vib_fields["man_ra"])
    man_ra.click()

    man_re = driver.find_element(By.ID, vib_fields["man_re"])
    man_re.click()

    final_btn = driver.find_element(By.ID, useful_btn["final_btn"])
    final_btn.click()