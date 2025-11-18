# Add HA Model Device with PSK

Pre-register a High Availability (HA) cluster with PSK authentication.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint pre-registers an HA cluster configuration, allowing both primary and secondary devices to authenticate when they connect.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom/{adom}/device`

## Request Format

Similar to single device registration, but includes HA configuration:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | Primary device name |
| `sn` | `string` | Yes | Primary serial number |
| `ha_mode` | `integer` | Yes | HA mode: 1 (A-P), 2 (A-A) |
| `ha_slave` | `array` | Yes | Secondary device(s) info |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/dvmdb/adom/root/device",
        "data": {
            "name": "prod-fw-ha",
            "sn": "FGT60FTK20012345",
            "platform_str": "FortiGate-60F",
            "ip": "192.168.1.100",
            "psk": "MySecretKey123",
            "ha_mode": 1,
            "ha_slave": [
                {
                    "name": "prod-fw-ha-slave",
                    "sn": "FGT60FTK20012346",
                    "ip": "192.168.1.101"
                }
            ],
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
            "name": "prod-fw-ha"
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
def add_ha_device(session_id, config, ha_info):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "add",
        "params": [{
            "url": f"/dvmdb/adom/{ha_info['adom']}/device",
            "data": {
                "name": ha_info['name'],
                "sn": ha_info['primary_sn'],
                "platform_str": ha_info['platform'],
                "ip": ha_info['primary_ip'],
                "psk": ha_info['psk'],
                "ha_mode": ha_info['ha_mode'],
                "ha_slave": ha_info['slaves'],
                "mgmt_mode": 2
            }
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    return result['result'][0]['status']['code'] == 0

# Add HA cluster
ha_cluster = {
    "adom": "root",
    "name": "prod-fw-ha",
    "primary_sn": "FGT60FTK20012345",
    "primary_ip": "192.168.1.100",
    "platform": "FortiGate-60F",
    "psk": "MySecretKey123",
    "ha_mode": 1,  # Active-Passive
    "slaves": [
        {
            "name": "prod-fw-ha-slave",
            "sn": "FGT60FTK20012346",
            "ip": "192.168.1.101"
        }
    ]
}
add_ha_device(session_id, config, ha_cluster)
```

## HA Mode Values

| Value | Mode | Description |
|-------|------|-------------|
| `1` | Active-Passive | One active, one standby |
| `2` | Active-Active | Both units active |

## Best Practices

> **💡 Tip:** Register HA cluster before powering on devices

> **⚠️ Warning:** Both HA units must use the same PSK

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
