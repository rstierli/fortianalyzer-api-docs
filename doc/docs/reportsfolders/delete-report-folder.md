# Delete Report Folder

Delete a report folder and optionally its contents.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint deletes report folders - useful for cleanup and reorganization of report structure.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/folders/{folder_id}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/report/adom/root/folders/5",
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

def delete_report_folder(session_id, folder_id, adom="root"):
    """Delete report folder"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "delete",
        "params": [{
            "url": f"/report/adom/{adom}/folders/{folder_id}",
            "confirm": 1
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Folder {folder_id} deleted")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
delete_report_folder(session_id="your_session_id", folder_id=5)
```

> **⚠️ Warning:** Deleting a folder may also delete all reports within it. Ensure backups exist before deletion.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
