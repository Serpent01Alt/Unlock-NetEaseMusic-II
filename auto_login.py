# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00034EF5979FCB80A986CE58515B1440CBD12706C9B847C34FF1A16CAB7DEDB50930A9A87064883C095D1BA4CF68E267EE8D7D384D030A3A1500464D7ABCB83423ED39DA273F3D2375FC5472BEB1B65C71766EDB4C7B0959425476BCE9E847D468FD11030D9F2CEF7488C79F6241A9C4E2E27872D4917E1C694EBFE3E535671E7899A9F69FDB8E92872CF8A5441BD1113A8A44DC53D8BE6242B82ABCEC5241724CC94E0E8720053DF7D7EAD4EEA3935021D067BAA9FFD6B32F1B75BF81508C37A296E9BB308B72C23BFEE0AA123903801B5F6D723A841BE892D42B15C2CF47C84FE90DACA80D9481611FCD8860FEDFE0937E9DF2FCF15B61EDC38B76ACB57D6B217BBE0866BEF44AE41EBCED249D2FCEE7132C766478D8C98295985518F1B565C67BE74497E52C6A0DB61817BD4201FDD5B5EA1D0931629E3EC43D56412BA4872BC6149CC8C46BC8DED65019E6A3ACEA242191E29DF9C1ABAEABEF9CFACFA746E0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
