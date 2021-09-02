import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip
from colored import fore, back, style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Contacts sheet')
CONTACTS_WORKSHEET = SHEET.worksheet('contact_list')


# Function to validate user response based upon number selection
def user_response(min_value, max_value):
    """
    Function used throughout programme
    to validate users input from a list of choices.
    """
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
    print("\nPlease select from the following options: \n")
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
    """
    Function to take users back to the
    main menu if they have something else
    they would like to do.
    This is called at the end of the
    other processes.
    """
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
            print(
                fore.WHITE + back.DARK_GRAY + style.BOLD +
                "Programme shutting down...\n")
            break


def retrieve_records():
    """
    Function to retrieve all records found
    in the contacts list spreadhseet.
    """
    return CONTACTS_WORKSHEET.get_all_records()


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
    for record in records:
        print_records_in_loop(record)


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
    """
    Function used when editing a contact
    to make changes to the worksheet.
    """
    worksheet_to_update = CONTACTS_WORKSHEET
    worksheet_to_update.update_cell(row, col, value)
    print(
            fore.WHITE + back.GREEN_4 + style.BLINK +
            'Change saved' + style.RESET
            )
    another_task()


# Save
def save_to_worksheet(info):
    """
    Function used when saving a contact
    to make changes to the worksheet.
    """
    print('\nWould you like to save this contact?\n Y or N')
    user_input = pyip.inputYesNo()
    if user_input == 'yes':
        print(f'\nNow saving {info}....\n')
        worksheet_to_update = CONTACTS_WORKSHEET
        worksheet_to_update.append_row(info)
        print(
            fore.WHITE + back.GREEN_4 + style.BLINK +
            'Save complete' + style.RESET
            )
        another_task()
    else:
        print('\nYou will now be taken to edit this contact...\n')
        edit_existing_contact(info)


# Get new contact_ID
def contact_id_creation():
    """
    Function called to generate
    a new contact ID, based upon
    the previous entry. Needed when
    adding new contact information.
    """
    all_values = CONTACTS_WORKSHEET.get_all_values()
    previous_row = all_values[-1]
    previous_contact_id = int(previous_row[6])
    new_contact_id = str(previous_contact_id + 1)
    return new_contact_id


# Search
def search(info_type):
    """
    Function that returns result based upon
    user input and info type selected.
    """
    search_by = pyip.inputStr(f'\nEnter {info_type}: ').capitalize()
    result = list(filter(
        lambda record: record[info_type] == search_by or
        search_by in record[info_type], retrieve_records()
        ))
    if len(result) != 0:
        print(
            fore.WHITE + back.GREEN_4 + style.BOLD +
            "Contact found" + style.RESET
            )
        print_records(result)
        global contact_info
        user_input = pyip.inputInt('Select an option from the following:\n \
1. Edit this contact\n 2. Delete this contact\n 3. Back to main menu\n')
        if user_input == 1:
            if len(result) > 6:
                print('list is longer than one')
                print(contact_info)
            else:
                edit_existing_contact(contact_info)
        elif user_input == 2:
            if len(result) > 6:
                print('list is longer than one')
                print(contact_info)
            else:
                delete(contact_info, 6)
        else:
            another_task()
    else:
        print(
            fore.WHITE + back.RED + style.BLINK +
            "No contact with that name found" + style.RESET)


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
            search('first_name')
        elif user_input == 2:
            search('last_name')
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
type NA for any fields you wish to leave blank.\n')
    first_name = pyip.inputStr('First Name: ').capitalize()
    last_name = pyip.inputStr('Last Name: ').capitalize()
    phone_number = pyip.inputStr('Phone Number: ', blockRegexes=['A-Za-z'])
    email_address = pyip.inputEmail('Email Address: ')
    address = pyip.inputStr('Address: ')
    group = pyip.inputChoice(
        ['Family', 'Favourites', 'General', 'Friends']
        )
    contact_id = contact_id_creation()
    new_contact_info = [
        first_name, last_name, phone_number,
        email_address, address, group, contact_id
        ]
    print(new_contact_info)
    save_to_worksheet(new_contact_info)


def edit(contact, cell_index, info_type):
    """
    Cell index is based upon which field is
    being edited, allows user to update cell by
    adding a new entry.
    """
    cell = CONTACTS_WORKSHEET.find(contact[cell_index])
    print(cell.row, cell.col)
    new_value = pyip.inputStr(f'Enter new {info_type}: ').capitalize()
    contact[cell_index] = new_value
    print(f'{info_type} now being updated...\n')
    update_worksheet(cell.row, cell.col, new_value)
    print(contact)


def delete(contact, index):
    """
    Retrieves cell index based upon search
    and allows user to update cell by
    adding a new entry.
    """
    contact_id = str(contact[index])
    contact_row = CONTACTS_WORKSHEET.find(contact_id)
    row_number = contact_row.row
    user_input = pyip.inputYesNo('Are you sure you want to delete this contact?\n')
    if user_input == 'yes':
        print(f'{contact} now being deleted...\n')
        CONTACTS_WORKSHEET.delete_rows(row_number)
        print('Deleted.\n')
        another_task()
    else:
        another_task()


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
        cell = CONTACTS_WORKSHEET.find(contact[5])
        new_value = pyip.inputChoice(
            ['Family', 'Favourites', 'General', 'Friends']
            )
        contact[5] = new_value
        print('Group now being updated...\n')
        update_worksheet(cell.row, cell.col, new_value)
        print(contact)


def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print(
        fore.WHITE + back.BLUE + style.BOLD +
        '\nWelcome to your contacts book application!\n' + style.RESET)
    main_menu_selection()


# retrieve_one_contact()
run_programme()
