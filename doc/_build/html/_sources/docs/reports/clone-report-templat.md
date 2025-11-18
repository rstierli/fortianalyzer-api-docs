# Clone Report Template

Clone an existing report template to create a new customizable copy.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint clones report templates - useful for creating custom reports based on existing templates.

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
    "method": "clone",
    "params": [{
        "url": "/config/adom/root/sql-report/layout/1000060042",
        "data": {
            "title": "Cloned Custom Report",
            "description": "Custom version of original report"
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

def clone_report_template(session_id, layout_id, new_title, new_description="", adom="root"):
    """Clone existing report template"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "clone",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/layout/{layout_id}",
            "data": {
                "title": new_title,
                "description": new_description
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        new_layout_id = result['result'][0]['data'].get('layout-id')
        print(f"✓ Template cloned successfully. New layout ID: {new_layout_id}")
        return new_layout_id
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
new_id = clone_report_template(
    session_id="your_session_id",
    layout_id=1000060042,
    new_title="Custom Traffic Report",
    new_description="Modified version for branch offices"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
