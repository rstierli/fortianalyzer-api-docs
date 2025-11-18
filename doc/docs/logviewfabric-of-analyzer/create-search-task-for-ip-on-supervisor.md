# Create Fabric Log Search Task

Submit a distributed log search across Fabric of FortiAnalyzer (Supervisor + Members).

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates distributed log searches across Fabric of FortiAnalyzer deployments - useful for:
- Searching logs across multiple FortiAnalyzer units simultaneously
- Distributed SIEM environments with Supervisor-Member topology
- Large-scale enterprise log analysis
- Multi-site distributed deployments

**Two-Step Pattern**: Submit task → Receive TID → Fetch results

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/soc-fabric/logsearch/`
**API Path (Step 2):** `/soc-fabric/logsearch/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Step 1: Submit Search Task

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/soc-fabric/logsearch/",
        "apiver": 3,
        "case-sensitive": false,
        "filter": "srcip=\"10.0.200.253\" dstip=\"140.82.121.5\"",
        "logtype": "traffic",
        "time-order": "desc",
        "time-range": {
            "start": "2025-11-10 00:00",
            "end": "2025-11-10 23:59"
        },
        "limit": 100,
        "devtype": "FortiGate",
        "members": []
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
            "tid": 12470
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

## Step 2: Fetch Results by Task ID

See [Fetch Fabric Log Search Results](./fetch-log-search-result-by-task-id-on-supervisor.md) for detailed polling and retrieval.

## Complete Python Example

```python
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_fabric_search(session_id, filter_expr, start_time, end_time, logtype="traffic"):
    """Create distributed fabric log search"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": "/soc-fabric/logsearch/",
            "apiver": 3,
            "case-sensitive": False,
            "filter": filter_expr,
            "logtype": logtype,
            "time-order": "desc",
            "time-range": {
                "start": start_time,
                "end": end_time
            },
            "limit": 100,
            "devtype": "FortiGate",
            "members": []  # Empty = all fabric members
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        tid = result['result'][0]['data']['tid']
        print(f"✓ Fabric search created. TID: {tid}")
        return tid
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
tid = create_fabric_search(
    session_id="your_session_id",
    filter_expr='srcip="10.0.200.253" dstip="140.82.121.5"',
    start_time="2025-11-10 00:00",
    end_time="2025-11-10 23:59"
)
```

## Related Endpoints

- [Fetch Fabric Log Search Results](./fetch-log-search-result-by-task-id-on-supervisor.md) - Retrieve results by TID

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
