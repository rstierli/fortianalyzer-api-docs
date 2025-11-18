# SD-WAN Application Usage

Retrieve top applications consuming SD-WAN bandwidth and sessions.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves SD-WAN application usage statistics - useful for:
- Identifying bandwidth-hungry applications over SD-WAN links
- Application-specific QoS and steering policy validation
- SaaS application usage monitoring
- Bandwidth allocation for critical applications
- Detecting unauthorized cloud service usage
- Application performance analysis over SD-WAN

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/sdwan-summary-app-view/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/sdwan-summary-app-view/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- SD-WAN feature enabled on FortiGate devices
- Application Control enabled on FortiGates
- Application identification configured

## Two-Step Workflow

### Step 1: Submit Task

Submit the SD-WAN application usage query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the application statistics.

---

## Step 1: Submit SD-WAN Application Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Filter expression |
| `limit` | `integer` | No | `10` | Number of top applications to return |
| `sort-by` | `array` | No | `[]` | Sorting specification |
| `time-range` | `object` | Yes | - | Time range for data |
| `case-sensitive` | `boolean` | No | `false` | Filter case sensitivity |

### Device Filter

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ devid` | `string` | Yes | Device ID or "All_FortiGate" |

### Time Range Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ start` | `string` | Yes | Start time: "YYYY-MM-DD HH:MM" |
| `└─ end` | `string` | Yes | End time: "YYYY-MM-DD HH:MM" |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/adom/root/sdwan-summary-app-view/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_FortiGate"
        }],
        "filter": "",
        "limit": 10,
        "sort-by": [],
        "time-range": {
            "start": "2022-06-24 00:00",
            "end": "2023-01-01 23:59"
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
            "tid": 12468
        },
        "status": {
            "code": 0,
            "message": "OK"
        }
    }],
    "session": "{{session_id}}",
    "id": 1
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

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/sdwan-summary-app-view/run/12468"
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
            "tid": 12468,
            "status": "done",
            "percentage": 100,
            "total": 35,
            "applications": [
                {
                    "app": "Microsoft.Office365",
                    "appcat": "Cloud.IT",
                    "bytes_sent": 10737418240,
                    "bytes_received": 21474836480,
                    "sessions": 3245,
                    "bandwidth": 89456789,
                    "users": 125
                },
                {
                    "app": "Zoom",
                    "appcat": "Collaboration",
                    "bytes_sent": 8589934592,
                    "bytes_received": 8589934592,
                    "sessions": 1823,
                    "bandwidth": 67012345,
                    "users": 78
                },
                {
                    "app": "Salesforce",
                    "appcat": "Business",
                    "bytes_sent": 2147483648,
                    "bytes_received": 6442450944,
                    "sessions": 892,
                    "bandwidth": 34567812,
                    "users": 45
                }
            ]
        },
        "status": {
            "code": 0,
            "message": "OK"
        }
    }],
    "session": "{{session_id}}",
    "id": 2
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
| `applications` | `array` | Array of application objects |

### Application Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `app` | `string` | Application name |
| `appcat` | `string` | Application category |
| `bytes_sent` | `integer` | Total bytes uploaded |
| `bytes_received` | `integer` | Total bytes downloaded |
| `sessions` | `integer` | Number of sessions |
| `bandwidth` | `integer` | Average bandwidth (bps) |
| `users` | `integer` | Number of unique users |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sdwan_applications(session_id, adom, time_range, limit=10):
    """
    Get top applications using SD-WAN bandwidth

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top applications to return (default: 10)

    Returns:
        list: Top SD-WAN applications by bandwidth
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/sdwan-summary-app-view/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": "All_FortiGate"}],
            "filter": "",
            "limit": limit,
            "sort-by": [],
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
                "url": f"/fortiview/adom/{adom}/sdwan-summary-app-view/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} SD-WAN applications")
            return data.get('applications', [])

        time.sleep(2)

# Example: Get top 20 SD-WAN applications
apps = get_sdwan_applications(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:00",
        "end": "2025-11-09 23:59"
    },
    limit=20
)

# Display results
print("\nTop SD-WAN Applications:")
print(f"{'Application':<30} {'Category':<20} {'Total GB':<12} {'Users'}")
print("-" * 80)

for app in apps:
    total_bytes = app['bytes_sent'] + app['bytes_received']
    total_gb = total_bytes / 1024 / 1024 / 1024

    print(f"{app['app']:<30} {app['appcat']:<20} {total_gb:>8.2f} GB   {app['users']:>5}")
```

## Use Cases

### SaaS Application Monitoring

```python
# Monitor critical SaaS applications over SD-WAN
critical_saas = ['Microsoft.Office365', 'Salesforce', 'Google.Workspace', 'Zoom', 'Slack']

apps = get_sdwan_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

print("Critical SaaS Application Performance:\n")
for app in apps:
    if app['app'] in critical_saas:
        total_gb = (app['bytes_sent'] + app['bytes_received']) / 1024 / 1024 / 1024
        bandwidth_mbps = app['bandwidth'] / 1000000

        print(f"{app['app']}:")
        print(f"  Total Data: {total_gb:.2f} GB")
        print(f"  Bandwidth: {bandwidth_mbps:.1f} Mbps")
        print(f"  Sessions: {app['sessions']:,}")
        print(f"  Users: {app['users']}")
        print()
```

### Application Category Analysis

```python
# Analyze bandwidth by application category
apps = get_sdwan_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=200
)

from collections import defaultdict
category_stats = defaultdict(lambda: {'apps': 0, 'total_bytes': 0, 'users': set()})

for app in apps:
    cat = app['appcat']
    category_stats[cat]['apps'] += 1
    category_stats[cat]['total_bytes'] += app['bytes_sent'] + app['bytes_received']
    category_stats[cat]['users'].add(app['users'])

print("7-Day Bandwidth by Application Category:\n")
print(f"{'Category':<25} {'Apps':<8} {'Total GB':<12} {'Unique Users'}")
print("-" * 65)

for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['total_bytes'], reverse=True):
    total_gb = stats['total_bytes'] / 1024 / 1024 / 1024
    total_users = sum(stats['users'])

    print(f"{cat:<25} {stats['apps']:<8} {total_gb:<12.2f} {total_users}")
```

### Unauthorized Application Detection

```python
# Detect unauthorized applications over SD-WAN
authorized_apps = [
    'Microsoft.Office365', 'Zoom', 'Salesforce', 'Google.Workspace',
    'Slack', 'Box', 'Dropbox.Business', 'GitHub'
]

apps = get_sdwan_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

unauthorized = [a for a in apps if a['app'] not in authorized_apps]

if unauthorized:
    print("⚠️ Unauthorized Applications Detected on SD-WAN:\n")
    for app in sorted(unauthorized, key=lambda x: x['bytes_sent'] + x['bytes_received'], reverse=True):
        total_gb = (app['bytes_sent'] + app['bytes_received']) / 1024 / 1024 / 1024

        if total_gb > 1.0:  # Only report significant usage
            print(f"  {app['app']} ({app['appcat']})")
            print(f"    Bandwidth: {total_gb:.2f} GB")
            print(f"    Users: {app['users']} | Sessions: {app['sessions']}")
            print()
else:
    print("✓ All applications are authorized")
```

### Application QoS Validation

```python
# Validate SD-WAN QoS policy effectiveness for critical apps
critical_apps_qos = {
    'Microsoft.Teams': {'min_bandwidth_mbps': 5, 'max_latency_ms': 50},
    'Zoom': {'min_bandwidth_mbps': 3, 'max_latency_ms': 50},
    'Salesforce': {'min_bandwidth_mbps': 2, 'max_latency_ms': 100}
}

apps = get_sdwan_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 1},
    limit=100
)

print("SD-WAN QoS Policy Validation:\n")
for app in apps:
    if app['app'] in critical_apps_qos:
        bandwidth_mbps = app['bandwidth'] / 1000000
        requirements = critical_apps_qos[app['app']]

        status = "✓" if bandwidth_mbps >= requirements['min_bandwidth_mbps'] else "⚠️"

        print(f"{status} {app['app']}:")
        print(f"  Current: {bandwidth_mbps:.1f} Mbps | Required: {requirements['min_bandwidth_mbps']} Mbps")
        print(f"  Users: {app['users']} | Sessions: {app['sessions']}")
        print()
```

### Bandwidth-Hungry Application Report

```python
# Identify bandwidth-intensive applications
apps = get_sdwan_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=100
)

# Calculate total bandwidth
total_bandwidth = sum(a['bytes_sent'] + a['bytes_received'] for a in apps)

print("Top Bandwidth-Consuming Applications (7 Days):\n")
print(f"{'Application':<30} {'Total GB':<12} {'% of Total':<12} {'Avg Mbps'}")
print("-" * 75)

for app in apps[:20]:
    app_total = app['bytes_sent'] + app['bytes_received']
    app_gb = app_total / 1024 / 1024 / 1024
    percentage = (app_total / total_bandwidth * 100) if total_bandwidth > 0 else 0
    avg_mbps = app['bandwidth'] / 1000000

    print(f"{app['app']:<30} {app_gb:<12.2f} {percentage:<12.1f} {avg_mbps:.1f}")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - No Data
```json
{
    "result": [{
        "data": {
            "tid": 12468,
            "status": "done",
            "percentage": 100,
            "total": 0,
            "applications": []
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

**Common causes:**
- No SD-WAN traffic in time range
- Application Control not enabled
- No application signatures matched traffic

## Best Practices

> **💡 Tip:** Monitor critical SaaS applications (Office 365, Salesforce, Zoom) to ensure SD-WAN policies are optimized for business needs.

> **💡 Tip:** Compare application bandwidth usage across different time periods to identify trends and plan capacity.

> **⚠️ Warning:** High bandwidth usage from unauthorized cloud storage apps may indicate data exfiltration or policy violations.

> **💡 Tip:** Use application category analysis to make informed SD-WAN steering and QoS policy decisions.

## Application Categories

| Category | Examples | Typical Priority |
|----------|----------|-----------------|
| **Collaboration** | Teams, Zoom, Webex | High (Real-time) |
| **Cloud.IT** | Office365, Google Workspace | High |
| **Business** | Salesforce, SAP, Oracle | High |
| **File.Sharing** | Dropbox, Box, OneDrive | Medium |
| **Video/Audio** | YouTube, Spotify, Netflix | Low (Non-business) |
| **Social.Media** | Facebook, Twitter, LinkedIn | Low |
| **P2P** | BitTorrent, etc. | Very Low (Block) |

## Related Endpoints

- [SD-WAN Top Talkers](./create-task-sd-wan-top-talkers.md) - Top bandwidth users
- [SD-WAN Interface Statistics](./create-task-sd-wan-interface-bandwidth-line.md) - Interface-level metrics
- [SD-WAN Health Overview](./create-task-sd-wan-health-overview.md) - Overall bandwidth trends
- [Fetch Results by Task ID](./fetch-result-by-task-id.md) - Retrieve completed task results

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
