# Export Report Layout

Export a report layout configuration to file.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint exports report layout configurations - useful for backup, migration, or sharing custom reports.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/layout/export`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/report/adom/root/layout/export",
        "data": {
            "layout-id": 123456
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
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def export_report_layout(session_id, layout_id, output_file, adom="root"):
    """Export report layout to file"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "exec",
        "params": [{
            "url": f"/report/adom/{adom}/layout/export",
            "data": {
                "layout-id": layout_id
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        # Decode and save exported data
        exported_data = result['result'][0]['data'].get('file', '')
        file_content = base64.b64decode(exported_data)
        
        with open(output_file, 'wb') as f:
            f.write(file_content)
        
        print(f"✓ Layout exported to {output_file}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
export_report_layout(
    session_id="your_session_id",
    layout_id=123456,
    output_file="./exported_layout.dat"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
