# Search Attack Logs - IPS Signatures

Search for intrusion prevention system (IPS) attack logs and security threats.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search IPS/IDS attack logs for detected security threats - useful for:
- Monitoring intrusion attempts and attacks
- Security incident investigation
- Threat analysis and pattern recognition
- Compliance reporting on security events
- SOC operations and threat hunting

This operation uses the **two-step asynchronous pattern**. See the [LogView Search Overview](../pilot/logview-search.md) for complete workflow details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/logview/adom/{adom}/logsearch`
**API Path (Step 2):** `/logview/adom/{adom}/logsearch/{tid}`

##Step 1: Submit Search Request

### Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `logtype` | `string` | Yes | Must be `"attack"` for IPS logs |
| `filter` | `string` | No | Optional filter expression |
| `time-range` | `object` | Yes | Time range for search |

### Filter Examples

**By Severity:**
```
severity=critical
severity=high
```

**By Attack Name:**
```
attack contains "SQL.Injection"
attack contains "XSS"
```

**By Source IP:**
```
srcip==10.0.1.100
```

**By Action:**
```
action=dropped
action=detected
```

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/logview/adom/root/logsearch",
        "data": {
            "logtype": "attack",
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
            "tid": 12349
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
        "url": "/logview/adom/root/logsearch/12349",
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
            "tid": 12349,
            "status": "done",
            "percentage": 100,
            "total_lines": 64,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "16:18:42",
                    "devname": "FGT-01",
                    "srcip": "203.0.113.25",
                    "dstip": "10.0.1.100",
                    "attack": "SQL.Injection",
                    "action": "dropped",
                    "severity": "critical",
                    "policyid": 8
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

def search_attack_logs(session_id, adom, time_range, filter_expr=None):
    """
    Search for IPS attack logs

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict
        filter_expr: Optional filter expression

    Returns:
        list: Attack log entries
    """
    url = "https://faz.example.com/jsonrpc"

    payload_data = {
        "logtype": "attack",
        "time-range": time_range
    }

    if filter_expr:
        payload_data["filter"] = filter_expr

    # Step 1: Submit search
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
    result = response.json()

    if result['result'][0]['status']['code'] != 0:
        raise Exception(f"Search failed")

    tid = result['result'][0]['data']['tid']
    print(f"✓ Attack search submitted. TID: {tid}")

    # Step 2: Poll and fetch
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
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total_lines']} attack logs")
            return data.get('logs', [])

        print(f"  Status: {data['percentage']}%")
        time.sleep(2)

# Example: Search for critical severity attacks
logs = search_attack_logs(
    session_id="your_session_id",
    adom="root",
    time_range={"last-n-hours": 24},
    filter_expr="severity=critical"
)

for log in logs[:10]:
    print(f"{log['time']} | {log['srcip']} -> {log['dstip']} | "
          f"Attack: {log.get('attack', 'Unknown')} | Severity: {log.get('severity', 'N/A')}")
```

## Use Cases

### Monitor Critical Attacks

```python
logs = search_attack_logs(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    filter_expr="severity=critical"
)
```

### Investigate Specific Attack Type

```python
logs = search_attack_logs(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 48},
    filter_expr='attack contains "SQL.Injection"'
)
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Search Attack - Botnet](./create-search-task-for-attack---botnet.md) - Botnet detection logs
- [Search Malware Logs](./create-search-task-for-malware---outbreak.md) - AntiVirus logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
