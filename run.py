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


def user_response(message, min_value, max_value):
    """
    Function used throughout programme
    to validate users input from a list of choices.
    """
    input = pyip.inputInt(prompt=message, min=min_value, max=max_value)
    return input


def main_menu_selection():
    """
    User selects which task they would like to do
    Take their input and runs elif loop to trigger next process.
    If invalid choice is input then will continue to ask for a
    valid input.
    """
    print(
        "\n 1. Retrieve all contacts\n 2. Search contacts\n\
 3. Add new contact\n 4. Edit existing contact\n")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 4
            )
        if user_input == 1:
            retrieve_all_contacts()
            break
        elif user_input == 2:
            search_contacts()
            break
        elif user_input == 3:
            add_new_contact()
            break
        else:
            edit_contact_from_menu()
            break
        return False


def another_task():
    """
    Function to take users back to the
    main menu if they have something else
    they would like to do.
    This is called at the end of the
    other processes.
    """
    print("\nWould you like to complete another task?\n")
    print("1. Yes, back to main menu\n\
2. No, end programme")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 2
            )
        if user_input == 1:
            print("\nNow taking you back to the main menu...\n")
            main_menu_selection()
            break
        else:
            print(
                fore.WHITE + back.DARK_GRAY + style.BOLD +
                "Programme shutting down...\n" + style.RESET)
            break


def retrieve_records():
    """
    Function to retrieve all records found
    in the contacts list spreadhseet.
    """
    return CONTACTS_WORKSHEET.get_all_records()


def retrieve_all_contacts():
    """
    Function to retrieve full list of contacts
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    for contact in all_contacts:
        print_records_in_loop(contact)
    another_task()


def print_records(records, function=None):
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
    list of key: values. Also returns a list of just
    the value items to be used when editing a contact.
    """
    print("Printing record...")
    global contact_info
    contact_info = []
    for key, value in record.items():
        print(f"{key}: {value}")
        contact_info.append(value)
    print("\n")
    return contact_info


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


def save_to_worksheet(info):
    """
    Function used when saving a contact
    to make changes to the worksheet.
    """
    print(f'\nNow saving {info}....\n')
    worksheet_to_update = CONTACTS_WORKSHEET
    worksheet_to_update.append_row(info)
    print(
        fore.WHITE + back.GREEN_4 + style.BLINK +
        'Save complete' + style.RESET
        )
    user_input = pyip.inputYesNo(
        '\nWould you like to edit this contact? (Y/N): '
        )
    if user_input == 'yes':
        print('\nYou will now be taken to edit this contact...\n')
        edit_existing_contact(info)
    else:
        another_task()


def contact_id_creation():
    """
    Function called to generate a new contact ID,
    based upon the previous entry in the worksheet.
    Needed when adding new contact information.
    """
    all_values = CONTACTS_WORKSHEET.get_all_values()
    previous_row = all_values[-1]
    previous_contact_id = int(previous_row[6])
    new_contact_id = str(previous_contact_id + 1)
    return new_contact_id


def convert_to_list_action(option, action):
    """
    Function to convert contact dictionary to list
    so that it can be properly indexed when editing
    or deleting the contact information; necessary if
    multiple contacts have been returned from a search.
    """
    values = option.values()
    values_list = list(values)
    if action == 'edit':
        edit_existing_contact(values_list)
    elif action == 'delete':
        delete(values_list, 6)
    else:
        print('Invalid action has been defined.')


def select_from_multiple_records(contacts):
    """
    Function to choose a single record from a list
    of records that have been returned
    """
    def print_record(record):
        for key, value in record.items():
            print(f"{key}: {value}")

    def print_records_as_options(records, function=None):
        """
        Function to print a single contact with an record number.
        To be used in the contact search functions.
        """
        for idx, record in enumerate(records):
            print(f"\nRecord: {idx}\n")
            print_record(record)

    print('\nList of contacts to choose from: ')
    print_records_as_options(contacts, print_record)
    user_input = user_response(
        '\nEnter the record number of the contact you would like to action: ',
        1, len(contacts))
    return contacts[user_input]


def search(info_type):
    """
    Function that returns result based upon
    user input and info type selected.
    """
    if info_type == 'category':
        user_input = user_response('*Choose category to search by: 1.Friends, \
2.Favourites, 3.Family or 4.General: ', 1, 4)
        if user_input == 1:
            category = 'Friends'
        elif user_input == 2:
            category = 'Favourites'
        elif user_input == 3:
            category = 'Family'
        else:
            category = 'General'
        search_by = category
    elif info_type == 'phone_number':
        phone_number = str(pyip.inputInt('*\nEnter phone number here:\n'))
        search_by = phone_number
    else:
        search_by = pyip.inputStr(f'\nEnter {info_type}: ').capitalize()
    # Filter function used to search within the worksheet
    result = list(filter(
        lambda record: record[info_type] == search_by or
        search_by in record[info_type], retrieve_records()
        ))
    # If there are any results found
    if len(result) != 0:
        print(
            fore.WHITE + back.GREEN_4 + style.BOLD +
            "Contact found" + style.RESET
            )
        print_records(result)
        print('1. Edit contact(s)\n2. Delete contact(s)\n\
3. Back to main menu\n')
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 3
            )
        """
        If there is more than one contact returned
        the user needs to be able to choose which
        contact to edit or delete which is done using the
        select_from_multiple_records function.
        """
        if user_input == 1:
            # Edit
            if len(result) == 1:
                edit_existing_contact(contact_info)
            elif len(result) > 1:
                contact_choice = select_from_multiple_records(result)
                convert_to_list_action(contact_choice, 'edit')
        # Delete
        elif user_input == 2:
            if len(result) == 1:
                delete(contact_info, 6)
            elif len(result) > 1:
                contact_choice = select_from_multiple_records(result)
                convert_to_list_action(contact_choice, 'delete')
        else:
            main_menu_selection()
    # If no results are found
    else:
        print(
            fore.WHITE + back.RED + style.BLINK +
            "\nNo contact with that name found\n" + style.RESET)
        print('\nYou will now be taken back to search again...\n')
        search_contacts()


def search_contacts():
    """
    Allows user to search for specific contact(s),
    either by first name, last name, phone number or category.
    Function will then print all matches if they are found.
    """
    print("\nHow would you like to search?\n\
1. By first name\n\
2. By last name\n\
3. By category\n\
4. By phone number\n\
5. Exit\n")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 5
            )
        if user_input == 1:
            search('first_name')
        elif user_input == 2:
            search('last_name')
        elif user_input == 3:
            search('category')
        elif user_input == 4:
            search('phone_number')
        else:
            another_task()
        return False


def edit_contact_from_menu():
    """
    Function to edit contact from the
    main menu. User will need to search for
    the contact first.
    """
    print(
        '\nIn order to edit a contact, \
you will first need to search for them.\n'
        )
    print('\nTaking you to search now...\n')
    search_contacts()


def validate_phone_number():
    """
    Function to validate phone number entries,
    enusring they are 10 digits only
    (the 0 at the beginning is not counted)
    """
    while True:
        phone_number = str(pyip.inputInt('*Phone Number: '))
        if len(phone_number) < 10 or len(phone_number) > 10:
            print(f"Phone number must be 11 digits long.\
You entered {len(phone_number)} digits.\n \
Please note only UK numbers allowed, starting with 0.")
        else:
            return phone_number


def add_new_contact():
    """
    Allows user to add new contact information
    """
    print('\nTo add a new contact please enter the details below.\n\
\nAll fields with a * are required.\n\
\nType NA for any fields you wish to leave blank.\n')
    first_name = pyip.inputStr('*First Name: ').capitalize()
    last_name = pyip.inputStr('*Last Name: ').capitalize()
    phone_number = validate_phone_number()
    email_address = pyip.inputEmail('*Email Address: ', allowRegexes='NA')
    address = pyip.inputStr('Address: ')
    user_input = user_response('*Choose category: 1.Friends, \
2.Favourites, 3.Family or 4.General: ', 1, 4)
    if user_input == 1:
        category = 'Friends'
    elif user_input == 2:
        category = 'Favourites'
    elif user_input == 3:
        category = 'Family'
    else:
        category = 'General'
    contact_id = contact_id_creation()
    new_contact_info = [
        first_name, last_name, phone_number,
        email_address, address, category, contact_id
        ]
    print(new_contact_info)
    save_to_worksheet(new_contact_info)


def edit(contact, cell_index, info_type):
    """
    Cell index is based upon which field is
    being edited, allows user to update cell by
    adding a new entry.
    """
    # Converts to a string first to allow any integers to be searched for.
    cell = CONTACTS_WORKSHEET.find(str(contact[cell_index]))
    if cell_index == 2:
        new_value = validate_phone_number()
    else:
        new_value = pyip.inputStr(f'Enter new {info_type}: ').capitalize()
    contact[cell_index] = new_value
    print(f'{info_type} now being updated...\n')
    update_worksheet(cell.row, cell.col, new_value)


def delete(contact, index):
    """
    Retrieves cell index based upon search
    and allows user to update cell by
    adding a new entry.
    """
    print(contact)
    contact_id = str(contact[index])
    contact_row = CONTACTS_WORKSHEET.find(contact_id)
    row_number = contact_row.row
    user_input = pyip.inputYesNo(
        '\nAre you sure you want to delete this contact?\n Y or N\n'
        )
    if user_input == 'yes':
        print(f'{contact} now being deleted...\n')
        CONTACTS_WORKSHEET.delete_rows(row_number)
        print('Deletion complete.\n')
        another_task()
    else:
        another_task()


def edit_existing_contact(contact):
    """
    Allows user to edit existing contact,
    choosing which input field they would like
    to edit.
    """
    print(contact)
    print('\nWhich value would you like to change?\n \
1.First name\n 2.Last name\n 3.Phone number\n 4.Email address\n \
5.Address\n 6.category\n 7.Exit')
    user_input = user_response(
        "\nPlease enter a number from the above options: ", 1, 7
        )
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
        user_input = user_response('*Choose category: 1.Friends, \
2.Favourites, 3.Family or 4.General: ', 1, 4)
        if user_input == 1:
            new_value = 'Friends'
        elif user_input == 2:
            new_value = 'Favourites'
        elif user_input == 3:
            new_value = 'Family'
        else:
            new_value = 'General'
        contact[5] = new_value
        print('\nCategory now being updated...\n')
        update_worksheet(cell.row, cell.col, new_value)
        print(contact)
        another_task()
    else:
        another_task()


def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print(
        fore.WHITE + back.BLUE + style.BOLD +
        '\nWelcome to your contacts book application!\n')
    print('\nInstructions:\n \
- When presented with a number menu you need to type the relevant \
\n number and press enter. This will take you to your desired choice.\n\
- If presented with a Y or N choice, \n please type Y or \
N in to the input field and press enter.')
    print('\nNow taking you to the main menu...\n' + style.RESET)
    main_menu_selection()


run_programme()
