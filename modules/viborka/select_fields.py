from selenium.webdriver.common.by import By


def select_fields(driver, vib_fields, useful_btn):
    po_dsm = driver.find_element(By.ID, vib_fields["po_dsm"])
    po_dsm.click()

    page2 = driver.find_element(By.ID, useful_btn["page2"])
    page2.click()

    po_npers = driver.find_element(By.ID, vib_fields["po_npers"])
    po_npers.click()

    page4 = driver.find_element(By.ID, useful_btn["page4"])
    page4.click()

    po_ra = driver.find_element(By.ID, vib_fields["po_ra"])
    po_ra.click()

    po_re = driver.find_element(By.ID, vib_fields["po_re"])
    po_re.click()

    page5 = driver.find_element(By.ID, useful_btn["page5"])
    page5.click()

    popay_pw = driver.find_element(By.ID, vib_fields["popay_pw"])
    popay_pw.click()

    final_btn = driver.find_element(By.ID, useful_btn["final_btn"])
    final_btn.click()
    