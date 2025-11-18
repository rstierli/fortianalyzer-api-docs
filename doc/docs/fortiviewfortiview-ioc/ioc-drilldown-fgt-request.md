# IOC Blacklist Drilldown - Device-Specific

Drill down into IOC blacklist threat detections for a specific FortiGate device to investigate compromised endpoints.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint performs device-specific IOC blacklist drilldown analysis - useful for:
- Investigating blacklisted IPs/domains detected on specific FortiGate devices
- Analyzing threat detection events at device granularity
- Identifying compromised endpoints behind specific gateways
- Forensic analysis of IOC matches on individual devices
- Fabric-aware threat correlation across Security Fabric
- Device-level threat hunting and incident response

This endpoint targets a specific device and VDOM for detailed IOC blacklist analysis.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/dev/{device_id}/vdom/{vdom}/threat-detect-drilldown-blacklist/run`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- Valid device ID for target FortiGate
- VDOM name (typically "root" for single-VDOM configs)
- IOC blacklist feature enabled
- Security Fabric configuration (if using CSF)

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `device_id` | `string` | Yes | - | FortiGate device ID (serial number) |
| `vdom` | `string` | Yes | - | VDOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | No | - | Device/Fabric filter specification |
| `filter` | `string` | Yes | - | Filter expression (e.g., "devid=...") |
| `sort-by` | `array` | No | - | Sorting specification |
| `limit` | `integer` | No | `100` | Number of results to return |
| `offset` | `integer` | No | `0` | Starting position for pagination |
| `time-range` | `object` | Yes | - | Time range for analysis |
| `case-sensitive` | `boolean` | No | `false` | Case-sensitive filtering |

### Device/Fabric Filter

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ csfname` | `string` | No | Security Fabric name |

### Sort By Specification

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ field` | `string` | Yes | Field to sort by (e.g., "event_num") |
| `└─ order` | `string` | Yes | Sort order: "asc" or "desc" |

### Time Range Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ start` | `string` | Yes | Start time: "YYYY-MM-DD HH:MM" |
| `└─ end` | `string` | Yes | End time: "YYYY-MM-DD HH:MM" |
| `└─ tz` | `string` | No | Timezone offset (e.g., "-7:00") |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/dev/FG100FTK00000001/vdom/root/threat-detect-drilldown-blacklist/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "csfname": "my40Fabric"
        }],
        "filter": "devid=FG100FTK00000001",
        "sort-by": [{
            "field": "event_num",
            "order": "desc"
        }],
        "limit": 100,
        "offset": 0,
        "time-range": {
            "start": "2025-11-10 00:00",
            "end": "2025-11-10 23:59",
            "tz": "-7:00"
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
            "tid": 12475,
            "events": [
                {
                    "event_num": 1523,
                    "srcip": "10.0.10.45",
                    "dstip": "185.220.101.45",
                    "threat": "Blacklist.IP.Botnet",
                    "severity": "critical",
                    "action": "blocked",
                    "timestamp": "2025-11-10 14:32:15",
                    "srcintf": "internal",
                    "dstintf": "wan1"
                },
                {
                    "event_num": 1524,
                    "srcip": "10.0.10.78",
                    "dstip": "malicious-domain.com",
                    "threat": "Blacklist.Domain.CnC",
                    "severity": "critical",
                    "action": "blocked",
                    "timestamp": "2025-11-10 14:35:22",
                    "srcintf": "internal",
                    "dstintf": "wan1"
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ioc_blacklist_drilldown(session_id, device_id, vdom, time_range, fabric_name=None, limit=100):
    """
    Perform IOC blacklist drilldown for specific device

    Args:
        session_id: Active session ID
        device_id: FortiGate device ID (serial number)
        vdom: VDOM name (e.g., "root")
        time_range: Time range dict with 'start', 'end', optional 'tz'
        fabric_name: Security Fabric name (optional)
        limit: Number of events to return (default: 100)

    Returns:
        dict: IOC blacklist events for device
    """
    url = "https://faz.example.com/jsonrpc"

    params_data = {
        "url": f"/fortiview/dev/{device_id}/vdom/{vdom}/threat-detect-drilldown-blacklist/run",
        "apiver": 3,
        "case-sensitive": False,
        "filter": f"devid={device_id}",
        "sort-by": [{
            "field": "event_num",
            "order": "desc"
        }],
        "limit": limit,
        "offset": 0,
        "time-range": time_range
    }

    # Add Security Fabric filter if specified
    if fabric_name:
        params_data["device"] = [{"csfname": fabric_name}]

    payload = {
        "method": "add",
        "params": [params_data],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Investigate specific FortiGate device
events = ioc_blacklist_drilldown(
    session_id="your_session_id",
    device_id="FG100FTK00000001",
    vdom="root",
    time_range={
        "start": "2025-11-10 00:00",
        "end": "2025-11-10 23:59",
        "tz": "-7:00"
    },
    fabric_name="my40Fabric",
    limit=100
)

# Display blacklist events
print(f"IOC Blacklist Events for Device FG100FTK00000001:\n")
for event in events.get('events', []):
    print(f"Event #{event['event_num']}: {event['threat']} ({event['severity']})")
    print(f"  Source: {event['srcip']} → Destination: {event['dstip']}")
    print(f"  Action: {event['action']} | Time: {event['timestamp']}")
    print(f"  Interface: {event['srcintf']} → {event['dstintf']}")
    print()
```

## Use Cases

### Incident Response - Compromised Device Investigation

```python
# Investigate specific device after security alert
suspicious_device = "FG100FTK00000001"

events = ioc_blacklist_drilldown(
    session_id=session,
    device_id=suspicious_device,
    vdom="root",
    time_range={
        "start": "2025-11-10 14:00",  # Time of alert
        "end": "2025-11-10 15:00"     # 1 hour window
    },
    limit=500
)

# Identify compromised internal hosts
compromised_hosts = set()
for event in events.get('events', []):
    if event['action'] == 'detected':  # Not blocked
        compromised_hosts.add(event['srcip'])

if compromised_hosts:
    print(f"⚠️ Potentially Compromised Hosts on {suspicious_device}:")
    for host in compromised_hosts:
        print(f"  - {host}")
    print("\nRecommendation: Isolate and investigate these endpoints immediately.")
else:
    print(f"✓ All IOC blacklist threats blocked on {suspicious_device}")
```

### Security Fabric Threat Correlation

```python
# Correlate blacklist detections across Security Fabric
fabric_devices = [
    {"id": "FG100FTK00000001", "vdom": "root"},
    {"id": "FG60F3X17000045", "vdom": "root"},
    {"id": "FG200E4Q17000789", "vdom": "root"}
]

fabric_name = "my40Fabric"
fabric_threats = {}

for device in fabric_devices:
    try:
        events = ioc_blacklist_drilldown(
            session_id=session,
            device_id=device['id'],
            vdom=device['vdom'],
            time_range={"last-n-hours": 24},
            fabric_name=fabric_name,
            limit=100
        )

        fabric_threats[device['id']] = events.get('events', [])
        print(f"✓ {device['id']}: {len(events.get('events', []))} blacklist events")

    except Exception as e:
        print(f"✗ {device['id']}: {e}")

# Find threats appearing on multiple devices (fabric-wide attack)
from collections import Counter
threat_names = Counter()

for device_id, events in fabric_threats.items():
    for event in events:
        threat_names[event['threat']] += 1

widespread_threats = {name: count for name, count in threat_names.items() if count > 1}

if widespread_threats:
    print("\n⚠️ Fabric-Wide IOC Threats Detected:")
    for threat, device_count in widespread_threats.items():
        print(f"  {threat}: Detected on {device_count} devices")
```

### Top Blacklisted Destinations

```python
# Identify most frequently blocked malicious destinations
events = ioc_blacklist_drilldown(
    session_id=session,
    device_id="FG100FTK00000001",
    vdom="root",
    time_range={"last-n-days": 7},
    limit=1000
)

# Count destination IPs/domains
from collections import Counter
blocked_destinations = Counter()

for event in events.get('events', []):
    if event['action'] == 'blocked':
        blocked_destinations[event['dstip']] += 1

print("Top 10 Blacklisted Destinations (7 Days):\n")
print(f"{'Destination':<40} {'Block Count'}")
print("-" * 60)

for dest, count in blocked_destinations.most_common(10):
    print(f"{dest:<40} {count:>10,}")
```

### Internal Host IOC Activity Summary

```python
# Summarize IOC activity by internal source IP
events = ioc_blacklist_drilldown(
    session_id=session,
    device_id="FG100FTK00000001",
    vdom="root",
    time_range={"last-n-hours": 24},
    limit=1000
)

# Group events by source IP
from collections import defaultdict
host_activity = defaultdict(lambda: {'blocked': 0, 'detected': 0, 'threats': set()})

for event in events.get('events', []):
    srcip = event['srcip']
    action = event['action']

    if action == 'blocked':
        host_activity[srcip]['blocked'] += 1
    elif action == 'detected':
        host_activity[srcip]['detected'] += 1

    host_activity[srcip]['threats'].add(event['threat'])

# Identify high-risk hosts
print("High-Risk Internal Hosts (24h):\n")
print(f"{'Source IP':<20} {'Blocked':<10} {'Detected':<10} {'Unique Threats'}")
print("-" * 65)

for srcip, stats in sorted(host_activity.items(), key=lambda x: x[1]['detected'], reverse=True):
    if stats['detected'] > 0 or stats['blocked'] > 10:  # High activity
        risk_indicator = "⚠️" if stats['detected'] > 0 else "ℹ️"
        print(f"{risk_indicator} {srcip:<18} {stats['blocked']:<10} {stats['detected']:<10} {len(stats['threats'])}")
```

### Blacklist Event Timeline Export

```python
# Export device-specific IOC blacklist timeline to CSV
import csv
from datetime import datetime

events = ioc_blacklist_drilldown(
    session_id=session,
    device_id="FG100FTK00000001",
    vdom="root",
    time_range={
        "start": "2025-11-10 00:00",
        "end": "2025-11-10 23:59"
    },
    limit=1000
)

filename = f"ioc_blacklist_FG100FTK00000001_{datetime.now().strftime('%Y%m%d')}.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'event_num', 'srcip', 'dstip', 'threat', 'severity', 'action', 'srcintf', 'dstintf']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for event in events.get('events', []):
        writer.writerow({
            'timestamp': event['timestamp'],
            'event_num': event['event_num'],
            'srcip': event['srcip'],
            'dstip': event['dstip'],
            'threat': event['threat'],
            'severity': event['severity'],
            'action': event['action'],
            'srcintf': event['srcintf'],
            'dstintf': event['dstintf']
        })

print(f"✓ IOC blacklist timeline exported to {filename}")
```

## Best Practices

> **💡 Tip:** Use device-specific drilldown when investigating alerts originating from specific FortiGate devices for faster root cause analysis.

> **💡 Tip:** Sort by `event_num` in descending order to see most recent blacklist events first.

> **⚠️ Warning:** Large time ranges or high `limit` values may impact performance. Use pagination for large result sets.

> **💡 Tip:** Combine with Security Fabric filtering (`csfname`) for fabric-wide threat correlation across multiple devices.

## Device Identification

**Finding Device ID:**
- Device ID is typically the FortiGate serial number
- Can be found using [Get Devices](../device-manager/get-devices-no-filter.md) endpoint
- Example format: `FG100FTK00000001`, `FG60F3X17000045`

**VDOM Name:**
- Use "root" for single-VDOM configurations
- Use specific VDOM name for multi-VDOM deployments
- VDOM list available via device management endpoints

## Related Endpoints

- [Create IOC Analysis Task](./create-ioc-task.md) - Submit IOC threat analysis
- [Fetch IOC Results by Task ID](./fetch-ioc-result-by-task.md) - Retrieve IOC analysis results
- [Configure IOC Rescan](../fortiviewioc/set-ioc-rescan.md) - Historical IOC scanning settings
- [Get Devices](../device-manager/get-devices-no-filter.md) - List managed devices

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
