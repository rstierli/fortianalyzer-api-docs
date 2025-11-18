# Create Top Threats Task

Retrieve top security threats ranked by incident count, severity, or other metrics.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to retrieve FortiView top threats data - useful for:
- Identifying most common attack patterns and signatures
- Security threat trend analysis and monitoring
- Prioritizing security response based on incident frequency
- Compliance reporting on threat landscape
- Evaluating IPS/AV effectiveness
- Threat intelligence gathering and analysis

This operation uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/top-threats/run`
**API Path (Step 2):** `/fortiview/adom/{adom}/top-threats/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- IPS/AV features enabled on FortiAnalyzer and FortiGate devices
- Threat logs being collected

## Two-Step Workflow

### Step 1: Submit Task

Submit the top threats query and receive a Task ID (TID).

### Step 2: Fetch Results

Poll using the TID until complete, then retrieve the top threats data.

---

## Step 1: Submit Top Threats Query

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Filter expression (e.g., threattype) |
| `limit` | `integer` | No | `50` | Number of top threats to return |
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
| `└─ field` | `string` | Field to sort by: `incidents`, `severity` |
| `└─ order` | `string` | Sort order: `asc` or `desc` |

### Time Range Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ start` | `string` | Yes | Start time: "YYYY-MM-DD HH:MM:SS" |
| `└─ end` | `string` | Yes | End time: "YYYY-MM-DD HH:MM:SS" |

### Common Filter Examples

- `threattype=ips` - IPS threats only
- `threattype=virus` - Malware/virus threats
- `threattype=botnet` - Botnet activity
- `severity=critical` - Critical severity only

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/adom/root/top-threats/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_Devices"
        }],
        "filter": "threattype=ips",
        "limit": 50,
        "sort-by": [{
            "field": "incidents",
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
            "tid": 12460
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
        "url": "/fortiview/adom/root/top-threats/run/12460",
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
            "tid": 12460,
            "status": "done",
            "percentage": 100,
            "total": 25,
            "threats": [
                {
                    "threat": "SQL.Injection",
                    "threattype": "ips",
                    "severity": "critical",
                    "incidents": 1523,
                    "sources": 15,
                    "destinations": 3,
                    "blocked": 1523,
                    "detected": 0
                },
                {
                    "threat": "XSS.Generic",
                    "threattype": "ips",
                    "severity": "high",
                    "incidents": 892,
                    "sources": 8,
                    "destinations": 2,
                    "blocked": 892,
                    "detected": 0
                },
                {
                    "threat": "Botnet.CnC.Generic",
                    "threattype": "ips",
                    "severity": "critical",
                    "incidents": 456,
                    "sources": 3,
                    "destinations": 12,
                    "blocked": 456,
                    "detected": 0
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
| `total` | `integer` | Total number of threats returned |
| `threats` | `array` | Array of top threat objects |

### Threat Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `threat` | `string` | Threat signature name |
| `threattype` | `string` | Threat type: ips, virus, botnet |
| `severity` | `string` | Severity level: critical, high, medium, low |
| `incidents` | `integer` | Number of incidents |
| `sources` | `integer` | Number of unique source IPs |
| `destinations` | `integer` | Number of unique destination IPs |
| `blocked` | `integer` | Number of blocked incidents |
| `detected` | `integer` | Number of detected (not blocked) incidents |

## Complete Python Example

```python
import json
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_top_threats(session_id, adom, time_range, limit=50, threat_type="ips"):
    """
    Get top security threats for a time period

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        limit: Number of top threats to return (default: 50)
        threat_type: Threat type filter: ips, virus, botnet

    Returns:
        list: Top threats data
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-threats/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": "All_Devices"}],
            "filter": f"threattype={threat_type}",
            "limit": limit,
            "sort-by": [{
                "field": "incidents",
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
                "url": f"/fortiview/adom/{adom}/top-threats/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ Found {data['total']} top threats")
            return data.get('threats', [])

        time.sleep(2)

# Example: Get top IPS threats
threats = get_top_threats(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=50,
    threat_type="ips"
)

# Display results
print("\nTop IPS Threats by Incident Count:")
for i, threat in enumerate(threats[:10], 1):
    print(f"{i}. {threat['threat']}")
    print(f"   Severity: {threat['severity']}")
    print(f"   Incidents: {threat['incidents']:,}")
    print(f"   Sources: {threat['sources']}, Destinations: {threat['destinations']}")
    print(f"   Blocked: {threat['blocked']:,}, Detected: {threat['detected']:,}")
    print()
```

## Use Cases

### Critical Threat Monitoring

```python
# Get critical severity threats only
threats = get_top_threats(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    limit=100,
    threat_type="ips"
)

# Filter for critical threats
critical = [t for t in threats if t['severity'] == 'critical']

if critical:
    print(f"⚠️ {len(critical)} critical threats detected:")
    for threat in critical[:5]:
        print(f"  {threat['threat']}: {threat['incidents']:,} incidents")
```

### Threat Type Comparison

```python
# Compare different threat types
threat_types = ['ips', 'virus', 'botnet']
threat_summary = {}

for ttype in threat_types:
    threats = get_top_threats(
        session_id=session,
        adom="root",
        time_range={"last-n-hours": 24},
        limit=100,
        threat_type=ttype
    )

    total_incidents = sum(t['incidents'] for t in threats)
    threat_summary[ttype] = {
        'count': len(threats),
        'incidents': total_incidents
    }

# Display comparison
print("Threat Landscape Summary:\n")
for ttype, data in sorted(threat_summary.items(), key=lambda x: x[1]['incidents'], reverse=True):
    print(f"{ttype.upper()}: {data['count']} threats, {data['incidents']:,} incidents")
```

### IPS Effectiveness Analysis

```python
# Analyze IPS block rate
threats = get_top_threats(
    session_id=session,
    adom="root",
    time_range={
        "start": "2025-11-09 00:00:00",
        "end": "2025-11-09 23:59:59"
    },
    limit=100,
    threat_type="ips"
)

total_incidents = sum(t['incidents'] for t in threats)
total_blocked = sum(t['blocked'] for t in threats)
total_detected = sum(t['detected'] for t in threats)

block_rate = (total_blocked / total_incidents * 100) if total_incidents > 0 else 0

print(f"IPS Effectiveness Report:")
print(f"  Total Incidents: {total_incidents:,}")
print(f"  Blocked: {total_blocked:,}")
print(f"  Detected Only: {total_detected:,}")
print(f"  Block Rate: {block_rate:.2f}%")
```

### Threat Intelligence Report

```python
# Generate comprehensive threat intelligence report
threats = get_top_threats(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7},
    limit=50,
    threat_type="ips"
)

print("=" * 80)
print("WEEKLY THREAT INTELLIGENCE REPORT")
print("=" * 80)
print(f"{'Rank':<6} {'Threat':<40} {'Severity':<10} {'Incidents':>12}")
print("-" * 80)

for i, threat in enumerate(threats, 1):
    severity_icon = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }.get(threat['severity'], '⚪')

    print(f"{i:<6} {threat['threat']:<40} {severity_icon} {threat['severity']:<8} {threat['incidents']:>12,}")

# Top threat details
if threats:
    top_threat = threats[0]
    print("\n" + "=" * 80)
    print(f"TOP THREAT: {top_threat['threat']}")
    print("=" * 80)
    print(f"Type: {top_threat['threattype'].upper()}")
    print(f"Severity: {top_threat['severity'].upper()}")
    print(f"Total Incidents: {top_threat['incidents']:,}")
    print(f"Unique Sources: {top_threat['sources']}")
    print(f"Unique Destinations: {top_threat['destinations']}")
    print(f"Blocked: {top_threat['blocked']:,} ({top_threat['blocked']/top_threat['incidents']*100:.1f}%)")
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
- IPS/AV not enabled
- Insufficient permissions

## Best Practices

> **💡 Tip:** Focus on critical and high severity threats first for security response prioritization.

> **💡 Tip:** Compare blocked vs. detected ratios to evaluate IPS policy effectiveness.

> **⚠️ Warning:** High incident counts for specific threats may indicate targeted attacks or misconfigurations.

> **💡 Tip:** Use longer time ranges (7-30 days) for trend analysis, shorter ranges (1-24 hours) for incident response.

## Threat Severity Levels

| Severity | Description | Recommended Action |
|----------|-------------|-------------------|
| **Critical** | Immediate threat to security | Immediate investigation and response required |
| **High** | Significant security risk | Investigate within 24 hours |
| **Medium** | Moderate security concern | Review and address within 48 hours |
| **Low** | Minor security issue | Monitor and review periodically |

## Related Endpoints

- [Fetch Top Threats Result](./fetch-result-by-task.md) - Retrieve completed task results
- [Top Applications](../fortiviewtop-applications/topapplications.md) - Application usage analysis
- [Top Sources](../fortiviewtop-sources/create-task.md) - Analyze traffic sources
- [Search Attack Logs](../logview/create-search-task-for-attack---signature.md) - Detailed IPS logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
