from Services.WebDriver.webdrivr import *
from Services.Interface.library import *
from Services.Interface.view import *
from Services.Booking.showBookings import *
from Services.Booking.newBooking import *
from Services.Interface.bookingStatus import *
from datetime import date
from sys import exit


def initialization():
    print("[*] Connecting to Kairos...")
    driver = setup_webdriver("https://kairos.unifi.it/portalePlanning/BIBL/")
    print("[*] Logging in...")
    login_status = login_studyrooms(driver)

    if login_status is False:
        print(
            "[!] Login failed: invalid credentials. Please try again with valid credentials"
        )
        quit_app(3, driver)
    else:
        print("[+] Logged in!")
        return driver


if __name__ == '__main__':
    if date.today().isoweekday() != 5:
        print("[*] Skipping... today is not friday.")
        exit(0)

    driver = None

    try:
        driver = initialization()
        new_studyroomsbooking(driver)

        if driver:
            driver.close()
            driver = None

    except Exception as e:
        print("[ERROR: main.py]" + " " + repr(e))
        quit_app(2, driver)

    quit_app(0)