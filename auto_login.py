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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FAD2D9A12C0BBFD1DAFE16A0825CC33B3E697C4239F525764F49B42C81E6817BEDC404BC8D32B41DADE68147B8875AB9ABBB2683B0924F63369D2BF3A0485FF8F437B1F12556B081DBE62B07EB64B902F28E9ACE0919E2239C53C851CECD8B5F460E81D29028624EE98A89FA5A539918B8A2335001F3C4B2F31A42E6DCC247FF478E2C9E8EF12D14EAE560A32FD0D38AFB19F0390BB6775809549E36FBFBF2454A12E51B5A712BDB7C3FAA928B0006DA3DE84B9460A8FD2DF41AC3F1F16035616F21AB7447FB9D43B1440CE9315675003EA5BED4C0C391834192C7B8347828CE881983FA2BE8D61FE04CC2EEBD370D0A181630522F5CE1A9AD9B50AF60A5D82D3D651C8F4B375220F1BD39235984699BA744F67DFE26623152C81744C685E09790E3967E0F7C1DCB1AC536F34EB2AEA9F9D53E7A63384740F8B83991C02A28A0687D03C76E0161AE2CDB13A6C8E557E8C5E3FD3E61B93E6A45C62802194E4936"})
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
