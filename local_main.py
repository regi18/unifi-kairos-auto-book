import credentials
from main import main
from os import environ

environ['IS_WIN_DEVELOPMENT'] = 'True'        # Tells the script that it's running locally (and not on Heroku)

main()

