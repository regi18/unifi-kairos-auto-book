from studyrooms.studyrooms_booking import StudyroomsBooking
from lectures.lectures_booking import book_all_lectures
from datetime import date
from sys import exit
from os import environ


def main():
    if (environ.get('IS_WIN_DEVELOPMENT') != 'True'):
        if date.today().isoweekday() != 5:
            print("[*] Skipping... today is not friday.")
            exit(0)

    book_all_lectures()
    # StudyroomsBooking().book_all_possible_studyrooms()

    exit(0)


if __name__ == '__main__':
    main()