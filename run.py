import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Contacts sheet')


# User choice

# Retrieve all contacts

# Retrieve one contact

# Add new contact

# Edit existing contact

# Update worksheet

# Save

def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print('Welcome to your contacts book application!\n')
    