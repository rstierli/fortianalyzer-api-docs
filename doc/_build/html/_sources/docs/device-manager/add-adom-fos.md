# Create ADOM (FortiOS/FortiGate)

Create a new Administrative Domain (ADOM) for FortiOS devices like FortiGate firewalls.

> **✅ All code examples tested:** Documentation based on FortiAnalyzer v8.0.0 API structure and tested parameter specifications.

## Overview

This endpoint creates a new ADOM for managing FortiGate and other FortiOS-based devices. ADOMs provide logical separation of devices, configurations, and logs based on customers, departments, regions, or any organizational requirement.

**Common use cases:**
- Create customer-specific ADOMs in MSP environments
- Separate production and development environments
- Segment devices by geographic region
- Isolate departments or business units
- Create tenant-specific log storage with quota limits

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom`
**ADOM Support:** N/A (creates new ADOM)
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0
**Required Permissions:** Super administrator or ADOM create permissions

## Prerequisites

- ADOM feature must be enabled (see [Enable ADOM](./enable-adom.md))
- Super administrator or appropriate ADOM management permissions
- Unique ADOM name (cannot duplicate existing ADOMs)
- Sufficient disk space for log storage quota

## Request Format

### Required Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | ADOM name (alphanumeric, underscore, hyphen) |
| `mr` | `integer` | Yes | Major release version (e.g., 4 for v4.x, 6 for v6.x, 7 for v7.x) |
| `os_ver` | `integer` | Yes | OS version: 0 (FortiOS), 2 (FortiCarrier), etc. |
| `restricted_prds` | `integer` | Yes | Product type bitmask (see values below) |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `desc` | `string` | `""` | ADOM description |
| `mode` | `integer` | `1` | ADOM mode: 0 (advanced), 1 (normal) |
| `log_disk_quota` | `integer` | `0` | Log disk quota in MB (0 = unlimited) |
| `log_db_retention_hours` | `integer` | `1440` | Database log retention (hours, default 60 days) |
| `log_file_retention_hours` | `integer` | `8760` | File log retention (hours, default 365 days) |
| `log_disk_quota_alert_thres` | `integer` | `90` | Alert threshold percentage |
| `log_disk_quota_split_ratio` | `integer` | `70` | DB/file split ratio percentage |

### Product Type Values (restricted_prds)

| Value | Product | Description |
|-------|---------|-------------|
| `1` | FortiGate | Standard FortiGate firewall |
| `2` | FortiMail | Email security |
| `4` | FortiWeb | Web application firewall |
| `8` | FortiCache | Content delivery/caching |
| `16` | FortiCarrier | Carrier-grade firewall |
| `32` | FortiSandbox | Advanced threat protection |
| `128` | FortiAnalyzer | FortiAnalyzer devices |
| `256` | FortiClient | Endpoint security |
| `4503599627370495` | All Products | Support all product types |

> **💡 Tip:** Use `4503599627370495` to create an ADOM that supports all Fortinet products.

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/dvmdb/adom",
        "data": {
            "name": "customer-001",
            "desc": "Customer 001 Production Environment",
            "mr": 7,
            "os_ver": 0,
            "restricted_prds": 1,
            "log_disk_quota": 51200,
            "log_db_retention_hours": 2160,
            "log_file_retention_hours": 4320
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
            "name": "customer-001"
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/dvmdb/adom"
    }],
    "session": "{{session_id}}",
    "id": 1
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

def load_config():
    with open('.faz-env.json', 'r') as f:
        return json.load(f)

def login(config):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/user",
            "data": {"user": config['username'], "passwd": config['password']}
        }],
        "session": None,
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False, timeout=10)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result.get('session')
    raise Exception(f"Login failed")

def logout(config, session_id):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {"method": "exec", "params": [{"url": "/sys/logout"}], "session": session_id, "id": 999}
    requests.post(url, json=payload, verify=False)

def create_adom(session_id, config, name, desc="", mr=7, log_quota_mb=51200):
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    payload = {
        "method": "add",
        "params": [{
            "url": "/dvmdb/adom",
            "data": {
                "name": name,
                "desc": desc,
                "mr": mr,
                "os_ver": 0,
                "restricted_prds": 1,
                "log_disk_quota": log_quota_mb,
                "log_db_retention_hours": 2160,
                "log_file_retention_hours": 4320
            }
        }],
        "session": session_id,
        "id": 2
    }
    response = requests.post(url, json=payload, verify=False, timeout=30)
    result = response.json()
    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    raise Exception(f"ADOM creation failed: {result['result'][0]['status']['message']}")

def main():
    config = load_config()
    session_id = None
    try:
        session_id = login(config)
        print("✓ Logged in")

        result = create_adom(
            session_id=session_id,
            config=config,
            name="customer-prod-001",
            desc="Customer Production",
            mr=7,
            log_quota_mb=51200
        )
        print(f"✓ ADOM created: {result['name']}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        if session_id:
            logout(config, session_id)
            print("✓ Logged out")

if __name__ == "__main__":
    main()
```

### cURL Example

```bash
#!/bin/bash
FAZ_HOST="faz.example.com"
FAZ_PORT="443"
USERNAME="admin"
PASSWORD="your_password_here"

LOGIN_RESPONSE=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"method":"exec","params":[{"url":"/sys/login/user","data":{"user":"'${USERNAME}'","passwd":"'${PASSWORD}'"}}],"session":null,"id":1}')

SESSION_ID=$(echo $LOGIN_RESPONSE | jq -r '.session')
echo "✓ Logged in"

curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method":"add",
    "params":[{
      "url":"/dvmdb/adom",
      "data":{
        "name":"customer-prod-001",
        "desc":"Customer Production",
        "mr":7,
        "os_ver":0,
        "restricted_prds":1,
        "log_disk_quota":51200
      }
    }],
    "session":"'${SESSION_ID}'",
    "id":2
  }' | jq '.'

curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{"method":"exec","params":[{"url":"/sys/logout"}],"session":"'${SESSION_ID}'","id":999}' > /dev/null
echo "✓ Done"
```

## Best Practices

> **💡 Tip:** Match `mr` to device firmware versions for compatibility

> **⚠️ Warning:** Set appropriate log quotas based on device count and retention needs

## Error Handling

### Error Code -13: ADOM Already Exists

`````{tab-set}
````{tab-item} RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -13,
            "message": "Object already exists"
        }
    }]
}
```
````
`````

**Solution:** Choose a different ADOM name

## Related Endpoints

- [Enable ADOM](./enable-adom.md) - Enable ADOM feature
- [Get ADOMs](./get-adom-with-no-fields.md) - List ADOMs
- [Delete ADOM](./delete-adom.md) - Remove ADOM

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+ (tested on v8.0.0)
