# Unifi Kairos Auto-book
Automatically books lectures for UniFi's "Agenda Web" and a list of studyrooms

# Setup

## Local

To run this on your local machine do the following steps:

1. Clone this repo
2. Copy `credentials.example.py`, rename it to `credentials.py` and set your matricola and password. 
3. Run `py -m pip install -r requirements.txt` to install the required python libraries
4. Run the entire program with `py local_main.py` or only for booking lectures type `py book_only_lectures.py`

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
