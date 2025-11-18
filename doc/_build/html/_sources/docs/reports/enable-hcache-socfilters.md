# Enable HCache SOC Filters

Enable historical cache and SOC filters for report data optimization.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint enables HCache (historical cache) and SOC filters - useful for improving report performance with frequently accessed data.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/sql-report/hcache`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "set",
    "params": [{
        "url": "/config/adom/root/sql-report/hcache",
        "data": {
            "status": "enable",
            "soc-filters": "enable"
        }
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def enable_hcache_soc_filters(session_id, adom="root"):
    """Enable historical cache and SOC filters"""
    url = "https://faz.example.com/jsonrpc"
    
    payload = {
        "method": "set",
        "params": [{
            "url": f"/config/adom/{adom}/sql-report/hcache",
            "data": {
                "status": "enable",
                "soc-filters": "enable"
            }
        }],
        "session": session_id,
        "id": 1
    }
    
    response = requests.post(url, json=payload, verify=False)
    result = response.json()
    
    if result['result'][0]['status']['code'] == 0:
        print("✓ HCache and SOC filters enabled")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
enable_hcache_soc_filters(session_id="your_session_id")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
