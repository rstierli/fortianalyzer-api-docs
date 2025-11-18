# Get ADOMs (With Field Filter)

Retrieve ADOMs with specific field filtering for optimized performance and reduced response size.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves ADOMs with field-level filtering, returning only requested fields instead of complete ADOM data. This significantly improves performance when you only need specific information.

**Common use cases:**
- Build dropdown menus (only need name and OID)
- Monitor log quotas (only quota and usage fields)
- Quick ADOM lookups (minimal data transfer)
- Dashboard displays with specific metrics

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom`
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0

## Request Format

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fields` | `array` | Yes | List of field names to return |

### Common Fields

| Field | Use Case |
|-------|----------|
| `name`, `oid` | Dropdown lists, references |
| `desc` | Descriptions, labels |
| `log_disk_quota`, `log_disk_quota_alert_thres` | Quota monitoring |
| `state` | Status checks |
| `mr`, `os_ver` | Version compatibility |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom",
        "fields": ["name", "oid", "desc", "log_disk_quota"]
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
                "name": "root",
                "oid": 3,
                "desc": "",
                "log_disk_quota": 1000
            },
            {
                "name": "customer-001",
                "oid": 236,
                "desc": "Customer Production",
                "log_disk_quota": 51200
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

## Complete Example

### Python Example

```python
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_adoms_filtered(session_id, config, fields):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "get",
        "params": [{"url": "/dvmdb/adom", "fields": fields}],
        "session": session_id,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    raise Exception(f"Error: {result['result'][0]['status']['message']}")

# Example: Get ADOM names for dropdown
adoms = get_adoms_filtered(session_id, config, ["name", "oid"])
print("ADOMs:", [(a['name'], a['oid']) for a in adoms])
```

### cURL Example

```bash
curl -k -s -X POST "https://faz.example.com:443/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method":"get",
    "params":[{
      "url":"/dvmdb/adom",
      "fields":["name","oid","desc"]
    }],
    "session":"'${SESSION_ID}'",
    "id":1
  }' | jq '.result[0].data'
```

## Best Practices

> **💡 Tip:** Always use field filtering when you don't need complete ADOM data

> **💡 Tip:** Minimal fields for dropdowns: `["name", "oid"]`

## Related Endpoints

- [Get ADOMs (No Filter)](./get-adom-with-no-fields.md) - Get complete ADOM data

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
