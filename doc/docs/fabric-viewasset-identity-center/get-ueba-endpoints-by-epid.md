# Get UEBA Endpoints by Endpoint ID

Retrieve User and Entity Behavior Analytics (UEBA) endpoint information filtered by specific endpoint ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves UEBA endpoint data for specific devices identified by their endpoint ID (epid) - useful for:
- Security posture assessment of specific endpoints
- Investigating behavior analytics for compromised devices
- Tracking endpoint activities and risk scores
- Compliance monitoring for specific assets
- Forensic analysis of endpoint behavior

UEBA provides behavioral analytics and risk scoring for endpoints based on their activities, helping identify anomalous behavior and potential security threats.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/ueba/adom/{adom}/endpoints/`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- UEBA feature must be enabled on FortiAnalyzer
- Endpoint must be registered and reporting to FortiAnalyzer
- Read access to UEBA data in specified ADOM

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `filter` | `string` | Yes | - | Filter expression: `epid={endpoint_id}` |
| `limit` | `integer` | No | `1000` | Maximum results to return |
| `offset` | `integer` | No | `0` | Starting position for pagination |
| `detail-level` | `string` | No | `standard` | Detail level: `standard` or `verbose` |
| `sort-by` | `array` | No | - | Sorting specification |
| `time-range` | `object` | No | - | Activity time range filter |
| `firstseen-time-range` | `object` | No | - | First seen time range filter |

### Sorting Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `└─ field` | `string` | Field to sort by (e.g., "epid") |
| `└─ order` | `string` | Sort order: `asc` or `desc` |

### Time Range Format

```json
{
    "start": "2023-10-06 13:09:00",
    "end": "2023-12-05 13:09:00"
}
```

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/ueba/adom/root/endpoints/",
        "filter": "epid=1041",
        "limit": 1000,
        "offset": 0,
        "detail-level": "standard",
        "sort-by": [{
            "field": "epid",
            "order": "asc"
        }],
        "time-range": {
            "start": "2023-10-06 13:09:00",
            "end": "2023-12-05 13:09:00"
        },
        "firstseen-time-range": {
            "start": "1970-01-01 00:00:01",
            "end": "2023-12-05 13:09:29"
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
        "data": [{
            "epid": 1041,
            "hostname": "LAPTOP-USER01",
            "ip": "10.0.1.150",
            "mac": "00:0c:29:3a:5f:12",
            "os": "Windows 10",
            "risk_score": 45,
            "first_seen": "2023-09-15 08:30:00",
            "last_seen": "2023-12-05 12:45:00",
            "user": "jdoe",
            "status": "active"
        }],
        "status": {
            "code": 0,
            "message": "OK"
        }
    }]
}
```
````
`````

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `epid` | `integer` | Unique endpoint identifier |
| `hostname` | `string` | Endpoint hostname |
| `ip` | `string` | IP address |
| `mac` | `string` | MAC address |
| `os` | `string` | Operating system |
| `risk_score` | `integer` | UEBA risk score (0-100) |
| `first_seen` | `string` | First seen timestamp |
| `last_seen` | `string` | Last activity timestamp |
| `user` | `string` | Associated user |
| `status` | `string` | Endpoint status |

## Complete Python Example

```python
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ueba_endpoint_by_id(session_id, adom, epid, time_range=None):
    """
    Get UEBA endpoint information by endpoint ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        epid: Endpoint ID to query
        time_range: Optional time range dict

    Returns:
        list: Endpoint data
    """
    url = "https://faz.example.com/jsonrpc"

    params_data = {
        "url": f"/ueba/adom/{adom}/endpoints/",
        "filter": f"epid={epid}",
        "limit": 1000,
        "offset": 0,
        "detail-level": "standard",
        "sort-by": [{
            "field": "epid",
            "order": "asc"
        }]
    }

    if time_range:
        params_data["time-range"] = time_range

    payload = {
        "method": "get",
        "params": [params_data],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0].get('data', [])
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example usage
endpoint_data = get_ueba_endpoint_by_id(
    session_id="your_session_id",
    adom="root",
    epid=1041,
    time_range={
        "start": "2023-10-06 13:09:00",
        "end": "2023-12-05 13:09:00"
    }
)

# Display results
if endpoint_data:
    ep = endpoint_data[0]
    print(f"Endpoint: {ep['hostname']}")
    print(f"  IP: {ep['ip']}")
    print(f"  OS: {ep['os']}")
    print(f"  Risk Score: {ep['risk_score']}")
    print(f"  User: {ep['user']}")
    print(f"  Last Seen: {ep['last_seen']}")
```

## Use Cases

### Security Investigation

```python
# Investigate specific endpoint flagged by security team
endpoint = get_ueba_endpoint_by_id(
    session_id=session,
    adom="root",
    epid=1041,
    time_range={
        "start": "2023-12-01 00:00:00",
        "end": "2023-12-05 23:59:59"
    }
)

if endpoint and endpoint[0]['risk_score'] > 70:
    print(f"High risk endpoint detected: {endpoint[0]['hostname']}")
```

### Asset Inventory

```python
# Get detailed information for asset inventory
endpoint = get_ueba_endpoint_by_id(
    session_id=session,
    adom="root",
    epid=1041
)

# Export to inventory system
for ep in endpoint:
    inventory_record = {
        "hostname": ep['hostname'],
        "ip": ep['ip'],
        "mac": ep['mac'],
        "os": ep['os'],
        "last_activity": ep['last_seen']
    }
```

### Compliance Monitoring

```python
# Monitor endpoint compliance status
endpoint = get_ueba_endpoint_by_id(
    session_id=session,
    adom="root",
    epid=1041
)

if endpoint:
    ep = endpoint[0]
    if ep['status'] != 'active':
        print(f"Warning: Endpoint {ep['hostname']} is {ep['status']}")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -2,
            "message": "No data available"
        }
    }]
}
```
````
`````

**Common causes:**
- Endpoint ID does not exist
- UEBA not enabled
- No data for specified time range
- Insufficient permissions

## Best Practices

> **💡 Tip:** Use time-range filters to improve query performance for large UEBA datasets.

> **💡 Tip:** Monitor risk_score values regularly to identify endpoints requiring attention.

> **⚠️ Warning:** High risk scores (>70) should trigger immediate investigation.

## Related Endpoints

- [Get UEBA Endpoints by OS](./get-ueba-endpoints-by-os.md) - Filter endpoints by operating system
- [Get Devices](../device-manager/get-devices-no-filter.md) - List all managed devices

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
