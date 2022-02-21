from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lectures.lectures_login import do_login


def book_all_lectures():
    """
    Book all possible lectures
    """

    # Logs in
    driver = do_login()

    webdriver_wait = WebDriverWait(driver, 3)

    while True:
        try:
            # Book a lecture
            webdriver_wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(text(), 'Verifica e prenota il tuo posto') or contains(text(), 'Check and book your seat')]"
                ))).click()

            # Check if booking was successful
            try:
                webdriver_wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="success-title"]')))
            except:
                err = driver.find_elements_by_xpath('//*[@class="mfp-content"]').text
                print("[!] Error while booking a lecture:", end="\n\n")
                print(err)

            
            booked_lecture_info  = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[1]/span[2]').text
            booked_lecture_info = booked_lecture_info.replace("\n", " ", 1).replace("\n", " - ")
            print(f"[+] {booked_lecture_info}")
            
            # Close the confirmation popup
            webdriver_wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="popup_conferma_buttons_row"]/button'))).click()

        # The while loop will exit when no more lectures are bookable
        except Exception as e:
            print("[+] Booked all possible lectures")
            return
