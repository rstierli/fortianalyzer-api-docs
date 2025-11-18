# Add Report Folder (FortiAnalyzer 7.0)

Create a new report folder for organization (FortiAnalyzer 7.0+ format).

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report folders using FortiAnalyzer 7.0+ API format - useful for organizing reports in hierarchical folder structures.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/folders`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/report/adom/root/folders",
        "data": {
            "name": "New_Report_Folder",
            "parent-folder-id": 0,
            "description": "Folder for organizing reports"
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

def add_report_folder_v70(session_id, folder_name, parent_id=0, description="", adom="root"):
    """Create report folder (v7.0+ format)"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/report/adom/{adom}/folders",
            "data": {
                "name": folder_name,
                "parent-folder-id": parent_id,
                "description": description
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        folder_id = result['result'][0]['data'].get('folder-id')
        print(f"✓ Folder '{folder_name}' created (ID: {folder_id})")
        return folder_id
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
folder_id = add_report_folder_v70(
    session_id="your_session_id",
    folder_name="Security_Reports",
    parent_id=0,
    description="Security and compliance reports"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.0.0+
