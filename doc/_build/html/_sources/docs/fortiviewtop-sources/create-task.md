# Create Top Sources Task

Retrieve top traffic sources ranked by session count, bandwidth usage, or other metrics.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves FortiView top sources data - useful for:
- Identifying bandwidth-heavy users and devices
- Network capacity planning and optimization
- Monitoring user activity patterns
- Security analysis of unusual traffic sources
- Compliance reporting on network usage
- Troubleshooting network performance issues

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/top-sources/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/top-sources/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- FortiView feature enabled on FortiAnalyzer

## Two-Step Workflow

### Step 1: Submit Task

Submit the top sources query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the top sources data.

---

## Step 1: Submit Top Sources Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Additional filter expression |
| `limit` | `integer` | No | `10` | Number of top sources to return |
| `sort-by` | `array` | Yes | - | Sorting specification |
| `time-range` | `object` | Yes | - | Time range for data |
| `case-sensitive` | `boolean` | No | `false` | Filter case sensitivity |

### Device Filter

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ devid` | `string` | Yes | Device ID or "All_Devices" |

### Sort Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `└─ field` | `string` | Field to sort by: `sessions`, `bytes`, `bandwidth` |
| `└─ order` | `string` | Sort order: `asc` or `desc` |

### Time Range Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ start` | `string` | Yes | Start time: "YYYY-MM-DD HH:MM:SS" |
| `└─ end` | `string` | Yes | End time: "YYYY-MM-DD HH:MM:SS" |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/adom/root/top-sources/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_Devices"
        }],
        "filter": "",
        "limit": 10,
        "sort-by": [{
            "field": "sessions",
            "order": "desc"
        }],
        "time-range": {
            "start": "2025-11-09 00:00:00",
            "end": "2025-11-09 23:59:59"
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
            "tid": 12450
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

---

## Step 2: Fetch Results

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (same as Step 1) |
| `tid` | `integer` | Yes | - | Task ID from Step 1 |
| `limit` | `integer` | No | `100` | Results per page |
| `offset` | `integer` | No | `0` | Starting position for pagination |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/top-sources/12450",
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
            "tid": 12450,
            "status": "done",
            "percentage": 100,
            "total": 10,
            "sources": [
                {
                    "srcip": "10.0.1.150",
                    "hostname": "LAPTOP-USER01",
                    "sessions": 4523,
                    "bytes": 2147483648,
                    "bandwidth": 45678901,
                    "country": "Reserved"
                },
                {
                    "srcip": "10.0.1.75",
                    "hostname": "DESKTOP-IT01",
                    "sessions": 3891,
                    "bytes": 1879048192,
                    "bandwidth": 39012345,
                    "country": "Reserved"
                },
                {
                    "srcip": "10.0.1.45",
                    "hostname": "SERVER-APP01",
                    "sessions": 3204,
                    "bytes": 1610612736,
                    "bandwidth": 33456789,
                    "country": "Reserved"
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

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `tid` | `integer` | Task ID |
| `status` | `string` | Task status: "done", "running", "error" |
| `percentage` | `integer` | Completion percentage (0-100) |
| `total` | `integer` | Total number of sources returned |
| `sources` | `array` | Array of top source objects |

### Source Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `srcip` | `string` | Source IP address |
| `hostname` | `string` | Resolved hostname (if available) |
| `sessions` | `integer` | Number of sessions |
| `bytes` | `integer` | Total bytes transferred |
| `bandwidth` | `integer` | Bandwidth usage (bps) |
| `country` | `string` | GeoIP country |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_top_sources(session_id, adom, time_range, limit=10, sort_field="sessions"):
    """
    Get top traffic sources for a time period

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top sources to return (default: 10)
        sort_field: Field to sort by: sessions, bytes, bandwidth

    Returns:
        list: Top sources data
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-sources/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": "All_Devices"}],
            "filter": "",
            "limit": limit,
            "sort-by": [{
                "field": sort_field,
                "order": "desc"
            }],
            "time-range": time_range
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    tid = result['result'][0]['data']['tid']
    print(f"✓ Task submitted. TID: {tid}")

    # Step 2: Poll for completion
    while True:
        poll_payload = {
            "method": "get",
            "params": [{
                "url": f"/fortiview/adom/{adom}/top-sources/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} top sources")
            return data.get('sources', [])

        time.sleep(2)

# Example: Get top 10 sources by session count
sources = get_top_sources(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=10,
    sort_field="sessions"
)

# Display results
print("\nTop Traffic Sources:")
for i, src in enumerate(sources, 1):
    print(f"{i}. {src['srcip']} ({src.get('hostname', 'Unknown')})")
    print(f"   Sessions: {src['sessions']:,}")
    print(f"   Bytes: {src['bytes']:,}")
    print(f"   Bandwidth: {src['bandwidth']:,} bps")
    print()
```

## Use Cases

### Identify Bandwidth-Heavy Users

```python
# Get top 20 sources by bandwidth usage
sources = get_top_sources(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=20,
    sort_field="bandwidth"
)

# Identify excessive bandwidth users
excessive_usage = [s for s in sources if s['bandwidth'] > 100000000]  # >100Mbps
for src in excessive_usage:
    print(f"High bandwidth: {src['srcip']} - {src['bandwidth']/1000000:.2f} Mbps")
```

### Network Capacity Planning

```python
# Analyze traffic patterns for last 7 days
import datetime

end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=7)

sources = get_top_sources(
    session_id=session,
    adom="root",
    time_range={
        "start": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end": end_time.strftime("%Y-%m-%d %H:%M:%S")
    },
    limit=50,
    sort_field="bytes"
)

# Calculate total traffic
total_bytes = sum(s['bytes'] for s in sources)
print(f"Total traffic (7 days): {total_bytes/1024/1024/1024:.2f} GB")

# Show top 10 consumers
for i, src in enumerate(sources[:10], 1):
    percentage = (src['bytes'] / total_bytes) * 100
    print(f"{i}. {src['srcip']}: {src['bytes']/1024/1024/1024:.2f} GB ({percentage:.1f}%)")
```

### Security Monitoring

```python
# Detect unusual traffic patterns
sources = get_top_sources(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 1},
    limit=100,
    sort_field="sessions"
)

# Flag sources with unusual session counts
threshold = 1000
suspicious = [s for s in sources if s['sessions'] > threshold]

if suspicious:
    print(f"⚠️ {len(suspicious)} sources with >1000 sessions/hour:")
    for src in suspicious:
        print(f"  {src['srcip']}: {src['sessions']:,} sessions")
```

### Top Sources Report

```python
# Generate comprehensive top sources report
sources = get_top_sources(
    session_id=session,
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=25,
    sort_field="sessions"
)

# Format as report
print("=" * 80)
print("TOP TRAFFIC SOURCES REPORT")
print("=" * 80)
print(f"{'Rank':<6} {'IP Address':<16} {'Hostname':<20} {'Sessions':>10} {'Bandwidth':>12}")
print("-" * 80)

for i, src in enumerate(sources, 1):
    hostname = src.get('hostname', 'Unknown')[:20]
    bandwidth_mbps = src['bandwidth'] / 1000000
    print(f"{i:<6} {src['srcip']:<16} {hostname:<20} {src['sessions']:>10,} {bandwidth_mbps:>11.2f}M")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -3,
            "message": "Invalid task ID"
        }
    }]
}
```
````
`````

**Common causes:**
- Task ID has expired
- Invalid TID value
- FortiView data not available for time range
- Insufficient permissions

## Best Practices

> **💡 Tip:** Use appropriate time ranges - shorter ranges return faster results and reduce server load.

> **💡 Tip:** Start with smaller limits (10-25) for quick overviews, increase to 100+ for comprehensive analysis.

> **⚠️ Warning:** Tasks expire after a period of inactivity. Fetch results promptly after task completion.

> **💡 Tip:** Sort by different fields (sessions, bytes, bandwidth) to get different perspectives on network usage.

## Related Endpoints

- [Fetch Top Sources Result](./fetch-result-by-task.md) - Retrieve completed task results
- [Top Applications](../fortiviewtop-applications/topapplications.md) - Analyze application usage
- [Top Threats](../fortiviewtop-threats/create-task.md) - Security threat analysis

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
