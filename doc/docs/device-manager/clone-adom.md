# Clone ADOM

Create a copy of an existing ADOM with the same configuration settings.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint clones an existing ADOM, copying its configuration, settings, and structure (but not logs or devices) to a new ADOM.

**Common use cases:**
- Create development/staging ADOMs from production
- Template-based ADOM creation
- Standardized customer ADOM deployment

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom`
**Method Type:** `clone`
**Requires Authentication:** Yes

## Request Format

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | New ADOM name |
| `clone_from` | `string` | Yes | Source ADOM name to clone |
| `desc` | `string` | No | Description for new ADOM |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "clone",
    "params": [{
        "url": "/dvmdb/adom",
        "data": {
            "name": "customer-staging",
            "desc": "Cloned from production",
            "clone_from": "customer-prod"
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
            "name": "customer-staging"
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
def clone_adom(session_id, config, source_adom, new_adom_name, desc=""):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "clone",
        "params": [{
            "url": "/dvmdb/adom",
            "data": {
                "name": new_adom_name,
                "desc": desc,
                "clone_from": source_adom
            }
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    raise Exception(f"Clone failed")

# Example
clone_adom(session_id, config, "customer-prod", "customer-staging", "Staging environment")
```

## Best Practices

> **💡 Tip:** Cloning is faster than manual ADOM creation with same settings

> **📝 Note:** Logs and device assignments are NOT cloned

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
