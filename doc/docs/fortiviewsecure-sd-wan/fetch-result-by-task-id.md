# Fetch SD-WAN Results by Task ID

Retrieve results of a previously created SD-WAN task using its Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches completed SD-WAN task results - useful for:
- Retrieving results from previously submitted SD-WAN queries
- Implementing asynchronous result fetching workflows
- Decoupling task submission from result retrieval
- Allowing multiple retrievals of the same task results
- Building scheduled reporting systems

This is Step 2 of the two-step SD-WAN workflow pattern used by all SD-WAN endpoints.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/fortiview/adom/{adom}/top-sources/run/{taskID}` (varies by endpoint type)
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Valid Task ID from a previously created SD-WAN task
- Read access to FortiView data in specified ADOM
- Task must be completed (status: "done")

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
            "total": 15,
            "results": [...]
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

def fetch_sdwan_result_by_tid(session_id, adom, task_id, endpoint_path):
    """
    Fetch SD-WAN task results by Task ID

    Args:
        session_id: Active session ID
        adom: ADOM name
        task_id: Task ID from create task operation
        endpoint_path: Endpoint path (e.g., 'top-sources', 'sdwan-dev-stats')

    Returns:
        dict: Task result data
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/fortiview/adom/{adom}/{endpoint_path}/run/{task_id}",
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

# Example: Fetch previously submitted task
result = fetch_sdwan_result_by_tid(
    session_id="your_session_id",
    adom="root",
    task_id=12450,
    endpoint_path="top-sources"
)

print(f"Task Status: {result['status']}")
print(f"Total Results: {result['total']}")
```

## Endpoint Path Reference

| Endpoint Type | Path |
|---------------|------|
| Top Sources | `top-sources` |
| Interface Stats | `sdwan-dev-stats` |
| Bandwidth Trends | `sdwan-intf-bandwidth-line` |
| Top Talkers | `sdwan-summary-user-view` |
| Applications | `sdwan-summary-app-view` |
| MOS Quality | `sdwan-intf-mos-line` |

## Task Lifecycle

1. **Created** - Task submitted, TID assigned
2. **Running** - Task executing (percentage < 100)
3. **Done** - Task complete (percentage = 100)
4. **Expired** - Task results no longer available

**Typical task lifetime:** 15-30 minutes depending on FortiAnalyzer configuration.

## Best Practices

> **💡 Tip:** Task IDs have a limited lifetime (typically 15-30 minutes). Fetch results promptly after task completion.

> **💡 Tip:** Multiple calls to fetch results do not re-run the query. Results are cached from the original task execution.

> **💡 Tip:** Check task status and percentage before processing data to ensure task completed successfully.

## Related Endpoints

- [SD-WAN Interface Statistics](./create-task-sd-wan-interface-bandwidth-line.md) - Submit interface stats task
- [SD-WAN Health Overview](./create-task-sd-wan-health-overview.md) - Submit bandwidth trends task
- [SD-WAN Top Talkers](./create-task-sd-wan-top-talkers.md) - Submit top users task
- [SD-WAN Applications](./create-task-sd-wan-application.md) - Submit applications task

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
