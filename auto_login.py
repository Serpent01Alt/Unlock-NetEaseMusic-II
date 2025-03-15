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
    browser.add_cookie({"name": "MUSIC_U", "value": "0011BE7E46F9D15454CF4D8873DD5F8CD9270325D380572086113673339DE5EC80A01F4AC5EAA8F00A3C100EC93BD1AE981E8B59597AF1B1741FCB986C6238F4B6BF44F7E6BFF43304D7D0D4DD94A9F81D443433F0C5BF61EB07FB6401A7F50E8B69398C5B77556276B752E4B010ADFD2B356B68C890C033936DC74927C0707E679E6CC9756817A10A8743071FE8EB40F16BF9CA7EAEC1088684A09FDE680E49F522D64689B0FFE90256B6E1D0220BB0128D9BFA0AA19BC38AE30C9E4577EE5990FF9A98201738E0BA1DF888CC68891831260F32F150EB1A1EDA85EBDD8BA89129015E54E0304A6B73877C6A25FA3506AF940C08D4F289704A00D2A93B8B1F25D279D37DA783709F5EBE91979F56F8A51BF076F7CD018BADC803704EB75893572E4B1F5398153B15316F7EE9F018CDA22CE52537A799587E31498B3188AD6ED643368AE5E431B0C71535A6174715F9A44CEEDD71231F2116A65DDE72AA46ADA3A7"})
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
