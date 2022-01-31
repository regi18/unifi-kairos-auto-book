from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from studyrooms.studyrooms_booking_utils import StudyroomsBookingUtils
from studyrooms.studyrooms_login import do_login

class StudyroomsBooking:
    STUDY_ROOMS = ("222", "223", "224", "315", "316", "318", "2A", "2B", "2C", "2D")
    SUFFICIENT_BOOKED_DAYS_COUNT = 10


    def __init__(self):
        self.driver = do_login()
        self.utils = StudyroomsBookingUtils(self.driver, self.SUFFICIENT_BOOKED_DAYS_COUNT)
        self.driver_wait = WebDriverWait(self.driver, 10)


    def book_all_possible_studyrooms(self):
        print("[*] Booking in progress...")

        try:
            # Enters the new booking section
            self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]'))).click()

            # Tries to book SUFFICIENT_BOOKED_DAYS_COUNT days. For each day it tries to find a slot in one of the rooms sets in STUDY_ROOMS
            booked_count = 0
            for i in range(self.SUFFICIENT_BOOKED_DAYS_COUNT):
                # Find a room for the morning or afternoon
                for period in ("morning", "afternoon"):
                    for room in self.STUDY_ROOMS:
                        s = '  ' if period == "morning" else ''
                        print(f"[*] ({i:02}) Checking room { room } ({ period })...{s}", end='')

                        res = self.utils.select_study_room(room, period)
                        if (res and self.utils.try_to_book_selected_room()):
                            # As soon as a room for the current period is found, exits and go to the next period (or day)
                            booked_count += 1
                            print(f"    Booked! (tot: {booked_count})")                                                
                            break

                        print("    Nothing found, skipping.")                                                

        except Exception as e:
            print("\n[ERROR: book_all_possible_studyrooms()]    " + repr(e))
            # exit(1)


        print("[+] Booking process completed")


    def __del__(self):
        if (self.driver):
            self.driver.close()
