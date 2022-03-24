from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver.webdriver import quit_app
from webdriver.webdriver import setup_webdriver
from os import environ


def do_login():
    """
    Logins to the https://kairos.unifi.it/agendaweb portal
    """

    print("[*] Connecting to Kairos AgendaWeb and Logging in...", end='', flush=True)

    driver = setup_webdriver("https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=en")

    try:
        # Accept privacy 
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="info_privacy"]/..'))).click()
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="info_easylesson"]/..'))).click()

        # Click login
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="oauth_btn"]'))).click()

        # Inserts username and password and clicks login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(environ.get("USERNAME"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(environ.get("PASSWORD"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[1]/form/div[5]/button'))).click()

        # # Checks if login was successfull
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"login-top-page-user-name")]')))

        # Goes to the "book new lesson" page
        driver.get("https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it")

        print("    Logged in!")
    except Exception as e:
        print("\n[!] Login failed: invalid credentials. Please try again with valid credentials")
        quit_app(3, driver)

    return driver

