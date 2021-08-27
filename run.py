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
        else:
            # user_input == 3:
            add_new_contact()
            break
        # else:
        #     # edit_existing_contact()
        #     break
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


def retrieve_records():
    """
    Function to retrieve all records found
    in the contacts list spreadhseet.
    """
    return SHEET.worksheet('contact_list').get_all_records()


# Retrieve all contacts
def retrieve_all_contacts():
    """
    Function to retrieve full list of contacts
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    # print(all_contacts)
    for contact in all_contacts:
        print_records_in_loop(contact)
    another_task()


def print_records(records):
    """
    Function to print a single contact.
    To be used in the contact search functions.
    """
    print("\nNow printing your contact(s)...\n")
    # records_list = list(records)
    # print(records_list)
    for record in records:
        print_records_in_loop(record)


def print_records_in_loop(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    print("Printing record...")
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")


# Update worksheet
def update_worksheet(info):
    worksheet_to_update = SHEET.worksheet('contact_list')
    worksheet_to_update.append_row(info)


# Save
def save_to_worksheet(info):
    print('Would you like to save this contact?')
    user_input = pyip.inputYesNo()
    if user_input == 'yes':
        print(f'Now saving {info}....')
        worksheet_to_update = SHEET.worksheet('contact_list')
        worksheet_to_update.append_row(info)
        print('Save complete')
        another_task()
    else:
        print('\nYou will now be taken to edit this contact...\n')
        edit_existing_contact(info)


# Retrieve one contact
def retrieve_one_contact():
    """
    Allows user to search for specific contact,
    either by first name, last name or phone number.
    Function will then print all matches if they are found.
    """
    print("\nPlease select how you would like to search\n\
by selecting a number from the menu below:\n\
\n1. Search by first name\n\
2. Search by last name\n\
3. Search by phone number\n")

    while True:
        user_input = user_response(1, 3)
        if user_input == 1:
            first_name = pyip.inputStr('Enter first name: ').capitalize()
            result = filter(
                lambda record: record['first_name'] == first_name or
                first_name in record['first_name'], retrieve_records()
                )
            print_records(result)
            # result_list = list(result)
            # if len(result_list) != 0:
            #     print("contact found")
            #     print(result)
            # else:
            #     print("No contact with that name found")
        elif user_input == 2:
            last_name = pyip.inputStr('Enter last name: ').capitalize()
            result = filter(
                lambda record: record['last_name'] == last_name or
                last_name in record['last_name'], retrieve_records()
                )
            print_records(result)
            break
        else:
            phone_number = str(pyip.inputInt('*remember phone numbers are formatted \
            like this: 079 8972 9384* \nEnter phone number here:\n'))
            result = filter(
                lambda record: record['phone_number'] == phone_number or
                phone_number in record['phone_number'], retrieve_records()
                )
            print_records(result)
            break
        return False


# Edit from main menu

# Add new contact
def add_new_contact():
    """
    Allows user to add new contact information
    """
    print('To add a new contact please enter the details below:')
    first_name = pyip.inputStr('First Name: ')
    last_name = pyip.inputStr('Last Name: ')
    phone_number = pyip.inputStr('Phone Number: ')
    email_address = pyip.inputStr('Email Address: ')
    address = pyip.inputStr('Address: ')
    group = pyip.inputChoice(
        ['Family', 'Favourites', 'General', 'Friends']
        )
    new_contact_info = [
        first_name, last_name, phone_number, email_address, address, group
        ]
    print(new_contact_info)
    save_to_worksheet(new_contact_info)


# Edit existing contact
def edit_existing_contact(contact):
    """
    Allows user to edit exiting contact
    """
    print('\nWhich value would you like to change?\n \
1. First name\n 2.Last name\n 3.Phone number\n 4.Email address\n \
5. Address\n 6.Group\n')
    user_input = user_response(1, 6)
    if user_input == 1:
        new_value = pyip.inputStr('Enter new first name below:')
        contact[0] = new_value
        print(contact)
    elif user_input == 2:
        new_value = pyip.inputStr('Enter new last name below:')
        contact[1] = new_value
        print(contact)
    elif user_input == 3:
        new_value = pyip.inputStr('Enter new phone number below:')
        contact[2] = new_value
        print(contact)
    elif user_input == 4:
        new_value = pyip.inputStr('Enter new email below:')
        contact[3] = new_value
        print(contact)
    elif user_input == 5:
        new_value = pyip.inputStr('Enter new address below:')
        contact[4] = new_value
        print(contact)
    elif user_input == 6:
        new_value = pyip.inputChoice(
            ['Family', 'Favourites', 'General', 'Friends']
            )
        contact[5] = new_value
        print(contact)
    save_to_worksheet(contact)


def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print('\nWelcome to your contacts book application!\n')
    main_menu_selection()


run_programme()
