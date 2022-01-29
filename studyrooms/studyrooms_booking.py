from typing import Literal
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver.webdriver import quit_app
from studyrooms.studyrooms_login import login_studyrooms


class StudyroomsBooking:
    driver = None
    STUDY_ROOMS = ("222", "223", "224", "315", "316", "318", "2A", "2B", "2C", "2D")

    def __init__(self):
        self.driver = login_studyrooms()
        self.driver_wait = WebDriverWait(self.driver, 10)


    def book_all_possible_studyrooms(self):
        print("[*] Booking in progress...")

        # Enters the new booking section
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]'))).click()

        # Tries to book 10 days. For each day it tries to find a slot in one of the rooms sets in STUDY_ROOMS
        j = 1
        try:
            for i in range(10):
                # Find a room for the morning or afternoon
                for period in ("morning", "afternoon"):
                    for room in self.STUDY_ROOMS:
                        s = '  ' if period == "morning" else ''
                        print(f"[*] ({i:02}) {j:02}/{len(self.STUDY_ROOMS)*2} Checking room { room } ({ period })...{s}", end='')
                        j += 1 

                        res = self.__set_study_room(room, period)
                        if (res and self.__try_to_book_set_room()):
                            # As soon as a room for the current period is found, exits and go to the next period (or day)
                            print("    Booked!")                                                
                            break

                        print("    Nothing found, skipping.")                                                

        except Exception as e:
            print("\n")
            print(e)

        print("[+] Booking process completed")


    def __set_study_room(self, room, period: Literal['morning', 'afternoon']):
        """
            Selects the study room
        """

        # Sets the time period (Mattina or Pomeriggio)
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="servizio-container"]/div/div[2]/span'))).click()
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/span/span/span[2]/ul/li[{'4' if period == 'morning' else '5'}]"))).click()

        # Clicks the dropdown
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="area-container"]/div/div[2]/span/span[1]/span'))).click()
        # Selects the requested room
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/span/span/span[2]/ul/li[contains(text(), '{ room }')]"))).click()
        # Waits for the current date to load on the "Scegli la data dell'appuntamento" input field
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='data_inizio']"))).click()
        # Clicks "VERIFICA DISPONIBILITÀ"
        self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='verify']"))).click()

        # Check if the "ANNULLA" button is present, i.e. if the previously clicked "VERIFICA DISPONIBILITÀ" button was successfull
        res = self.driver_wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='annulla']")))
        return res


    def __try_to_book_set_room(self):
        """
        Tries to book the specified room
        """

        if (self.__is_set_room_available()):
            return self.__confirm_booking()
        else:
            # Clicks "ANNULLA" button to go back and select a different room/period
            self.driver.find_element_by_xpath("//button[@id='annulla']").click()
            return False


    def __is_set_room_available(self):
        """
            Clicks first available time slot relatively to the current day
        """

        self.__load_entire_timetable()

        # If 10 days have the message "Limite raggiunto! Ti ricordiamo che non puoi prenotare questo servizio più di 1 volte ogni 1 giorni",
        # this means that the maximum number of bookable days has been reached.
        if (len(self.driver.find_elements_by_xpath("//span[contains(text(), 'Limite raggiunto') or contains(text(), 'Limit reached')]")) >= 10):
            raise Exception("[+] Maximum number of days booked")

        try:
            # Make sure that the "Lista orari" is open (this clicks on "vedi orari")
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'vedi orari') or contains(text(), 'see timetables')]"))).click()

            # Tries to find a time slot
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'slot_available')]"))).click()

            return True
        except:
            pass

        return False


    def __confirm_booking(self):
        """
            Confirms the booking
        """

        try:
            # Clicks on "CONFERMA PRENOTAZIONE"
            self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='conferma']"))).click()

            # Clicks on "NUOVA PRENOTAZIONE"
            self.driver_wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div[1]/form/button"))).click()

            return True
        except:
            return False


    def __load_entire_timetable(self):
        """
            Attempts to load the entire timetable, this way it'll be possible to book all days
            (Clicks on "Giorni Successivi" until it's all loaded).
        """

        # Clicks the "Giorni Successivi" button until it's available
        while True:
            try:
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//h4[@id='load_next']"))).click()
            except:
                return

    def __del__(self):
        if (self.driver):
            self.driver.close()
