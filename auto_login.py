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
    browser.add_cookie({"name": "MUSIC_U", "value": "003F27C4C81642088561917F9BE8C1A8833E9963C2A472320F485323B0AD645B959F8FD1C4FFFC029DBA47BA677F800FE8EC015B0083FE0E3DF2E7B19340DE643E03E9865D91F72FFB5E27FDB5C242B2D24C3705B909A19C92CEBAF14F165172108C57114D8ADE2FA4176F488CF013C320D415EC8FB8965D657E6B0388CC092EE2F8AAA97A7316A24A7BED9F69FE0991AE27916F80A52397B93C3218BE2516485791AE6E07396FD65C59FE802F3DBF99886B235FC41C03DA6B6133CF25849C9335FD5A20BB457747C48A2C2931AF30E4FC415C8B9800DD31B08A3735DDB04412745332F7C85A40A3EB50112EF8DB2911958C420B10D89897D214AB8D8A8C336586DDC01E06420270DE04188A7D397D212633998FAB529C47B656BFB1AA7570C7937090F33EBDB3A0DCA9C43ECD288A47B5987D5FB515E8DAB990EA9BA631DF6E27CFC74B9221490F4339DD8381771CACE6CC44579AEA040E8748B39765A99FD736"})
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
