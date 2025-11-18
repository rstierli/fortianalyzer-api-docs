# Create Top Applications Task

Retrieve top applications ranked by usage, bandwidth, sessions, or other metrics.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to retrieve FortiView top applications data - useful for:
- Identifying bandwidth-consuming applications
- Application usage monitoring and reporting
- Security analysis of application traffic patterns
- Bandwidth optimization and QoS policy tuning
- Compliance monitoring for unauthorized applications
- Network capacity planning by application type

This operation uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/top-applications/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/top-applications/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- FortiView and Application Control features enabled on FortiAnalyzer
- Application identification configured on FortiGate devices

## Two-Step Workflow

### Step 1: Submit Task

Submit the top applications query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the top applications data.

---

## Step 1: Submit Top Applications Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Additional filter expression |
| `limit` | `integer` | No | `100` | Number of top applications to return |
| `sort-by` | `array` | No | - | Sorting specification |
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

### Common Filter Examples

- `policyid=46` - Filter by specific firewall policy
- `appcat=Network.Service` - Filter by application category
- `app contains "Facebook"` - Filter by application name

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/adom/root/top-applications/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_Devices"
        }],
        "filter": "policyid=46",
        "limit": 100,
        "sort-by": [{
            "field": "bytes",
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
            "tid": 12455
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
        "url": "/fortiview/adom/root/top-applications/run/12455",
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
            "tid": 12455,
            "status": "done",
            "percentage": 100,
            "total": 15,
            "applications": [
                {
                    "app": "YouTube",
                    "appcat": "Video/Audio",
                    "sessions": 8932,
                    "bytes": 4294967296,
                    "bandwidth": 89456789,
                    "policyid": 46,
                    "policyname": "Internet_Access"
                },
                {
                    "app": "Netflix",
                    "appcat": "Video/Audio",
                    "sessions": 5421,
                    "bytes": 3221225472,
                    "bandwidth": 67012345,
                    "policyid": 46,
                    "policyname": "Internet_Access"
                },
                {
                    "app": "Microsoft.Office365",
                    "appcat": "Cloud.IT",
                    "sessions": 4523,
                    "bytes": 536870912,
                    "bandwidth": 11234567,
                    "policyid": 46,
                    "policyname": "Internet_Access"
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
| `total` | `integer` | Total number of applications returned |
| `applications` | `array` | Array of top application objects |

### Application Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `app` | `string` | Application name |
| `appcat` | `string` | Application category |
| `sessions` | `integer` | Number of sessions |
| `bytes` | `integer` | Total bytes transferred |
| `bandwidth` | `integer` | Bandwidth usage (bps) |
| `policyid` | `integer` | Firewall policy ID |
| `policyname` | `string` | Firewall policy name |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_top_applications(session_id, adom, time_range, limit=100, filter_expr=""):
    """
    Get top applications for a time period

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top applications to return (default: 100)
        filter_expr: Optional filter expression (e.g., "policyid=46")

    Returns:
        list: Top applications data
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-applications/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": "All_Devices"}],
            "filter": filter_expr,
            "limit": limit,
            "sort-by": [{
                "field": "bytes",
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
                "url": f"/fortiview/adom/{adom}/top-applications/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} top applications")
            return data.get('applications', [])

        time.sleep(2)

# Example: Get top applications by bandwidth
apps = get_top_applications(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=100,
    filter_expr="policyid=46"
)

# Display results
print("\nTop Applications by Bandwidth:")
for i, app in enumerate(apps[:10], 1):
    print(f"{i}. {app['app']} ({app['appcat']})")
    print(f"   Sessions: {app['sessions']:,}")
    print(f"   Bytes: {app['bytes']:,} ({app['bytes']/1024/1024/1024:.2f} GB)")
    print(f"   Bandwidth: {app['bandwidth']/1000000:.2f} Mbps")
    print(f"   Policy: {app['policyname']} (ID: {app['policyid']})")
    print()
```

## Use Cases

### Identify Bandwidth-Consuming Applications

```python
# Get top 20 applications by bandwidth
apps = get_top_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=20
)

# Identify high bandwidth consumers
high_bandwidth = [a for a in apps if a['bandwidth'] > 50000000]  # >50Mbps
for app in high_bandwidth:
    print(f"High bandwidth: {app['app']} - {app['bandwidth']/1000000:.2f} Mbps")
```

### Monitor Streaming Services Usage

```python
# Get all video/audio applications
apps = get_top_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

# Filter for streaming services
streaming = [a for a in apps if "Video/Audio" in a['appcat']]
total_streaming_gb = sum(a['bytes'] for a in streaming) / 1024 / 1024 / 1024

print(f"Total streaming traffic: {total_streaming_gb:.2f} GB")
print(f"\nTop streaming applications:")
for i, app in enumerate(sorted(streaming, key=lambda x: x['bytes'], reverse=True)[:5], 1):
    print(f"{i}. {app['app']}: {app['bytes']/1024/1024/1024:.2f} GB")
```

### Application Category Analysis

```python
# Categorize application usage
apps = get_top_applications(
    session_id=session,
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=100
)

# Group by category
from collections import defaultdict
categories = defaultdict(lambda: {'bytes': 0, 'sessions': 0, 'apps': []})

for app in apps:
    cat = app['appcat']
    categories[cat]['bytes'] += app['bytes']
    categories[cat]['sessions'] += app['sessions']
    categories[cat]['apps'].append(app['app'])

# Display results
print("Application Usage by Category:\n")
for cat, data in sorted(categories.items(), key=lambda x: x[1]['bytes'], reverse=True):
    print(f"{cat}:")
    print(f"  Total: {data['bytes']/1024/1024/1024:.2f} GB")
    print(f"  Sessions: {data['sessions']:,}")
    print(f"  Applications: {len(data['apps'])}")
    print()
```

### Policy-Based Application Monitoring

```python
# Monitor applications by policy
policy_ids = [46, 47, 48]  # Different internet access policies

for policy_id in policy_ids:
    apps = get_top_applications(
        session_id=session,
        adom="root",
        time_range={"last-n-hours": 24},
        limit=50,
        filter_expr=f"policyid={policy_id}"
    )

    if apps:
        policy_name = apps[0]['policyname']
        total_bytes = sum(a['bytes'] for a in apps)

        print(f"Policy: {policy_name} (ID: {policy_id})")
        print(f"  Total traffic: {total_bytes/1024/1024/1024:.2f} GB")
        print(f"  Applications: {len(apps)}")
        print(f"  Top 3: {', '.join(a['app'] for a in apps[:3])}")
        print()
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
- Application Control not enabled
- Insufficient permissions

## Best Practices

> **💡 Tip:** Use appropriate time ranges - shorter ranges return faster results and reduce server load.

> **💡 Tip:** Filter by policy ID to analyze specific traffic segments (e.g., guest vs. employee traffic).

> **⚠️ Warning:** Application identification requires deep packet inspection. Ensure AppCtrl is enabled on FortiGate devices.

> **💡 Tip:** Combine with bandwidth thresholds to identify applications requiring QoS policies.

## Application Categories

Common application categories returned:

- **Video/Audio** - Streaming services (YouTube, Netflix, Spotify)
- **Cloud.IT** - Cloud services (Office365, Google Workspace, Salesforce)
- **Social.Media** - Social networks (Facebook, Twitter, LinkedIn)
- **Network.Service** - Network infrastructure (DNS, NTP, SNMP)
- **File.Sharing** - File transfer (Dropbox, OneDrive, FTP)
- **Email** - Email services (SMTP, IMAP, Gmail)
- **Web.Based** - Generic web traffic
- **Business** - Business applications (SAP, Oracle)
- **Game** - Online gaming
- **P2P** - Peer-to-peer applications

## Related Endpoints

- [Fetch Top Applications Result](./fetch-result-by-task.md) - Retrieve completed task results
- [Top Applications with Policy Name](./topapplications-w-policyname.md) - Include policy name filtering
- [Top Sources](../fortiviewtop-sources/create-task.md) - Analyze traffic sources
- [Top Threats](../fortiviewtop-threats/create-task.md) - Security threat analysis

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
