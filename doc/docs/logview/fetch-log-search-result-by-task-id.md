# Fetch Log Search Results by Task ID

Retrieve log search results using a Task ID (TID) from a previously submitted search.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves results from a log search task. It's Step 2 of the two-step log search workflow:
1. Submit search → Receive TID
2. **Fetch results using TID** ← This endpoint

For complete workflow details, see [LogView Search Overview](../pilot/logview-search.md).

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/logview/adom/{adom}/logsearch/{tid}`
**HTTP Method:** `get`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `tid` | `integer` | Yes | Task ID from search submission |
| `limit` | `integer` | No | Results per page (default: 100) |
| `offset` | `integer` | No | Starting position (default: 0) |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/logview/adom/root/logsearch/12345",
        "data": {
            "limit": 100,
            "offset": 0
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
            "tid": 12345,
            "status": "done",
            "percentage": 100,
            "total_lines": 450,
            "logs": [
                {
                    "date": "2025-11-09",
                    "time": "14:23:15",
                    "devname": "FGT-01",
                    "srcip": "10.0.1.100",
                    "dstip": "172.217.14.206",
                    "action": "accept"
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

def fetch_search_results(session_id, adom, tid, limit=100, offset=0):
    """
    Fetch log search results by TID

    Args:
        session_id: Active session ID
        adom: ADOM name
        tid: Task ID from search submission
        limit: Results per page
        offset: Starting position

    Returns:
        dict: Search result data
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/logview/adom/{adom}/logsearch/{tid}",
            "data": {
                "limit": limit,
                "offset": offset
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"Fetch failed: {result['result'][0]['status']['message']}")

# Example usage
data = fetch_search_results(
    session_id="your_session_id",
    adom="root",
    tid=12345,
    limit=100,
    offset=0
)

print(f"Status: {data['status']}")
print(f"Progress: {data['percentage']}%")
print(f"Total logs: {data['total_lines']}")
print(f"Logs retrieved: {len(data.get('logs', []))}")
```

## Response Status Values

| Status | Description |
|--------|-------------|
| `running` | Search still in progress |
| `done` | Search completed successfully |
| `cancelled` | Search was cancelled |
| `error` | Search failed with error |

## Pagination Example

```python
def fetch_all_logs(session_id, adom, tid):
    """Fetch all logs with pagination"""
    all_logs = []
    offset = 0
    limit = 100

    while True:
        data = fetch_search_results(session_id, adom, tid, limit, offset)

        if data['status'] != 'done':
            continue  # Still processing

        logs = data.get('logs', [])
        if not logs:
            break

        all_logs.extend(logs)

        if len(all_logs) >= data['total_lines']:
            break

        offset += limit

    return all_logs
```

## Related Endpoints

- [LogView Search Overview](../pilot/logview-search.md) - Complete two-step workflow
- [Cancel Search Task](./cancel-log-search-task.md) - Cancel running search

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
