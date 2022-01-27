from Services.WebDriver.webdrivr import *
from Services.Interface.library import *
from Services.Interface.view import *
from Services.Booking.showBookings import *
from Services.Booking.newBooking import *
from Services.Interface.bookingStatus import *

driver_type = 0

def initialization(driver_type):
    print("Authenticating...")
    try:
        print("Connecting...")
        if driver_type == 2:
            driver = setup_webdriver("https://kairos.unifi.it/portalePlanning/BIBL/")
        else:
            driver = setup_webdriver("https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&_lang=it")

        print("Logging in...")
        if driver_type == 2:
            login_status = login_studyrooms(driver)
        else:
            login_status = login_lessons(driver)
        if login_status is False:
            print("Login failed: invalid credentials. Please try again with valid credentials")
            quit_app(3, driver)
        else:
            print("Logged in!")
            return driver

    except Exception as e:
        print("[ERROR] Unknown Error {}".format(e))
        print("Please check your internet connection or contact one of the administrators if the error occur again!")
        choice = input('Would you like to retry? [Y/N]')
        if choice.lower() == 'y':
            if driver:
                driver.close()
            driver = initialization()
        else:
            print("[ERROR DETAILS]" + " " + repr(e))
            quit_app(2, driver)


if __name__ == '__main__':
    not_done = True
    driver = None
    time.sleep(1)
    while not_done:
        try:
            action = ask_for_command()
            if action is None or action == "":
                not_done = False
            elif action == "1":
                driver_type = 1
                driver = initialization(driver_type)
                new_lessonsbooking(driver)
                if driver:
                    driver.close()
                    driver = None
            elif action == "2":
                driver_type = 2
                driver = initialization(driver_type)
                new_studyroomsbooking(driver)
                if driver:
                    driver.close()
                    driver = None
            elif action == "3":
                driver_type = 2
                driver = initialization(driver_type)
                show_bookings(driver)
                if driver:
                    driver.close()
                    driver = None
            else:
                not_done = False

        except NoSuchElementException as e:
            print("[ERROR] Generic error probably related to internet connection.")
            print("Please check your internet connection!")
            choice = input('Would you like to retry? [Y/N]')
            if choice.lower() == 'y':
                if driver:
                    driver.close()
            else:
                print("[ERROR DETAILS]" + " " + repr(e))
                quit_app(2, driver)
        except ConnectionError as e:
            print("[ERROR] Bad internet connection.")
            print("Please check your internet connection!")
            choice = input('Would you like to retry? [Y/N]')
            if choice.lower() == 'y':
                if driver:
                    driver.close()
                driver = initialization(driver_type)
            else:
                print("[ERROR DETAILS]" + " " + repr(e))
                quit_app(2, driver)
        except Exception as e:
            print("[ERROR] Unknown Error {}".format(e))
            print("Please check your internet connection or contact one of the administrators if the error occur again!")
            choice = input('Would you like to retry? [Y/N]')
            if choice.lower() == 'y':
                if driver:
                    driver.close()
                driver = initialization(driver_type)
            else:
                print("[ERROR DETAILS]" + " " + repr(e))
                quit_app(2, driver)
    quit_app(0)
