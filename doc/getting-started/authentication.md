# Authentication

Complete guide to FortiAnalyzer API authentication methods.

## Overview

FortiAnalyzer API supports two authentication methods:
1. **Session-Based** - Username/password authentication with session management
2. **API Key** - Token-based authentication for automation

## Session-Based Authentication

### Overview
- Best for: Interactive applications, scripts with defined lifecycle
- Advantages: Simple, no pre-configuration needed
- Disadvantages: Requires session management, expires after inactivity

### Login Process

**Endpoint**: `/sys/login/user`

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login(faz_host, username, password):
    """Authenticate and get session ID"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/user",
            "data": {
                "user": username,
                "passwd": password
            }
        }],
        "session": None,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        session_id = result['session']
        print(f"✓ Logged in successfully")
        return session_id
    else:
        raise Exception(f"Login failed: {result['result'][0]['status']['message']}")

# Example usage
session_id = login("faz.example.com", "admin", "your_password")
```

### Using Session ID

Include the session ID in all subsequent requests:

```python
def get_system_status(session_id, faz_host):
    """Example API call with session"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{"url": "/sys/status"}],
        "session": session_id,  # ← Session ID here
        "id": 2
    }
    
    response = requests.post(url, json=payload, verify=False)
    return response.json()['result'][0]['data']
```

### Logout

**Always logout** when done to free server resources:

**Endpoint**: `/sys/logout`

```python
def logout(session_id, faz_host):
    """Terminate session"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{"url": "/sys/logout"}],
        "session": session_id,
        "id": 999
    }
    
    requests.post(url, json=payload, verify=False)
    print("✓ Logged out successfully")

# Always use try/finally to ensure logout
session_id = None
try:
    session_id = login("faz.example.com", "admin", "password")
    # ... your API operations ...
finally:
    if session_id:
        logout(session_id, "faz.example.com")
```

### Session Expiration

Sessions expire after **15 minutes of inactivity** (default). Handle expiration gracefully:

```python
def api_call_with_retry(session_id, faz_host):
    """API call with automatic re-authentication on timeout"""
    try:
        return get_system_status(session_id, faz_host)
    except Exception as e:
        if "Session timeout" in str(e) or "code: -10" in str(e):
            # Re-authenticate
            session_id = login(faz_host, "admin", "password")
            return get_system_status(session_id, faz_host)
        raise
```

## API Key Authentication

### Overview
- Best for: Long-running services, automation, CI/CD pipelines
- Advantages: No session management, doesn't expire
- Disadvantages: Requires API user setup in FortiAnalyzer

### Setup API Key (FortiAnalyzer GUI)

1. Navigate to **System Settings > Administrators**
2. Create new administrator or edit existing
3. Enable **REST API Access**
4. Generate API Key
5. Copy and securely store the key

### Using API Key

Include API key in `Authorization` header:

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def api_call_with_key(faz_host, api_key):
    """API call using API key authentication"""
    url = f"https://{faz_host}/jsonrpc"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "method": "get",
        "params": [{"url": "/sys/status"}],
        "session": None,  # ← Set to None when using API key
        "id": 1
    }
    
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response.json()

# Example usage
API_KEY = "your_api_key_here"
result = api_call_with_key("faz.example.com", API_KEY)
```

### API Key Best Practices

> **🔒 Security Best Practices:**
> - Store API keys in environment variables or secrets manager
> - Never commit API keys to version control
> - Rotate API keys regularly (every 90 days recommended)
> - Use dedicated API users with minimal required permissions
> - Monitor API key usage for anomalies

```python
import os

# Load from environment variable
API_KEY = os.getenv('FAZ_API_KEY')
if not API_KEY:
    raise ValueError("FAZ_API_KEY environment variable not set")
```

## FortiCloud Token Authentication

For FortiAnalyzer Cloud instances:

**Endpoint**: `/sys/login/cloud`

```python
def forticloud_login(faz_host, forticloud_token):
    """Authenticate with FortiCloud token"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/cloud",
            "data": {"token": forticloud_token}
        }],
        "session": None,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    session_id = response.json()['session']
    return session_id
```

**See also**: [FortiCloud Authentication](../docs/fortianalyzercloudlogin/forticloud-token.md)

## Comparison

| Feature | Session-Based | API Key |
|---------|--------------|---------|
| **Setup** | None required | Requires FortiAnalyzer configuration |
| **Expiration** | 15 min inactivity | Never expires |
| **Session Management** | Required (login/logout) | None needed |
| **Best For** | Interactive use, scripts | Automation, services |
| **Security** | Username/password | Token-based |
| **Rotation** | Password changes | Manual key rotation |

## Configuration File Pattern

Store credentials securely in a configuration file:

**`.faz-env.json`** (add to `.gitignore`):
```json
{
    "faz_host": "faz.example.com",
    "faz_port": "443",
    "auth_method": "apikey",
    "api_key": "your_api_key_here",
    "username": "admin",
    "password": "backup_password",
    "adom": "root"
}
```

**Load configuration**:
```python
import json

def load_config(config_file='.faz-env.json'):
    """Load FortiAnalyzer configuration"""
    with open(config_file, 'r') as f:
        return json.load(f)

config = load_config()

if config['auth_method'] == 'apikey':
    # Use API key
    result = api_call_with_key(config['faz_host'], config['api_key'])
else:
    # Use session-based
    session_id = login(config['faz_host'], config['username'], config['password'])
    # ... API calls ...
    logout(session_id, config['faz_host'])
```

## Troubleshooting

### Error: Session Timeout (Code -10)

**Symptom:**
```json
{
    "result": [{
        "status": {
            "code": -10,
            "message": "Session timeout"
        }
    }]
}
```

**Solutions:**
- Re-authenticate and get new session ID
- Implement automatic re-authentication
- Consider using API key authentication instead

### Error: Invalid Credentials

**Symptom:**
```json
{
    "result": [{
        "status": {
            "code": -11,
            "message": "Permission denied"
        }
    }]
}
```

**Solutions:**
- Verify username and password
- Check user account status (not locked/disabled)
- Verify user has API access permissions
- Check ADOM access rights

### Error: API Key Not Working

**Solutions:**
- Verify API key is enabled for the user
- Check Authorization header format: `Bearer <key>`
- Ensure REST API access is enabled
- Try regenerating the API key

---

**Related Documentation:**
- [FortiCloud Login](../docs/fortianalyzercloudlogin/get-session-id.md)
- [System Admin Users](../docs/system-settings/get-admin-users.md)
