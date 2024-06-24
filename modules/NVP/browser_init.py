from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os, sys

def browser(out_path):
    options = Options()
    options.headless = False
    options.binary_location = 'C:\\For_programs\\soft\\Mozilla Firefox\\firefox.exe'

    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", out_path)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    # Ставим драйвер
    driver_local_path = Service('C:\\For_programs\\soft\\geckodriver.exe')
    driver = webdriver.Firefox(options=options, service=driver_local_path)

    return driver
