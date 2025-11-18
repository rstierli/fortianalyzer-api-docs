# Get System Status

Retrieve FortiAnalyzer system status and health information.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves system status - useful for monitoring, health checks, and operations management.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/status`
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
        "url": "/sys/status"
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
        "data": {
            "version": "v7.6.4",
            "serial": "FAZ-VM0123456789",
            "hostname": "FortiAnalyzer-01"
        },
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

def get_system_status(session_id):
    """Get system status"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{"url": "/sys/status"}],
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
status = get_system_status(session_id="your_session_id")
print(f"Version: {status['version']}")
print(f"Serial: {status['serial']}")
print(f"Hostname: {status['hostname']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
