# Search Webfilter Logs

Search for web filtering logs to analyze blocked websites, URL filtering activity, and web access patterns.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to search webfilter logs - useful for:
- Investigating blocked website access attempts
- Monitoring web filtering policy effectiveness
- Compliance reporting on web access
- Identifying users visiting inappropriate sites
- Analyzing web threat patterns

This operation uses the **two-step asynchronous pattern**. See the [LogView Search Overview](../pilot/logview-search.md) for complete workflow details.

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
| `device` | `array` | Optional | Device list (omit for all devices) |
| `logtype` | `string` | Yes | Must be `"webfilter"` |
| `filter` | `string` | No | Filter expression (e.g., "action=blocked") |
| `time-range` | `object` | Yes | Time range for search |

### Common Filters

**Blocked Sites:**
```
action=blocked
```

**Specific Category:**
```
cat desc=gambling
cat desc=social-networking
```

**By User:**
```
user=jdoe
```

**By URL Pattern:**
```
hostname contains "facebook"
```

**Combined Filters:**
```
action=blocked and user=jdoe
cat desc=malware and action=blocked
```

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/logview/adom/root/logsearch",
        "data": {
            "logtype": "webfilter",
            "filter": "action=blocked",
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
            "tid": 12346
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
        "url": "/logview/adom/root/logsearch/12346",
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
            "tid": 12346,
            "status": "done",
            "percentage": 100,
            "total_lines": 127,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "09:15:32",
                    "devname": "FGT-01",
                    "srcip": "10.0.1.50",
                    "user": "jdoe",
                    "hostname": "blocked-site.example.com",
                    "url": "https://blocked-site.example.com/page",
                    "action": "blocked",
                    "cat desc": "gambling",
                    "policyid": 10
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

def search_webfilter_logs(session_id, adom, filter_expr, time_range):
    """
    Search webfilter logs

    Args:
        session_id: Active session ID
        adom: ADOM name
        filter_expr: Filter expression (e.g., "action=blocked")
        time_range: Time range dict

    Returns:
        list: Matching webfilter log entries
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit search
    payload = {
        "method": "add",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch",
            "data": {
                "logtype": "webfilter",
                "filter": filter_expr,
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
    print(f"✓ Webfilter search submitted. TID: {tid}")

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
            print(f"✓ Found {data['total_lines']} webfilter logs")
            return data.get('logs', [])

        print(f"  Status: {data['percentage']}%")
        time.sleep(2)

# Example: Find all blocked websites in last 24 hours
logs = search_webfilter_logs(
    session_id="your_session_id",
    adom="root",
    filter_expr="action=blocked",
    time_range={"last-n-hours": 24}
)

# Display summary
for log in logs[:10]:
    print(f"{log['time']} | {log.get('user', 'unknown')} -> "
          f"{log['hostname']} | Category: {log.get('cat desc', 'N/A')}")
```

## Use Cases

### Monitor Blocked Access Attempts

```python
# Find all blocked website access in last 24 hours
logs = search_webfilter_logs(
    session_id=session,
    adom="root",
    filter_expr="action=blocked",
    time_range={"last-n-hours": 24}
)
```

### Investigate Specific User Activity

```python
# Check web filtering for specific user
logs = search_webfilter_logs(
    session_id=session,
    adom="root",
    filter_expr="user=jsmith and action=blocked",
    time_range={"last-n-hours": 8}
)
```

### Category Analysis

```python
# Find all social media access attempts
logs = search_webfilter_logs(
    session_id=session,
    adom="root",
    filter_expr='cat desc=social-networking',
    time_range={"last-n-hours": 24}
)
```

### Compliance Reporting

```python
# Generate report of inappropriate content access
logs = search_webfilter_logs(
    session_id=session,
    adom="root",
    filter_expr='(cat desc=gambling or cat desc=adult) and action=blocked',
    time_range={
        "start": "2025-11-01 00:00:00",
        "end": "2025-11-30 23:59:59"
    }
)
```

## Webfilter Categories

Common category descriptors for filtering:

- `gambling` - Gambling and betting sites
- `social-networking` - Social media platforms
- `adult` - Adult content
- `malware` - Known malware sites
- `phishing` - Phishing sites
- `spyware` - Spyware and adware
- `file-sharing` - File sharing and P2P
- `streaming-media` - Video streaming sites
- `gaming` - Online gaming sites

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Search by Destination IP](./create-search-task-for-ip-dst.md) - Search traffic logs
- [Search Attack Logs](./create-search-task-for-attack---signature.md) - IPS logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
