# Get Report Charts

Retrieve available chart configurations for reports.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves chart configurations - useful for listing available visualization options for custom reports.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/chart`
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
        "url": "/config/adom/root/sql-report/chart"
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
                "name": "traffic_by_application",
                "chart-type": "pie",
                "sql-query": "SELECT ..."
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

def get_report_charts(session_id, adom="root"):
    """Get available report charts"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/chart"
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
charts = get_report_charts(session_id="your_session_id")
for chart in charts:
    print(f"Chart: {chart['name']}")
    print(f"  Type: {chart.get('chart-type', 'N/A')}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
