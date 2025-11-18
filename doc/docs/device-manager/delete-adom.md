# Delete ADOM

Delete an Administrative Domain (ADOM) from FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint permanently deletes an ADOM and all associated data including devices, configurations, and logs. This is a **destructive operation** that cannot be undone.

**⚠️ WARNING:** Deleting an ADOM is irreversible. All logs, devices, and configurations in the ADOM will be permanently removed.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom/{adom_name}`
**Requires Authentication:** Yes
**Required Permissions:** Super administrator

## Prerequisites

- ADOM must exist
- ADOM must be empty (no devices assigned) or use force delete
- Super administrator permissions
- **BACKUP before deleting**

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/dvmdb/adom/customer-001"
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
        },
        "url": "/dvmdb/adom/customer-001"
    }]
}
```
````
`````

## Complete Example

### Python Example

```python
def delete_adom(session_id, config, adom_name):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "delete",
        "params": [{"url": f"/dvmdb/adom/{adom_name}"}],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return True
    raise Exception(f"Delete failed: {result['result'][0]['status']['message']}")

# WARNING: This is destructive!
# delete_adom(session_id, config, "customer-001")
```

## Best Practices

> **⚠️ Warning:** Cannot delete built-in ADOMs (root, rootp, FortiGate, etc.)

> **💡 Tip:** Move devices to another ADOM before deleting

> **⚠️ Warning:** Export logs and configurations before deletion

## Related Endpoints

- [Get ADOMs](./get-adom-with-no-fields.md) - List ADOMs before deletion

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
