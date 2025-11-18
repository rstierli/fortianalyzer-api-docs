# Get Unregistered Devices

Retrieve list of devices that have contacted FortiAnalyzer but are not yet authorized.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves devices that are pending registration - devices that have attempted to connect to FortiAnalyzer but haven't been authorized yet.

**Common use cases:**
- Discover new devices connecting to FortiAnalyzer
- Bulk device registration workflows
- Audit unauthorized connection attempts
- Automated device onboarding

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/device/unreg`
**Requires Authentication:** Yes

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/device/unreg"
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
                "name": "FGT-12345",
                "sn": "FGT60FTK20012345",
                "ip": "192.168.1.100",
                "platform_str": "FortiGate-60F",
                "os_ver": 7
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

## Complete Example

```python
def get_unregistered_devices(session_id, config):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "get",
        "params": [{"url": "/dvmdb/device/unreg"}],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    return []

# Get pending devices
devices = get_unregistered_devices(session_id, config)
print(f"Found {len(devices)} unregistered devices")
for dev in devices:
    print(f"  - {dev['name']} ({dev['sn']}) at {dev['ip']}")
```

## Related Endpoints

- [Add Unregistered Device](./add-unregistered-device.md) - Register a device

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
