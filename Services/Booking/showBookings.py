from os import system
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from ..Booking.deleteBookings import *


def delete_or_back():
    print("================================================================")
    print("Choose an action: 1. Delete a pending booking || 2. Go back")
    return input("Your choice: ")


def show_bookings(driver):
    enter_booking_page(driver)
    get_data_from_page(driver)
    action = delete_or_back()
    if action != "1" and action != "2":
        print("Invalid input, returning to main menu...")
        travel(driver, "home")
    elif action == "2":
        print("Returning to main menu...")
        travel(driver, "home")
    elif action == "1":
        code = input("Please type in the booking ID (not number!) you want to delete (press RETURN to cancel): ")
        if code == "":
            print("Booking deletion process canceled.")
            travel(driver, "home")
        else:
            print("Processing your request...")
            try:
                delete_booking(driver, code)
            except NoSuchElementException:
                print("You inserted a wrong booking ID, returning to main menu...")
                time.sleep(2)
            except ElementClickInterceptedException:
                print("You have exceeded the deadline for canceling this booking, returning to main menu...")
                time.sleep(2)
            travel(driver, "home")
    else:
        travel(driver, "home")


def enter_booking_page(driver):
    print("Processing your request, this may take some time...")
    element1_found = False
    while element1_found is False:
        try:
            # Found
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="mybookings"]').submit()
            element1_found = True
        except NoSuchElementException:
            # Not Found
            element1_found = False


def get_data_from_page(driver):
    print("Number\t#B.ID\tStatus\t\t\tDate and time\t\tBuilding")
    seat_expired_not_found = True
    i = 0
    while seat_expired_not_found:
        time_and_date = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[' + str(i+2) + ']/td[2]').get_attribute('innerText')
        building = driver.find_element_by_xpath(
            '/html/body/div[2]/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[' + str(i+2) + ']/td[5]').get_attribute('innerText')
        bookingID = driver.find_element_by_xpath(
            '/html/body/div[2]/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[' + str(i+2) + ']/td[7]').get_attribute('innerText')
        statusTmp = driver.find_element_by_xpath(
            '/html/body/div[2]/div[4]/div[2]/div/div/div[1]/div[2]/table/tbody/tr[' + str(i+2) + ']/td[8]/form/button/span[2]').get_attribute('innerText')[0]
        if statusTmp == "G":
            status = "SEAT BOOKED"
        elif statusTmp == "V":
            seat_expired_not_found = False
        else:
            status = "ERROR"
        print(str(i + 1) + "\t" + bookingID + "\t" + status + "\t\t" + time_and_date + "\t" + building)
        i += 1
