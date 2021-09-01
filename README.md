# My Contact Book
--
[Live application can be found here]()

This is a command-line-interface application designed to allow the user to access their contacts book, retrieve specific contact information, edit/delete exisiting contacts & add new contact information. This project has been designed for educational purposes.

## UX
To begin planning this project I started first with UX, designing the logic of the programme based upon the user stories. As this is a command-line application there is no design featured as HTML & CSS have not been used.

### Strategy
User Stories:
- As a user, I want to be able to easily access all of my contacts at once.
- As a user, I want to be able to retrieve a contact's information based upon their name.
- As a user, I want to update an existing contact's information if there has been a change.
- As a user, I want to be able to download contact information by group (family/friends).
- As a user, I want to be able to delete a contact entry.

### Structure
![Flowchart of Python logic](assets/images/flowchart.png)

As you can see from the flowchart above the logic has been based around the four key user options, retrieving contacts, adding contacts & editing existing contacts. Each path will take the user back to the beginning once finished. 

--
## Features

## Technologies Useds

I have used several technologies that have enabled this design to work:

- [Python](https://www.python.org/)
    - Python is the core programming language used to write all of the code in this application to make it fully functional.
    - In addition to core Python I have used the following Python modules:
        - [Gspread](https://docs.gspread.org/en/latest/)
            - Used to access my google sheets document throughout the application, to access and edit data.
        - [Google Auth](https://google-auth.readthedocs.io/en/master/)
            - Used to provide access to the application to interact with my google sheet.
        - [Pyip](https://pyinputplus.readthedocs.io/en/latest/)
            - Used to validate all of the user inputs.
        - [Colored](https://pypi.org/project/colored/)
        - Used to add colours to the printed terminal messages
- [GitHub](https://github.com/)
    - Used to store code for the project after being pushed.
- [Git](https://git-scm.com/)
    - Used for version control by utilising the Gitpod terminal to commit to Git and Push to GitHub.
- [Gitpod](https://www.gitpod.io/)
    - Used as the development environment.
- [Lucid](https://lucid.app/documents#/dashboard)
    - Used to create the flowchart for the project.
- [Grammarly](https://www.grammarly.com/)
    - Used to fix the thousands of grammar errors across the project.
- [Google Sheets](https://www.google.co.uk/sheets/about/)
    - Used to store the 'Contacts' data used for the application.

## Testing

## Deployment

## Credits

