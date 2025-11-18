# Add Fabric of FortiAnalyzer Group with Members

Create FAZ fabric group and add member FortiAnalyzer units.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates FAZ fabric groups with member assignments for distributed log collection topology.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/csf/fabric-connector`
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
        "url": "/cli/global/system/csf/fabric-connector",
        "data": {
            "serial": "FAZVM1234567890",
            "status": "enable"
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

def add_faz_fabric_member(session_id, serial):
    """Add member to FAZ fabric"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": "/cli/global/system/csf/fabric-connector",
            "data": {
                "serial": serial,
                "status": "enable"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Added FAZ member: {serial}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_faz_fabric_member(session_id="your_session_id", serial="FAZVM1234567890")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
