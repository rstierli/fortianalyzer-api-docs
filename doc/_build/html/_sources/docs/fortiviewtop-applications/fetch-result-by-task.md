# Fetch Top Applications Results by Task ID

Retrieve the results of a previously created top applications task using its Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches completed top applications results - useful for:
- Retrieving results from a previously submitted task
- Implementing asynchronous result fetching patterns
- Building decoupled task submission and result retrieval workflows
- Allowing multiple result retrievals from the same task
- Enabling result caching and delayed processing
- Scheduled reporting and automation workflows

This endpoint is part of the two-step FortiView workflow. First create a task with [Create Top Applications Task](./topapplications.md), then use this endpoint to fetch the results.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/adom/{adom}/top-applications/run/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Valid Task ID from a previously created top applications task
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
        "url": "/fortiview/adom/root/top-applications/run/12455",
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
            "tid": 12455,
            "status": "done",
            "percentage": 100,
            "total": 15,
            "applications": [
                {
                    "app": "YouTube",
                    "appcat": "Video/Audio",
                    "sessions": 8932,
                    "bytes": 4294967296,
                    "bandwidth": 89456789,
                    "policyid": 46,
                    "policyname": "Internet_Access"
                },
                {
                    "app": "Netflix",
                    "appcat": "Video/Audio",
                    "sessions": 5421,
                    "bytes": 3221225472,
                    "bandwidth": 67012345,
                    "policyid": 46,
                    "policyname": "Internet_Access"
                },
                {
                    "app": "Microsoft.Office365",
                    "appcat": "Cloud.IT",
                    "sessions": 4523,
                    "bytes": 536870912,
                    "bandwidth": 11234567,
                    "policyid": 46,
                    "policyname": "Internet_Access"
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
| `total` | `integer` | Total number of applications returned |
| `applications` | `array` | Array of top application objects |

### Application Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `app` | `string` | Application name |
| `appcat` | `string` | Application category |
| `sessions` | `integer` | Number of sessions |
| `bytes` | `integer` | Total bytes transferred |
| `bandwidth` | `integer` | Bandwidth usage (bps) |
| `policyid` | `integer` | Firewall policy ID |
| `policyname` | `string` | Firewall policy name |

## Complete Python Example

```python
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_top_applications_result(session_id, adom, task_id):
    """
    Fetch top applications results by Task ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        task_id: Task ID from create task operation

    Returns:
        dict: Task result data including applications
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-applications/run/{task_id}",
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

# Example: Fetch results for task ID 12455
result = fetch_top_applications_result(
    session_id="your_session_id",
    adom="root",
    task_id=12455
)

# Display results
print(f"Task Status: {result['status']}")
print(f"Total Applications: {result['total']}\n")

for i, app in enumerate(result['applications'], 1):
    print(f"{i}. {app['app']} ({app['appcat']})")
    print(f"   Sessions: {app['sessions']:,}")
    print(f"   Bytes: {app['bytes']:,} ({app['bytes']/1024/1024/1024:.2f} GB)")
    print(f"   Bandwidth: {app['bandwidth']/1000000:.2f} Mbps")
    print(f"   Policy: {app['policyname']} (ID: {app['policyid']})")
    print()
```

## Use Cases

### Scheduled Reporting Workflow

```python
# Submit task and save TID for scheduled retrieval
from create_task import create_top_applications_task

tid = create_top_applications_task(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24}
)

# Store TID for scheduled report generation
import json
with open('scheduled_tasks.json', 'r+') as f:
    tasks = json.load(f)
    tasks['daily_app_report'] = tid
    f.seek(0)
    json.dump(tasks, f, indent=2)

# Later (in scheduled job): Retrieve and process results
with open('scheduled_tasks.json', 'r') as f:
    tasks = json.load(f)
    tid = tasks['daily_app_report']

result = fetch_top_applications_result(session, "root", tid)
generate_report(result['applications'])
```

### Multi-Report Aggregation

```python
# Collect application data from multiple time periods
task_ids = {
    'morning': 12455,
    'afternoon': 12456,
    'evening': 12457
}

all_apps = {}
for period, tid in task_ids.items():
    result = fetch_top_applications_result(
        session_id=session,
        adom="root",
        task_id=tid
    )
    all_apps[period] = result['applications']

# Compare usage across time periods
print("Application Usage Comparison:\n")
for period, apps in all_apps.items():
    total_gb = sum(a['bytes'] for a in apps) / 1024 / 1024 / 1024
    print(f"{period.capitalize()}: {total_gb:.2f} GB - {len(apps)} applications")
```

### Result Caching Pattern

```python
# Cache results to avoid re-querying
import time

class ApplicationResultCache:
    def __init__(self):
        self.cache = {}

    def get_result(self, session_id, adom, task_id):
        cache_key = f"{adom}:{task_id}"

        if cache_key in self.cache:
            cached_time, result = self.cache[cache_key]
            # Cache valid for 5 minutes
            if time.time() - cached_time < 300:
                print(f"✓ Using cached result for task {task_id}")
                return result

        # Fetch fresh result
        result = fetch_top_applications_result(session_id, adom, task_id)
        self.cache[cache_key] = (time.time(), result)
        return result

# Usage
cache = ApplicationResultCache()

# First call: fetches from API
apps1 = cache.get_result(session, "root", 12455)

# Second call: uses cache
apps2 = cache.get_result(session, "root", 12455)
```

### Batch Application Analysis

```python
# Analyze multiple task results for trend analysis
historical_tasks = [12450, 12451, 12452, 12453, 12454]
app_trends = {}

for tid in historical_tasks:
    try:
        result = fetch_top_applications_result(
            session_id=session,
            adom="root",
            task_id=tid
        )

        for app in result['applications']:
            app_name = app['app']
            if app_name not in app_trends:
                app_trends[app_name] = []

            app_trends[app_name].append({
                'tid': tid,
                'bytes': app['bytes'],
                'sessions': app['sessions']
            })

    except Exception as e:
        print(f"✗ Task {tid} failed: {e}")

# Identify trending applications
print("\nTop Trending Applications:")
for app_name, data in sorted(app_trends.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    total_bytes = sum(d['bytes'] for d in data)
    print(f"  {app_name}: {len(data)} occurrences, {total_bytes/1024/1024/1024:.2f} GB total")
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
            "tid": 12455,
            "status": "running",
            "percentage": 72
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

> **💡 Tip:** Check task status before processing results. Status should be "done" and percentage should be 100.

> **💡 Tip:** Task IDs have a limited lifetime (typically 15-30 minutes). Fetch results promptly after task completion.

> **⚠️ Warning:** Multiple calls to fetch results do not re-run the query. Results are cached from the original task execution.

> **💡 Tip:** Use this endpoint for building asynchronous workflows where task submission and result retrieval are separated by time or process.

## Task Lifecycle

Tasks go through the following states:

1. **Created** - Task submitted, TID assigned
2. **Running** - Task executing (percentage < 100)
3. **Done** - Task complete (percentage = 100)
4. **Expired** - Task results no longer available

**Typical task lifetime:** 15-30 minutes depending on FortiAnalyzer configuration.

## Performance Considerations

- **Result Reuse**: Fetch once and cache if multiple analyses are needed
- **Task Expiration**: Don't rely on task results being available indefinitely
- **Batch Processing**: Process multiple tasks concurrently for efficiency
- **Error Handling**: Implement robust retry logic for transient failures

## Related Endpoints

- [Create Top Applications Task](./topapplications.md) - Submit new top applications query
- [Top Applications with Policy Name](./topapplications-w-policyname.md) - Filter by policy name
- [Top Sources](../fortiviewtop-sources/create-task.md) - Analyze traffic sources
- [Top Threats](../fortiviewtop-threats/create-task.md) - Security threat analysis

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
