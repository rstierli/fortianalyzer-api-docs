# Add Report Schedule with Source IP Filter

Create a scheduled report with source IP address filtering.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report schedules with source IP filters - useful for department-specific or network segment reporting.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/schedule/{layout_id}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "update",
    "params": [{
        "url": "/config/adom/root/sql-report/schedule/123456",
        "data": {
            "schedule-name": "IP_Filtered_Report",
            "schedule-type": "daily",
            "time": "08:00",
            "filter": {
                "srcip": "10.0.1.0/24"
            }
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

def add_schedule_with_srcip_filter(session_id, layout_id, schedule_name, srcip_filter, adom="root"):
    """Create report schedule with source IP filter"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "update",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/schedule/{layout_id}",
            "data": {
                "schedule-name": schedule_name,
                "schedule-type": "daily",
                "time": "08:00",
                "filter": {
                    "srcip": srcip_filter
                }
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print(f"✓ IP-filtered schedule '{schedule_name}' created")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_schedule_with_srcip_filter(
    session_id="your_session_id",
    layout_id=123456,
    schedule_name="Marketing_Dept_Report",
    srcip_filter="10.0.100.0/24"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
