# Add Report Folder (FortiAnalyzer 6.4)

Create a new report folder for organization (FortiAnalyzer 6.4 format).

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report folders using FortiAnalyzer 6.4 API format - useful for organizing reports in hierarchical folder structures on older systems.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/folders`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 6.4.0

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
            "parent-id": 0
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

def add_report_folder_v64(session_id, folder_name, parent_id=0, adom="root"):
    """Create report folder (v6.4 format)"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/report/adom/{adom}/folders",
            "data": {
                "name": folder_name,
                "parent-id": parent_id
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
folder_id = add_report_folder_v64(
    session_id="your_session_id",
    folder_name="Branch_Reports",
    parent_id=0
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 6.4.0+
