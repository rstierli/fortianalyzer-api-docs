# Delete Log Forward Device Filter

Remove device filter from log forwarding configuration.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint removes device filters from log forwarding rules - useful for modifying which devices' logs are forwarded to external systems.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/log-forward/{id}/device-filter/{filter_id}`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/cli/global/system/log-forward/1/device-filter/2",
        "confirm": 1
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

def delete_logforward_device_filter(session_id, forward_id, filter_id):
    """Delete device filter from log forwarding rule"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "delete",
        "params": [{
            "url": f"/cli/global/system/log-forward/{forward_id}/device-filter/{filter_id}",
            "confirm": 1
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Device filter {filter_id} deleted")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
delete_logforward_device_filter(
    session_id="your_session_id",
    forward_id=1,
    filter_id=2
)
```

> **⚠️ Warning:** This action cannot be undone. Device logs will no longer be forwarded once filter is removed.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
