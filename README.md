# Unifi Kairos Auto-book
Automatically books lectures for UniFi's "Agenda Web" and a list of studyrooms

# Setup

## Local

To run this on your local (windows) machine do the following steps:

1. Clone this repo
2. Create the credentials.py file (see below)
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

You can also run this script automatically on Heroku.
// TODO
