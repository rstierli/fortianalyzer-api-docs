# Get ADOMs (No Field Filter)

Retrieve a list of all Administrative Domains (ADOMs) configured on the FortiAnalyzer with complete details.

> **✅ All code examples tested:** All Python and cURL examples in this guide have been verified against a live FortiAnalyzer system and work as documented.

## Overview

This endpoint retrieves all ADOMs configured on your FortiAnalyzer without field filtering, returning complete ADOM information. ADOMs are logical containers that allow you to segregate devices and logs based on organization, customer, or administrative requirements.

**Common use cases:**
- Inventory all ADOMs in your FortiAnalyzer
- Audit ADOM configurations
- Build ADOM selection dropdowns in applications
- Monitor log storage quotas per ADOM
- Verify ADOM settings and status

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom`
**ADOM Support:** N/A (system-level operation)
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0

## Prerequisites

- Active session or valid API key
- Read permissions for device database
- ADOMs must be enabled on FortiAnalyzer (see [Enable ADOM](./enable-adom.md))

## Request Format

### Parameters

This endpoint accepts no required parameters. Optional field filtering is available via the `fields` parameter.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `fields` | `array` | No | All fields | List of specific fields to return |

### Common Fields

When using field filtering, you can specify:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | ADOM name |
| `oid` | `integer` | Object ID (unique identifier) |
| `desc` | `string` | Description |
| `mr` | `integer` | Major release version support |
| `os_ver` | `integer` | OS version support |
| `state` | `integer` | ADOM state (1=enabled, 0=disabled) |
| `mode` | `integer` | ADOM mode |
| `log_disk_quota` | `integer` | Log disk quota in MB |
| `log_disk_quota_alert_thres` | `integer` | Alert threshold percentage |
| `log_db_retention_hours` | `integer` | Database log retention in hours |
| `log_file_retention_hours` | `integer` | File log retention in hours |
| `uuid` | `string` | Unique identifier |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom"
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
                "create_time": 0,
                "desc": "",
                "flags": 136,
                "lock_override": 0,
                "log_db_retention_hours": 1440,
                "log_disk_quota": 1000,
                "log_disk_quota_alert_thres": 90,
                "log_disk_quota_split_ratio": 70,
                "log_file_retention_hours": 8760,
                "mig_mr": 0,
                "mig_os_ver": 0,
                "mode": 1,
                "mr": 4,
                "name": "root",
                "oid": 3,
                "os_ver": 7,
                "primary_dns_ip4": "0.0.0.0",
                "restricted_prds": 128,
                "secondary_dns_ip4": "0.0.0.0",
                "state": 1,
                "tz": -1,
                "uuid": "039f0634-53d9-51ef-6e5c-b41767d7c754",
                "workspace_mode": 0
            },
            {
                "name": "FortiGate",
                "oid": 128,
                "desc": "FortiGate devices",
                "mr": 4,
                "os_ver": 7,
                "state": 1
            }
        ],
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

## Response Format

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | ADOM name (e.g., "root", "FortiGate") |
| `oid` | `integer` | Object ID - unique identifier for the ADOM |
| `desc` | `string` | ADOM description |
| `mr` | `integer` | Major release version (e.g., 4 = v4.x) |
| `os_ver` | `integer` | Operating system version (e.g., 7 = v7.x) |
| `state` | `integer` | ADOM state: 1 (enabled), 0 (disabled) |
| `mode` | `integer` | ADOM mode setting |
| `log_disk_quota` | `integer` | Log disk quota in megabytes |
| `log_disk_quota_alert_thres` | `integer` | Alert threshold percentage (default: 90) |
| `log_db_retention_hours` | `integer` | Database log retention time in hours |
| `log_file_retention_hours` | `integer` | File log retention time in hours |
| `workspace_mode` | `integer` | Workspace mode: 0 (disabled), 1 (enabled) |
| `uuid` | `string` | Universally unique identifier |
| `create_time` | `integer` | ADOM creation timestamp |
| `flags` | `integer` | ADOM flags bitfield |
| `tz` | `integer` | Timezone setting (-1 = use system timezone) |

## Complete Example

### Python Example

```python
import json
import requests
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config():
    """Load FortiAnalyzer configuration from .faz-env.json"""
    with open('.faz-env.json', 'r') as f:
        return json.load(f)

def login(config):
    """Establish session with FortiAnalyzer"""
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "exec",
        "params": [{
            "url": "/sys/login/user",
            "data": {
                "user": config['username'],
                "passwd": config['password']
            }
        }],
        "session": None,
        "id": 1
    }

    try:
        response = requests.post(url, json=payload, verify=False, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result['result'][0]['status']['code'] == 0:
            return result.get('session')
        else:
            raise Exception(f"Login failed: {result['result'][0]['status']['message']}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection error: {str(e)}")

def logout(config, session_id):
    """Terminate session with FortiAnalyzer"""
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "exec",
        "params": [{"url": "/sys/logout"}],
        "session": session_id,
        "id": 999
    }

    requests.post(url, json=payload, verify=False)

def get_all_adoms(session_id, config):
    """
    Get all ADOMs with complete details

    Args:
        session_id: Active session ID
        config: Configuration dictionary

    Returns:
        list: List of ADOM dictionaries
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": "/dvmdb/adom"
        }],
        "session": session_id,
        "id": 2
    }

    try:
        response = requests.post(url, json=payload, verify=False, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result['result'][0]['status']['code'] == 0:
            return result['result'][0]['data']
        else:
            raise Exception(f"API error: {result['result'][0]['status']['message']}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def display_adom_summary(adoms):
    """Display summary of ADOMs"""
    print(f"\n{'='*70}")
    print(f"{'ADOM Name':<25} {'OID':<8} {'State':<10} {'Description'}")
    print(f"{'='*70}")

    for adom in adoms:
        name = adom.get('name', 'N/A')
        oid = adom.get('oid', 'N/A')
        state = 'Enabled' if adom.get('state', 0) == 1 else 'Disabled'
        desc = adom.get('desc', '')[:30]  # Truncate long descriptions

        print(f"{name:<25} {oid:<8} {state:<10} {desc}")

def main():
    """Main execution"""
    config = load_config()
    session_id = None

    try:
        # Login
        session_id = login(config)
        print("✓ Logged in successfully")

        # Get all ADOMs
        print("\nRetrieving all ADOMs...")
        adoms = get_all_adoms(session_id, config)

        print(f"✓ Found {len(adoms)} ADOMs")

        # Display summary
        display_adom_summary(adoms)

        # Display detailed info for root ADOM
        root_adom = next((a for a in adoms if a.get('name') == 'root'), None)
        if root_adom:
            print(f"\n{'='*70}")
            print("Root ADOM Details:")
            print(f"{'='*70}")
            print(f"  Name: {root_adom.get('name')}")
            print(f"  OID: {root_adom.get('oid')}")
            print(f"  Major Release: v{root_adom.get('mr')}.x")
            print(f"  OS Version: v{root_adom.get('os_ver')}.x")
            print(f"  Log Disk Quota: {root_adom.get('log_disk_quota')} MB")
            print(f"  Alert Threshold: {root_adom.get('log_disk_quota_alert_thres')}%")
            print(f"  DB Retention: {root_adom.get('log_db_retention_hours')} hours")
            print(f"  File Retention: {root_adom.get('log_file_retention_hours')} hours")
            print(f"  Workspace Mode: {'Enabled' if root_adom.get('workspace_mode') else 'Disabled'}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")
    finally:
        # Always logout
        if session_id:
            logout(config, session_id)
            print("\n✓ Logged out")

if __name__ == "__main__":
    main()
```

### cURL Example

```bash
#!/bin/bash

# Configuration
FAZ_HOST="faz.example.com"
FAZ_PORT="443"
USERNAME="admin"
PASSWORD="your_password_here"

# Step 1: Login
echo "Logging in..."
LOGIN_RESPONSE=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "exec",
    "params": [{
      "url": "/sys/login/user",
      "data": {"user": "'${USERNAME}'", "passwd": "'${PASSWORD}'"}
    }],
    "session": null,
    "id": 1
  }')

SESSION_ID=$(echo $LOGIN_RESPONSE | jq -r '.session')
echo "✓ Session ID: $SESSION_ID"
echo

# Step 2: Get all ADOMs
echo "Getting all ADOMs..."
ADOMS=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": [{
      "url": "/dvmdb/adom"
    }],
    "session": "'${SESSION_ID}'",
    "id": 2
  }')

# Display results
echo "✓ ADOMs retrieved"
echo
echo "ADOM List:"
echo "$ADOMS" | jq -r '.result[0].data[] | "  - \(.name) (OID: \(.oid), State: \(if .state == 1 then "Enabled" else "Disabled" end))"'

# Step 3: Logout
echo
echo "Logging out..."
curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "exec",
    "params": [{"url": "/sys/logout"}],
    "session": "'${SESSION_ID}'",
    "id": 999
  }' > /dev/null

echo "✓ Logged out"
```

## Best Practices

> **💡 Tip: Caching ADOM List**
> Cache the ADOM list in your application as ADOMs rarely change. Refresh periodically (e.g., every 15 minutes) rather than on every operation.

> **💡 Tip: Field Filtering**
> Use field filtering (see [Get ADOMs with Fields](./get-adom-with-fields.md)) when you only need specific information to reduce response size and improve performance.

> **💡 Tip: OID vs Name**
> Use the ADOM OID (Object ID) for internal operations as it's immutable. The ADOM name can be changed by administrators.

> **⚠️ Warning: Built-in ADOMs**
> Some ADOMs like "root", "rootp", and product-specific ADOMs (FortiGate, FortiMail, etc.) are built-in and cannot be deleted.

## Use Cases

### Use Case 1: Build ADOM Selection Menu

Create a dropdown menu for users to select an ADOM:

```python
def get_adom_choices(session_id, config):
    """Get ADOM list for UI dropdown"""
    adoms = get_all_adoms(session_id, config)

    # Filter to only enabled, non-system ADOMs
    user_adoms = [
        {'name': a['name'], 'oid': a['oid']}
        for a in adoms
        if a.get('state') == 1 and a.get('name') not in ['rootp', 'Unmanaged_Devices']
    ]

    return sorted(user_adoms, key=lambda x: x['name'])
```

### Use Case 2: Monitor Log Storage Quotas

Alert when ADOMs approach their log storage limits:

```python
def check_adom_quotas(session_id, config, alert_threshold=80):
    """Check ADOMs approaching storage quotas"""
    adoms = get_all_adoms(session_id, config)
    alerts = []

    for adom in adoms:
        quota = adom.get('log_disk_quota', 0)
        alert_pct = adom.get('log_disk_quota_alert_thres', 90)

        # In real scenario, you'd query actual usage
        # This is just the configured threshold
        if alert_pct >= alert_threshold:
            alerts.append({
                'adom': adom['name'],
                'quota_mb': quota,
                'alert_threshold': alert_pct
            })

    return alerts
```

### Use Case 3: ADOM Inventory Report

Generate a comprehensive ADOM inventory:

```python
def generate_adom_inventory(session_id, config):
    """Generate ADOM inventory report"""
    adoms = get_all_adoms(session_id, config)

    inventory = []
    for adom in adoms:
        inventory.append({
            'Name': adom.get('name'),
            'OID': adom.get('oid'),
            'Status': 'Enabled' if adom.get('state') == 1 else 'Disabled',
            'Version': f"v{adom.get('mr')}.{adom.get('os_ver')}",
            'Log Quota (MB)': adom.get('log_disk_quota'),
            'DB Retention (hrs)': adom.get('log_db_retention_hours'),
            'Workspace Mode': 'Yes' if adom.get('workspace_mode') else 'No'
        })

    return inventory
```

## Error Handling

### Common Errors

#### Error Code -10: Session Timeout

`````{tab-set}
````{tab-item} RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -10,
            "message": "Session timeout"
        }
    }]
}
```
````
`````

**Cause:** Session has expired or is invalid

**Solution:**
- Re-authenticate and obtain a new session ID
- Use API key authentication for stateless operations

#### Error: ADOMs Not Enabled

**Symptom:** Empty ADOM list or error response

**Solution:**
- Verify ADOM feature is enabled on FortiAnalyzer
- Use the [Enable ADOM](./enable-adom.md) endpoint
- Check administrator has permissions to view ADOMs

## Related Endpoints

- [Get ADOMs with Field Filter](./get-adom-with-fields.md) - Get ADOMs with specific fields only
- [Enable ADOM](./enable-adom.md) - Enable ADOM feature on FortiAnalyzer
- [Add ADOM (FortiOS)](./add-adom-fos.md) - Create a new ADOM
- [Delete ADOM](./delete-adom.md) - Remove an ADOM

## Troubleshooting

### Issue: Too Many ADOMs Returned

**Symptoms:**
- Response contains many product-specific ADOMs
- Slow response times

**Solution:**
1. Use field filtering to reduce response size
2. Filter client-side to show only relevant ADOMs
3. Cache results to avoid repeated API calls

### Issue: Missing Expected ADOM

**Symptoms:**
- ADOM exists in UI but not in API response
- Inconsistent ADOM counts

**Solution:**
1. Verify administrator permissions
2. Check ADOM state (may be disabled)
3. Refresh FortiAnalyzer ADOM cache
4. Verify API session is using correct credentials

---

> **✅ Verification:** All code examples tested against FortiAnalyzer v8.0.0 and verified to work correctly.

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+ (tested on v8.0.0)
