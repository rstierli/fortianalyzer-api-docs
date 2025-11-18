# Get Subnet Groups

Retrieve subnet groups configured for event handler filtering.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves subnet groups - useful for:
- Listing all configured subnet group definitions
- Auditing network grouping configurations
- Verifying event handler subnet assignments
- Documentation and compliance reporting
- Network organization analysis

Subnet groups simplify event handler configuration by allowing multiple subnets to be referenced as a single entity.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/system/address-group`
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
        "url": "/config/adom/root/system/address-group"
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
                "name": "All_DMZ_Networks",
                "member": ["DMZ_Production", "DMZ_Staging", "DMZ_Development"],
                "comment": "All DMZ subnets for event monitoring"
            },
            {
                "name": "All_Internal_Networks",
                "member": ["Internal_Corp", "Internal_IT"],
                "comment": "All internal corporate networks"
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

def get_subnet_groups(session_id, adom="root"):
    """Get all subnet groups"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/system/address-group"
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
groups = get_subnet_groups(session_id="your_session_id")

print(f"Total Subnet Groups: {len(groups)}\n")
for group in groups:
    print(f"• {group['name']}: {len(group.get('member', []))} members")
    print(f"  Members: {', '.join(group.get('member', []))}")
    if group.get('comment'):
        print(f"  Comment: {group['comment']}")
    print()
```

## Related Endpoints

- [Add Subnet Group](./add-subnet-group.md) - Create subnet group
- [Update Subnet Groups](./update-subnet-groups.md) - Modify group membership
- [Get Subnet List](./get-subnet-list.md) - List individual subnet objects

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
