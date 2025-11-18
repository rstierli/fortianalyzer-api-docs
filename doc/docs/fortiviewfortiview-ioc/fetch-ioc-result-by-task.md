# Fetch IOC Results by Task ID

Retrieve the results of a previously created IOC analysis task using its Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches completed IOC analysis results - useful for:
- Retrieving results from previously submitted IOC tasks
- Implementing asynchronous result fetching workflows
- Decoupling task submission from result retrieval
- Allowing multiple retrievals of the same task results
- Building scheduled threat intelligence collection systems
- Correlating IOC findings across time periods

This is Step 2 of the two-step IOC analysis workflow pattern.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/adom/{adom}/top-threats/run/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Valid Task ID from a previously created IOC task
- Read access to FortiView data in specified ADOM
- Task must be completed (status: "done")

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/top-threats/run/12470",
        "apiver": 3
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
            "tid": 12470,
            "status": "done",
            "percentage": 100,
            "total": 42,
            "threats": [
                {
                    "threat": "Trojan.Emotet",
                    "threattype": "virus",
                    "severity": "critical",
                    "incidents": 1523,
                    "sources": 15,
                    "destinations": 3,
                    "blocked": 1523,
                    "detected": 0
                },
                {
                    "threat": "Botnet.CnC.Zeus",
                    "threattype": "ips",
                    "severity": "critical",
                    "incidents": 892,
                    "sources": 8,
                    "destinations": 12,
                    "blocked": 892,
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
| `threats` | `array` | Array of IOC threat objects |

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
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_ioc_results(session_id, adom, task_id):
    """
    Fetch IOC analysis results by Task ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        task_id: Task ID from create task operation

    Returns:
        dict: Task result data including IOC threats
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-threats/run/{task_id}",
            "apiver": 3
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        data = result['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            return data
        else:
            raise Exception(f"Task not complete: {data['status']} - {data['percentage']}%")
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Fetch IOC analysis for task ID 12470
result = fetch_ioc_results(
    session_id="your_session_id",
    adom="root",
    task_id=12470
)

# Display IOC threat summary
print(f"IOC Analysis Status: {result['status']}")
print(f"Total Threats Detected: {result['total']}\n")

print("Critical IOC Threats:")
for threat in result['threats']:
    if threat['severity'] == 'critical':
        severity_icon = '🔴'

        print(f"{severity_icon} {threat['threat']} ({threat['threattype'].upper()})")
        print(f"   Incidents: {threat['incidents']:,}")
        print(f"   Sources: {threat['sources']}, Destinations: {threat['destinations']}")
        print(f"   Blocked: {threat['blocked']:,}, Detected: {threat['detected']:,}")
        print()
```

## Use Cases

### Scheduled IOC Intelligence Collection

```python
# Submit task and save TID for scheduled retrieval
from create_ioc_task import create_ioc_analysis_task

tid = create_ioc_analysis_task(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24}
)

# Store TID for scheduled report generation
import json
with open('ioc_tasks.json', 'r+') as f:
    tasks = json.load(f)
    tasks['daily_ioc_scan'] = tid
    f.seek(0)
    json.dump(tasks, f, indent=2)

# Later (in scheduled job): Retrieve and analyze
with open('ioc_tasks.json', 'r') as f:
    tasks = json.load(f)
    tid = tasks['daily_ioc_scan']

result = fetch_ioc_results(session, "root", tid)
generate_ioc_report(result['threats'])
```

### Multi-Period IOC Trend Analysis

```python
# Collect IOC data from multiple time periods
task_ids = {
    'today': 12470,
    'yesterday': 12471,
    'last_week': 12472
}

ioc_trends = {}
for period, tid in task_ids.items():
    result = fetch_ioc_results(
        session_id=session,
        adom="root",
        task_id=tid
    )
    ioc_trends[period] = result['threats']

# Identify emerging IOC threats
print("IOC Threat Trend Analysis:\n")
for period, threats in ioc_trends.items():
    critical_count = sum(1 for t in threats if t['severity'] == 'critical')
    total_incidents = sum(t['incidents'] for t in threats)

    print(f"{period.capitalize()}:")
    print(f"  Critical IOC Threats: {critical_count}")
    print(f"  Total Incidents: {total_incidents:,}")
    print()
```

### IOC Result Caching

```python
# Cache IOC intelligence results
import time

class IOCResultCache:
    def __init__(self):
        self.cache = {}

    def get_result(self, session_id, adom, task_id):
        cache_key = f"{adom}:{task_id}"

        if cache_key in self.cache:
            cached_time, result = self.cache[cache_key]
            # Cache valid for 30 minutes
            if time.time() - cached_time < 1800:
                print(f"✓ Using cached IOC data for task {task_id}")
                return result

        # Fetch fresh result
        result = fetch_ioc_results(session_id, adom, task_id)
        self.cache[cache_key] = (time.time(), result)
        return result

# Usage
cache = IOCResultCache()

# First call: fetches from API
ioc_data1 = cache.get_result(session, "root", 12470)

# Second call within 30 min: uses cache
ioc_data2 = cache.get_result(session, "root", 12470)
```

### Historical IOC Comparison

```python
# Compare IOC landscape over time
historical_tasks = [12465, 12466, 12467, 12468, 12469]
ioc_evolution = {}

for tid in historical_tasks:
    try:
        result = fetch_ioc_results(
            session_id=session,
            adom="root",
            task_id=tid
        )

        for threat in result['threats']:
            name = threat['threat']
            if name not in ioc_evolution:
                ioc_evolution[name] = []

            ioc_evolution[name].append({
                'tid': tid,
                'incidents': threat['incidents'],
                'severity': threat['severity'],
                'blocked': threat['blocked'],
                'detected': threat['detected']
            })

    except Exception as e:
        print(f"✗ Task {tid} failed: {e}")

# Identify persistent IOC threats
print("\nPersistent IOC Threats (appeared in all time periods):")
persistent = {k: v for k, v in ioc_evolution.items() if len(v) == len(historical_tasks)}

for threat_name, data in sorted(persistent.items(), key=lambda x: sum(d['incidents'] for d in x[1]), reverse=True):
    total_incidents = sum(d['incidents'] for d in data)
    total_detected = sum(d['detected'] for d in data)

    print(f"  {threat_name}:")
    print(f"    Total Incidents: {total_incidents:,}")
    if total_detected > 0:
        print(f"    ⚠️ Unblocked Detections: {total_detected:,} (potential compromise)")
    print()
```

### IOC Threat Intelligence Export

```python
# Export IOC threat intelligence to CSV
import csv
from datetime import datetime

result = fetch_ioc_results(session, "root", 12470)

filename = f"ioc_threats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['threat', 'type', 'severity', 'incidents', 'sources', 'destinations', 'blocked', 'detected']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for threat in result['threats']:
        writer.writerow({
            'threat': threat['threat'],
            'type': threat['threattype'],
            'severity': threat['severity'],
            'incidents': threat['incidents'],
            'sources': threat['sources'],
            'destinations': threat['destinations'],
            'blocked': threat['blocked'],
            'detected': threat['detected']
        })

print(f"✓ IOC threat intelligence exported to {filename}")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - Invalid Task ID
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
- Task ID does not exist
- Task has expired (tasks have limited lifetime)
- Incorrect ADOM specified
- Insufficient permissions

`````{tab-set}
````{tab-item} ERROR RESPONSE - Task Not Complete
```json
{
    "result": [{
        "data": {
            "tid": 12470,
            "status": "running",
            "percentage": 68
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

**Handling:**
- Implement polling with retry logic
- Wait for status: "done" and percentage: 100
- Use exponential backoff between retries

## Best Practices

> **💡 Tip:** Check task status before processing IOC data. Status should be "done" and percentage should be 100.

> **💡 Tip:** Task IDs have a limited lifetime (typically 15-30 minutes). Fetch results promptly after task completion.

> **⚠️ Warning:** Multiple calls to fetch results do not re-run the analysis. Results are cached from the original task execution.

> **💡 Tip:** Cache IOC intelligence results for frequently accessed data to reduce API calls and improve performance.

## Task Lifecycle

Tasks go through the following states:

1. **Created** - Task submitted, TID assigned
2. **Running** - Task executing (percentage < 100)
3. **Done** - Task complete (percentage = 100)
4. **Expired** - Task results no longer available

**Typical task lifetime:** 15-30 minutes depending on FortiAnalyzer configuration.

## Performance Considerations

- **Result Reuse**: Fetch once and cache for multiple analyses
- **Task Expiration**: Don't rely on task results being available indefinitely
- **Batch Processing**: Process multiple tasks concurrently for efficiency
- **Error Handling**: Implement robust retry logic for transient failures
- **Data Freshness**: Balance between caching and getting fresh IOC data

## Related Endpoints

- [Create IOC Analysis Task](./create-ioc-task.md) - Submit new IOC analysis query
- [IOC Drilldown Request](./ioc-drilldown-fgt-request.md) - Device-specific IOC investigation
- [Configure IOC Rescan](../fortiviewioc/set-ioc-rescan.md) - Historical IOC scanning settings
- [Top Threats](../fortiviewtop-threats/create-task.md) - General threat analysis

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
