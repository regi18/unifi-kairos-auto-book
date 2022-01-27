import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
from ..WebDriver.webdrivr import quit_app
from os import environ


def login_studyrooms(driver):
    file = ConfigParser()
    file.read("config.ini")

    password = environ.get("PASSWORD")
    element1_found = False
    while element1_found is False:
        try:
            # Found
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="username"]').send_keys(
                environ.get("USERNAME"))
            element1_found = True
        except NoSuchElementException:
            # Not Found
            element1_found = False

    element2_found = False
    while element2_found is False:
        try:
            # Found
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="password"]').send_keys(
                password)
            element2_found = True
        except NoSuchElementException:
            # Not Found
            element2_found = False
    driver.find_element_by_xpath('//*[@id="fm1"]/div[3]/button').click()

    time.sleep(2)
    try:
        # Found
        driver.find_element_by_xpath('/html/body/div/main/div/div[1]/div')
        return False
    except NoSuchElementException:
        # Not Found
        return True


def login_lessons(driver):
    file = ConfigParser()
    file.read("config.ini")

    delay = 5  # seconds
    try:
        myelem = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, 'info_privacy')))
    except TimeoutException:
        print("[ERROR] Connection failed. Quitting.")
        quit_app(2, driver)

    check_conditions = driver.find_element_by_id("info_privacy")
    driver.execute_script("arguments[0].click();", check_conditions)

    check_conditions = driver.find_element_by_id("info_easylesson")
    driver.execute_script("arguments[0].click();", check_conditions)

    driver.find_element_by_id("oauth_btn").click()
    username = environ.get("USERNAME")
    password = environ.get("PASSWORD")

    for i in range(5):
        try:
            driver.find_element_by_id("username")
            break
        except NoSuchElementException as e:
            if i < 4:
                time.sleep(1)
            else:
                print(
                    '[ERROR] Kairos is not responding. Connection timed out.')
                quit_app(2, driver)
    else:
        raise e

    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)

    driver.find_element_by_name("_eventId_proceed").click()

    time.sleep(3)

    try:
        wrongUsername = driver.find_element_by_xpath(
            "//div[contains(.,'Il nome utente immesso non può essere identificato.')]"
        )
        return False
    except NoSuchElementException as e:
        try:
            wrongPassword = driver.find_element_by_xpath(
                "//div[contains(.,'La password immessa non è corretta.')]")
            return False
        except NoSuchElementException as e:
            delay = 5
            try:
                WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located(
                        (By.ID, 'section-main-menu-title-home')))
                return True
            except NoSuchElementException as e:
                print("[ERROR] Connection problem during log in. Quitting.")
                quit_app(2, driver)
