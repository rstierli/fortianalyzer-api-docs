# Get Specific Report Layout

Retrieve a specific report layout by ID (example: Daily Summary).

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves a specific report layout by ID - useful for examining layout details and configuration.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/layout/{layout_id}`
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
        "url": "/config/adom/root/sql-report/layout/123456"
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
            "layout-id": 123456,
            "title": "Daily Summary Report",
            "description": "Daily traffic and security summary",
            "section": [...]
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

def get_report_layout_by_id(session_id, layout_id, adom="root"):
    """Get specific report layout by ID"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/layout/{layout_id}"
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
layout = get_report_layout_by_id(session_id="your_session_id", layout_id=123456)
print(f"Layout: {layout['title']}")
print(f"Description: {layout.get('description', 'N/A')}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
