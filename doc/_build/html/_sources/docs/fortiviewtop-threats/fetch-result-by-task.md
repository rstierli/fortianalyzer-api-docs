# Fetch Top Threats Results by Task ID

Retrieve the results of a previously created top threats task using its Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches completed top threats results - useful for:
- Retrieving results from a previously submitted threat analysis task
- Implementing asynchronous result fetching patterns
- Building decoupled task submission and result retrieval workflows
- Allowing multiple result retrievals from the same task
- Enabling result caching for threat intelligence analysis
- Scheduled threat monitoring and reporting workflows

This endpoint is part of the two-step FortiView workflow. First create a task with [Create Top Threats Task](./create-task.md), then use this endpoint to fetch the results.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/adom/{adom}/top-threats/run/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Valid Task ID from a previously created top threats task
- Read access to FortiView data in specified ADOM
- Task must be completed (status: "done")

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `taskID` | `integer` | Yes | - | Task ID from create task operation |
| `apiver` | `integer` | No | `3` | API version |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/fortiview/adom/root/top-threats/run/12460",
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_top_threats_result(session_id, adom, task_id):
    """
    Fetch top threats results by Task ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        task_id: Task ID from create task operation

    Returns:
        dict: Task result data including threats
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

# Example: Fetch results for task ID 12460
result = fetch_top_threats_result(
    session_id="your_session_id",
    adom="root",
    task_id=12460
)

# Display results
print(f"Task Status: {result['status']}")
print(f"Total Threats: {result['total']}\n")

print("Top Threats by Incident Count:")
for i, threat in enumerate(result['threats'], 1):
    severity_icon = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }.get(threat['severity'], '⚪')

    print(f"{i}. {threat['threat']} {severity_icon}")
    print(f"   Type: {threat['threattype'].upper()}, Severity: {threat['severity'].upper()}")
    print(f"   Incidents: {threat['incidents']:,}")
    print(f"   Sources: {threat['sources']}, Destinations: {threat['destinations']}")
    print(f"   Blocked: {threat['blocked']:,}, Detected: {threat['detected']:,}")
    print()
```

## Use Cases

### Scheduled Threat Intelligence Collection

```python
# Submit task and save TID for scheduled retrieval
from create_task import create_top_threats_task

tid = create_top_threats_task(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24},
    threat_type="ips"
)

# Store TID for scheduled report generation
import json
with open('threat_tasks.json', 'r+') as f:
    tasks = json.load(f)
    tasks['daily_threat_intel'] = tid
    f.seek(0)
    json.dump(tasks, f, indent=2)

# Later (in scheduled job): Retrieve and analyze
with open('threat_tasks.json', 'r') as f:
    tasks = json.load(f)
    tid = tasks['daily_threat_intel']

result = fetch_top_threats_result(session, "root", tid)
generate_threat_report(result['threats'])
```

### Multi-Period Threat Trend Analysis

```python
# Collect threat data from multiple time periods
task_ids = {
    'today': 12460,
    'yesterday': 12461,
    'last_week': 12462
}

threat_trends = {}
for period, tid in task_ids.items():
    result = fetch_top_threats_result(
        session_id=session,
        adom="root",
        task_id=tid
    )
    threat_trends[period] = result['threats']

# Identify emerging threats
print("Threat Trend Analysis:\n")
for period, threats in threat_trends.items():
    critical_count = sum(1 for t in threats if t['severity'] == 'critical')
    total_incidents = sum(t['incidents'] for t in threats)
    print(f"{period.capitalize()}:")
    print(f"  Critical Threats: {critical_count}")
    print(f"  Total Incidents: {total_incidents:,}")
    print()
```

### Threat Result Caching

```python
# Cache threat intelligence results
import time

class ThreatResultCache:
    def __init__(self):
        self.cache = {}

    def get_result(self, session_id, adom, task_id):
        cache_key = f"{adom}:{task_id}"

        if cache_key in self.cache:
            cached_time, result = self.cache[cache_key]
            # Cache valid for 30 minutes
            if time.time() - cached_time < 1800:
                print(f"✓ Using cached threat data for task {task_id}")
                return result

        # Fetch fresh result
        result = fetch_top_threats_result(session_id, adom, task_id)
        self.cache[cache_key] = (time.time(), result)
        return result

# Usage
cache = ThreatResultCache()

# First call: fetches from API
threats1 = cache.get_result(session, "root", 12460)

# Second call within 30 min: uses cache
threats2 = cache.get_result(session, "root", 12460)
```

### Historical Threat Comparison

```python
# Compare threat landscape over time
historical_tasks = [12455, 12456, 12457, 12458, 12459]
threat_evolution = {}

for tid in historical_tasks:
    try:
        result = fetch_top_threats_result(
            session_id=session,
            adom="root",
            task_id=tid
        )

        for threat in result['threats']:
            name = threat['threat']
            if name not in threat_evolution:
                threat_evolution[name] = []

            threat_evolution[name].append({
                'tid': tid,
                'incidents': threat['incidents'],
                'severity': threat['severity']
            })

    except Exception as e:
        print(f"✗ Task {tid} failed: {e}")

# Identify persistent threats
print("\nPersistent Threats (appeared in all time periods):")
persistent = {k: v for k, v in threat_evolution.items() if len(v) == len(historical_tasks)}
for threat_name, data in sorted(persistent.items(), key=lambda x: sum(d['incidents'] for d in x[1]), reverse=True):
    total_incidents = sum(d['incidents'] for d in data)
    print(f"  {threat_name}: {total_incidents:,} total incidents")
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
            "tid": 12460,
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

> **💡 Tip:** Check task status before processing threat data. Status should be "done" and percentage should be 100.

> **💡 Tip:** Task IDs have a limited lifetime (typically 15-30 minutes). Fetch results promptly after task completion.

> **⚠️ Warning:** Multiple calls to fetch results do not re-run the query. Results are cached from the original task execution.

> **💡 Tip:** Cache threat intelligence results for frequently accessed data to reduce API calls and improve performance.

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
- **Data Freshness**: Balance between caching and getting fresh threat data

## Related Endpoints

- [Create Top Threats Task](./create-task.md) - Submit new top threats query
- [Top Applications](../fortiviewtop-applications/topapplications.md) - Application usage analysis
- [Top Sources](../fortiviewtop-sources/create-task.md) - Analyze traffic sources
- [Search Attack Logs](../logview/create-search-task-for-attack---signature.md) - Detailed IPS logs

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
