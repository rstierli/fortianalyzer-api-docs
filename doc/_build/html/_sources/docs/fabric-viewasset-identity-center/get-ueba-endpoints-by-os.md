# Get UEBA Endpoints by Operating System

Retrieve User and Entity Behavior Analytics (UEBA) endpoint information filtered by operating system.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves UEBA endpoint data filtered by operating system type - useful for:
- Security posture assessment by OS platform
- Identifying vulnerable OS versions requiring patches
- Compliance monitoring for specific OS platforms
- Asset inventory and management by OS type
- Risk analysis across different operating systems
- Planning OS migration or upgrade strategies

UEBA provides behavioral analytics and risk scoring for endpoints, helping security teams identify anomalous behavior and potential threats across different operating system platforms.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/ueba/adom/{adom}/endpoints/`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- UEBA feature must be enabled on FortiAnalyzer
- Endpoints must be registered and reporting to FortiAnalyzer
- Read access to UEBA data in specified ADOM

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `filter` | `string` | Yes | - | Filter expression: `osname={OS_name}` |
| `limit` | `integer` | No | `1000` | Maximum results to return |
| `offset` | `integer` | No | `0` | Starting position for pagination |
| `detail-level` | `string` | No | `standard` | Detail level: `standard` or `verbose` |
| `sort-by` | `array` | No | - | Sorting specification |
| `time-range` | `object` | No | - | Activity time range filter |
| `firstseen-time-range` | `object` | No | - | First seen time range filter |

### Common OS Name Values

- `Windows 10`
- `Windows 11`
- `Windows Server 2019`
- `Windows Server 2022`
- `Debian`
- `Ubuntu`
- `CentOS`
- `Red Hat Enterprise Linux`
- `macOS`
- `iOS`
- `Android`

### Sorting Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `└─ field` | `string` | Field to sort by (e.g., "epid", "risk_score") |
| `└─ order` | `string` | Sort order: `asc` or `desc` |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/ueba/adom/root/endpoints/",
        "filter": "osname=Debian",
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
        "data": [
            {
                "epid": 2045,
                "hostname": "debian-server-01",
                "ip": "10.0.2.50",
                "mac": "00:0c:29:4b:6f:23",
                "osname": "Debian",
                "osversion": "11.5",
                "risk_score": 25,
                "first_seen": "2023-08-20 10:15:00",
                "last_seen": "2023-12-05 11:30:00",
                "user": "admin",
                "status": "active"
            },
            {
                "epid": 2108,
                "hostname": "debian-web-02",
                "ip": "10.0.2.75",
                "mac": "00:0c:29:5c:7a:34",
                "osname": "Debian",
                "osversion": "12.0",
                "risk_score": 18,
                "first_seen": "2023-09-10 14:22:00",
                "last_seen": "2023-12-05 12:15:00",
                "user": "webadmin",
                "status": "active"
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

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `epid` | `integer` | Unique endpoint identifier |
| `hostname` | `string` | Endpoint hostname |
| `ip` | `string` | IP address |
| `mac` | `string` | MAC address |
| `osname` | `string` | Operating system name |
| `osversion` | `string` | OS version |
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

def get_ueba_endpoints_by_os(session_id, adom, os_name, time_range=None, limit=1000):
    """
    Get UEBA endpoints filtered by operating system

    Args:
        session_id: Active session ID
        adom: ADOM name
        os_name: Operating system name to filter
        time_range: Optional time range dict
        limit: Maximum results (default: 1000)

    Returns:
        list: Endpoint data
    """
    url = "https://faz.example.com/jsonrpc"

    params_data = {
        "url": f"/ueba/adom/{adom}/endpoints/",
        "filter": f"osname={os_name}",
        "limit": limit,
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

# Example: Get all Debian endpoints
endpoints = get_ueba_endpoints_by_os(
    session_id="your_session_id",
    adom="root",
    os_name="Debian",
    time_range={
        "start": "2023-10-06 13:09:00",
        "end": "2023-12-05 13:09:00"
    }
)

# Display results
print(f"Found {len(endpoints)} Debian endpoints:\n")
for ep in endpoints:
    print(f"  {ep['hostname']} ({ep['ip']})")
    print(f"    OS Version: {ep['osversion']}")
    print(f"    Risk Score: {ep['risk_score']}")
    print(f"    Last Seen: {ep['last_seen']}")
    print()
```

## Use Cases

### Vulnerability Assessment by OS

```python
# Identify all Windows 10 endpoints for patching
win10_endpoints = get_ueba_endpoints_by_os(
    session_id=session,
    adom="root",
    os_name="Windows 10"
)

high_risk = [ep for ep in win10_endpoints if ep['risk_score'] > 60]
print(f"High-risk Windows 10 endpoints: {len(high_risk)}")

for ep in high_risk:
    print(f"  {ep['hostname']} - Risk: {ep['risk_score']}")
```

### OS Migration Planning

```python
# Get all endpoints running legacy OS versions
legacy_os = ["Windows 7", "Windows Server 2008", "Ubuntu 16.04"]
endpoints_to_migrate = []

for os_name in legacy_os:
    endpoints = get_ueba_endpoints_by_os(
        session_id=session,
        adom="root",
        os_name=os_name
    )
    endpoints_to_migrate.extend(endpoints)

print(f"Total endpoints requiring migration: {len(endpoints_to_migrate)}")

# Generate migration report
for ep in endpoints_to_migrate:
    print(f"{ep['hostname']}: {ep['osname']} {ep['osversion']} -> Upgrade Required")
```

### Compliance Reporting

```python
# Check compliance: All servers must run approved OS versions
approved_server_os = ["Windows Server 2019", "Windows Server 2022", "Ubuntu 22.04", "Debian"]

server_endpoints = get_ueba_endpoints_by_os(
    session_id=session,
    adom="root",
    os_name="Windows Server 2016"  # Non-compliant version
)

if server_endpoints:
    print("⚠️ COMPLIANCE ALERT: Non-compliant OS detected")
    for ep in server_endpoints:
        print(f"  {ep['hostname']} running {ep['osname']} {ep['osversion']}")
```

### Security Posture by Platform

```python
# Analyze risk scores by OS platform
os_platforms = ["Windows 10", "Windows 11", "macOS", "Ubuntu", "Debian"]
risk_by_os = {}

for os_name in os_platforms:
    endpoints = get_ueba_endpoints_by_os(
        session_id=session,
        adom="root",
        os_name=os_name
    )

    if endpoints:
        avg_risk = sum(ep['risk_score'] for ep in endpoints) / len(endpoints)
        risk_by_os[os_name] = {
            'count': len(endpoints),
            'avg_risk': round(avg_risk, 2)
        }

# Display results
print("Security Posture by OS Platform:")
for os_name, data in sorted(risk_by_os.items(), key=lambda x: x[1]['avg_risk'], reverse=True):
    print(f"  {os_name}: {data['count']} endpoints, Avg Risk: {data['avg_risk']}")
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
- No endpoints with specified OS name
- UEBA not enabled
- No data for specified time range
- Incorrect OS name format
- Insufficient permissions

## Best Practices

> **💡 Tip:** Use exact OS names as they appear in FortiAnalyzer. OS names are case-sensitive.

> **💡 Tip:** Combine with risk_score sorting to prioritize high-risk endpoints for remediation.

> **⚠️ Warning:** Legacy OS versions (Windows 7, Server 2008) pose significant security risks and should be upgraded.

> **💡 Tip:** Regular OS inventory helps identify unauthorized or non-compliant systems.

## Related Endpoints

- [Get UEBA Endpoints by ID](./get-ueba-endpoints-by-epid.md) - Query specific endpoint
- [Get Devices](../device-manager/get-devices-no-filter.md) - List all managed devices

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
