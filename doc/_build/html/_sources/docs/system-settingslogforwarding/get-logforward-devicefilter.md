# Get Log Forward Device Filter

Retrieve device filters configured for log forwarding rules.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint lists device filters applied to log forwarding - useful for selective log forwarding based on device groups or specific FortiGates.

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
    "method": "get",
    "params": [{
        "url": "/cli/global/system/log-forward/1/device-filter"
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
                "id": 1,
                "device": "FGT-Branch-01",
                "adom": "root"
            },
            {
                "id": 2,
                "device": "FGT-Branch-02",
                "adom": "root"
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

def get_logforward_device_filters(session_id, forward_id):
    """Get device filters for log forwarding rule"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/cli/global/system/log-forward/{forward_id}/device-filter"
        }],
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
filters = get_logforward_device_filters(session_id="your_session_id", forward_id=1)
for filt in filters:
    print(f"Device Filter: {filt['device']} (ADOM: {filt['adom']})")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
