# Get Admin Users

Retrieve list of administrative users configured on FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves admin user accounts - useful for user management, auditing, and access control.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/admin/user`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/admin/user"
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
        "data": [
            {
                "userid": "admin",
                "profileid": "Super_User",
                "user_type": "local"
            }
        ],
        "status": {
            "code": 0,
            "message": "OK"
        }
    }]
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_admin_users(session_id):
    """Get admin users"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{"url": "/cli/global/system/admin/user"}],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
users = get_admin_users(session_id="your_session_id")
for user in users:
    print(f"User: {user['userid']} - Profile: {user['profileid']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
