# Get Report Schedules

Retrieve configured report schedules from FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves scheduled report configurations - useful for auditing automated report generation settings.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/schedule`
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
        "url": "/config/adom/root/sql-report/schedule"
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
                "id": 1,
                "layout-id": 123456,
                "schedule-name": "Daily_Traffic_Report",
                "schedule-type": "daily",
                "time": "08:00"
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

def get_report_schedules(session_id, adom="root"):
    """Get configured report schedules"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/schedule"
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
schedules = get_report_schedules(session_id="your_session_id")
for schedule in schedules:
    print(f"Schedule: {schedule['schedule-name']}")
    print(f"  Type: {schedule['schedule-type']}")
    print(f"  Time: {schedule.get('time', 'N/A')}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
