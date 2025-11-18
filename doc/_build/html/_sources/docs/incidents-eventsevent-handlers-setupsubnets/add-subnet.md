# Add Subnet Address Object

Create a subnet address object for event handler filtering and network segmentation.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates subnet address objects - useful for:
- Defining network segments for event handler targeting
- Creating reusable subnet definitions for multiple event handlers
- Organizing networks by function, security zone, or location
- Implementing network-based security policies
- Supporting multi-tenant or multi-site configurations

Subnet address objects enable precise network-based event filtering and targeted automated responses.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/system/address-obj`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/config/adom/root/system/address-obj",
        "data": {
            "name": "DMZ_Subnet",
            "type": "subnet",
            "subnet": "10.10.100.0/24",
            "comment": "Production DMZ network"
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
        "data": {},
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

def add_subnet(session_id, adom, name, subnet, comment=""):
    """Create subnet address object"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/config/adom/{adom}/system/address-obj",
            "data": {
                "name": name,
                "type": "subnet",
                "subnet": subnet,
                "comment": comment or f"Subnet {subnet}"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Created subnet '{name}': {subnet}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_subnet(
    session_id="your_session_id",
    adom="root",
    name="DMZ_Subnet",
    subnet="10.10.100.0/24",
    comment="Production DMZ network"
)
```

## Use Cases

### Define Network Zones

```python
# Create subnet objects for different security zones
network_zones = [
    ("DMZ_Production", "10.10.100.0/24", "Production DMZ"),
    ("DMZ_Staging", "10.10.200.0/24", "Staging DMZ"),
    ("Internal_Corp", "192.168.10.0/24", "Corporate network"),
    ("Internal_Guest", "172.16.0.0/16", "Guest WiFi network")
]

for name, subnet, comment in network_zones:
    add_subnet(
        session_id=session,
        adom="root",
        name=name,
        subnet=subnet,
        comment=comment
    )
```

## Related Endpoints

- [Get Subnet List](./get-subnet-list.md) - List all subnet objects
- [Add Subnet Group](./add-subnet-group.md) - Create subnet group
- [Add Subnet to Event Handler](../incidents-eventsevent-handlers-setup/add-subnet-eventhandler.md) - Link subnet to event handler

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
