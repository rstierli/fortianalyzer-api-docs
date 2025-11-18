# Search Traffic Logs by Destination IP

Search for all traffic logs matching a specific destination IP address.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search traffic logs filtered by destination IP address - useful for:
- Investigating connections to specific servers or services
- Tracking traffic to external IP addresses
- Security incident analysis for known malicious IPs
- Compliance auditing for access to regulated systems

This operation uses the **two-step asynchronous pattern**. See the [LogView Search Overview](../pilot/logview-search.md) for complete workflow details, polling strategies, and pagination examples.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/logview/adom/{adom}/logsearch`
**API Path (Step 2):** `/logview/adom/{adom}/logsearch/{tid}`

## Step 1: Submit Search Request

### Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `device` | `array` | Yes | Device list to search |
| `logtype` | `string` | Yes | Must be `"traffic"` for IP searches |
| `filter` | `string` | Yes | Filter expression: `dstip==<ip_address>` |
| `time-range` | `object` | Yes | Time range for search |

### Filter Syntax

**Single IP:**
```
dstip==192.168.1.100
```

**IP with Subnet:**
```
dstip==192.168.1.0/24
```

**Combined Filters:**
```
dstip==192.168.1.100 and dstport==443
dstip==10.0.0.0/8 and action==deny
```

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/logview/adom/root/logsearch",
        "data": {
            "device": [{"devname": "FGT-01"}],
            "logtype": "traffic",
            "filter": "dstip==154.52.10.106",
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
            "tid": 12345
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

> **📝 Note:** Save the TID value for Step 2!

## Step 2: Fetch Results

Use the TID from Step 1 to poll and retrieve results. See [LogView Search Overview](../pilot/logview-search.md#step-2-poll-status-and-fetch-results) for complete polling implementation.

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/logview/adom/root/logsearch/12345",
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
            "tid": 12345,
            "status": "done",
            "percentage": 100,
            "total_lines": 45,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "14:23:15",
                    "devname": "FGT-01",
                    "srcip": "10.0.1.100",
                    "srcport": 54321,
                    "dstip": "154.52.10.106",
                    "dstport": 443,
                    "action": "accept",
                    "policyid": 5,
                    "service": "HTTPS",
                    "sentbyte": 2048,
                    "rcvdbyte": 8192
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
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_by_destination_ip(session_id, adom, device, dst_ip, time_range):
    """
    Search traffic logs by destination IP

    Args:
        session_id: Active session ID
        adom: ADOM name
        device: Device name or list
        dst_ip: Destination IP address or subnet
        time_range: Time range dict

    Returns:
        list: Matching log entries
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit search
    payload = {
        "method": "add",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch",
            "data": {
                "device": [{"devname": device}] if isinstance(device, str) else device,
                "logtype": "traffic",
                "filter": f"dstip=={dst_ip}",
                "time-range": time_range
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] != 0:
        raise Exception(f"Search failed: {result['result'][0]['status']['message']}")

    tid = result['result'][0]['data']['tid']
    print(f"✓ Search submitted. TID: {tid}")

    # Step 2: Poll until complete
    while True:
        payload = {
            "method": "get",
            "params": [{
                "url": f"/logview/adom/{adom}/logsearch/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=payload, verify=False)
        result = response.json()
        data = result['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total_lines']} logs")
            return data.get('logs', [])

        print(f"  Status: {data['percentage']}%")
        time.sleep(2)

# Example usage
logs = search_by_destination_ip(
    session_id="your_session_id",
    adom="root",
    device="FGT-01",
    dst_ip="154.52.10.106",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    }
)

# Display results
for log in logs[:5]:
    print(f"{log['time']} | {log['srcip']}:{log['srcport']} -> "
          f"{log['dstip']}:{log['dstport']} | {log['action']}")
```

## Use Cases

### Investigate Traffic to Specific Server

```python
# Find all connections to database server
search_by_destination_ip(
    session_id=session,
    adom="root",
    device="All_FortiGate",
    dst_ip="10.10.10.50",
    time_range={"last-n-hours": 24}
)
```

### Track External API Calls

```python
# Monitor traffic to external API endpoint
search_by_destination_ip(
    session_id=session,
    adom="root",
    device="FGT-DMZ",
    dst_ip="203.0.113.45",
    time_range={"last-n-hours": 1}
)
```

### Security Analysis

```python
# Investigate connections to suspicious IP
search_by_destination_ip(
    session_id=session,
    adom="root",
    device="All_FortiGate",
    dst_ip="198.51.100.75",
    time_range={"last-n-hours": 48}
)
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Search by Source IP](./README.md) - Search by source IP
- [Cancel Search Task](./cancel-log-search-task.md) - Cancel running search

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
