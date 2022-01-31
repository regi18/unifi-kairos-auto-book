from studyrooms.studyrooms_booking import *
from datetime import date
from sys import exit
from os import environ


if __name__ == '__main__':
    if (environ.get('IS_WIN_DEVELOPMENT') != 'True'):
        if date.today().isoweekday() != 5:
            print("[*] Skipping... today is not friday.")
            exit(0)

    StudyroomsBooking().book_all_possible_studyrooms()

    exit(0)