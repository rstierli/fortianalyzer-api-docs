# Get Session ID

Obtain session ID for FortiAnalyzer API authentication.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint establishes authenticated session for FortiAnalyzer API - required for all subsequent API operations.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/login/user`
**ADOM Support:** No
**Requires Authentication:** No (this is the authentication endpoint)
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/login/user",
        "data": {
            "user": "admin",
            "passwd": "your_password"
        }
    }],
    "session": null,
    "id": 1
}
```
````
````{tab-item} RESPONSE
```json
{
    "result": [{
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/sys/login/user"
    }],
    "session": "AbCdEfGhIjKlMnOpQrStUvWxYz123456",
    "id": 1
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session_id(faz_host, username, password):
    """Get FortiAnalyzer session ID"""
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
        print(f"✓ Session established: {session_id[:20]}...")
        return session_id
    else:
        raise Exception(f"Login failed: {result['result'][0]['status']['message']}")

# Example
session_id = get_session_id(
    faz_host="faz.example.com",
    username="admin",
    password="your_password"
)
```

> **🔒 Security Note:** Always use HTTPS and secure credential storage. Consider using API keys instead of passwords for automation.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
