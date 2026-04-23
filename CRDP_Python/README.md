# CRDP Data Protection Manager

A user-friendly GUI application for protecting and revealing sensitive data using CipherTrust CRDP (CipherTrust RESTful Data Protection).

## Features

- **Data Protection**: Encrypt sensitive data using CRDP protection policies
- **Data Revelation**: Decrypt protected data with flexible display options
- **Masking Support**: Display decrypted data in clear text or masked format (showing only last 4 characters)
- **Username Tracking**: Username field for audit logging
- **Policy Selection**: Choose from available application protection policies
- **Status Monitoring**: Real-time connection status and API health checks

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
    "data": "data_to_protect"
  }
  ```

### Reveal Endpoint
- **URL**: `POST /v1/reveal`
- **Payload**:
  ```json
  {
    "protected_data": "encrypted_data",
    "protection_policy_name": "policy_name",
    "user_name": "username"
  }
  ```

## Architecture

### CRDPClient Class
Handles all API communication with the CRDP service:
- `protect()`: Encrypts data using specified policy
- `reveal()`: Decrypts protected data
- `load_policies()`: Retrieves available policies

### CRDPApplication Class
Main GUI application with three tabs:
1. **Protect Data**: Encryption UI
2. **Reveal Data**: Decryption UI with display options
3. **Status & Info**: Connection status and documentation

### ConfigManager Class
Load and read `config.json` file to manage all configuration.
Using this file keeps sensitive information separate from the source code.


### Setup Configuration

**Create config.json** with your environment details:
   See Quickstart.md for more details.

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
