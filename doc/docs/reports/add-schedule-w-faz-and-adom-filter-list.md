# Add Report Schedule with FAZ and ADOM Filter List

Create a scheduled report with multiple FAZ and ADOM filters.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates report schedules with multiple filter criteria - useful for complex multi-tenant reporting scenarios.

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
            "schedule-name": "Multi_Filter_Report",
            "schedule-type": "daily",
            "time": "08:00",
            "filter": {
                "faz-filter-list": ["FAZ-01", "FAZ-02"],
                "adom-filter-list": ["adom1", "adom2"]
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

def add_schedule_with_filter_lists(session_id, layout_id, schedule_name, 
                                    faz_list=None, adom_list=None, adom="root"):
    """Create report schedule with multiple filters"""
    url = "https://faz.example.com/jsonrpc"
    
    data = {
        "schedule-name": schedule_name,
        "schedule-type": "daily",
        "time": "08:00",
        "filter": {}
    }
    
    if faz_list:
        data["filter"]["faz-filter-list"] = faz_list
    if adom_list:
        data["filter"]["adom-filter-list"] = adom_list
    
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
        print(f"✓ Multi-filter schedule '{schedule_name}' created")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_schedule_with_filter_lists(
    session_id="your_session_id",
    layout_id=123456,
    schedule_name="Consolidated_Report",
    faz_list=["FAZ-HQ", "FAZ-Branch-01", "FAZ-Branch-02"],
    adom_list=["headquarters", "branches"]
)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
