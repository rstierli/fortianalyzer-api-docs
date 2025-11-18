# Download Report

Download a generated report file.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint downloads generated reports - useful for retrieving completed reports for distribution or archival.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/reports/{report_id}`
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
        "url": "/report/adom/root/reports/12345"
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

def download_report(session_id, report_id, output_file, adom="root"):
    """Download generated report"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/report/adom/{adom}/reports/{report_id}"
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        # Decode and save report
        report_data = result['result'][0]['data'].get('file', '')
        file_content = base64.b64decode(report_data)
        
        with open(output_file, 'wb') as f:
            f.write(file_content)
        
        print(f"✓ Report downloaded to {output_file}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
download_report(
    session_id="your_session_id",
    report_id=12345,
    output_file="./daily_report.pdf"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
