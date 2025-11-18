# Add Log Forward Device Filter

Add device filter to log forwarding configuration for selective forwarding.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint adds device-specific filters to log forwarding rules - useful for forwarding logs only from specific FortiGates or device groups to external systems.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/log-forward/{id}/device-filter`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/cli/global/system/log-forward/1/device-filter",
        "data": {
            "device": "FGT-Branch-03",
            "adom": "root"
        }
    }],
    "session": "{{session_id}}",
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

def add_logforward_device_filter(session_id, forward_id, device_name, adom="root"):
    """Add device filter to log forwarding rule"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/cli/global/system/log-forward/{forward_id}/device-filter",
            "data": {
                "device": device_name,
                "adom": adom
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Device filter added: {device_name}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_logforward_device_filter(
    session_id="your_session_id",
    forward_id=1,
    device_name="FGT-Branch-03"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
