from selenium.webdriver.common.by import By


def select_table(driver, vib_fields, useful_btn):
    vpl_po = driver.find_element(By.ID, vib_fields["vpl_po"])
    vpl_po.click()

    page2 = driver.find_element(By.ID, useful_btn["page2"])
    page2.click()

    vpl_popay = driver.find_element(By.ID, vib_fields["vpl_popay"])
    vpl_popay.click()

    next_btn = driver.find_element(By.ID, useful_btn["next_btn"])
    next_btn.click()
