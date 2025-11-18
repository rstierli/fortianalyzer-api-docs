# Get Report Layouts

Retrieve report layout configurations from FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves report layouts - useful for listing configured report structures and customizations.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/layout`
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
        "url": "/config/adom/root/sql-report/layout"
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
                "layout-id": 123456,
                "title": "Daily Traffic Summary",
                "description": "Network traffic report"
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

def get_report_layouts(session_id, adom="root"):
    """Get report layouts"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/layout"
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
layouts = get_report_layouts(session_id="your_session_id")
for layout in layouts:
    print(f"Layout ID: {layout['layout-id']}")
    print(f"  Title: {layout['title']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
