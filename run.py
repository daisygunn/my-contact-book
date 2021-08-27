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
        return record


def print_records_in_loop(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    print("Printing record...")
    global contact_info
    contact_info = []
    for key, value in record.items():
        print(f"{key}: {value}")
        contact_info.append(value)
    print("\n")
    return contact_info


# Update worksheet
def update_worksheet(row, col, value):
    worksheet_to_update = SHEET.worksheet('contact_list')
    worksheet_to_update.update_cell(
            row, col, value
            )


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
            result = list(filter(
                lambda record: record['first_name'] == first_name or
                first_name in record['first_name'], retrieve_records()
                ))
            if len(result) != 0:
                print("Contact found")
                print_records(result)
                global contact_info
                user_input = pyip.inputYesNo('Would you like to edit this contact? \
# Type yes or no -')
                if user_input == 'yes':
                    if len(result) > 6:
                        print('list is longer than one')
                        print(contact_info)
                    else:
                        edit_existing_contact(contact_info)
                else:
                    another_task()
            else:
                print("No contact with that name found")
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
    print('To add a new contact please enter the details below, \
type NA for any fields you wish to leave blank.')
    first_name = pyip.inputStr('First Name: ').capitalize()
    last_name = pyip.inputStr('Last Name: ').capitalize()
    phone_number = pyip.inputStr('Phone Number: ', blockRegexes=['A-Za-z'])
    email_address = pyip.inputEmail('Email Address: ')
    address = pyip.inputStr('Address: ')
    group = pyip.inputChoice(
        ['Family', 'Favourites', 'General', 'Friends']
        )
    new_contact_info = [
        first_name, last_name, phone_number, email_address, address, group
        ]
    print(new_contact_info)
    save_to_worksheet(new_contact_info)


def edit(contact, cell_index, info_type):
    """
    Retrieves cell index based upon search
    and allows user to update cell by
    adding a new entry.
    """
    cell = SHEET.worksheet('contact_list').find(contact[cell_index])
    print(cell.row, cell.col)
    new_value = pyip.inputStr(f'Enter new {info_type}: ').capitalize()
    contact[cell_index] = new_value
    print(f'{info_type} now being updated...')
    update_worksheet(cell.row, cell.col, new_value)
    print(contact)


# Edit existing contact
def edit_existing_contact(contact):
    """
    Allows user to edit existing contact,
    choosing which input field they would like
    to edit.
    """
    print(contact)
    print('\nWhich value would you like to change?\n \
1.First name\n 2.Last name\n 3.Phone number\n 4.Email address\n \
5.Address\n 6.Group\n')
    user_input = user_response(1, 6)
    if user_input == 1:
        edit(contact, 0, 'first name')
        another_task()
    elif user_input == 2:
        edit(contact, 1, 'last name')
        print(contact)
        another_task()
    elif user_input == 3:
        edit(contact, 2, 'phone number')
        print(contact)
        another_task()
    elif user_input == 4:
        edit(contact, 3, 'email address')
        print(contact)
        another_task()
    elif user_input == 5:
        edit(contact, 4, 'address')
        print(contact)
        another_task()
    elif user_input == 6:
        cell = SHEET.worksheet('contact_list').find(contact[5])
        new_value = pyip.inputChoice(
            ['Family', 'Favourites', 'General', 'Friends']
            )
        contact[5] = new_value
        print('Group now being updated...')
        update_worksheet(cell.row, cell.col, new_value)
        print(contact)


def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print('\nWelcome to your contacts book application!\n')
    main_menu_selection()


# retrieve_one_contact()
run_programme()
