# Unifi Kairos Auto-book
Automatically books lectures for UniFi's "Agenda Web" and a list of studyrooms

# Setup

## Local

To run this on your local machine do the following steps:

1. Clone this repo
2. Create the credentials.py file (see below)
4. Run `py -m pip install -r requirements.txt` to install the required python libraries
3. Run the entire program with `py local_main.py` or only for booking lectures type `py book_only_lectures.py`

### credentials.py

Create a new file in the root of the project called `credentials.py` and replace `<matricola here>` and `<password here>` with your matricola and password

```
from os import environ

environ['IS_WIN_DEVELOPMENT'] = 'True'        # Tells the script that it's running locally (and not on Heroku)
environ['IS_HEADLESS_WIN_DEV'] = 'True'       # Comment or set to another value to see the simulated Chrome Browser (leave like this to run headlessly)

environ['USERNAME'] = '<matricola here>'
environ['PASSWORD'] = '<password here>'
```

#### OS Compatibility

The scripts are fully compatible with any *nix os, you only have to adjust the webdriver so that it points to a correct binary executable for your system.

## Heroku

You can also run this script automatically on Heroku. Just follow the steps:
1. **Create** a new app
2. **Deploy** this repo to Heroku via the preferred method (Heroku Git, Github, etc.)

3. Add the following **Buildpacks**:
    - `heroku/python`
    - `https://github.com/heroku/heroku-buildpack-google-chrome`
    - `https://github.com/heroku/heroku-buildpack-chromedriver`

4. Set the following **Config Vars**:
    - `PASSWORD` = your password
    - `USERNAME` = your matricola

5. Finally setup **Heroku Scheduler** to have it run automatically:
    -  Choose the daily interval with a time of your choosing (e.g. Every day at... 9:30 AM)
    -  Set it to run the following command: `python main.py`
