# Import Report

Import a report configuration file into FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint imports report configurations from file - useful for migrating reports between FortiAnalyzer instances or restoring backups.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/config-file/import`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/report/adom/root/config-file/import",
        "data": {
            "file": "base64_encoded_file_content",
            "filename": "report_config.dat"
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

def import_report(session_id, file_path, adom="root"):
    """Import report configuration from file"""
    url = "https://faz.example.com/jsonrpc"
    
    # Read and encode file
    with open(file_path, 'rb') as f:
        file_content = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/report/adom/{adom}/config-file/import",
            "data": {
                "file": file_content,
                "filename": file_path.split('/')[-1]
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print("✓ Report imported successfully")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
import_report(session_id="your_session_id", file_path="./report_config.dat")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
