# Create IOC Analysis Task

Create an Indicator of Compromise (IOC) threat analysis task to identify security threats and compromised endpoints.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This example shows how to create an IOC analysis task to identify threats across your network - useful for:
- Real-time threat detection and analysis
- Identifying compromised endpoints and users
- Security incident investigation
- Threat hunting across network traffic
- IOC signature matching against logs
- Post-incident forensic analysis

This operation uses the **two-step asynchronous pattern**. Submit the task, receive a Task ID (TID), then poll for results.

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
- IOC feature enabled on FortiAnalyzer
- UEBA configured for IOC detection
- Device filters configured properly

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `apiver` | `integer` | No | `3` | API version |
| `device` | `array` | Yes | - | Device filter specification |
| `filter` | `string` | No | `""` | Additional filter expression |
| `time-range` | `object` | Yes | - | Time range for analysis |
| `case-sensitive` | `boolean` | No | `false` | Case-sensitive filtering |

### Device Filter

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `└─ devid` | `string` | Yes | Device ID or "All_Devices" |

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
        "url": "/fortiview/adom/root/top-threats/run",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_Devices"
        }],
        "filter": "",
        "time-range": {
            "start": "2025-11-10 00:00",
            "end": "2025-11-10 23:59"
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
            "tid": 12470
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/fortiview/adom/root/top-threats/run"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_ioc_analysis_task(session_id, adom, time_range, device_filter="All_Devices"):
    """
    Create IOC threat analysis task

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        device_filter: Device ID or "All_Devices" (default)

    Returns:
        int: Task ID (TID)
    """
    url = "https://faz.example.com/jsonrpc"

    # Step 1: Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-threats/run",
            "apiver": 3,
            "case-sensitive": False,
            "device": [{"devid": device_filter}],
            "filter": "",
            "time-range": time_range
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    tid = response.json()['result'][0]['data']['tid']
    print(f"✓ IOC analysis task created. TID: {tid}")

    return tid

def poll_ioc_task(session_id, adom, tid):
    """
    Poll IOC task until complete

    Args:
        session_id: Active session ID
        adom: ADOM name
        tid: Task ID

    Returns:
        dict: Completed task data
    """
    url = "https://faz.example.com/jsonrpc"

    while True:
        poll_payload = {
            "method": "get",
            "params": [{
                "url": f"/fortiview/adom/{adom}/top-threats/run/{tid}",
                "apiver": 3
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            print(f"✓ IOC analysis complete. Found {data['total']} threats")
            return data

        print(f"  Progress: {data['percentage']}%")
        time.sleep(2)

# Example usage
tid = create_ioc_analysis_task(
    session_id="your_session_id",
    adom="root",
    time_range={
        "start": "2025-11-10 00:00",
        "end": "2025-11-10 23:59"
    }
)

# Poll for completion
results = poll_ioc_task(
    session_id="your_session_id",
    adom="root",
    tid=tid
)

# Display threat summary
for threat in results.get('threats', [])[:10]:
    print(f"Threat: {threat['threat']} | Severity: {threat['severity']} | Events: {threat['incidents']}")
```

## Use Cases

### Security Incident Investigation

```python
# Investigate specific time window after security alert
tid = create_ioc_analysis_task(
    session_id=session,
    adom="root",
    time_range={
        "start": "2025-11-10 14:30",  # Time of alert
        "end": "2025-11-10 15:30"     # 1 hour window
    },
    device_filter="All_Devices"
)

results = poll_ioc_task(session, "root", tid)

# Identify affected systems
affected_ips = set()
for threat in results.get('threats', []):
    affected_ips.update(threat.get('sources', []))

print(f"Compromised endpoints detected: {len(affected_ips)}")
for ip in affected_ips:
    print(f"  - {ip}")
```

### Daily Threat Summary Report

```python
# Generate daily IOC threat summary
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)

tid = create_ioc_analysis_task(
    session_id=session,
    adom="root",
    time_range={
        "start": yesterday.strftime("%Y-%m-%d 00:00"),
        "end": yesterday.strftime("%Y-%m-%d 23:59")
    }
)

results = poll_ioc_task(session, "root", tid)

# Generate summary report
critical_threats = [t for t in results['threats'] if t['severity'] == 'critical']
high_threats = [t for t in results['threats'] if t['severity'] == 'high']

print(f"Daily Threat Summary for {yesterday.strftime('%Y-%m-%d')}:")
print(f"  Critical: {len(critical_threats)} threats")
print(f"  High: {len(high_threats)} threats")
print(f"  Total Events: {sum(t['incidents'] for t in results['threats'])}")
```

### Targeted Device Analysis

```python
# Analyze specific device for IOC matches
suspicious_device = "FGT60F3X17000001"

tid = create_ioc_analysis_task(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    device_filter=suspicious_device
)

results = poll_ioc_task(session, "root", tid)

if results['total'] > 0:
    print(f"⚠️ IOC threats detected on device {suspicious_device}:")
    for threat in results['threats']:
        print(f"  - {threat['threat']} ({threat['severity']}): {threat['incidents']} events")
else:
    print(f"✓ No IOC threats detected on device {suspicious_device}")
```

### Threat Hunting - Unknown Threats

```python
# Search for threats not yet blocked
tid = create_ioc_analysis_task(
    session_id=session,
    adom="root",
    time_range={"last-n-days": 7}
)

results = poll_ioc_task(session, "root", tid)

# Find threats that were detected but not blocked
unblocked_threats = [
    t for t in results['threats']
    if t.get('detected', 0) > 0 and t.get('blocked', 0) == 0
]

if unblocked_threats:
    print("⚠️ Unblocked Threats Detected (Potential Compromise):")
    for threat in unblocked_threats:
        print(f"  {threat['threat']} ({threat['severity']})")
        print(f"    Detected: {threat['detected']} | Sources: {threat['sources']}")
        print(f"    Action Required: Review and update security policies")
        print()
```

### Multi-ADOM Threat Correlation

```python
# Correlate IOC threats across multiple ADOMs
adoms = ["root", "Branch_Office", "Data_Center"]
all_threats = {}

for adom in adoms:
    tid = create_ioc_analysis_task(
        session_id=session,
        adom=adom,
        time_range={"last-n-hours": 24}
    )

    results = poll_ioc_task(session, adom, tid)
    all_threats[adom] = results['threats']
    print(f"✓ {adom}: {len(results['threats'])} unique threats detected")

# Find threats appearing in multiple ADOMs (potentially widespread attack)
from collections import Counter
threat_names = Counter()
for adom, threats in all_threats.items():
    for t in threats:
        threat_names[t['threat']] += 1

widespread_threats = {name: count for name, count in threat_names.items() if count > 1}

if widespread_threats:
    print("\n⚠️ Widespread Threats Detected Across Multiple ADOMs:")
    for threat, adom_count in widespread_threats.items():
        print(f"  {threat}: Present in {adom_count} ADOMs")
```

## Best Practices

> **💡 Tip:** Run IOC analysis tasks regularly (hourly or daily) to maintain continuous threat visibility and early detection.

> **💡 Tip:** Use specific time ranges for faster task completion. Broader time ranges (7+ days) take longer to process.

> **⚠️ Warning:** IOC task IDs expire after 15-30 minutes. Fetch results promptly after task completion.

> **💡 Tip:** Combine IOC analysis with UEBA endpoint data for comprehensive threat intelligence gathering.

## Task Lifecycle

1. **Created** - Task submitted, TID assigned
2. **Running** - IOC analysis in progress (percentage < 100)
3. **Done** - Analysis complete (percentage = 100)
4. **Expired** - Task results no longer available

**Typical task lifetime:** 15-30 minutes depending on FortiAnalyzer configuration and data volume.

## Related Endpoints

- [Fetch IOC Results by Task ID](./fetch-ioc-result-by-task.md) - Retrieve IOC analysis results
- [IOC Drilldown Request](./ioc-drilldown-fgt-request.md) - Device-specific IOC investigation
- [Configure IOC Rescan](../fortiviewioc/set-ioc-rescan.md) - Historical IOC scanning settings
- [Get UEBA Endpoints](../fabric-viewasset-identity-center/get-ueba-endpoints-by-epid.md) - Endpoint threat intelligence

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
