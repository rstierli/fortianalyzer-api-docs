# Restart FortiAnalyzer

Restart the FortiAnalyzer system.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint restarts FortiAnalyzer - useful for applying system updates, configuration changes, or troubleshooting.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/sys/reboot`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/reboot"
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

def restart_fortianalyzer(session_id):
    """Restart FortiAnalyzer system"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "exec",
        "params": [{"url": "/sys/reboot"}],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print("✓ FortiAnalyzer restart initiated")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example with confirmation
confirm = input("Restart FortiAnalyzer? (yes/no): ")
if confirm.lower() == 'yes':
    restart_fortianalyzer(session_id="your_session_id")
```

> **⚠️ Warning:** This will restart the FortiAnalyzer system. All active sessions will be terminated.

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
