# CRDP Data Protection Manager

A user-friendly GUI application for protecting and revealing sensitive data using CipherTrust CRDP (CipherTrust RESTful Data Protection).

## Features

- **Data Protection**: Encrypt sensitive data using CRDP protection policies
- **Data Revelation**: Decrypt protected data with flexible display options
- **Masking Support**: Display decrypted data in clear text or masked format (showing only last 4 characters)
- **Username Tracking**: Optional username field for audit logging
- **Policy Selection**: Choose from available CRDP protection policies
- **Status Monitoring**: Real-time connection status and API health checks
- **Clipboard Integration**: Easy copy-to-clipboard functionality

## Requirements

- Python 3.8+
- tkinter (usually comes with Python)
- requests library
- Network access to:
  - CRDP Service
  - CipherTrust Manager

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Workflow

#### Protect Data Tab
1. Enter the data you want to protect in the "Data to Protect" field
2. Select a protection policy from the dropdown
3. Click "Protect Data"
4. The encrypted/protected data will appear in the result area
5. Use "Copy Protected Data" to copy it to clipboard

#### Reveal Data Tab
1. Paste the protected/encrypted data in the "Protected Data" field
2. Enter your username
3. Click "Reveal Data"
4. The decrypted data will appear in the result area
5. Use "Copy Revealed Data" to copy it to clipboard

#### Status & Info Tab
- View connection status to CRDP service
- View available protection policies
- Check API health
- Review usage documentation

## API Integration

The application integrates with CRDP API endpoints:

### Protect Endpoint
- **URL**: `POST /v1/protect`
- **Payload**:
  ```json
  {
    "protection_policy_name": "policy_name",
    "data": "data_to_protect",
    "user_name": "optional_username"
  }
  ```

### Unprotect Endpoint
- **URL**: `POST /v1/unprotect`
- **Payload**:
  ```json
  {
    "protected_data": "encrypted_data",
    "user_name": "optional_username"
  }
  ```

## Architecture

### CRDPClient Class
Handles all API communication with the CRDP service:
- `protect()`: Encrypts data using specified policy
- `unprotect()`: Decrypts protected data
- `get_policies()`: Retrieves available policies

### CRDPApplication Class
Main GUI application with three tabs:
1. **Protect Data**: Encryption UI
2. **Reveal Data**: Decryption UI with display options
3. **Status & Info**: Connection status and documentation

## Configuration

The application uses a `config.json` file to manage all configuration. This keeps sensitive information separate from the source code.

### Configuration File Structure

```json
{
  "crdp": {
    "url": "http://192.168.0.18:32085",
    "timeout": 10,
    "ssl_verify": false,
    "default_policy": "default"
  },
  "ciphertrust": {
    "url": "http://192.168.0.23",
    "port": 5696
  },
  "ui": {
    "window_width": 800,
    "window_height": 700
  }
}
```

### Setup Configuration

1. **Create from template**:
   ```bash
   cp config.template.json config.json
   ```

2. **Edit config.json** with your environment details:
   - `crdp.url`: CRDP service endpoint
   - `crdp.timeout`: Request timeout in seconds
   - `ciphertrust.url`: CipherTrust Manager address
   - `ui.window_width/height`: Application window size

3. **Security notes**:
   - Keep `config.json` in `.gitignore` to prevent accidental commits
   - Don't store credentials in config (use environment variables if needed)
   - SSL verification can be enabled for production (`ssl_verify: true`)

### Dynamic Configuration

If `config.json` is not found, the application uses sensible defaults with localhost:

```python
CRDPClient will default to: http://localhost:32085
```

This allows the application to run even without configuration, but you **must** provide `config.json` with actual service URLs for production use.

## Notes

- **No Sensitive Data in Source Code**: All IPs, URLs, and ports are stored in `config.json`, not in the application code
- **Configuration Management**: Use `ConfigManager` class to load settings from configuration file
- **SSL verification** is disabled by default for internal services. For production, enable it in config.json (`ssl_verify: true`)
- **Protected data** can be quite long. Use the scrolled text widgets for large data
- **Username field** is optional but recommended for audit trailing
- **Masked display** is useful for security-sensitive environments where you only need to verify data integrity

## Troubleshooting

### Connection Failed
- Verify CRDP service is running on `192.168.0.18:32085`
- Check network connectivity to the CRDP server
- Review firewall rules

### API Errors
- Check server logs for detailed error messages
- Verify protection policy name exists
- Ensure data format is supported by the policy

### No Policies Available
- Verify CipherTrust Manager on `192.168.0.23` is configured correctly
- Check that policies are defined in CipherTrust Manager
- Review CRDP service configuration

## Support

For issues with CRDP API, refer to the official documentation:
https://docs-cybersec.thalesgroup.com/bundle/latest-cdsp-crdp/page/crdp-apis/index.html

## License

Internal use only - Thales Group
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
