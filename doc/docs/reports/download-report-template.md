# Download Report Template

Download a report template file for backup or sharing.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint downloads report templates - useful for backup, migration, or sharing templates between FortiAnalyzer instances.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/template/export`
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
        "url": "/report/adom/root/template/export",
        "data": {
            "template-name": "Daily_Traffic_Report"
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

def download_report_template(session_id, template_name, output_file, adom="root"):
    """Download report template"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/report/adom/{adom}/template/export",
            "data": {
                "template-name": template_name
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        # Decode and save template
        template_data = result['result'][0]['data'].get('file', '')
        file_content = base64.b64decode(template_data)
        
        with open(output_file, 'wb') as f:
            f.write(file_content)
        
        print(f"✓ Template downloaded to {output_file}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
download_report_template(
    session_id="your_session_id",
    template_name="Daily_Traffic_Report",
    output_file="./template_backup.dat"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
