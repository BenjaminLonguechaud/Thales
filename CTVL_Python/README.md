# TOKENIZATION-CT-VL
# Tokenization Application

This project is a Python-based GUI application for managing tokenization and detokenization of sensitive data. The application interacts with a server to securely tokenize data such as credit card numbers and then retrieve the original data when necessary.

## Features

- *Multi-tab Interface*: The application provides three different tabs:
  - *Application Tab*: For standard users to tokenize credit card data.
  - *Payable Tab*: Allows users to detokenize the previously tokenized data.
  - *Support Tab*: Provides similar functionality for support users with masked display of detokenized data.
- *User Authentication*: Users must log in with their credentials to access tokenization and detokenization features.
- *Configurable Server URL*: The URL for the tokenization server can be set dynamically via the application.
- *Data Security*: Utilizes tokenization to securely handle sensitive data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/tokenization-application.git
   
2. Navigate to the project directory:
   cd tokenization-application

3. Install the required Python packages:
   pip install -r requirements.txt

4. Ensure you have the following dependencies installed:
   tkinter
   requests
   Pillow
   urllib3

## Usage

1. Run the application:
   python main.py
   
2. The application window will open with three tabs:
   Application: Enter your username, password, and the data you wish to tokenize.
   Payable: Log in and detokenize data.
   Support: Log in and detokenize data with a masked display.
   
3. To change the server URL, navigate to Settings > Set CT-VL URL in the menu.

## Configuration 
The application allows you to configure the following variables in the AdminVariables class:

 1. ct_url: The base URL of the tokenization server.
 2. tokengroupCC, tokentemplateCC: Token group and template for standard users.
 3. tokengroupSupport, tokentemplateSupport: Token group and template for support users.

## Code description
This code creates a GUI application using Python'stkinterlibrary. The application interacts with a tokenization and detokenization service
provided by a Thales CipherTrust Vaultless Tokenization (CT-VL) server. The main purpose of the application is to allow users to log in, tokenize sensitive data (like credit card numbers), and detokenize the tokens to retrieve the original data. Below is a detailed explanation of the code.
### Imports
1. tkinter: The primary library for creating the graphical user interface.
2. ttk: A module in tkinter that provides themed widgets.
3. messagebox: A module in tkinter used to show popup messages.
4. Menu: A module in tkinter used to create dropdown menus.
5. requests: A Python library for making HTTP requests, used to interact with the CT-VL API.
6. json: A module to handle JSON data.
7. PIL (Python Imaging Library): Specifically, Image and ImageTk are used to handle and display images (like logos).
8. urllib3: Used to handle HTTPS requests without verification warnings, which is useful for self-signed certificates.

### AdminVariables Class
1. Purpose: Stores configuration variables like the URL of the CT-VL server, and token group and template names for both the tokenization and support user roles.
2. Variables:
  ct_url: The URL of the CT-VL server.
  tokengroupCCandtokentemplateCC: Used for tokenization by the tokenadmin.
  tokengroupSupportandtokentemplateSupport: Used for tokenization by the support user.

### Helper Functions
1. give_token_from_json(entry_node): Extracts and returns the token from a JSON string. If the string is empty or an error occurs during parsing, it returns an empty string.
2. give_data_from_json(entry_node): Similar to the above, but it extracts and returns the original data associated with a token.

### TokenizationApplication Class
1. Purpose: This is the main application class that inherits from tk.Tk, which is the base class for all tkinter applications. It sets up the GUI, handles user interactions, and communicates with the CT-VL API.
2. Attributes and Methods:

**__init__():**
   * Initializes the application window with a title and size.
   * Creates a session object for making HTTP requests.
   * Sets up a menu with options like "Set CT-VL URL."
   * Creates and adds tabs (Application, Payable, Support) for different user roles.
   * Calls methods to create widgets and add a logo to each tab.

**set_url() and save_url():**
   * Allows the user to set and save the CT-VL server URL via a popup window.

**create_application_tab(), create_payable_t ab(),  create_support_tab():**
   * Each method creates the respective tab with input fields for username, password, and data (e.g., credit card numbers or tokens).
   * Adds buttons for actions like login, tokenize, and detokenize, and sets the initial state of these buttons.

**add_logo(tab):**
   * Attempts to load and display the Thales logo in the bottom right corner of each tab.
   * Resizes the image to fit within the GUI and uses ImageTk.PhotoImage to display it.

**login(tab_number):**
   * Handles user login for the selected tab (Application, Payable, or Support).
   * SendsaPOSTrequesttotheCT-VLAPItoauthenticate the user.
   * If successful, the authentication token is stored and the relevant buttons are enabled.

**tokenize():**
* Takes the user-inputted data (e.g., credit card number), sends it to the CT-VL API for tokenization, and displays the resulting token in the application.
* The token is also propagated to the Payable and Support tabs for potential detokenization.

**detokenize(tab_number):**
* Takes a token from the respective tab (Payable or Support), sends it to the CT-VL API for detokenization, and displays the original data.
* TheSupporttabadditionallymasksthedetokenizeddata (e.g., showing only the last four digits of a credit card number).
