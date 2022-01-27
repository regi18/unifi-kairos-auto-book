import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..Interface.bookingStatus import *
from ..WebDriver.webdrivr import quit_app
classrooms = ("222", "223", "224", "315", "316", "318", "2A", "2B", "2C", "2D")


def new_lessonsbooking(driver):
    for i in range(5):
        try:
            newbooking = driver.find_element_by_xpath("//a[contains(.,'Nuova prenotazione')]")
            break
        except NoSuchElementException as e:
            if i < 4:
                time.sleep(1)
            else:
                print('[ERROR] Kairos is not responding. Connection timed out.')
                quit_app(2, driver)
    else:
        raise e

    driver.execute_script("arguments[0].click();", newbooking)

    delay = 5  # seconds
    try:
        myelem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'prenotalezioni_avviso')))
        system("cls")
        print("BOOKING PROCESS")
        print("================================================================")
        newbooking = driver.find_elements_by_xpath("//a[@title='Verifica e prenota il tuo posto']")
        foundbookable = len(newbooking)
        print("Found %d lessons to book." % foundbookable)
        if foundbookable > 0:
            print('Booking in progress...')
        for i in range(foundbookable):
            booklesson(driver, newbooking[i])

        input('Press enter to proceed...')
    except TimeoutException:
        print("[ERROR] Booking service not avaible. Quitting.")
        print("================================================================")
        quit_app(2, driver)


def booklesson(driver, lesson):
    lesson.click()
    for i in range(5):
        try:
            successMsg = driver.find_element_by_class_name('success-title')
            if successMsg.get_attribute("innerText") == 'Prenotazione effettuata':
                print("================================================================")
                lessonDetails = driver.find_element_by_xpath("//span[contains(.,'Hai prenotato la lezione:')]")
                print(lessonDetails.get_attribute('innerText'))
                print("================================================================")
                driver.find_element_by_class_name('mfp-close').click()
            break
        except NoSuchElementException as e:
            if i < 4:
                time.sleep(1)
            else:
                print('[ERROR] Kairos is not responding or the lesson is not bookable.')
                print('Skipping to next lesson...')
    else:
        raise e


def new_studyroomsbooking(driver):
    print("[*] Booking in progress...\n")
    msg = ''
    bookings_found = 0
    enter_booking_page(driver=driver)

    for i in range(10):
        print("[*] Checking for available seats in room {1} (morning)...  {0}%".format((i + 1) * 5, classrooms[i]))
        set_time_period(driver=driver, period=1)
        set_study_room(driver=driver, room=i)

        # Clicks form button
        view_time_table(driver=driver)
        available = check_if_available(driver=driver)
        if available:
            confirm_booking(driver=driver)
            bookings_found += 1
            i -= 1
        else:
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/div/div/button').click()
            time.sleep(0.5)

    for i in range(10):
        print("[*] Checking for available seats in room {1} (afternoon)...  {0}%".format(50 + (i + 1) * 5, classrooms[i]))
        set_time_period(driver=driver, period=2)
        set_study_room(driver=driver, room=i)

        # Clicks form button
        view_time_table(driver=driver)
        available = check_if_available(driver=driver)
        if available:
            confirm_booking(driver=driver)
            bookings_found += 1
            i -= 1
        else:
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/div/div/button').click()
            time.sleep(0.5)

    update_status("[+] Booking process completed. Returning to main menu...", 100, None)

    time.sleep(5)


def enter_booking_page(driver):
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="form"]').submit()
    time.sleep(2)


def set_time_period(driver, period):
    driver.find_element_by_xpath('//*[@id="servizio-container"]/div/div[2]/span').click()
    if period == 1:
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[4]').click()   # Morning
    elif period == 2:
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[5]').click()   # Afternoon


def set_study_room(driver, room):
    element1_found = False
    fails = 0
    while element1_found is False and fails < 10:
        try:
            # Found
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="area-container"]/div/div[2]/span/span[1]/span').click()
            element1_found = True
        except NoSuchElementException:
            # Not Found
            fails += 1
    if fails == 10:
        raise ConnectionError('Generic connection error.')

    element2_found = False
    fails = 0
    while element2_found is False and fails < 10:
        try:
            # Found
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[' + str(2 + room) + ']').click()
            element2_found = True
        except NoSuchElementException:
            # Not Found
            fails += 1
    if fails == 10:
        raise ConnectionError('Generic connection error.')

    alert_not_found = True
    while alert_not_found:
        try:
            # Not Found
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/form/div/div[4]/div[1]/div/button').click()
            time.sleep(2)
        except NoSuchElementException:
            # Found
            alert_not_found = False


# Attempts to view the date and time period table
def view_time_table(driver):
    load_next_button_found = False
    fails = 0
    while load_next_button_found is False and fails < 10:
        try:
            driver.find_element_by_id('load_next').click()
            time.sleep(0.5)
            load_next_button_found = True
        except NoSuchElementException:
            fails += 1

    if fails == 10:
        raise ConnectionError('Generic connection error.')
    time.sleep(1)

    alert_not_found = True
    while alert_not_found:
        try:
            # Not Found
            driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div/form/div/div[4]/div[1]/div/button').click()
            time.sleep(2)
        except NoSuchElementException:
            # Found
            alert_not_found = False


# Clicks first available time slot relatively to the current day
def check_if_available(driver):
    try:  # Found
        driver.find_element_by_xpath('//span[contains(text(), "vedi orari")]').click()
    except NoSuchElementException:  # Not Found
        print("[!] No seats available in this room")
        return False

    time.sleep(2)
    element_found = False
    for i in range(3):
        if element_found is False:
            try:
                driver.find_element_by_xpath(
                    '/html/body/div[2]/div[4]/div[2]/div/div/div/div/div/div[' + str(i + 1) +
                    ']/div[1]/div/div/div[2]/div/p').click()
                element_found = True
            except NoSuchElementException:
                # Not Found
                element_found = False
        else:
            break
    if element_found is False:
        print("No seats available in this room")
    return element_found


def confirm_booking(driver):
    time.sleep(0.4)
    print("[*] Seat has been found, booking in progress...")
    driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div/div[1]/form/button").click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div[1]/form/button").click()

    print("[+] Seat has been booked successfully!")


def travel(driver, url):
    driver.get("https://kairos.unifi.it/portalePlanning/BIBL/index.php?include=" + url)
