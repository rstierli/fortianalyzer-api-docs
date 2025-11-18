# Add Fabric of FortiAnalyzer Group

Create a Fabric of FortiAnalyzer group for distributed log management.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates FAZ fabric groups - useful for distributed log collection, supervisor-member topologies, and multi-site deployments.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/csf`
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
        "url": "/cli/global/system/csf",
        "data": {
            "name": "FAZ_Fabric_Group",
            "status": "enable"
        }
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

def add_faz_fabric_group(session_id, name):
    """Create FAZ fabric group"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": "/cli/global/system/csf",
            "data": {
                "name": name,
                "status": "enable"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ FAZ fabric group '{name}' created")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_faz_fabric_group(session_id="your_session_id", name="FAZ_Fabric_Group")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
