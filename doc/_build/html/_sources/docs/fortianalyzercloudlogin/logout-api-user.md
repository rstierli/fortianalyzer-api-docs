# Logout API User

Terminate active FortiAnalyzer API session.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint terminates API sessions - best practice for freeing server resources and security compliance.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/logout`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/logout"
    }],
    "session": "{{session_id}}",
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
        }
    }],
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

def logout_api_user(session_id):
    """Logout and terminate API session"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/logout"
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print("✓ Session terminated")
        return True
    else:
        raise Exception(f"Logout failed: {result['result'][0]['status']['message']}")

# Example - Always logout when done
try:
    # ... API operations ...
    pass
finally:
    logout_api_user(session_id="your_session_id")
```

> **✅ Best Practice:** Always logout when API operations complete to free server resources.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
