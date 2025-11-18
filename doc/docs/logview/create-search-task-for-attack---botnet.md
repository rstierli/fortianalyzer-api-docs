# Search Attack Logs - Botnet Detection

Search for botnet-related attack logs and command & control (C2) communications.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search IPS logs for botnet detection events - useful for:
- Detecting botnet C2 communications
- Identifying compromised hosts
- Tracking botnet activity patterns
- Incident response for infected devices
- Compliance and security reporting

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
            "filter": "attack contains \"botnet\"",
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
            "tid": 12351
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
        "url": "/logview/adom/root/logsearch/12351",
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
            "tid": 12351,
            "status": "done",
            "percentage": 100,
            "total_lines": 12,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "17:05:23",
                    "devname": "FGT-01",
                    "srcip": "10.0.1.150",
                    "dstip": "198.51.100.45",
                    "attack": "Botnet.CnC.Connection",
                    "action": "dropped",
                    "severity": "high"
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

def search_botnet_logs(session_id, adom, time_range):
    """Search for botnet detection logs"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch",
            "data": {
                "logtype": "attack",
                "filter": 'attack contains "botnet"',
                "time-range": time_range
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    tid = response.json()['result'][0]['data']['tid']
    print(f"✓ Botnet search submitted. TID: {tid}")

    while True:
        response = requests.post(url, json={
            "method": "get",
            "params": [{"url": f"/logview/adom/{adom}/logsearch/{tid}"}],
            "session": session_id,
            "id": 2
        }, verify=False)

        data = response.json()['result'][0]['data']
        if data['status'] == 'done' and data['percentage'] == 100:
            return data.get('logs', [])
        time.sleep(2)
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Search Attack - Signature](./create-search-task-for-attack---signature.md) - All IPS logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
