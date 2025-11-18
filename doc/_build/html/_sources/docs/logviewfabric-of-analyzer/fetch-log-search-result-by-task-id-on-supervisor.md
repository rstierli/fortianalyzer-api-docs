# Fetch Fabric Log Search Results

Retrieve distributed log search results from Fabric of FortiAnalyzer using Task ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint fetches results from fabric-wide log searches - useful for:
- Retrieving results from distributed searches across multiple FAZ units
- Polling search status across Supervisor and Members
- Paginating large result sets from fabric deployments

**Two-Step Pattern**: Create search → Wait for completion → Fetch results

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/soc-fabric/logsearch/{taskID}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/soc-fabric/logsearch/12470",
        "apiver": 3,
        "limit": 10,
        "offset": 0
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
            "total_lines": 450,
            "logs": [
                {
                    "srcip": "10.0.200.253",
                    "dstip": "140.82.121.5",
                    "service": "HTTPS",
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
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_fabric_search_results(session_id, tid, limit=100):
    """Fetch fabric search results with polling"""
    url = "https://faz.example.com/jsonrpc"

    # Poll until complete
    max_attempts = 30
    for attempt in range(max_attempts):
        payload = {
            "method": "get",
            "params": [{
                "url": f"/soc-fabric/logsearch/{tid}",
                "apiver": 3,
                "limit": limit,
                "offset": 0
            }],
            "session": session_id,
            "id": 1
        }

        response = requests.post(url, json=payload, verify=False)
        result = response.json()

        if result['result'][0]['status']['code'] == 0:
            data = result['result'][0]['data']
            status = data.get('status', 'unknown')
            percentage = data.get('percentage', 0)

            print(f"  Status: {status} - {percentage}% complete")

            if status == 'done' and percentage == 100:
                return data.get('logs', [])

        time.sleep(2)  # Wait 2 seconds between polls

    raise TimeoutError("Search did not complete within timeout")

# Example
logs = fetch_fabric_search_results(
    session_id="your_session_id",
    tid=12470
)

print(f"Retrieved {len(logs)} log entries from fabric search")
```

## Related Endpoints

- [Create Fabric Log Search Task](./create-search-task-for-ip-on-supervisor.md) - Submit distributed search

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
