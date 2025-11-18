# Cancel Log Search Task

Cancel a running log search task to free up system resources.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint cancels an in-progress log search task - useful for:
- Stopping long-running searches that are no longer needed
- Freeing up FortiAnalyzer resources
- Aborting searches with incorrect parameters
- Managing concurrent search limits

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/logview/adom/{adom}/logsearch/{tid}`
**HTTP Method:** `delete`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `tid` | `integer` | Yes | Task ID to cancel |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/logview/adom/root/logsearch/12345"
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

def cancel_log_search(session_id, adom, tid):
    """
    Cancel a running log search task

    Args:
        session_id: Active session ID
        adom: ADOM name
        tid: Task ID to cancel

    Returns:
        bool: True if cancelled successfully
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "delete",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch/{tid}"
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Search task {tid} cancelled successfully")
        return True
    else:
        print(f"✗ Failed to cancel task {tid}: {result['result'][0]['status']['message']}")
        return False

# Example usage
success = cancel_log_search(
    session_id="your_session_id",
    adom="root",
    tid=12345
)
```

## Use Cases

### Cancel Long-Running Search

```python
# Submit search
tid = submit_log_search(session_id, adom, device, logtype, filter, time_range)

# Realize search parameters were wrong
cancel_log_search(session_id, adom, tid)

# Submit corrected search
new_tid = submit_log_search(session_id, adom, device, logtype, correct_filter, time_range)
```

### Timeout Handling

```python
import time

def search_with_timeout(session_id, adom, device, logtype, filter, time_range, timeout=30):
    """Search with automatic cancellation on timeout"""
    tid = submit_log_search(session_id, adom, device, logtype, filter, time_range)

    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            print(f"Search timeout after {timeout}s, cancelling...")
            cancel_log_search(session_id, adom, tid)
            raise TimeoutError("Search exceeded timeout")

        status = check_search_status(session_id, adom, tid)
        if status['status'] == 'done':
            return fetch_search_results(session_id, adom, tid)

        time.sleep(2)
```

## Important Notes

> **💡 Tip:** Always cancel searches that are no longer needed to free up system resources.

> **⚠️ Warning:** Once cancelled, the search results cannot be retrieved. The TID becomes invalid.

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
- TID already completed or expired
- TID does not exist
- TID belongs to different ADOM

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete workflow guide
- [Fetch Search Results](./fetch-log-search-result-by-task-id.md) - Retrieve results by TID

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
