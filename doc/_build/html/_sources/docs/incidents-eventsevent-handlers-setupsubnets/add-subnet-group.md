# Add Subnet Group

Create a subnet group containing multiple subnet address objects for simplified event handler configuration.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates subnet groups - useful for:
- Grouping related subnets for easier management
- Applying event handlers to multiple subnets simultaneously
- Creating logical network segment collections (e.g., "All_DMZ", "Production_Networks")
- Simplifying multi-site or multi-tenant configurations
- Reducing event handler configuration complexity

Subnet groups enable efficient management of event handler assignments across multiple network segments.

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
    "method": "add",
    "params": [{
        "url": "/config/adom/root/system/address-group",
        "data": {
            "name": "All_DMZ_Networks",
            "member": ["DMZ_Production", "DMZ_Staging", "DMZ_Development"],
            "comment": "All DMZ subnets for event monitoring"
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

def add_subnet_group(session_id, adom, name, members, comment=""):
    """Create subnet group"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/config/adom/{adom}/system/address-group",
            "data": {
                "name": name,
                "member": members,
                "comment": comment or f"Subnet group: {name}"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Created subnet group '{name}' with {len(members)} members")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example
add_subnet_group(
    session_id="your_session_id",
    adom="root",
    name="All_DMZ_Networks",
    members=["DMZ_Production", "DMZ_Staging", "DMZ_Development"],
    comment="All DMZ subnets for event monitoring"
)
```

## Use Cases

### Create Logical Network Groupings

```python
# Group subnets by security zone
network_groups = {
    "All_DMZ_Networks": {
        "members": ["DMZ_Production", "DMZ_Staging", "DMZ_Development"],
        "comment": "All DMZ security zones"
    },
    "All_Internal_Networks": {
        "members": ["Internal_Corp", "Internal_IT", "Internal_Management"],
        "comment": "All internal corporate networks"
    },
    "All_Guest_Networks": {
        "members": ["Guest_WiFi", "Guest_Wired", "Visitor_Network"],
        "comment": "All guest and visitor networks"
    }
}

for group_name, config in network_groups.items():
    add_subnet_group(
        session_id=session,
        adom="root",
        name=group_name,
        members=config['members'],
        comment=config['comment']
    )
    print(f"✓ Created group: {group_name}")
```

### Multi-Site Network Organization

```python
# Create site-specific subnet groups
sites = {
    "HQ_Networks": ["HQ_DMZ", "HQ_Internal", "HQ_Management"],
    "Branch_Office_1": ["BO1_Internal", "BO1_Guest"],
    "Branch_Office_2": ["BO2_Internal", "BO2_Guest"],
    "Cloud_Networks": ["Cloud_DMZ", "Cloud_Private"]
}

for site_name, subnets in sites.items():
    add_subnet_group(
        session_id=session,
        adom="root",
        name=site_name,
        members=subnets,
        comment=f"{site_name} network segments"
    )
```

## Related Endpoints

- [Get Subnet Groups](./get-subnet-groups.md) - List all subnet groups
- [Update Subnet Groups](./update-subnet-groups.md) - Modify group membership
- [Get Subnet List](./get-subnet-list.md) - List available subnet objects

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
