from typing import Literal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StudyroomsBookingUtils:

    def __init__(self, driver, SUFFICIENT_BOOKED_DAYS_COUNT):
        self.driver = driver
        self.SUFFICIENT_BOOKED_DAYS_COUNT = SUFFICIENT_BOOKED_DAYS_COUNT
        self.driver_wait_10s = WebDriverWait(self.driver, 10)
        self.driver_wait_3s = WebDriverWait(self.driver, 3)


    def select_study_room(self, room, period: Literal['morning', 'afternoon']):
        """
            Selects the study room
        """

        # Selects "Posti studi in ateneo" (instead of "Servizi bibliotecari")
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-raggruppamento_servizi-container"]'))).click()
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[2]/ul/li[2]'))).click()

        # Sets the time period (Mattina or Pomeriggio)
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-servizio-container"]'))).click()
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/span/span/span[2]/ul/li[{'2' if period == 'morning' else '3'}]"))).click()
        # Simulate a click outside the dropdown to close it
        self.driver.find_element_by_xpath('//*[@id="servizio-container"]').click()

        # Clicks the dropdown
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[4]/div[2]/div/div/form/div/div[1]/div/div[4]/div/div[2]/span/span[1]/span/span[2]'))).click()
        # Selects the requested room
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[2]/ul/li[contains(text(), ' + room + ')]'))).click()
        # Waits for the current date to load on the "Scegli la data dell'appuntamento" input field
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='data_inizio']"))).click()
        # Clicks "VERIFICA DISPONIBILIT??"
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='verify']"))).click()

        # Check if the "ANNULLA" button is present, i.e. if the previously clicked "VERIFICA DISPONIBILIT??" button was successfull
        res = self.driver_wait_10s.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='annulla']")))
        return res


    def try_to_book_selected_room(self):
        """
        Tries to book the specified room
        """

        if (self.__is_selected_room_available()):
            return self.__confirm_booking()
        else:
            # Clicks "ANNULLA" button to go back and select a different room/period
            self.driver.find_element_by_xpath("//button[@id='annulla']").click()
            return False


    def fix_missing_form_data(self):
        """
            Make a useless click on Verifica Disponibilit?? to overcome missing data error.
            (This is needed because after clicking "Annulla" and going back to the "new booking" page, 
            the previously chosen settings will still be there, but the system won't consider them)
        """
        self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='verify']"))).click()


    # -------------------- PRIVATE  -------------------- #


    def __confirm_booking(self):
        """
            Confirms the booking
        """

        try:
            # Clicks on "CONFERMA PRENOTAZIONE"
            self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='conferma']"))).click()

            # Clicks on "NUOVA PRENOTAZIONE"
            self.driver_wait_10s.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div[1]/form/button"))).click()

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
                self.driver_wait_3s.until(EC.element_to_be_clickable((By.XPATH, "//h4[@id='load_next']"))).click()
            except:
                return


    def __is_selected_room_available(self):
        """
            Clicks first available time slot relatively to the current day
        """

        self.__load_entire_timetable()

        # If 10 days have the message "Limite raggiunto! Ti ricordiamo che non puoi prenotare questo servizio pi?? di 1 volte ogni 1 giorni",
        # this means that already SUFFICIENT_BOOKED_DAYS_COUNT days have been booked.
        already_booked_days_count = len(self.driver.find_elements_by_xpath("//span[contains(text(), 'Limite raggiunto') or contains(text(), 'Limit reached')]"))
        available_count = len(self.driver.find_elements_by_xpath("//span[contains(text(), 'vedi orari') or contains(text(), 'see timetables')]"))
        if (available_count == 0 and already_booked_days_count >= self.SUFFICIENT_BOOKED_DAYS_COUNT):
            print("\n[+] 10 or more days already booked. Closing...")
            exit(0)

        try:
            # Make sure that the "Lista orari" is open (this clicks on "vedi orari")
            self.driver_wait_3s.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'vedi orari') or contains(text(), 'see timetables')]"))).click()

            # Tries to find a time slot
            self.driver_wait_3s.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'slot_available')]"))).click()

            return True
        except:
            pass

        return False

