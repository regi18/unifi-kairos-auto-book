from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import sys


def quit_app(errcode, driver=None):
    if driver:
        driver.close()
    print("Program terminated. You can now close this window.")
    sys.exit(errcode)


def setup_webdriver(website):
    try:
        # If Machine is running on Windows
        if (os.environ.get('IS_WINDOWS') == 'True'):
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.headless = True
            driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), 'chromedriver.exe'), options=options)
        # Heroku
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        driver.get(website)

    except WebDriverException as e:
        print("[ERROR: webdrivr.py] Chrome Driver is not responding")
        print("[ERROR DETAILS: webdrivr.py]" + " " + repr(e))
        quit_app(2, driver)

    return driver
