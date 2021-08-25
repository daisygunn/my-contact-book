import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip

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
def user_choice():
    """
    User selects which task they would like to do
    Take their input and runs elif loop to trigger next process.
    If invalid choice is input then will continue to ask for a
    valid input.
    """
    print(
        "Please select from the following options: \n")
    print(
        "1.Retrieve all contacts 2.Retreive specific contact \
3.Add new contact 4.Edit existing contact\n")

    while True:
        try:
            user_input = int(input('Type your input here: '))
            if user_input <= 0 or user_input > 4:
                print("Please only select a number between 1 & 4.")
                break
        except ValueError as e:
            print(f"You have input an invalid option {e},\
                please select a number between 1 & 4.")
            return False
        if user_input == 1:
            retrieve_all_contacts()
        elif user_input == 2:
            retrieve_one_contact
        elif user_input == 3:
            add_new_contact()
        elif user_input == 4:
            edit_existing_contact()
        return True


# Retrieve all contacts
def retrieve_all_contacts():
    """
    Function to retrieve full list of contacts
    """
    contacts_all = SHEET.worksheet('contact_list').get_all_values()
    print(contacts_all)


# Retrieve one contact
def retrieve_one_contact():
    """
    Allows user to search for specific contact
    """
    print('Retrieve one')


# Add new contact
def add_new_contact():
    """
    Allows user to add new contact information
    """
    print('Add')


# Edit existing contact
def edit_existing_contact():
    """
    Allows user to edit exiting contact
    """
    print('Edit')

# Update worksheet

# Save


def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print('\nWelcome to your contacts book application!\n')
    user_choice()


run_programme()
