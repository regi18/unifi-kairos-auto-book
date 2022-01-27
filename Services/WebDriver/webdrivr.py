from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import sys

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


def quit_app(errcode, driver=None):
    if driver:
        driver.close()
    input("Program terminated. You can now close this window.")
    sys.exit(errcode)


def setup_webdriver(website):
    executable_path = ''
    script_dir = os.path.dirname(__file__)

    # If Machine is running on Windows
    if os.name in ('nt', 'dos'):
        executable_path = os.path.join(script_dir, 'chromedriver.exe')
    else:
        executable_path = os.path.join(script_dir, 'chromedriver_linux')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.headless = True
    driver = None
    try:
        driver = webdriver.Chrome(executable_path, options=options)
        driver.get(website)
    except WebDriverException as e:
        print("[Error] Chrome Driver is not responding")
        print("[ERROR DETAILS]" + " " + repr(e))
        os.system("pause")
        quit_app(2, driver)

    return driver
