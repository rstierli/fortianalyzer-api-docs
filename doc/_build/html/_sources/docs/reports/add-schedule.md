# Add Report Schedule

Create a scheduled report generation task.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report schedules - useful for automating regular report generation and distribution.

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
            "schedule-name": "Daily_Traffic_Report",
            "schedule-type": "daily",
            "time": "08:00",
            "output-format": "pdf",
            "email-recipients": ["admin@example.com"]
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

def add_report_schedule(session_id, layout_id, schedule_name, schedule_type="daily", 
                        time="08:00", email=None, adom="root"):
    """Create report schedule"""
    url = "https://faz.example.com/jsonrpc"
    
    data = {
        "schedule-name": schedule_name,
        "schedule-type": schedule_type,
        "time": time,
        "output-format": "pdf"
    }
    
    if email:
        data["email-recipients"] = [email] if isinstance(email, str) else email
    
    payload = {
        "method": "update",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/schedule/{layout_id}",
            "data": data
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Report schedule '{schedule_name}' created")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_report_schedule(
    session_id="your_session_id",
    layout_id=123456,
    schedule_name="Daily_Traffic_Report",
    schedule_type="daily",
    time="08:00",
    email="admin@example.com"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
