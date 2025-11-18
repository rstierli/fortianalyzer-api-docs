# Get Report Folders

Retrieve report folder structure and organization.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves report folder hierarchy - useful for understanding report organization and folder structure.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/folders`
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
        "url": "/report/adom/root/folders"
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
                "folder-id": 1,
                "name": "Executive_Reports",
                "parent-id": 0
            },
            {
                "folder-id": 2,
                "name": "Daily_Reports",
                "parent-id": 0
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

def get_report_folders(session_id, adom="root"):
    """Get report folder structure"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/report/adom/{adom}/folders"
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
folders = get_report_folders(session_id="your_session_id")
for folder in folders:
    print(f"Folder: {folder['name']} (ID: {folder['folder-id']})")
    print(f"  Parent ID: {folder.get('parent-id', 'Root')}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
