# Get Subnet Address Objects

Retrieve subnet address objects configured for event handler filtering.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves subnet address objects - useful for:
- Listing all configured subnet definitions
- Auditing network segment configurations
- Identifying subnets available for event handler assignments
- Documentation and compliance reporting
- Network topology mapping

Subnet address objects define network segments that can be referenced by event handlers for targeted monitoring and automated responses.

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
    "method": "get",
    "params": [{
        "url": "/config/adom/root/system/address-obj"
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
                "name": "DMZ_Subnet",
                "subnet": "10.10.100.0/24",
                "type": "subnet",
                "comment": "Production DMZ network"
            },
            {
                "name": "Internal_Network",
                "subnet": "192.168.10.0/24",
                "type": "subnet",
                "comment": "Internal corporate network"
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

def get_subnet_list(session_id, adom="root"):
    """Get all subnet address objects"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/system/address-obj"
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
subnets = get_subnet_list(session_id="your_session_id")

print(f"Total Subnet Objects: {len(subnets)}\n")
for subnet in subnets:
    print(f"• {subnet['name']}: {subnet.get('subnet', 'N/A')}")
    if subnet.get('comment'):
        print(f"  Comment: {subnet['comment']}")
```

## Related Endpoints

- [Add Subnet](./add-subnet.md) - Create subnet address object
- [Add Subnet Group](./add-subnet-group.md) - Create subnet group
- [Get Subnet Groups](./get-subnet-groups.md) - List subnet groups

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
