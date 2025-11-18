# Add Unregistered Device

Register (authorize) an unregistered device to accept logs from it.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint authorizes an unregistered device, moving it from pending status to registered, allowing FortiAnalyzer to accept and store its logs.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/device`
**Method Type:** `exec`
**Action:** `add-device`

## Request Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | Target ADOM name |
| `device` | `object` | Yes | Device to register |
| `device.name` | `string` | Yes | Device name or serial number |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/dvmdb/device",
        "data": {
            "adom": "root",
            "device": {
                "name": "FGT60FTK20012345"
            },
            "action": "add-device"
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
def add_device(session_id, config, device_sn, adom="root"):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "exec",
        "params": [{
            "url": "/dvmdb/device",
            "data": {
                "adom": adom,
                "device": {"name": device_sn},
                "action": "add-device"
            }
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    return result['result'][0]['status']['code'] == 0

# Register device
success = add_device(session_id, config, "FGT60FTK20012345", "root")
print(f"Device registered: {success}")
```

## Related Endpoints

- [Get Unregistered Devices](./get-unregistered-devices.md) - List pending devices

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
