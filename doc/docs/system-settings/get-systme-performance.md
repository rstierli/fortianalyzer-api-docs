# Get System Performance

Retrieve FortiAnalyzer system performance metrics.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves performance metrics - useful for capacity planning, monitoring, and troubleshooting.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/performance`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/sys/performance"
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
            "cpu": 45,
            "memory": 62,
            "disk": 78
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

def get_system_performance(session_id):
    """Get system performance metrics"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{"url": "/sys/performance"}],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
perf = get_system_performance(session_id="your_session_id")
print(f"CPU: {perf['cpu']}%")
print(f"Memory: {perf['memory']}%")
print(f"Disk: {perf['disk']}%")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
