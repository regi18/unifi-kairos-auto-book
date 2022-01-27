import time
from configparser import ConfigParser


def travel(driver, url):
    driver.get("https://kairos.unifi.it/portalePlanning/BIBL/index.php?include=" + url)


def delete_booking(driver, code):
    enter_manage_booking_page(driver)
    travel(driver, "manage")
    prepare_form(driver, code)
    confirm_deletion(driver)
    print("Booking (with ID: " + code + ") has been removed!")
    time.sleep(2)

def prepare_form(driver, code):
    file = ConfigParser()
    file.read("config.ini")

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="chiave_primaria"]').send_keys(file["ACCOUNT"]["user"])
    driver.find_element_by_xpath('//*[@id="codice"]').send_keys(code)

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="submit"]').click()


def confirm_deletion(driver):
    driver.find_element_by_xpath('//*[@id="formverifica"]/div[3]/div/div[2]/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/button').click()
    travel(driver, "home")
