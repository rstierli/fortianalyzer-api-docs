# Get Log Forwarding Configuration

Retrieve log forwarding settings from FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves log forwarding configurations - useful for auditing syslog, CEF, or SIEM integrations.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/log-forward`
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
        "url": "/cli/global/system/log-forward"
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
        "data": [
            {
                "id": 1,
                "name": "Syslog_Server_01",
                "mode": "forwarding",
                "server-name": "syslog.example.com",
                "server-addr": "10.0.5.100",
                "log-field-exclusion-status": "disable",
                "log-masking-status": "disable"
            }
        ],
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

def get_log_forwarding_config(session_id):
    """Get log forwarding configuration"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": "/cli/global/system/log-forward"
        }],
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
configs = get_log_forwarding_config(session_id="your_session_id")
for config in configs:
    print(f"Forwarder: {config['name']}")
    print(f"  Server: {config['server-name']} ({config['server-addr']})")
    print(f"  Mode: {config['mode']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
