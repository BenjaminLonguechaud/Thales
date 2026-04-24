# Data Protection with CRDP - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Network access to CRDP service (configured in config.json)
- Network access to CipherTrust Manager (configured in config.json)

## Setup

### 1. Configure Your Environment
Create `config.json` with your environment details. Start from config.template.json:
```json
{
  "crdp": {
    "url": "http://crdp-ip:32085",             // CRDP API endpoint
    "timeout": 10,                             // Request timeout (seconds)
    "ssl_verify": false,                       // SSL verification
  },
  "ciphertrust": {
    "url": "http://ciphertrust-ip",            // CipherTrust Manager
    "username": "ciphertrust-username",        // CipherTrust admin username
    "password": "ciphertrust-password"         // CipherTrust admin passwrd
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

### Reveal Protected Data

1. **Go to "Reveal Data" Tab**

2. **Paste Protected Data**
   - Click in the "Protected Data" text area
   - Paste the encrypted data (Ctrl+V or right-click > Paste)

3. **Enter User Name**
   - Data will be revealed according to Policy and Username as defined in CipherTrust Manager.

4. **Reveal the Data**
   - Click the "Reveal Data" button
   - The revealed data appears in the result area

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
  2. Check data format is correct
  3. Review CRDP service logs

## Security Best Practices

1. **Keep IPs Out of Code**: All network addresses in `config.json`, never in source
2. **Enable SSL for Production**: Set `ssl_verify: true` in production
3. **Monitor Logs**: Regularly review audit logs in CipherTrust Manager

## Support and Documentation

- **CRDP API**: https://docs-cybersec.thalesgroup.com/bundle/latest-cdsp-crdp/page/crdp-apis/index.html
- **CipherTrust Manager**: https://docs-cybersec.thalesgroup.com/bundle/latest-cdsp-cm/page/admin/cm_admin/index.html
