from studyrooms.studyrooms_booking import *
from datetime import date
from sys import exit

if __name__ == '__main__':
    if (os.environ.get('IS_WINDOWS') != 'True'):
        if date.today().isoweekday() != 5:
            print("[*] Skipping... today is not friday.")
            exit(0)

    try:
        sb = StudyroomsBooking().book_all_possible_studyrooms()

    except Exception as e:
        print("[ERROR: main.py]" + " " + repr(e))
        exit(1)

    exit(0)