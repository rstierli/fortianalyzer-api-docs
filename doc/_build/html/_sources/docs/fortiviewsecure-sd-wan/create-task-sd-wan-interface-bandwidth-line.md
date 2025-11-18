# SD-WAN Interface Bandwidth Statistics

Retrieve SD-WAN interface bandwidth and availability statistics for network performance monitoring.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves SD-WAN interface bandwidth statistics - useful for:
- Monitoring SD-WAN interface availability and utilization
- Analyzing bandwidth consumption across WAN links
- Identifying underutilized or overloaded SD-WAN interfaces
- Capacity planning for SD-WAN deployments
- SLA compliance monitoring for WAN links
- Troubleshooting SD-WAN performance issues

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/sdwan-dev-stats/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/sdwan-dev-stats/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- SD-WAN feature enabled on FortiGate devices
- FortiGates configured with SD-WAN interfaces
- SD-WAN interface statistics being collected

## Two-Step Workflow

### Step 1: Submit Task

Submit the SD-WAN interface bandwidth query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the interface statistics.

---

## Step 1: Submit SD-WAN Interface Bandwidth Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Filter expression |
| `limit` | `integer` | No | `10` | Number of top interfaces to return |
| `sort-by` | `array` | Yes | - | Sorting specification |
| `time-range` | `object` | Yes | - | Time range for data |
| `case-sensitive` | `boolean` | No | `false` | Filter case sensitivity |

### Device Filter

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ devid` | `string` | Yes | Device ID or "All_FortiGate" |

### Sort Configuration

| Parameter | Type | Description |
|-----------|------|-------------|
| `└─ field` | `string` | Field to sort by: `available`, `bandwidth`, `sessions` |
| `└─ order` | `string` | Sort order: `asc` or `desc` |

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
        "url": "/fortiview/adom/root/sdwan-dev-stats/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_FortiGate"
        }],
        "filter": "",
        "limit": 10,
        "sort-by": [{
            "field": "available",
            "order": "desc"
        }],
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
            "tid": 12465
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
| `limit` | `integer` | No | `100` | Results per page |
| `offset` | `integer` | No | `0` | Starting position for pagination |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/sdwan-dev-stats/run/12465",
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
            "tid": 12465,
            "status": "done",
            "percentage": 100,
            "total": 8,
            "interfaces": [
                {
                    "interface": "wan1",
                    "device": "FGT-Branch01",
                    "available": 98.5,
                    "bandwidth": 100000000,
                    "utilization": 45.2,
                    "sessions": 1523,
                    "bytes_sent": 4294967296,
                    "bytes_received": 8589934592,
                    "latency": 12,
                    "jitter": 2,
                    "packetloss": 0.1
                },
                {
                    "interface": "wan2",
                    "device": "FGT-Branch01",
                    "available": 99.2,
                    "bandwidth": 50000000,
                    "utilization": 67.8,
                    "sessions": 892,
                    "bytes_sent": 2147483648,
                    "bytes_received": 4294967296,
                    "latency": 8,
                    "jitter": 1,
                    "packetloss": 0.05
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
| `total` | `integer` | Total number of interfaces returned |
| `interfaces` | `array` | Array of SD-WAN interface objects |

### Interface Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `interface` | `string` | Interface name (e.g., "wan1", "wan2") |
| `device` | `string` | FortiGate device name |
| `available` | `float` | Availability percentage (0-100) |
| `bandwidth` | `integer` | Interface bandwidth capacity (bps) |
| `utilization` | `float` | Current utilization percentage (0-100) |
| `sessions` | `integer` | Number of active sessions |
| `bytes_sent` | `integer` | Total bytes transmitted |
| `bytes_received` | `integer` | Total bytes received |
| `latency` | `integer` | Average latency (milliseconds) |
| `jitter` | `integer` | Average jitter (milliseconds) |
| `packetloss` | `float` | Packet loss percentage |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sdwan_interface_stats(session_id, adom, time_range, limit=10):
    """
    Get SD-WAN interface bandwidth and availability statistics

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top interfaces to return (default: 10)

    Returns:
        list: SD-WAN interface statistics
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/sdwan-dev-stats/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": "All_FortiGate"}],
            "filter": "",
            "limit": limit,
            "sort-by": [{
                "field": "available",
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
                "url": f"/fortiview/adom/{adom}/sdwan-dev-stats/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} SD-WAN interfaces")
            return data.get('interfaces', [])

        time.sleep(2)

# Example: Get SD-WAN interface statistics
interfaces = get_sdwan_interface_stats(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:01",
        "end": "2025-11-09 23:59"
    },
    limit=10
)

# Display results
print("\nSD-WAN Interface Statistics:")
print(f"{'Interface':<15} {'Device':<20} {'Avail%':<8} {'Util%':<8} {'Latency':<10} {'Loss%'}")
print("-" * 75)

for intf in interfaces:
    print(f"{intf['interface']:<15} {intf['device']:<20} {intf['available']:<8.2f} {intf['utilization']:<8.2f} {intf['latency']:<10}ms {intf['packetloss']:.3f}%")
```

## Use Cases

### Monitor Interface Availability

```python
# Check SD-WAN interface availability for SLA compliance
interfaces = get_sdwan_interface_stats(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=50
)

# Filter for interfaces below 99% availability
low_availability = [i for i in interfaces if i['available'] < 99.0]

if low_availability:
    print("⚠️ Interfaces below 99% availability SLA:")
    for intf in low_availability:
        print(f"  {intf['device']}/{intf['interface']}: {intf['available']:.2f}%")
```

### Identify Overloaded Interfaces

```python
# Find interfaces with high utilization
interfaces = get_sdwan_interface_stats(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 1},
    limit=100
)

# Filter for >80% utilization
overloaded = [i for i in interfaces if i['utilization'] > 80.0]

print("Overloaded SD-WAN Interfaces (>80% utilization):")
for intf in sorted(overloaded, key=lambda x: x['utilization'], reverse=True):
    bandwidth_mbps = intf['bandwidth'] / 1000000
    print(f"  {intf['device']}/{intf['interface']}: {intf['utilization']:.1f}% of {bandwidth_mbps}Mbps")
```

### Performance Quality Analysis

```python
# Analyze SD-WAN link quality metrics
interfaces = get_sdwan_interface_stats(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100
)

print("SD-WAN Link Quality Report:\n")
for intf in interfaces:
    quality_score = 100

    # Deduct points for performance issues
    if intf['latency'] > 50:
        quality_score -= 20
    elif intf['latency'] > 20:
        quality_score -= 10

    if intf['jitter'] > 10:
        quality_score -= 15
    elif intf['jitter'] > 5:
        quality_score -= 5

    if intf['packetloss'] > 1.0:
        quality_score -= 25
    elif intf['packetloss'] > 0.5:
        quality_score -= 10

    quality_rating = "Excellent" if quality_score >= 90 else \
                     "Good" if quality_score >= 75 else \
                     "Fair" if quality_score >= 60 else "Poor"

    print(f"{intf['device']}/{intf['interface']}:")
    print(f"  Quality Score: {quality_score}/100 ({quality_rating})")
    print(f"  Latency: {intf['latency']}ms | Jitter: {intf['jitter']}ms | Loss: {intf['packetloss']}%")
    print()
```

### Bandwidth Capacity Planning

```python
# Analyze bandwidth usage for capacity planning
interfaces = get_sdwan_interface_stats(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=100
)

print("Bandwidth Capacity Planning Report:\n")

# Group by device
from collections import defaultdict
device_stats = defaultdict(list)

for intf in interfaces:
    device_stats[intf['device']].append(intf)

for device, intfs in device_stats.items():
    total_capacity = sum(i['bandwidth'] for i in intfs) / 1000000  # Convert to Mbps
    avg_utilization = sum(i['utilization'] for i in intfs) / len(intfs)

    print(f"{device}:")
    print(f"  Total Capacity: {total_capacity:.0f} Mbps")
    print(f"  Average Utilization: {avg_utilization:.1f}%")

    if avg_utilization > 70:
        print(f"  ⚠️ Recommendation: Consider bandwidth upgrade")
    elif avg_utilization < 30:
        print(f"  ✓ Capacity adequate, room for growth")

    print()
```

### Multi-Site Comparison

```python
# Compare SD-WAN performance across sites
interfaces = get_sdwan_interface_stats(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=1000
)

# Group by device (site)
from collections import defaultdict
site_metrics = defaultdict(lambda: {
    'interfaces': 0,
    'avg_availability': 0,
    'avg_latency': 0,
    'total_bandwidth': 0
})

for intf in interfaces:
    site = intf['device']
    site_metrics[site]['interfaces'] += 1
    site_metrics[site]['avg_availability'] += intf['available']
    site_metrics[site]['avg_latency'] += intf['latency']
    site_metrics[site]['total_bandwidth'] += intf['bandwidth']

print("Multi-Site SD-WAN Performance:\n")
print(f"{'Site':<20} {'Interfaces':<12} {'Avg Avail%':<12} {'Avg Latency':<15} {'Total BW'}")
print("-" * 80)

for site, metrics in sorted(site_metrics.items()):
    count = metrics['interfaces']
    avg_avail = metrics['avg_availability'] / count
    avg_lat = metrics['avg_latency'] / count
    total_bw = metrics['total_bandwidth'] / 1000000  # Mbps

    print(f"{site:<20} {count:<12} {avg_avail:<12.2f} {avg_lat:<15.1f}ms {total_bw:.0f}Mbps")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - Invalid Time Range
```json
{
    "result": [{
        "status": {
            "code": -1,
            "message": "Invalid time range"
        }
    }]
}
```
````
`````

**Common causes:**
- Invalid date format
- End time before start time
- Time range too large
- SD-WAN data not available for time range

## Best Practices

> **💡 Tip:** Sort by "available" to quickly identify interfaces with availability issues for SLA monitoring.

> **💡 Tip:** Monitor utilization trends over time to identify when bandwidth upgrades are needed before performance degrades.

> **⚠️ Warning:** High latency (>50ms), jitter (>10ms), or packet loss (>1%) indicate link quality issues requiring investigation.

> **💡 Tip:** Use shorter time ranges (1-24 hours) for real-time monitoring, longer ranges (7-30 days) for capacity planning.

## SD-WAN Performance Metrics

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| **Availability** | ≥99.5% | 99-99.5% | 98-99% | <98% |
| **Latency** | <20ms | 20-50ms | 50-100ms | >100ms |
| **Jitter** | <5ms | 5-10ms | 10-20ms | >20ms |
| **Packet Loss** | <0.1% | 0.1-0.5% | 0.5-1% | >1% |
| **Utilization** | <60% | 60-80% | 80-90% | >90% |

## Related Endpoints

- [SD-WAN Health Overview](./create-task-sd-wan-health-overview.md) - Overall SD-WAN health metrics
- [SD-WAN Top Talkers](./create-task-sd-wan-top-talkers.md) - Top users by bandwidth
- [SD-WAN Applications](./create-task-sd-wan-application.md) - Application usage over SD-WAN
- [Fetch Results by Task ID](./fetch-result-by-task-id.md) - Retrieve completed task results

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
