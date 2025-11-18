# Run Report from GUI

Generate a report using GUI-initiated parameters.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint generates reports with GUI-style parameters - useful for programmatically triggering reports configured in the GUI.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/report/adom/{adom}/run`
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
        "url": "/report/adom/root/run",
        "runfrom": "GUI",
        "schedule-param": {
            "device": "all",
            "time-period": "last-30-days",
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_report_from_gui(session_id, layout_id, device="all", time_period="last-7-days", adom="root"):
    """Run report with GUI parameters"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/report/adom/{adom}/run",
            "runfrom": "GUI",
            "schedule-param": {
                "device": device,
                "time-period": time_period,
                "layout-id": layout_id
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        tid = result['result'][0]['data'].get('tid')
        print(f"✓ GUI report generation started. Task ID: {tid}")
        return tid
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
tid = run_report_from_gui(
    session_id="your_session_id",
    layout_id=123456,
    device="FGT-Branch-01",
    time_period="last-24-hours"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
