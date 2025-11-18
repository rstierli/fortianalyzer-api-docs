# Run Report

Generate a report on-demand using specified parameters.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint generates reports on-demand - useful for ad-hoc reporting and immediate analysis needs.

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
        "apiver": 3,
        "schedule-param": {
            "device": "all",
            "time-period": "last-30-days",
            "filter-logic": "all",
            "filter": [
                {
                    "name": "All",
                    "value": "All",
                    "opcode": 0
                }
            ],
            "layout-id": 123456
        }
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
        "data": {
            "tid": 98765
        },
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
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_report(session_id, layout_id, device="all", time_period="last-7-days", adom="root"):
    """Run report generation"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "add",
        "params": [{
            "url": f"/report/adom/{adom}/run",
            "apiver": 3,
            "schedule-param": {
                "device": device,
                "time-period": time_period,
                "filter-logic": "all",
                "filter": [
                    {
                        "name": "All",
                        "value": "All",
                        "opcode": 0
                    }
                ],
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
        print(f"✓ Report generation started. Task ID: {tid}")
        return tid
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

def check_report_status(session_id, tid, adom="root"):
    """Check report generation status"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": f"/report/adom/{adom}/reports/{tid}"
        }],
        "session": session_id,
        "id": 2
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Run report and wait for completion
tid = run_report(session_id="your_session_id", layout_id=123456)

# Poll for completion
max_wait = 300  # 5 minutes
start_time = time.time()

while time.time() - start_time < max_wait:
    status = check_report_status(session_id="your_session_id", tid=tid)
    
    if status.get('status') == 'done':
        print(f"✓ Report completed: {status.get('file')}")
        break
    
    print(f"  Report status: {status.get('percentage', 0)}% complete")
    time.sleep(10)
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
