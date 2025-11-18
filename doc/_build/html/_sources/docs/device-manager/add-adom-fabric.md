# Create ADOM (Security Fabric)

Create an ADOM configured for Fortinet Security Fabric multi-product environments.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates an ADOM optimized for Security Fabric deployments, supporting multiple Fortinet product types in an integrated security architecture.

**Common use cases:**
- Security Fabric environments with FortiGate + FortiSandbox + FortiMail
- Multi-product deployments
- Integrated threat intelligence environments

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom`
**Requires Authentication:** Yes

## Request Format

Same as FortiOS ADOM creation, but use `restricted_prds: 4503599627370495` for all products:

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/dvmdb/adom",
        "data": {
            "name": "fabric-prod",
            "desc": "Security Fabric Production",
            "mr": 7,
            "os_ver": 0,
            "restricted_prds": 4503599627370495,
            "log_disk_quota": 204800
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
            "name": "fabric-prod"
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
def create_fabric_adom(session_id, config, name, desc=""):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "add",
        "params": [{
            "url": "/dvmdb/adom",
            "data": {
                "name": name,
                "desc": desc,
                "mr": 7,
                "os_ver": 0,
                "restricted_prds": 4503599627370495,  # All products
                "log_disk_quota": 204800  # 200GB
            }
        }],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    raise Exception("Creation failed")
```

## Best Practices

> **💡 Tip:** Use higher log quotas for Security Fabric (multiple products = more logs)

> **💡 Tip:** Product type `4503599627370495` supports all Fortinet products

## Related Endpoints

- [Create ADOM (FortiOS)](./add-adom-fos.md) - Standard ADOM creation

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
