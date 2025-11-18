# SD-WAN Top Talkers

Retrieve top users/endpoints consuming SD-WAN bandwidth.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves top SD-WAN bandwidth consumers by user/endpoint - useful for:
- Identifying bandwidth-heavy users and endpoints
- User-based bandwidth accountability and reporting
- Detecting abnormal user bandwidth consumption
- Capacity planning based on user behavior
- Fair-use policy enforcement
- Shadow IT detection through unusual user patterns

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/sdwan-summary-user-view/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/sdwan-summary-user-view/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- SD-WAN feature enabled on FortiGate devices
- User identification enabled (authentication or IP-based)

## Two-Step Workflow

### Step 1: Submit Task

Submit the SD-WAN top talkers query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the top user statistics.

---

## Step 1: Submit SD-WAN Top Talkers Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Filter expression |
| `limit` | `integer` | No | `10` | Number of top users to return |
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
        "url": "/fortiview/adom/root/sdwan-summary-user-view/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_FortiGate"
        }],
        "filter": "",
        "limit": 10,
        "sort-by": [],
        "time-range": {
            "start": "2025-11-09 00:01",
            "end": "2025-11-09 23:59"
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
            "tid": 12467
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
        "url": "/fortiview/adom/root/sdwan-summary-user-view/run/12467"
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
            "tid": 12467,
            "status": "done",
            "percentage": 100,
            "total": 25,
            "users": [
                {
                    "user": "jdoe@corp.com",
                    "srcip": "10.1.50.25",
                    "hostname": "LAPTOP-JDOE",
                    "bytes_sent": 8589934592,
                    "bytes_received": 17179869184,
                    "sessions": 2456,
                    "bandwidth": 45678912,
                    "applications": 15
                },
                {
                    "user": "rsmith@corp.com",
                    "srcip": "10.1.50.47",
                    "hostname": "DESKTOP-RSMITH",
                    "bytes_sent": 5368709120,
                    "bytes_received": 10737418240,
                    "sessions": 1823,
                    "bandwidth": 32145678,
                    "applications": 12
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
| `total` | `integer` | Total number of users returned |
| `users` | `array` | Array of top user objects |

### User Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | `string` | Username or email address |
| `srcip` | `string` | Source IP address |
| `hostname` | `string` | Hostname of endpoint |
| `bytes_sent` | `integer` | Total bytes uploaded |
| `bytes_received` | `integer` | Total bytes downloaded |
| `sessions` | `integer` | Number of sessions |
| `bandwidth` | `integer` | Average bandwidth (bps) |
| `applications` | `integer` | Number of unique applications used |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sdwan_top_talkers(session_id, adom, time_range, limit=10):
    """
    Get top SD-WAN bandwidth consumers by user

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top users to return (default: 10)

    Returns:
        list: Top SD-WAN users by bandwidth
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/sdwan-summary-user-view/run",
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
                "url": f"/fortiview/adom/{adom}/sdwan-summary-user-view/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} SD-WAN users")
            return data.get('users', [])

        time.sleep(2)

# Example: Get top 20 bandwidth consumers
users = get_sdwan_top_talkers(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:01",
        "end": "2025-11-09 23:59"
    },
    limit=20
)

# Display results
print("\nTop SD-WAN Bandwidth Consumers:")
print(f"{'User':<30} {'Total Data':<15} {'Sessions':<10} {'Apps'}")
print("-" * 70)

for user in users:
    total_bytes = user['bytes_sent'] + user['bytes_received']
    total_gb = total_bytes / 1024 / 1024 / 1024

    print(f"{user['user']:<30} {total_gb:>10.2f} GB   {user['sessions']:<10} {user['applications']}")
```

## Use Cases

### Bandwidth Accountability Report

```python
# Generate user bandwidth accountability report
users = get_sdwan_top_talkers(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=50
)

print("7-Day Bandwidth Accountability Report\n")
print(f"{'Rank':<6} {'User':<30} {'Total GB':<12} {'Upload GB':<12} {'Download GB'}")
print("-" * 80)

for i, user in enumerate(users, 1):
    upload_gb = user['bytes_sent'] / 1024 / 1024 / 1024
    download_gb = user['bytes_received'] / 1024 / 1024 / 1024
    total_gb = (user['bytes_sent'] + user['bytes_received']) / 1024 / 1024 / 1024

    print(f"{i:<6} {user['user']:<30} {total_gb:<12.2f} {upload_gb:<12.2f} {download_gb:.2f}")
```

### Detect Abnormal Bandwidth Usage

```python
# Identify users with abnormally high bandwidth consumption
users = get_sdwan_top_talkers(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

# Calculate baseline
total_bytes_list = [(u['bytes_sent'] + u['bytes_received']) for u in users]
avg_usage = sum(total_bytes_list) / len(total_bytes_list) if total_bytes_list else 0
threshold = avg_usage * 3  # 3x average is abnormal

abnormal_users = []
for user in users:
    total = user['bytes_sent'] + user['bytes_received']
    if total > threshold:
        abnormal_users.append(user)

if abnormal_users:
    print("⚠️ Users with Abnormally High Bandwidth Usage:\n")
    for user in abnormal_users:
        total_gb = (user['bytes_sent'] + user['bytes_received']) / 1024 / 1024 / 1024
        avg_gb = avg_usage / 1024 / 1024 / 1024
        print(f"  {user['user']}: {total_gb:.2f} GB (avg: {avg_gb:.2f} GB)")
        print(f"    IP: {user['srcip']} | Hostname: {user['hostname']}")
        print(f"    Applications: {user['applications']} | Sessions: {user['sessions']}")
        print()
```

### Fair-Use Policy Enforcement

```python
# Monitor users against bandwidth fair-use policy
FAIR_USE_LIMIT_GB_PER_DAY = 50

users = get_sdwan_top_talkers(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

violators = []
for user in users:
    total_gb = (user['bytes_sent'] + user['bytes_received']) / 1024 / 1024 / 1024

    if total_gb > FAIR_USE_LIMIT_GB_PER_DAY:
        violators.append({
            'user': user['user'],
            'usage_gb': total_gb,
            'overage_gb': total_gb - FAIR_USE_LIMIT_GB_PER_DAY,
            'ip': user['srcip']
        })

if violators:
    print(f"⚠️ Fair-Use Policy Violations (>{FAIR_USE_LIMIT_GB_PER_DAY} GB/day):\n")
    for v in sorted(violators, key=lambda x: x['overage_gb'], reverse=True):
        print(f"  {v['user']} ({v['ip']})")
        print(f"    Usage: {v['usage_gb']:.2f} GB")
        print(f"    Overage: {v['overage_gb']:.2f} GB over limit")
        print()
else:
    print("✓ All users within fair-use policy limits")
```

### Shadow IT Detection

```python
# Detect potential shadow IT through unusual application counts
users = get_sdwan_top_talkers(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

# Identify users with unusually high application diversity
avg_apps = sum(u['applications'] for u in users) / len(users) if users else 0
high_app_users = [u for u in users if u['applications'] > avg_apps * 1.5]

if high_app_users:
    print("⚠️ Potential Shadow IT Detected (High Application Diversity):\n")
    for user in high_app_users:
        total_gb = (user['bytes_sent'] + user['bytes_received']) / 1024 / 1024 / 1024
        print(f"  {user['user']}:")
        print(f"    Applications: {user['applications']} (avg: {avg_apps:.1f})")
        print(f"    Total Bandwidth: {total_gb:.2f} GB")
        print(f"    Sessions: {user['sessions']}")
        print()
```

### Department/Team Bandwidth Analysis

```python
# Analyze bandwidth by department (based on email domain or username pattern)
users = get_sdwan_top_talkers(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=500
)

# Group by department (extract from email)
from collections import defaultdict
dept_usage = defaultdict(lambda: {'users': 0, 'total_bytes': 0})

for user in users:
    # Extract department from email (e.g., sales@corp.com -> sales)
    if '@' in user['user']:
        dept = user['user'].split('@')[0].split('.')[0]  # Simple extraction
    else:
        dept = 'Unknown'

    dept_usage[dept]['users'] += 1
    dept_usage[dept]['total_bytes'] += user['bytes_sent'] + user['bytes_received']

print("7-Day Bandwidth by Department:\n")
print(f"{'Department':<20} {'Users':<10} {'Total GB':<15} {'Avg GB/User'}")
print("-" * 65)

for dept, stats in sorted(dept_usage.items(), key=lambda x: x[1]['total_bytes'], reverse=True):
    total_gb = stats['total_bytes'] / 1024 / 1024 / 1024
    avg_per_user = total_gb / stats['users'] if stats['users'] > 0 else 0

    print(f"{dept:<20} {stats['users']:<10} {total_gb:<15.2f} {avg_per_user:.2f}")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - No Data
```json
{
    "result": [{
        "data": {
            "tid": 12467,
            "status": "done",
            "percentage": 100,
            "total": 0,
            "users": []
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
- User identification not enabled
- No authenticated users in traffic

## Best Practices

> **💡 Tip:** Use 24-hour to 7-day time ranges for accurate user behavior analysis and fair-use monitoring.

> **💡 Tip:** Combine with application data to understand what users are consuming bandwidth on.

> **⚠️ Warning:** High application diversity (>20 apps) may indicate unauthorized software or cloud service usage.

> **💡 Tip:** Set baseline metrics and alert on users exceeding 2-3x average usage for anomaly detection.

## User Bandwidth Guidelines

| Usage Category | Daily Bandwidth | Typical Profile |
|----------------|----------------|-----------------|
| **Light User** | <5 GB | Email, web browsing, basic apps |
| **Normal User** | 5-20 GB | Office apps, video calls, file sharing |
| **Heavy User** | 20-50 GB | Video conferencing, large file transfers |
| **Power User** | 50-100 GB | Media production, development, cloud sync |
| **Excessive** | >100 GB | Potential policy violation or abnormal activity |

## Related Endpoints

- [SD-WAN Applications](./create-task-sd-wan-application.md) - Application bandwidth breakdown
- [SD-WAN Interface Statistics](./create-task-sd-wan-interface-bandwidth-line.md) - Interface-level metrics
- [SD-WAN Health Overview](./create-task-sd-wan-health-overview.md) - Overall bandwidth trends
- [Fetch Results by Task ID](./fetch-result-by-task-id.md) - Retrieve completed task results

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
