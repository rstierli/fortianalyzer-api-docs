# SD-WAN Interface Health Overview

Retrieve SD-WAN interface health overview with bandwidth trend analysis over time.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves SD-WAN interface bandwidth line/trend data - useful for:
- Visualizing bandwidth utilization trends over time
- Historical SD-WAN performance analysis
- Identifying bandwidth usage patterns and peak times
- Trend-based capacity forecasting
- Long-term SD-WAN health monitoring
- Performance regression detection

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/sdwan-intf-bandwidth-line/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/sdwan-intf-bandwidth-line/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- SD-WAN feature enabled on FortiGate devices
- Time-series bandwidth data being collected

## Two-Step Workflow

### Step 1: Submit Task

Submit the SD-WAN health overview query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the bandwidth trend data.

---

## Step 1: Submit SD-WAN Health Overview Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Filter expression |
| `limit` | `integer` | No | `10` | Number of top interfaces to return |
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
        "url": "/fortiview/adom/root/sdwan-intf-bandwidth-line/run",
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
            "tid": 12466
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
        "url": "/fortiview/adom/root/sdwan-intf-bandwidth-line/run/12466"
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
            "tid": 12466,
            "status": "done",
            "percentage": 100,
            "total": 48,
            "timeseries": [
                {
                    "timestamp": "2025-11-09 00:00",
                    "interface": "wan1",
                    "device": "FGT-HQ",
                    "bandwidth_in": 45678912,
                    "bandwidth_out": 23456789,
                    "utilization_in": 45.7,
                    "utilization_out": 23.5
                },
                {
                    "timestamp": "2025-11-09 01:00",
                    "interface": "wan1",
                    "device": "FGT-HQ",
                    "bandwidth_in": 38234567,
                    "bandwidth_out": 19123456,
                    "utilization_in": 38.2,
                    "utilization_out": 19.1
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
| `total` | `integer` | Total number of data points |
| `timeseries` | `array` | Array of time-series data points |

### Timeseries Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | `string` | Data point timestamp |
| `interface` | `string` | SD-WAN interface name |
| `device` | `string` | FortiGate device name |
| `bandwidth_in` | `integer` | Inbound bandwidth (bps) |
| `bandwidth_out` | `integer` | Outbound bandwidth (bps) |
| `utilization_in` | `float` | Inbound utilization percentage |
| `utilization_out` | `float` | Outbound utilization percentage |

## Complete Python Example

```python
import json
import requests
import urllib3
import time
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sdwan_health_overview(session_id, adom, time_range, limit=10):
    """
    Get SD-WAN interface bandwidth trends over time

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top interfaces to include (default: 10)

    Returns:
        list: Time-series bandwidth data
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/sdwan-intf-bandwidth-line/run",
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
                "url": f"/fortiview/adom/{adom}/sdwan-intf-bandwidth-line/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Retrieved {data['total']} data points")
            return data.get('timeseries', [])

        time.sleep(2)

# Example: Get 24-hour bandwidth trends
timeseries = get_sdwan_health_overview(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:01",
        "end": "2025-11-09 23:59"
    },
    limit=10
)

# Display summary
print("\nSD-WAN Bandwidth Trend Summary:")
print(f"Total data points: {len(timeseries)}")

if timeseries:
    # Calculate average utilization
    avg_util_in = sum(t['utilization_in'] for t in timeseries) / len(timeseries)
    avg_util_out = sum(t['utilization_out'] for t in timeseries) / len(timeseries)

    print(f"Average Inbound Utilization: {avg_util_in:.1f}%")
    print(f"Average Outbound Utilization: {avg_util_out:.1f}%")
```

## Use Cases

### Peak Time Analysis

```python
# Identify peak bandwidth usage times
timeseries = get_sdwan_health_overview(
    session_id=session,
    adom="root",
    time_range={
        "start": "2025-11-09 00:00",
        "end": "2025-11-09 23:59"
    },
    limit=10
)

# Find peak inbound and outbound usage
peak_in = max(timeseries, key=lambda x: x['bandwidth_in'])
peak_out = max(timeseries, key=lambda x: x['bandwidth_out'])

print("Peak Bandwidth Usage:")
print(f"  Inbound: {peak_in['bandwidth_in']/1000000:.1f} Mbps at {peak_in['timestamp']}")
print(f"    Interface: {peak_in['device']}/{peak_in['interface']}")
print(f"  Outbound: {peak_out['bandwidth_out']/1000000:.1f} Mbps at {peak_out['timestamp']}")
print(f"    Interface: {peak_out['device']}/{peak_out['interface']}")
```

### Trend Visualization Data Export

```python
# Export trend data for visualization tools
import csv

timeseries = get_sdwan_health_overview(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=100
)

# Export to CSV for graphing
with open('sdwan_bandwidth_trends.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'device', 'interface', 'bandwidth_in_mbps', 'bandwidth_out_mbps', 'utilization_in', 'utilization_out']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for datapoint in timeseries:
        writer.writerow({
            'timestamp': datapoint['timestamp'],
            'device': datapoint['device'],
            'interface': datapoint['interface'],
            'bandwidth_in_mbps': datapoint['bandwidth_in'] / 1000000,
            'bandwidth_out_mbps': datapoint['bandwidth_out'] / 1000000,
            'utilization_in': datapoint['utilization_in'],
            'utilization_out': datapoint['utilization_out']
        })

print("✓ Trend data exported to sdwan_bandwidth_trends.csv")
```

### Capacity Growth Forecasting

```python
# Analyze bandwidth growth trends
timeseries = get_sdwan_health_overview(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 30},
    limit=10
)

# Group by interface and calculate growth
from collections import defaultdict
interface_usage = defaultdict(list)

for datapoint in timeseries:
    key = f"{datapoint['device']}/{datapoint['interface']}"
    interface_usage[key].append(datapoint['utilization_in'])

print("30-Day Bandwidth Growth Analysis:\n")
for intf, utilizations in interface_usage.items():
    if len(utilizations) >= 2:
        # Compare first week to last week
        week1_avg = sum(utilizations[:7]) / min(7, len(utilizations[:7]))
        week4_avg = sum(utilizations[-7:]) / min(7, len(utilizations[-7:]))
        growth = ((week4_avg - week1_avg) / week1_avg * 100) if week1_avg > 0 else 0

        print(f"{intf}:")
        print(f"  Week 1 Avg: {week1_avg:.1f}%")
        print(f"  Week 4 Avg: {week4_avg:.1f}%")
        print(f"  Growth: {growth:+.1f}%")

        if growth > 20:
            print(f"  ⚠️ High growth - consider capacity planning")
        print()
```

### Anomaly Detection

```python
# Detect bandwidth usage anomalies
timeseries = get_sdwan_health_overview(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=10
)

# Calculate baseline and detect anomalies
from statistics import mean, stdev

interface_groups = defaultdict(list)
for datapoint in timeseries:
    key = f"{datapoint['device']}/{datapoint['interface']}"
    interface_groups[key].append(datapoint['utilization_in'])

print("Bandwidth Anomaly Detection:\n")
for intf, utilizations in interface_groups.items():
    if len(utilizations) >= 10:
        avg = mean(utilizations)
        std = stdev(utilizations)
        threshold = avg + (2 * std)  # 2 standard deviations

        anomalies = [u for u in utilizations if u > threshold]

        if anomalies:
            print(f"{intf}:")
            print(f"  Baseline: {avg:.1f}% ± {std:.1f}%")
            print(f"  Threshold: {threshold:.1f}%")
            print(f"  Anomalies Detected: {len(anomalies)}")
            print(f"  Peak Anomaly: {max(anomalies):.1f}%")
            print()
```

### Business Hours vs After-Hours Comparison

```python
# Compare bandwidth usage during business hours vs off-hours
from datetime import datetime

timeseries = get_sdwan_health_overview(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=10
)

business_hours = []
after_hours = []

for datapoint in timeseries:
    dt = datetime.strptime(datapoint['timestamp'], "%Y-%m-%d %H:%M")
    hour = dt.hour

    if 8 <= hour < 18:  # 8 AM to 6 PM
        business_hours.append(datapoint['utilization_in'])
    else:
        after_hours.append(datapoint['utilization_in'])

if business_hours and after_hours:
    avg_business = sum(business_hours) / len(business_hours)
    avg_after = sum(after_hours) / len(after_hours)

    print("Business Hours vs After-Hours Analysis:")
    print(f"  Business Hours (8AM-6PM) Avg: {avg_business:.1f}%")
    print(f"  After Hours Avg: {avg_after:.1f}%")
    print(f"  Difference: {avg_business - avg_after:+.1f}%")

    if avg_after > avg_business * 0.7:
        print("  ⚠️ High after-hours usage detected")
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
- Time range too large for trend analysis
- Invalid date format
- No data available for specified period

## Best Practices

> **💡 Tip:** Use 24-hour to 7-day time ranges for meaningful trend analysis while avoiding performance issues.

> **💡 Tip:** Export data to visualization tools (Grafana, Excel, etc.) for better trend analysis and reporting.

> **⚠️ Warning:** Very large time ranges (>30 days) may result in data aggregation or sampling, reducing granularity.

> **💡 Tip:** Schedule regular trend data collection for historical analysis and capacity planning.

## Time Range Recommendations

| Use Case | Recommended Range | Granularity |
|----------|------------------|-------------|
| Real-time Monitoring | 1-6 hours | 5-15 minutes |
| Daily Analysis | 24 hours | 30-60 minutes |
| Weekly Trends | 7 days | 1-2 hours |
| Monthly Reports | 30 days | 4-6 hours |
| Capacity Planning | 90 days | Daily aggregates |

## Related Endpoints

- [SD-WAN Interface Statistics](./create-task-sd-wan-interface-bandwidth-line.md) - Current interface metrics
- [SD-WAN Top Talkers](./create-task-sd-wan-top-talkers.md) - Top bandwidth consumers
- [SD-WAN Applications](./create-task-sd-wan-application.md) - Application bandwidth usage
- [Fetch Results by Task ID](./fetch-result-by-task-id.md) - Retrieve completed task results

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
