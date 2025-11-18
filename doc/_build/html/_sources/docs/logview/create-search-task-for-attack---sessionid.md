# Search Attack Logs - By Session ID

Search for attack logs by specific session ID to track related events.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search IPS logs by session ID - useful for:
- Tracking all attacks in a specific session
- Investigating related security events
- Session-based forensic analysis
- Correlating multiple attack attempts

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
            "logtype": "attack",
            "filter": "sessionid==12345678",
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
            "tid": 12352
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
        "url": "/logview/adom/root/logsearch/12352",
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
            "tid": 12352,
            "status": "done",
            "percentage": 100,
            "total_lines": 5,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "14:32:18",
                    "devname": "FGT-01",
                    "sessionid": 12345678,
                    "srcip": "10.0.1.75",
                    "dstip": "203.0.113.100",
                    "attack": "XSS.Attempt",
                    "action": "detected"
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

def search_attack_by_session(session_id, adom, session_filter, time_range):
    """Search attack logs by session ID"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch",
            "data": {
                "logtype": "attack",
                "filter": f"sessionid=={session_filter}",
                "time-range": time_range
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    tid = response.json()['result'][0]['data']['tid']

    while True:
        response = requests.post(url, json={
            "method": "get",
            "params": [{"url": f"/logview/adom/{adom}/logsearch/{tid}"}],
            "session": session_id,
            "id": 2
        }, verify=False)

        data = response.json()['result'][0]['data']
        if data['status'] == 'done':
            return data.get('logs', [])
        time.sleep(2)
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
