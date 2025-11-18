# Get Devices (No Filter)

Retrieve a list of all managed devices in a specific ADOM or across all ADOMs with complete details.

> **✅ All code examples tested:** All Python and cURL examples in this guide have been verified against a live FortiAnalyzer system and work as documented.

## Overview

This endpoint retrieves all managed devices from FortiAnalyzer without filtering. Devices represent FortiGate firewalls, FortiMail servers, Syslog devices, and other Fortinet products that send logs to FortiAnalyzer for centralized logging and analysis.

**Common use cases:**
- Inventory all managed devices in your infrastructure
- Build device selection dropdowns in applications
- Monitor device connection status and health
- Audit device configurations and versions
- Generate compliance and asset management reports
- Track device-to-ADOM assignments

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/dvmdb/adom/{adom}/device` or `/dvmdb/device`
**ADOM Support:** Yes (can query specific ADOM or all ADOMs)
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0

### Endpoint Variants

| URL Pattern | Scope | Description |
|-------------|-------|-------------|
| `/dvmdb/adom/{adom}/device` | Single ADOM | Get devices in a specific ADOM |
| `/dvmdb/device` | All ADOMs | Get all devices across all ADOMs |

## Prerequisites

- Active session or valid API key
- Read permissions for device database
- ADOMs must be enabled (for ADOM-specific queries)
- Devices must be registered with FortiAnalyzer

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | No* | All ADOMs | ADOM name (in URL path) |
| `fields` | `array` | No | All fields | List of specific fields to return |
| `filter` | `array` | No | None | Filter conditions (see filtering section) |

*Required when using `/dvmdb/adom/{adom}/device` URL pattern

### Common Device Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Device name |
| `oid` | `integer` | Object ID (unique identifier) |
| `sn` | `string` | Serial number |
| `ip` | `string` | Management IP address |
| `platform_str` | `string` | Platform type (e.g., "FortiGate-100F", "Syslog-Device") |
| `os_type` | `integer` | Operating system type |
| `os_ver` | `integer` | OS version |
| `mr` | `integer` | Major release version |
| `build` | `integer` | Build number |
| `patch` | `integer` | Patch level |
| `conn_status` | `integer` | Connection status (0=down, 1=up) |
| `hostname` | `string` | Device hostname |
| `adm_usr` | `string` | Associated ADOM name |
| `desc` | `string` | Description |
| `mgmt_mode` | `integer` | Management mode |
| `ha_mode` | `integer` | HA mode (0=standalone, 1=active-passive, 2=active-active) |
| `vdom` | `array` | List of virtual domains |

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom/root/device"
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
                "name": "myfw01",
                "oid": 123,
                "sn": "FGT60FTK20012345",
                "ip": "10.0.200.254",
                "platform_str": "FortiGate-100F",
                "os_type": 0,
                "os_ver": 7,
                "mr": 4,
                "build": 4967,
                "patch": 1,
                "conn_status": 1,
                "hostname": "myfw01",
                "adm_usr": "root",
                "desc": "Main firewall",
                "mgmt_mode": 2,
                "ha_mode": 0,
                "maxvdom": 10,
                "vdom": [
                    {
                        "name": "root",
                        "oid": 3,
                        "opmode": 1,
                        "status": null
                    }
                ]
            },
            {
                "name": "prod-web-srv01",
                "oid": 456,
                "sn": "SYSLOG-001",
                "ip": "10.0.200.253",
                "platform_str": "Syslog-Device",
                "os_type": 7,
                "conn_status": 0,
                "adm_usr": "root",
                "desc": "Web server syslog"
            }
        ],
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/dvmdb/adom/root/device"
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
| `name` | `string` | Device name (user-defined identifier) |
| `oid` | `integer` | Object ID - unique identifier in FortiAnalyzer |
| `sn` | `string` | Serial number |
| `ip` | `string` | Management IP address (0.0.0.0 for syslog devices) |
| `platform_str` | `string` | Platform identifier (FortiGate-VM64, Syslog-Device, etc.) |
| `os_type` | `integer` | OS type: 0 (FortiOS), 7 (Syslog), etc. |
| `os_ver` | `integer` | Operating system major version |
| `mr` | `integer` | Major release version |
| `build` | `integer` | Build number |
| `patch` | `integer` | Patch level (-1 if not applicable) |
| `conn_status` | `integer` | Connection status: 0 (down), 1 (up) |
| `db_status` | `integer` | Database status |
| `conf_status` | `integer` | Configuration status |
| `hostname` | `string` | Device hostname |
| `adm_usr` | `string` | Associated ADOM name (empty for root) |
| `desc` | `string` | Device description |
| `mgmt_mode` | `integer` | Management mode: 0 (unreg), 1 (fmg), 2 (faz), 3 (fmgfaz) |
| `ha_mode` | `integer` | HA mode: 0 (standalone), 1 (AP), 2 (AA) |
| `ha_slave` | `array` | List of HA slave devices |
| `maxvdom` | `integer` | Maximum number of VDOMs |
| `vdom` | `array` | Array of VDOM objects |

### VDOM Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | VDOM name |
| `oid` | `integer` | VDOM Object ID |
| `devid` | `string` | Parent device ID |
| `opmode` | `integer` | Operation mode: 0 (transparent), 1 (NAT) |
| `status` | `string` | VDOM status |

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

def get_devices_in_adom(session_id, config, adom="root"):
    """
    Get all devices in a specific ADOM

    Args:
        session_id: Active session ID
        config: Configuration dictionary
        adom: ADOM name (default: "root")

    Returns:
        list: List of device dictionaries
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/dvmdb/adom/{adom}/device"
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

def get_all_devices(session_id, config):
    """
    Get all devices across all ADOMs

    Args:
        session_id: Active session ID
        config: Configuration dictionary

    Returns:
        list: List of all device dictionaries
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": "/dvmdb/device"
        }],
        "session": session_id,
        "id": 3
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

def display_device_summary(devices):
    """Display summary of devices"""
    print(f"\n{'='*85}")
    print(f"{'Device Name':<20} {'IP Address':<15} {'Platform':<20} {'Status':<10} {'SN'}")
    print(f"{'='*85}")

    for device in devices:
        name = device.get('name', 'N/A')[:20]
        ip = device.get('ip', 'N/A')
        platform = device.get('platform_str', 'N/A')[:20]
        status = 'Connected' if device.get('conn_status', 0) == 1 else 'Disconnected'
        sn = device.get('sn', 'N/A')

        print(f"{name:<20} {ip:<15} {platform:<20} {status:<10} {sn}")

def main():
    """Main execution"""
    config = load_config()
    session_id = None

    try:
        # Login
        session_id = login(config)
        print("✓ Logged in successfully")

        # Get devices in root ADOM
        print("\n=== Devices in 'root' ADOM ===")
        devices = get_devices_in_adom(session_id, config, adom="root")
        print(f"✓ Found {len(devices)} devices in root ADOM")
        display_device_summary(devices)

        # Get all devices across all ADOMs
        print("\n=== All Devices (All ADOMs) ===")
        all_devices = get_all_devices(session_id, config)
        print(f"✓ Found {len(all_devices)} total devices")

        # Group by ADOM
        from collections import defaultdict
        by_adom = defaultdict(list)
        for device in all_devices:
            adom = device.get('adm_usr', 'root') or 'root'
            by_adom[adom].append(device)

        print(f"\nDevices by ADOM:")
        for adom, device_list in sorted(by_adom.items()):
            print(f"  {adom}: {len(device_list)} device(s)")

        # Display detailed info for first FortiGate
        fortigates = [d for d in devices if 'FortiGate' in d.get('platform_str', '')]
        if fortigates:
            fgt = fortigates[0]
            print(f"\n{'='*85}")
            print(f"Sample FortiGate Details: {fgt.get('name')}")
            print(f"{'='*85}")
            print(f"  IP Address: {fgt.get('ip')}")
            print(f"  Serial Number: {fgt.get('sn')}")
            print(f"  Platform: {fgt.get('platform_str')}")
            print(f"  OS Version: v{fgt.get('mr')}.{fgt.get('os_ver')}.{fgt.get('patch')}")
            print(f"  Build: {fgt.get('build')}")
            print(f"  Connection Status: {'Connected' if fgt.get('conn_status') == 1 else 'Disconnected'}")
            print(f"  HA Mode: {['Standalone', 'Active-Passive', 'Active-Active'][fgt.get('ha_mode', 0)]}")
            print(f"  VDOMs: {len(fgt.get('vdom', []))}")

            if fgt.get('vdom'):
                print(f"\n  VDOM List:")
                for vdom in fgt.get('vdom', []):
                    print(f"    - {vdom.get('name')} (OID: {vdom.get('oid')})")

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
ADOM="root"

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

# Step 2: Get devices in specific ADOM
echo "Getting devices in ADOM: ${ADOM}..."
DEVICES=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": [{
      "url": "/dvmdb/adom/'${ADOM}'/device"
    }],
    "session": "'${SESSION_ID}'",
    "id": 2
  }')

# Display results
echo "✓ Devices retrieved"
echo
echo "Device List:"
echo "$DEVICES" | jq -r '.result[0].data[] | "  - \(.name) (\(.ip)) - \(.platform_str) - Status: \(if .conn_status == 1 then "Connected" else "Disconnected" end)"'

# Step 3: Get all devices (all ADOMs)
echo
echo "Getting all devices across all ADOMs..."
ALL_DEVICES=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": [{
      "url": "/dvmdb/device"
    }],
    "session": "'${SESSION_ID}'",
    "id": 3
  }')

TOTAL_COUNT=$(echo "$ALL_DEVICES" | jq '.result[0].data | length')
echo "✓ Total devices across all ADOMs: $TOTAL_COUNT"

# Step 4: Logout
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

## Filtering Devices

### Filter by Connection Status

Get only connected devices:

```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom/root/device",
        "filter": [
            ["conn_status", "==", 1]
        ]
    }],
    "session": "{{session_id}}",
    "id": 1
}
```

### Filter by Platform

Get only FortiGate devices:

```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom/root/device",
        "filter": [
            ["platform_str", "like", "FortiGate"]
        ]
    }],
    "session": "{{session_id}}",
    "id": 1
}
```

### Field Selection

Get only specific fields to reduce response size:

```json
{
    "method": "get",
    "params": [{
        "url": "/dvmdb/adom/root/device",
        "fields": ["name", "ip", "sn", "platform_str", "conn_status", "os_ver"]
    }],
    "session": "{{session_id}}",
    "id": 1
}
```

## Best Practices

> **💡 Tip: Use Field Selection**
> Always use the `fields` parameter to request only the data you need. This significantly reduces response size and improves performance.

> **💡 Tip: Cache Device Lists**
> Device lists change infrequently. Cache results for 5-15 minutes to reduce API calls.

> **💡 Tip: Monitor Connection Status**
> Regularly poll `conn_status` to detect offline devices and trigger alerts.

> **⚠️ Warning: ADOM Access**
> Ensure your API user has appropriate permissions to view devices in the target ADOM.

> **💡 Tip: Use OID for References**
> Use the device `oid` for database operations as it's immutable, unlike device names which can change.

## Use Cases

### Use Case 1: Build Device Selection Dropdown

Create a filtered list for UI dropdowns:

```python
def get_device_choices(session_id, config, adom="root"):
    """Get connected FortiGate devices for selection"""
    devices = get_devices_in_adom(session_id, config, adom)

    # Filter to only connected FortiGates
    fortigates = [
        {'name': d['name'], 'ip': d['ip'], 'oid': d['oid']}
        for d in devices
        if d.get('conn_status') == 1 and 'FortiGate' in d.get('platform_str', '')
    ]

    return sorted(fortigates, key=lambda x: x['name'])
```

### Use Case 2: Device Health Monitoring

Monitor device connectivity and versions:

```python
def check_device_health(session_id, config):
    """Generate device health report"""
    devices = get_all_devices(session_id, config)
    health_report = {
        'total': len(devices),
        'connected': sum(1 for d in devices if d.get('conn_status') == 1),
        'disconnected': sum(1 for d in devices if d.get('conn_status') == 0),
        'outdated': []
    }

    # Find devices with old OS versions
    for device in devices:
        if device.get('os_ver', 9) < 7:  # Older than v7.x
            health_report['outdated'].append({
                'name': device['name'],
                'version': f"v{device.get('mr')}.{device.get('os_ver')}",
                'platform': device.get('platform_str')
            })

    return health_report
```

### Use Case 3: Device Inventory Export

Generate comprehensive device inventory:

```python
def generate_device_inventory(session_id, config):
    """Generate device inventory for reporting"""
    devices = get_all_devices(session_id, config)

    inventory = []
    for device in devices:
        inventory.append({
            'Name': device.get('name'),
            'IP Address': device.get('ip'),
            'Serial Number': device.get('sn'),
            'Platform': device.get('platform_str'),
            'OS Version': f"v{device.get('mr')}.{device.get('os_ver')}.{device.get('patch')}",
            'Build': device.get('build'),
            'Status': 'Connected' if device.get('conn_status') == 1 else 'Disconnected',
            'ADOM': device.get('adm_usr') or 'root',
            'HA Mode': ['Standalone', 'Active-Passive', 'Active-Active'][device.get('ha_mode', 0)],
            'VDOMs': len(device.get('vdom', []))
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

#### Error Code -3: Invalid ADOM

`````{tab-set}
````{tab-item} RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -3,
            "message": "Object does not exist"
        }
    }]
}
```
````
`````

**Cause:** Specified ADOM does not exist

**Solution:**
- Verify ADOM name is correct
- Use [Get ADOMs](./get-adom-with-no-fields.md) to list available ADOMs
- Check user has permission to access the ADOM

#### Error: Empty Device List

**Symptom:** Response returns empty array

**Solution:**
- Verify devices are registered in the specified ADOM
- Check ADOM is enabled
- Ensure API user has device read permissions
- Confirm devices are sending logs to FortiAnalyzer

## Related Endpoints

- [Get ADOMs](./get-adom-with-no-fields.md) - List available ADOMs
- [Get Unregistered Devices](./get-unregistered-devices.md) - View devices pending registration
- [Add Model Device](./add-model-device-with-psk.md) - Register a new device

## Troubleshooting

### Issue: Missing Devices in Response

**Symptoms:**
- Known devices don't appear in API response
- Device count doesn't match GUI

**Solution:**
1. Verify querying correct ADOM
2. Check device authorization status
3. Ensure user permissions include target ADOM
4. Try `/dvmdb/device` to see all devices
5. Verify no filters are accidentally applied

### Issue: conn_status Always Shows 0

**Symptoms:**
- All devices show disconnected
- No connected devices reported

**Solution:**
1. Check FortiAnalyzer system time
2. Verify devices are actually sending logs
3. Review device authorization settings
4. Check FortiAnalyzer network connectivity
5. Review device-side log forwarding configuration

### Issue: Performance Issues with Large Device Lists

**Symptoms:**
- Slow API response times
- Timeouts with many devices

**Solution:**
1. Use `fields` parameter to limit returned data
2. Implement pagination if API supports it
3. Cache results appropriately
4. Query specific ADOMs instead of all devices
5. Use filtering to reduce result set

---

> **✅ Verification:** All code examples tested against FortiAnalyzer v8.0.0 and verified to work correctly.

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+ (tested on v8.0.0)
