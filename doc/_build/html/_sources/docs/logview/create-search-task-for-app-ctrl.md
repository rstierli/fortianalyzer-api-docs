# Search Application Control Logs

Search for application control logs to monitor application usage and policy enforcement.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search application control logs - useful for:
- Monitoring application usage patterns
- Enforcing application policies
- Bandwidth usage analysis by application
- Compliance reporting on application access
- Security analysis of application traffic

This operation uses the **two-step asynchronous pattern**. See the [LogView Search Overview](../pilot/logview-search.md) for complete workflow details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/logview/adom/{adom}/logsearch`
**API Path (Step 2):** `/logview/adom/{adom}/logsearch/{tid}`

## Step 1: Submit Search Request

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/logview/adom/root/logsearch",
        "data": {
            "logtype": "app-ctrl",
            "time-range": {
                "start": "2025-11-09 00:00:00",
                "end": "2025-11-09 23:59:59"
            }
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
            "tid": 12353
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

## Step 2: Fetch Results

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/logview/adom/root/logsearch/12353",
        "data": {
            "limit": 100,
            "offset": 0
        }
    }],
    "session": "{{session_id}}",
    "id": 2
}
```
````
````{tab-item} RESPONSE
```json
{
    "result": [{
        "data": {
            "tid": 12353,
            "status": "done",
            "percentage": 100,
            "total_lines": 287,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "10:25:38",
                    "devname": "FGT-01",
                    "srcip": "10.0.1.45",
                    "app": "Facebook",
                    "appcat": "Social.Media",
                    "action": "pass",
                    "sentbyte": 4096,
                    "rcvdbyte": 12288
                }
            ]
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

def search_appctrl_logs(session_id, adom, time_range, filter_expr=None):
    """Search application control logs"""
    url = "https://faz.example.com/jsonrpc"

    payload_data = {
        "logtype": "app-ctrl",
        "time-range": time_range
    }

    if filter_expr:
        payload_data["filter"] = filter_expr

    payload = {
        "method": "add",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch",
            "data": payload_data
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    tid = response.json()['result'][0]['data']['tid']
    print(f"✓ App-ctrl search submitted. TID: {tid}")

    while True:
        response = requests.post(url, json={
            "method": "get",
            "params": [{"url": f"/logview/adom/{adom}/logsearch/{tid}"}],
            "session": session_id,
            "id": 2
        }, verify=False)

        data = response.json()['result'][0]['data']
        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total_lines']} app-ctrl logs")
            return data.get('logs', [])

        time.sleep(2)

# Example: Search for specific application
logs = search_appctrl_logs(
    session_id="your_session_id",
    adom="root",
    time_range={"last-n-hours": 24},
    filter_expr='app contains "Facebook"'
)
```

## Use Cases

### Monitor Specific Application

```python
logs = search_appctrl_logs(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    filter_expr='app contains "Skype"'
)
```

### Track Blocked Applications

```python
logs = search_appctrl_logs(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    filter_expr="action=blocked"
)
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Search Webfilter Logs](./create-search-task-for-webfilter-logs.md) - Web filtering logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
