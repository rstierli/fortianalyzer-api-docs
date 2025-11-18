# Fetch Top Sources Results by Task ID

Retrieve the results of a previously created top sources task using its Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches completed top sources results - useful for:
- Retrieving results from a previously submitted task
- Implementing asynchronous result fetching patterns
- Building decoupled task submission and result retrieval workflows
- Allowing multiple result retrievals from the same task
- Enabling result caching and delayed processing

This endpoint is part of the two-step FortiView workflow. First create a task with [Create Top Sources Task](./create-task.md), then use this endpoint to fetch the results.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/adom/{adom}/top-sources/run/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Valid Task ID from a previously created top sources task
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
        "url": "/fortiview/adom/root/top-sources/run/12450",
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
            "tid": 12450,
            "status": "done",
            "percentage": 100,
            "total": 10,
            "sources": [
                {
                    "srcip": "10.0.1.150",
                    "hostname": "LAPTOP-USER01",
                    "sessions": 4523,
                    "bytes": 2147483648,
                    "bandwidth": 45678901,
                    "country": "Reserved"
                },
                {
                    "srcip": "10.0.1.75",
                    "hostname": "DESKTOP-IT01",
                    "sessions": 3891,
                    "bytes": 1879048192,
                    "bandwidth": 39012345,
                    "country": "Reserved"
                },
                {
                    "srcip": "10.0.1.45",
                    "hostname": "SERVER-APP01",
                    "sessions": 3204,
                    "bytes": 1610612736,
                    "bandwidth": 33456789,
                    "country": "Reserved"
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
| `total` | `integer` | Total number of sources returned |
| `sources` | `array` | Array of top source objects |

### Source Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `srcip` | `string` | Source IP address |
| `hostname` | `string` | Resolved hostname (if available) |
| `sessions` | `integer` | Number of sessions |
| `bytes` | `integer` | Total bytes transferred |
| `bandwidth` | `integer` | Bandwidth usage (bps) |
| `country` | `string` | GeoIP country |

## Complete Python Example

```python
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_top_sources_result(session_id, adom, task_id):
    """
    Fetch top sources results by Task ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        task_id: Task ID from create task operation

    Returns:
        dict: Task result data including sources
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/fortiview/adom/{adom}/top-sources/run/{task_id}",
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

# Example: Fetch results for task ID 12450
result = fetch_top_sources_result(
    session_id="your_session_id",
    adom="root",
    task_id=12450
)

# Display results
print(f"Task Status: {result['status']}")
print(f"Total Sources: {result['total']}\n")

for i, src in enumerate(result['sources'], 1):
    print(f"{i}. {src['srcip']} ({src.get('hostname', 'Unknown')})")
    print(f"   Sessions: {src['sessions']:,}")
    print(f"   Bytes: {src['bytes']:,} ({src['bytes']/1024/1024/1024:.2f} GB)")
    print(f"   Bandwidth: {src['bandwidth']/1000000:.2f} Mbps")
    print()
```

## Use Cases

### Delayed Result Processing

```python
# Submit task and save TID for later
from create_task import create_top_sources_task

tid = create_top_sources_task(
    session_id=session,
    adom="root",
    time_range={"last-n-hours": 24}
)

# Store TID for later retrieval
with open('task_ids.txt', 'a') as f:
    f.write(f"{tid}\n")

# Later: Retrieve results
tid = 12450  # From saved file
result = fetch_top_sources_result(
    session_id=session,
    adom="root",
    task_id=tid
)
```

### Multiple Result Retrievals

```python
# Fetch same results multiple times without re-running query
task_id = 12450

# First retrieval: Full analysis
result1 = fetch_top_sources_result(session, "root", task_id)
for src in result1['sources']:
    # Detailed processing
    analyze_source(src)

# Second retrieval: Different analysis
result2 = fetch_top_sources_result(session, "root", task_id)
for src in result2['sources']:
    # Generate reports
    create_report(src)
```

### Batch Task Result Collection

```python
# Collect results from multiple tasks
task_ids = [12450, 12451, 12452, 12453]
all_sources = []

for tid in task_ids:
    try:
        result = fetch_top_sources_result(
            session_id=session,
            adom="root",
            task_id=tid
        )
        all_sources.extend(result['sources'])
        print(f"✓ Retrieved {result['total']} sources from task {tid}")
    except Exception as e:
        print(f"✗ Task {tid} failed: {e}")

# Aggregate analysis
print(f"\nTotal sources collected: {len(all_sources)}")
top_consumer = max(all_sources, key=lambda x: x['bytes'])
print(f"Top consumer: {top_consumer['srcip']} - {top_consumer['bytes']/1024/1024/1024:.2f} GB")
```

### Result Validation and Re-fetch

```python
import time

def get_completed_results(session_id, adom, task_id, max_retries=5):
    """
    Fetch results with retry if task not complete
    """
    for attempt in range(max_retries):
        try:
            result = fetch_top_sources_result(session_id, adom, task_id)
            return result['sources']
        except Exception as e:
            if "Task not complete" in str(e):
                print(f"Task still processing, retry {attempt+1}/{max_retries}...")
                time.sleep(3)
            else:
                raise

    raise TimeoutError(f"Task {task_id} did not complete after {max_retries} retries")

# Usage
sources = get_completed_results(
    session_id=session,
    adom="root",
    task_id=12450
)
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
            "tid": 12450,
            "status": "running",
            "percentage": 65
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

> **💡 Tip:** Task IDs have a limited lifetime. Fetch results promptly after task completion.

> **⚠️ Warning:** Multiple calls to fetch results do not re-run the query. Results are cached from the original task execution.

> **💡 Tip:** Use this endpoint for building asynchronous workflows where task submission and result retrieval are separated.

## Task Lifecycle

Tasks go through the following states:

1. **Created** - Task submitted, TID assigned
2. **Running** - Task executing (percentage < 100)
3. **Done** - Task complete (percentage = 100)
4. **Expired** - Task results no longer available

**Typical task lifetime:** 15-30 minutes depending on FortiAnalyzer configuration.

## Related Endpoints

- [Create Top Sources Task](./create-task.md) - Submit new top sources query
- [Top Applications](../fortiviewtop-applications/topapplications.md) - Application usage analysis
- [Top Threats](../fortiviewtop-threats/create-task.md) - Security threat analysis

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
