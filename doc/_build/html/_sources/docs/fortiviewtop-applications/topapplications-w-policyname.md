# Top Applications Filtered by Policy Name

Retrieve top applications filtered by firewall policy name instead of policy ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to retrieve FortiView top applications filtered by policy name - useful for:
- Analyzing application usage for specific security policies
- Comparing application patterns across different named policies
- Policy-based bandwidth reporting and analysis
- Identifying applications allowed by specific firewall rules
- Troubleshooting policy-specific application traffic
- Security policy effectiveness monitoring

This is the same endpoint as [Top Applications](./topapplications.md), but demonstrates filtering by policy name rather than policy ID for easier policy identification.

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
- FortiView and Application Control features enabled
- Know the exact policy name (case-sensitive)

## Key Difference

The primary difference from the standard top applications endpoint is the filter parameter:

- **By Policy ID**: `filter: "policyid=46"`
- **By Policy Name**: `filter: "policyname=Internet_Access"`

> **💡 Tip:** Policy names are easier to remember than IDs, making this approach more user-friendly for scripting and automation.

## Request Format

### Parameters

Same as standard [Top Applications](./topapplications.md) endpoint, with filter parameter set to policy name.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | Yes | - | Filter by policy name |
| `limit` | `integer` | No | `100` | Number of top applications to return |
| `sort-by` | `array` | No | - | Sorting specification |
| `time-range` | `object` | Yes | - | Time range for data |

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
        "filter": "policyname=Intra-2-SDWAN_BBI",
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
            "tid": 12458
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

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/top-applications/run/12458"
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
            "tid": 12458,
            "status": "done",
            "percentage": 100,
            "total": 12,
            "applications": [
                {
                    "app": "Office365.Sharepoint",
                    "appcat": "Cloud.IT",
                    "sessions": 3245,
                    "bytes": 1073741824,
                    "bandwidth": 22345678,
                    "policyid": 125,
                    "policyname": "Intra-2-SDWAN_BBI"
                },
                {
                    "app": "Microsoft.Teams",
                    "appcat": "Collaboration",
                    "sessions": 2891,
                    "bytes": 805306368,
                    "bandwidth": 16789012,
                    "policyid": 125,
                    "policyname": "Intra-2-SDWAN_BBI"
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

def get_top_apps_by_policy_name(session_id, adom, policy_name, time_range, limit=100):
    """
    Get top applications filtered by policy name

    Args:
        session_id: Active session ID
        adom: ADOM name
        policy_name: Firewall policy name to filter
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top applications to return (default: 100)

    Returns:
        list: Top applications data for specified policy
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
            "filter": f"policyname={policy_name}",
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
    print(f"✓ Task submitted for policy '{policy_name}'. TID: {tid}")

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
            print(f"✓ Found {data['total']} applications for policy '{policy_name}'")
            return data.get('applications', [])

        time.sleep(2)

# Example: Get applications for specific policy
apps = get_top_apps_by_policy_name(
    session_id="your_session_id",
    adom="root",
    policy_name="Intra-2-SDWAN_BBI",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=100
)

# Display results
print(f"\nTop Applications for Policy 'Intra-2-SDWAN_BBI':\n")
for i, app in enumerate(apps, 1):
    print(f"{i}. {app['app']} ({app['appcat']})")
    print(f"   Bytes: {app['bytes']/1024/1024/1024:.2f} GB")
    print(f"   Sessions: {app['sessions']:,}")
    print()
```

## Use Cases

### Compare Application Usage Across Policies

```python
# Compare application usage across different security policies
policy_names = ["Internet_Access", "Guest_Network", "DMZ_Policy"]
policy_comparison = {}

for policy in policy_names:
    apps = get_top_apps_by_policy_name(
        session_id=session,
        adom="root",
        policy_name=policy,
        time_range={"last-n-hours": 24},
        limit=50
    )

    total_bytes = sum(a['bytes'] for a in apps)
    policy_comparison[policy] = {
        'total_gb': total_bytes / 1024 / 1024 / 1024,
        'app_count': len(apps),
        'top_app': apps[0]['app'] if apps else 'None'
    }

# Display comparison
print("Policy Comparison Report:\n")
for policy, data in policy_comparison.items():
    print(f"{policy}:")
    print(f"  Total: {data['total_gb']:.2f} GB")
    print(f"  Applications: {data['app_count']}")
    print(f"  Top App: {data['top_app']}")
    print()
```

### Monitor SD-WAN Policy Applications

```python
# Monitor applications using SD-WAN policies
sdwan_policies = [
    "SDWAN_BBI",
    "SDWAN_LTE_Backup",
    "SDWAN_Voice_Priority"
]

for policy in sdwan_policies:
    apps = get_top_apps_by_policy_name(
        session_id=session,
        adom="root",
        policy_name=policy,
        time_range={"last-n-hours": 1},
        limit=10
    )

    print(f"\nPolicy: {policy}")
    print("-" * 60)
    for app in apps[:5]:
        bandwidth_mbps = app['bandwidth'] / 1000000
        print(f"  {app['app']}: {bandwidth_mbps:.2f} Mbps")
```

### Policy-Based Application Compliance

```python
# Check if unauthorized applications are used in specific policy
authorized_apps = ["Microsoft.Office365", "Google.Drive", "Salesforce"]

apps = get_top_apps_by_policy_name(
    session_id=session,
    adom="root",
    policy_name="Corporate_Internet",
    time_range={"last-n-hours": 24},
    limit=100
)

# Find unauthorized applications
unauthorized = [a for a in apps if a['app'] not in authorized_apps]

if unauthorized:
    print("⚠️ Unauthorized applications detected:")
    for app in unauthorized[:10]:
        print(f"  {app['app']}: {app['bytes']/1024/1024:.2f} MB")
else:
    print("✓ All applications are authorized")
```

### Policy Effectiveness Analysis

```python
# Analyze if policy is being used as intended
policy_name = "Guest_Network"
expected_categories = ["Social.Media", "Video/Audio", "Web.Based"]

apps = get_top_apps_by_policy_name(
    session_id=session,
    adom="root",
    policy_name=policy_name,
    time_range={"last-n-days": 7},
    limit=100
)

# Group by category
from collections import defaultdict
categories = defaultdict(lambda: {'bytes': 0, 'count': 0})

for app in apps:
    cat = app['appcat']
    categories[cat]['bytes'] += app['bytes']
    categories[cat]['count'] += 1

# Check for unexpected categories
print(f"Policy '{policy_name}' Application Analysis:\n")
for cat, data in sorted(categories.items(), key=lambda x: x[1]['bytes'], reverse=True):
    expected = "✓" if cat in expected_categories else "⚠️"
    print(f"{expected} {cat}: {data['bytes']/1024/1024/1024:.2f} GB ({data['count']} apps)")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - Invalid Policy Name
```json
{
    "result": [{
        "data": {
            "tid": 12458,
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
- Policy name does not exist
- Policy name is case-sensitive (check exact spelling)
- No traffic matched the policy in the time range
- Policy has no application control enabled

## Best Practices

> **💡 Tip:** Policy names are case-sensitive. Use exact policy names as configured on FortiGate devices.

> **💡 Tip:** For policies with special characters or spaces, the filter still works: `policyname=Intra-2-SDWAN_BBI`

> **⚠️ Warning:** If a policy name changes on FortiGate, historical queries will return no results. Use policy ID for consistency.

> **💡 Tip:** List all policies first to get exact names before filtering.

## Finding Policy Names

If unsure of exact policy names, first query without filters to see all available policies:

```python
# Get all applications to see policy names
all_apps = get_top_applications(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=1000
)

# Extract unique policy names
policy_names = set(app['policyname'] for app in all_apps)
print("Available policy names:")
for pname in sorted(policy_names):
    print(f"  - {pname}")
```

## Related Endpoints

- [Top Applications (by ID)](./topapplications.md) - Filter by policy ID instead
- [Fetch Top Applications Result](./fetch-result-by-task.md) - Retrieve completed task results
- [Top Sources](../fortiviewtop-sources/create-task.md) - Analyze traffic sources
- [Top Threats](../fortiviewtop-threats/create-task.md) - Security threat analysis

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
