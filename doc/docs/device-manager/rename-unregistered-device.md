# Rename Unregistered Device

Change the name of an unregistered device before authorizing it.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint renames an unregistered device, useful for standardizing device names before registration.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/device/unreg/{old_name}`

## Request Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | New device name |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "update",
    "params": [{
        "url": "/dvmdb/device/unreg/FGT-12345",
        "data": {
            "name": "prod-firewall-01"
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
        "status": {
            "code": 0,
            "message": "OK"
        }
    }]
}
```
````
`````

## Complete Example

```python
def rename_device(session_id, config, old_name, new_name):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "update",
        "params": [{
            "url": f"/dvmdb/device/unreg/{old_name}",
            "data": {"name": new_name}
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    return result['result'][0]['status']['code'] == 0

# Rename before registration
rename_device(session_id, config, "FGT-12345", "prod-firewall-01")
```

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
