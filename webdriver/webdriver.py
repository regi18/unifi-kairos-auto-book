from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
from sys import exit

def quit_app(errcode, driver=None):
    if driver:
        driver.close()

    print("[+] Program terminated")
    exit(errcode)


def setup_webdriver(website):
    try:
        chrome_options = webdriver.ChromeOptions()

        # If Machine is running on Windows
        if (os.environ.get('IS_WINDOWS') == 'True'):
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chromedriver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
        # Heroku
        else:
            chrome_options.add_argument("--headless")
            chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome"
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chromedriver_path = "/app/.chromedriver/bin/chromedriver"

        driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        driver.get(website)

    except WebDriverException as e:
        print("[ERROR DETAILS: webdriver.py]" + " " + repr(e))
        quit_app(2, driver)

    return driver
