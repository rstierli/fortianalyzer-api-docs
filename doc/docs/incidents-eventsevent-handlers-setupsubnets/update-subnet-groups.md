# Update Subnet Groups

Modify subnet group membership and configuration.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint updates subnet groups - useful for:
- Adding or removing subnets from groups
- Updating group descriptions and comments
- Reorganizing network segment groupings
- Adapting to network topology changes
- Managing dynamic network configurations

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/system/address-group/{group_name}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "update",
    "params": [{
        "url": "/config/adom/root/system/address-group/All_DMZ_Networks",
        "data": {
            "member": ["DMZ_Production", "DMZ_Staging", "DMZ_Development", "DMZ_Testing"],
            "comment": "All DMZ subnets including new testing environment"
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

def update_subnet_group(session_id, adom, group_name, members=None, comment=None):
    """Update subnet group"""
    url = "https://faz.example.com/jsonrpc"

    data = {}
    if members is not None:
        data['member'] = members
    if comment is not None:
        data['comment'] = comment

    payload = {
        "method": "update",
        "params": [{
            "url": f"/config/adom/{adom}/system/address-group/{group_name}",
            "data": data
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Updated subnet group '{group_name}'")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Add new subnet to group
from get_subnet_groups import get_subnet_groups

group_name = "All_DMZ_Networks"
groups = get_subnet_groups(session_id=session, adom="root")
current_group = next((g for g in groups if g['name'] == group_name), None)

if current_group:
    current_members = current_group.get('member', [])
    new_members = current_members + ["DMZ_Testing"]  # Add new subnet

    update_subnet_group(
        session_id=session,
        adom="root",
        group_name=group_name,
        members=new_members,
        comment="All DMZ subnets including new testing environment"
    )
```

## Use Cases

### Add Subnet to Group

```python
# Safely add subnet to existing group
def add_subnet_to_group(session_id, adom, group_name, subnet_name):
    """Add subnet to group without removing existing members"""
    groups = get_subnet_groups(session_id=session_id, adom=adom)
    group = next((g for g in groups if g['name'] == group_name), None)

    if not group:
        raise Exception(f"Group '{group_name}' not found")

    members = group.get('member', [])

    if subnet_name in members:
        print(f"ℹ️ Subnet '{subnet_name}' already in group '{group_name}'")
        return False

    members.append(subnet_name)

    update_subnet_group(
        session_id=session_id,
        adom=adom,
        group_name=group_name,
        members=members
    )
    return True

# Add new subnet
add_subnet_to_group(
    session_id=session,
    adom="root",
    group_name="All_DMZ_Networks",
    subnet_name="DMZ_Testing"
)
```

### Remove Subnet from Group

```python
# Remove subnet from group
def remove_subnet_from_group(session_id, adom, group_name, subnet_name):
    """Remove subnet from group"""
    groups = get_subnet_groups(session_id=session_id, adom=adom)
    group = next((g for g in groups if g['name'] == group_name), None)

    if not group:
        raise Exception(f"Group '{group_name}' not found")

    members = group.get('member', [])

    if subnet_name not in members:
        print(f"ℹ️ Subnet '{subnet_name}' not in group '{group_name}'")
        return False

    members.remove(subnet_name)

    update_subnet_group(
        session_id=session_id,
        adom=adom,
        group_name=group_name,
        members=members
    )
    return True

# Remove subnet
remove_subnet_from_group(
    session_id=session,
    adom="root",
    group_name="All_DMZ_Networks",
    subnet_name="DMZ_Old"
)
```

## Related Endpoints

- [Get Subnet Groups](./get-subnet-groups.md) - List all subnet groups
- [Add Subnet Group](./add-subnet-group.md) - Create new group
- [Get Subnet List](./get-subnet-list.md) - List available subnets

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
