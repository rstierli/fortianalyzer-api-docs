# FortiCloud Token ZTP Authentication

Authenticate using FortiCloud Zero Touch Provisioning (ZTP) token.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint supports FortiCloud ZTP authentication - useful for automated provisioning and cloud-managed deployments.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/login/cloud/ztp`
**ADOM Support:** No
**Requires Authentication:** No (ZTP token-based)
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/login/cloud/ztp",
        "data": {
            "token": "your_ztp_token",
            "serial": "FAZVM1234567890"
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
    "session": "ZtpSessionId123456",
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

def forticloud_ztp_login(faz_host, ztp_token, serial_number):
    """Authenticate with FortiCloud ZTP token"""
    url = f"https://{faz_host}/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/cloud/ztp",
            "data": {
                "token": ztp_token,
                "serial": serial_number
            }
        }],
        "session": None,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        session_id = result['session']
        print(f"✓ ZTP session established for {serial_number}")
        return session_id
    else:
        raise Exception(f"ZTP login failed: {result['result'][0]['status']['message']}")

# Example
session_id = forticloud_ztp_login(
    faz_host="faz-cloud.fortinet.com",
    ztp_token="your_ztp_token",
    serial_number="FAZVM1234567890"
)
```

> **🔧 Automation:** Designed for zero-touch provisioning workflows and automated cloud deployments.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
