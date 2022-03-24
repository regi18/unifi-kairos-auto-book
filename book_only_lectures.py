from lectures.lectures_booking import *
from sys import exit
import credentials
from os import environ

environ['IS_WIN_DEVELOPMENT'] = 'True'        # Tells the script that it's running locally (and not on Heroku)
book_all_lectures()
exit(0)