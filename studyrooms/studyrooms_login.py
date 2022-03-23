from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver.webdriver import quit_app
from webdriver.webdriver import setup_webdriver
from os import environ


def do_login():
    """
    Logins to the kairos.unifi.it/portalePlanning/BIBL portal
    """

    print("[*] Connecting to Kairos and Logging in...", end='')

    driver = setup_webdriver("https://kairos.unifi.it/portalePlanning/BIBL/")

    try:
        # Inserts username and password and clicks login
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(environ.get("USERNAME"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(environ.get("PASSWORD"))
        el_click_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fm1"]/div[3]/button')))
        # Execute scipt instead of simulating a mouse click in order to avoid problems
        driver.execute_script("arguments[0].click();", el_click_btn)
        # Checks if login was successfull
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form/div[2]/h4')))
        # Clicks "Go to homepage" to avoid waiting 3 seconds
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="index.php"]'))).click()
        print("    Logged in!")
    except Exception as e:
        print("\n[!] Login failed: invalid credentials. Please try again with valid credentials")
        quit_app(3, driver)

    return driver

