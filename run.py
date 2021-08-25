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


# Function to validate user response based upon number selection
def user_response(min_value, max_value):
    input = pyip.inputInt(min=min_value, max=max_value)
    return input


# Main menu selection
def main_menu_selection():
    """
    User selects which task they would like to do
    Take their input and runs elif loop to trigger next process.
    If invalid choice is input then will continue to ask for a
    valid input.
    """
    print(
        "\nPlease select from the following options: \n")
    print(
        "1.Retrieve all contacts\n2.Retreive specific contact\n\
3.Add new contact\n4.Edit existing contact\n")
    while True:
        user_input = user_response(1, 4)
        if user_input == 1:
            retrieve_all_contacts()
            break
        elif user_input == 2:
            retrieve_one_contact()
            break
        elif user_input == 3:
            add_new_contact()
            break
        else:
            edit_existing_contact()
            break
        return False


# Function for user to choose if they want to complete another task
# or shut the programme down
def another_task():
    print("Would you like to complete another task?")
    print("1. Yes, back to main menu\n\
2. No, end programme")
    while True:
        user_input = user_response(1, 2)
        if user_input == 1:
            print("\nNow taking you back to the main menu...\n")
            main_menu_selection()
            break
        else:
            print("Programme shutting down...\n")
            break


# Retrieve all contacts
def retrieve_all_contacts():
    """
    Function to retrieve full list of contacts
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    # print(all_contacts)
    for contact in all_contacts:
        print_record(contact)
    another_task()


def print_records(records):
    """
    Function to retrieve full list of contacts
    """
    print("\nNow printing all of your contacts...\n")
    for contact in records:
        print_record(contact)


def retrieve_records():
    return SHEET.worksheet('contact_list').get_all_records()


def print_record(record):
    print("Printing record...")
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")


# Retrieve one contact
def retrieve_one_contact():
    """
    Allows user to search for specific contact
    """
    print("\nPlease select how you would like to search...\n\
\n1. Search by first name\n\
2. Search by last name\n\
3. Search by phone number\n")

    while True:
        user_input = user_response(1, 3)
        if user_input == 1:
            print('search_by_first_name')
            name = input('Enter name:')
            result = filter(
                lambda record: record['first_name'] == name, retrieve_records()
                )
            print_records(result)
            break
        elif user_input == 2:
            print('search_by_last_name')
            break
        else:
            print('search_by_phone_number')
            break
        return False


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
    main_menu_selection()


run_programme()
