# Add Model Device with PSK

Pre-register a device with pre-shared key (PSK) authentication before the device connects.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint pre-registers a device model with PSK authentication, allowing the device to authenticate when it first connects to FortiAnalyzer.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom/{adom}/device`

## Request Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | Device name |
| `sn` | `string` | Yes | Serial number |
| `platform_str` | `string` | Yes | Platform type |
| `ip` | `string` | Yes | Device IP address |
| `psk` | `string` | Yes | Pre-shared key |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/dvmdb/adom/root/device",
        "data": {
            "name": "prod-fw-01",
            "sn": "FGT60FTK20012345",
            "platform_str": "FortiGate-60F",
            "ip": "192.168.1.100",
            "psk": "MySecretKey123",
            "mgmt_mode": 2
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
            "name": "prod-fw-01"
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

## Complete Example

```python
def add_device_with_psk(session_id, config, device_info):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "add",
        "params": [{
            "url": f"/dvmdb/adom/{device_info['adom']}/device",
            "data": {
                "name": device_info['name'],
                "sn": device_info['sn'],
                "platform_str": device_info['platform'],
                "ip": device_info['ip'],
                "psk": device_info['psk'],
                "mgmt_mode": 2
            }
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    return result['result'][0]['status']['code'] == 0

# Add device
device = {
    "adom": "root",
    "name": "prod-fw-01",
    "sn": "FGT60FTK20012345",
    "platform": "FortiGate-60F",
    "ip": "192.168.1.100",
    "psk": "MySecretKey123"
}
add_device_with_psk(session_id, config, device)
```

## Best Practices

> **💡 Tip:** Use strong PSK keys (16+ characters, mixed case, numbers, symbols)

> **⚠️ Warning:** Store PSK securely - it's used for device authentication

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
