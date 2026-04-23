# CRDP Data Protection Manager - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Network access to CRDP service (configured in config.json)
- Network access to CipherTrust Manager (configured in config.json)

## Setup

### 1. Configure Your Environment
Create `config.json` with your environment details:
```json
{
  "crdp": {
    "url": "http://your-crdp-host:32085",      // CRDP API endpoint
    "timeout": 10,                             // Request timeout (seconds)
    "ssl_verify": false,                       // SSL verification
  },
  "ciphertrust": {
    "url": "http://cm-manager",                // CipherTrust Manager
    "username": "admin",                       // CipherTrust admin username
    "password": "password"                     // CipherTrust admin passwrd
  },
  "ui": {
    "window_width": 800,                       // Application window width
    "window_height": 700                       // Application window height
  },
  "logging": {
    "level": "INFO",
    "file": "crdp_app.log",
    "max_size": 10485760,
    "backup_count": 5
  }
}
```

**Security Note**: `config.json` is in `.gitignore` and won't be committed to version control, protecting your sensitive configuration.

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python main.py
```

## First Steps

### Protect Data

1. **Open the Application**
   - The main window opens with three tabs

2. **Go to "Protect Data" Tab**
   - You'll see input fields for data entry

3. **Enter Your Data**
   - Click in the "Data to Protect" text area
   - Type or paste the data you want to protect (e.g., credit card number: 4111111111111111)

4. **Select Protection Policy**
   - Click the "Protection Policy" dropdown
   - Select a policy
   - If no policies appear, check the "Status & Info" tab for connection issues

5. **Protect the Data**
   - Click the "Protect Data" button
   - Wait for processing (usually 1-2 seconds)
   - The encrypted/protected data appears in the result area
   - You'll see a "Success" message

7. **Copy Protected Data**
   - Click "Copy Protected Data" to copy it to your clipboard
   - You can now use this protected data in other applications

### Reveal Protected Data

1. **Go to "Reveal Data" Tab**

2. **Paste Protected Data**
   - Click in the "Protected Data" text area
   - Paste the encrypted data (Ctrl+V or right-click > Paste)

3. **Select Display Format**
   - **Clear Text**: Shows the full decrypted value
   - **Masked**: Shows asterisks with only the last 4 characters visible (security mode)
   - For example: `4111111111111111` becomes `************1111`

4. **Reveal the Data**
   - Click the "Reveal Data" button
   - Wait for processing
   - The original data appears in the result area

5. **Copy if Needed**
   - Click "Copy Revealed Data" to copy to clipboard

## Monitoring Connection Status

1. **Go to "Status & Info" Tab**
2. **View Connection Status**
   - Shows if CRDP service is reachable
   - Lists available protection policies
   - Displays connection errors (if any)

3. **Refresh Status**
   - Click "Refresh Status" button to update connection information
   - Useful if you've restarted services

## Troubleshooting

### "Connection Failed" Error
- **Problem**: Cannot reach CRDP service
- **Solution**:
  1. Check `config.json` has correct CRDP URL
  2. Verify service is running: `ping <crdp_ip>`
  3. Check if port is open: `ping <crdp_ip> -p <crdp_port>`
  4. Verify network connectivity to the CRDP server

### "No Policies Available"
- **Problem**: Dropdown shows no policies
- **Solution**:
  1. Check CipherTrust Manager (from config.json) is running
  2. Verify policies are configured in CipherTrust Manager
  3. Go to Status & Info tab and click "Refresh Status"
  4. Check `config.json` URLs are correct

### "Failed to Protect Data" Error
- **Problem**: Protect operation fails
- **Solution**:
  1. Verify selected policy exists in CipherTrust Manager
  2. Check data format is correct (must be string)
  3. Review CRDP service logs
  4. Try using default policy from config.json

### Application Won't Start
- **Problem**: Python error on launch or Config error
- **Solution**:
  1. Verify Python version: `python --version` (should be 3.8+)
  2. Install dependencies: `pip install -r requirements.txt`
  3. Check `config.json` exists and has valid JSON format
  4. Check tkinter: `python -c "import tkinter; print(tkinter.TkVersion)"`
  5. Review error message in console

## Security Best Practices

1. **Keep IPs Out of Code**: All network addresses in `config.json`, never in source
2. **Protect config.json**: File is in `.gitignore` - don't commit it
3. **Enable SSL for Production**: Set `ssl_verify: true` in production
4. **Use Strong Policies**: Select high_security policy for sensitive data
5. **Enable Audit Logging**: Always provide username for tracking
6. **Mask in Shared Screens**: Use masked display when sharing screens
7. **Monitor Logs**: Regularly review audit logs in CipherTrust Manager

## Support and Documentation

- **CRDP API**: https://docs-cybersec.thalesgroup.com/bundle/latest-cdsp-crdp/page/crdp-apis/index.html
- **CipherTrust Manager**: https://docs-cybersec.thalesgroup.com/bundle/csp-cm9.x/page/ccm-admin/index.html
- **README.md**: Full feature documentation
- **Status & Info Tab**: In-app help and connection status
