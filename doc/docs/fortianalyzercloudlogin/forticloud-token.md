# FortiCloud Token Authentication

Authenticate using FortiCloud token for cloud-managed FortiAnalyzer instances.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint enables FortiCloud token-based authentication - useful for SaaS FortiAnalyzer instances and cloud integrations.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/login/cloud`
**ADOM Support:** No
**Requires Authentication:** No (token-based authentication)
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/login/cloud",
        "data": {
            "token": "your_forticloud_token"
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
        }
    }],
    "session": "CloudSessionIdHere123456",
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

def forticloud_token_login(faz_host, forticloud_token):
    """Authenticate with FortiCloud token"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/cloud",
            "data": {
                "token": forticloud_token
            }
        }],
        "session": None,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        session_id = result['session']
        print(f"✓ FortiCloud session established")
        return session_id
    else:
        raise Exception(f"FortiCloud login failed: {result['result'][0]['status']['message']}")

# Example
session_id = forticloud_token_login(
    faz_host="faz-cloud.fortinet.com",
    forticloud_token="your_forticloud_token"
)
```

> **☁️ Use Case:** Required for FortiAnalyzer Cloud instances and FortiCloud-managed deployments.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
