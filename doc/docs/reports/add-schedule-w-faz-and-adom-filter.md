# Add Report Schedule with FAZ and ADOM Filter

Create a scheduled report with FortiAnalyzer and ADOM filtering.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report schedules with FAZ and ADOM filters - useful for multi-tenant or multi-device report automation.

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
            "schedule-name": "Filtered_Report",
            "schedule-type": "daily",
            "time": "08:00",
            "filter": {
                "faz-filter": "FAZ-01",
                "adom-filter": "branch-adom"
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

def add_schedule_with_filters(session_id, layout_id, schedule_name, faz_filter=None, 
                               adom_filter=None, adom="root"):
    """Create report schedule with FAZ/ADOM filters"""
    url = "https://faz.example.com/jsonrpc"
    
    data = {
        "schedule-name": schedule_name,
        "schedule-type": "daily",
        "time": "08:00",
        "filter": {}
    }
    
    if faz_filter:
        data["filter"]["faz-filter"] = faz_filter
    if adom_filter:
        data["filter"]["adom-filter"] = adom_filter
    
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
        print(f"✓ Filtered schedule '{schedule_name}' created")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_schedule_with_filters(
    session_id="your_session_id",
    layout_id=123456,
    schedule_name="Branch_Report",
    faz_filter="FAZ-Branch-01",
    adom_filter="branch-offices"
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
