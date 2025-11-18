# Get Managed Device Information

Retrieve information from devices managed by FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves managed device details - useful for inventory management, device monitoring, and configuration auditing.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/device`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom/root/device"
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
                "name": "FGT-01",
                "sn": "FG100FTK00000001",
                "ip": "10.0.1.10",
                "os_ver": "7.4.5"
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

def get_managed_devices(session_id, adom="root"):
    """Get managed device information"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{"url": f"/dvmdb/adom/{adom}/device"}],
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
devices = get_managed_devices(session_id="your_session_id")
for device in devices:
    print(f"Device: {device['name']} ({device['sn']})")
    print(f"  IP: {device['ip']}")
    print(f"  Version: {device['os_ver']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
