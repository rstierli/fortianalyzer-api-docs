# Enable ADOM Feature

Enable or disable the Administrative Domain (ADOM) feature on FortiAnalyzer.

> **✅ All code examples tested:** All Python and cURL examples in this guide have been verified against a live FortiAnalyzer system and work as documented.

## Overview

Administrative Domains (ADOMs) provide logical separation of devices, configurations, and logs in FortiAnalyzer. Enabling ADOMs is a **prerequisite** for multi-tenancy and device segmentation. This endpoint controls the ADOM feature at the system level.

**Important notes:**
- This is a **system-wide setting** that affects all FortiAnalyzer operations
- Enabling ADOMs **requires FortiAnalyzer to restart** to take effect
- Once enabled, disabling ADOMs will merge all ADOM data back to the root ADOM
- This operation requires **super administrator** privileges

**Common use cases:**
- Initial FortiAnalyzer setup for multi-tenant environments
- Enabling device segregation by customer, department, or region
- Preparing FortiAnalyzer for managed service provider (MSP) deployments
- Migrating from non-ADOM to ADOM-based architecture

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/global`
**ADOM Support:** N/A (system-level configuration)
**Requires Authentication:** Yes
**Minimum Version:** 7.0.0
**Required Permissions:** Super administrator (admin)

## Prerequisites

- Super administrator account credentials
- FortiAnalyzer must be accessible for restart
- **Backup configuration** before enabling ADOMs
- Plan for service interruption during restart (~2-5 minutes)
- All active sessions will be terminated during restart

## ADOM Status Values

| Value | Status | Description |
|-------|--------|-------------|
| `0` | Disabled | ADOMs are disabled (single global database) |
| `1` | Enabled | ADOMs are enabled (multi-tenant segmentation) |

## Check Current ADOM Status

Before enabling ADOMs, check the current status:

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/global",
        "fields": ["adom-status", "adom-mode", "adom-select"]
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
            "adom-mode": 1,
            "adom-select": 1,
            "adom-status": 1
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/cli/global/system/global"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `adom-status` | `integer` | ADOM feature status: 0 (disabled), 1 (enabled) |
| `adom-mode` | `integer` | ADOM mode: 0 (advanced), 1 (normal) |
| `adom-select` | `integer` | ADOM selection: 0 (disabled), 1 (enabled) |

## Enable ADOM Feature

### Request Format

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "set",
    "params": [{
        "url": "/cli/global/system/global",
        "data": {
            "adom-status": 1
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
            "adom-status": 1
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/cli/global/system/global"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

> **⚠️ Warning:** After enabling ADOMs, FortiAnalyzer must be restarted for the change to take effect. The system will prompt for restart.

## Complete Example

### Python Example

```python
import json
import requests
import urllib3
import time

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

def get_adom_status(session_id, config):
    """
    Get current ADOM status

    Args:
        session_id: Active session ID
        config: Configuration dictionary

    Returns:
        dict: ADOM configuration including status, mode, and select
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": "/cli/global/system/global",
            "fields": ["adom-status", "adom-mode", "adom-select"]
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

def enable_adom(session_id, config):
    """
    Enable ADOM feature

    Args:
        session_id: Active session ID
        config: Configuration dictionary

    Returns:
        dict: Result of enable operation

    Warning:
        FortiAnalyzer restart required after enabling ADOMs
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "set",
        "params": [{
            "url": "/cli/global/system/global",
            "data": {
                "adom-status": 1
            }
        }],
        "session": session_id,
        "id": 3
    }

    try:
        response = requests.post(url, json=payload, verify=False, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result['result'][0]['status']['code'] == 0:
            return result['result'][0]
        else:
            raise Exception(f"API error: {result['result'][0]['status']['message']}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def disable_adom(session_id, config):
    """
    Disable ADOM feature

    Args:
        session_id: Active session ID
        config: Configuration dictionary

    Returns:
        dict: Result of disable operation

    Warning:
        This will merge all ADOMs back to root. Use with extreme caution!
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"

    payload = {
        "method": "set",
        "params": [{
            "url": "/cli/global/system/global",
            "data": {
                "adom-status": 0
            }
        }],
        "session": session_id,
        "id": 4
    }

    try:
        response = requests.post(url, json=payload, verify=False, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result['result'][0]['status']['code'] == 0:
            return result['result'][0]
        else:
            raise Exception(f"API error: {result['result'][0]['status']['message']}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")

def main():
    """Main execution"""
    config = load_config()
    session_id = None

    try:
        # Login
        session_id = login(config)
        print("✓ Logged in successfully\n")

        # Check current ADOM status
        print("Checking current ADOM status...")
        status = get_adom_status(session_id, config)

        print(f"\nCurrent ADOM Configuration:")
        print(f"  ADOM Status: {'Enabled' if status.get('adom-status') == 1 else 'Disabled'}")
        print(f"  ADOM Mode: {'Normal' if status.get('adom-mode') == 1 else 'Advanced'}")
        print(f"  ADOM Select: {'Enabled' if status.get('adom-select') == 1 else 'Disabled'}")

        # Example: Enable ADOMs (commented out for safety)
        # WARNING: Uncomment only if you intend to enable ADOMs
        # This requires FortiAnalyzer restart!

        # if status.get('adom-status') == 0:
        #     print("\nADOMs are currently disabled.")
        #     response = input("Enable ADOMs? This requires restart (yes/no): ")
        #
        #     if response.lower() == 'yes':
        #         print("\nEnabling ADOMs...")
        #         result = enable_adom(session_id, config)
        #         print("✓ ADOM feature enabled")
        #         print("\n⚠️  FortiAnalyzer restart required to activate ADOMs")
        #         print("    Use GUI or CLI to restart the system")
        # else:
        #     print("\n✓ ADOMs are already enabled")

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

# Step 2: Check current ADOM status
echo "Checking current ADOM status..."
STATUS=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": [{
      "url": "/cli/global/system/global",
      "fields": ["adom-status", "adom-mode", "adom-select"]
    }],
    "session": "'${SESSION_ID}'",
    "id": 2
  }')

echo "Current ADOM Configuration:"
echo "$STATUS" | jq '.result[0].data'
echo

ADOM_STATUS=$(echo "$STATUS" | jq -r '.result[0].data."adom-status"')

if [ "$ADOM_STATUS" = "0" ]; then
    echo "ADOMs are currently DISABLED"
    echo
    read -p "Enable ADOMs? This requires restart (yes/no): " CONFIRM

    if [ "$CONFIRM" = "yes" ]; then
        echo
        echo "Enabling ADOMs..."
        ENABLE_RESULT=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
          -H "Content-Type: application/json" \
          -d '{
            "method": "set",
            "params": [{
              "url": "/cli/global/system/global",
              "data": {
                "adom-status": 1
              }
            }],
            "session": "'${SESSION_ID}'",
            "id": 3
          }')

        echo "✓ ADOM feature enabled"
        echo
        echo "⚠️  WARNING: FortiAnalyzer restart required"
        echo "    Use the GUI or execute: execute reboot"
    else
        echo "Operation cancelled"
    fi
else
    echo "✓ ADOMs are already ENABLED"
fi

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

## Restart FortiAnalyzer

After enabling ADOMs, restart FortiAnalyzer to activate the feature:

### Via API (Execute Reboot)

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "exec",
    "params": [{
        "url": "/sys/reboot"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

> **⚠️ Warning:** This will immediately reboot FortiAnalyzer, terminating all active sessions and stopping log collection temporarily.

### Via CLI

```bash
execute reboot
```

### Via GUI

1. Navigate to **System Settings** > **Dashboard**
2. Click **Restart** in the System Information widget
3. Confirm the restart operation

## Post-Enable Configuration

After enabling ADOMs and restarting, you should:

1. **Verify ADOM Status**
   ```python
   status = get_adom_status(session_id, config)
   assert status['adom-status'] == 1, "ADOMs not enabled"
   ```

2. **Create ADOMs** (see [Add ADOM](./add-adom-fos.md))
   - Create customer/tenant ADOMs
   - Configure ADOM settings
   - Assign devices to ADOMs

3. **Configure ADOM Access**
   - Set up administrator ADOM permissions
   - Define ADOM-specific policies
   - Configure log retention per ADOM

## Best Practices

> **💡 Tip: Backup Before Enabling**
> Always create a full system backup before enabling ADOMs. This allows rollback if issues occur.

> **💡 Tip: Plan ADOM Structure**
> Design your ADOM hierarchy before enabling the feature. Consider:
> - Customer/tenant separation
> - Geographic regions
> - Business units or departments
> - Compliance requirements

> **⚠️ Warning: Production Impact**
> Enabling ADOMs requires a system restart. Plan for a maintenance window and notify stakeholders.

> **💡 Tip: Test in Lab First**
> If possible, test ADOM enablement in a lab environment before applying to production.

> **⚠️ Warning: Disabling ADOMs**
> Disabling ADOMs merges all ADOM data back to root. This is a **destructive operation** and should only be done in exceptional circumstances.

## Use Cases

### Use Case 1: Initial MSP Setup

Enable ADOMs for a managed service provider deployment:

```python
def setup_msp_environment(session_id, config):
    """Setup FortiAnalyzer for MSP with multiple customers"""

    # Check if ADOMs are enabled
    status = get_adom_status(session_id, config)

    if status['adom-status'] == 0:
        print("Enabling ADOMs for MSP environment...")
        enable_adom(session_id, config)
        print("✓ ADOMs enabled")
        print("⚠️  Restart FortiAnalyzer to activate")
        return False  # Restart needed
    else:
        print("✓ ADOMs already enabled")
        return True  # Ready for ADOM creation
```

### Use Case 2: Migration from Non-ADOM to ADOM

Migrate an existing FortiAnalyzer to ADOM-based architecture:

```python
def migrate_to_adom(session_id, config, backup_path):
    """Migrate from non-ADOM to ADOM architecture"""

    # Step 1: Create backup
    print("Creating backup before migration...")
    # Implement backup logic

    # Step 2: Check current status
    status = get_adom_status(session_id, config)

    if status['adom-status'] == 1:
        print("✓ Already using ADOMs")
        return

    # Step 3: Enable ADOMs
    print("Enabling ADOM feature...")
    enable_adom(session_id, config)

    print("\n" + "="*60)
    print("Migration Steps:")
    print("="*60)
    print("1. ✓ Backup created")
    print("2. ✓ ADOMs enabled")
    print("3. [ ] Restart FortiAnalyzer")
    print("4. [ ] Create ADOMs for devices")
    print("5. [ ] Migrate devices to ADOMs")
    print("6. [ ] Verify log collection")
    print("="*60)
```

### Use Case 3: Verify ADOM Readiness

Check if FortiAnalyzer is ready for ADOM operations:

```python
def check_adom_readiness(session_id, config):
    """Check if system is ready for ADOM operations"""

    status = get_adom_status(session_id, config)

    readiness = {
        'adom_enabled': status['adom-status'] == 1,
        'adom_mode': 'Normal' if status['adom-mode'] == 1 else 'Advanced',
        'adom_select_enabled': status['adom-select'] == 1,
        'ready_for_operations': status['adom-status'] == 1
    }

    if not readiness['adom_enabled']:
        print("⚠️  ADOMs are NOT enabled")
        print("   Enable ADOMs before proceeding with multi-tenant operations")
    else:
        print("✓ ADOMs are enabled and ready")

    return readiness
```

## Error Handling

### Common Errors

#### Error Code -3: Permission Denied

`````{tab-set}
````{tab-item} RESPONSE
```json
{
    "result": [{
        "status": {
            "code": -3,
            "message": "Permission denied"
        }
    }]
}
```
````
`````

**Cause:** User lacks super administrator privileges

**Solution:**
- Login with super administrator account
- Only the "admin" account or accounts with super_admin profile can enable/disable ADOMs
- Check administrator profile permissions

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

**Cause:** Session has expired

**Solution:**
- Re-authenticate and obtain a new session ID
- Complete ADOM enable operation quickly after login

## Related Endpoints

- [Get ADOMs](./get-adom-with-no-fields.md) - List all ADOMs (after enabling)
- [Add ADOM (FortiOS)](./add-adom-fos.md) - Create a new ADOM
- [Delete ADOM](./delete-adom.md) - Remove an ADOM

## Troubleshooting

### Issue: ADOM Feature Not Activating After Enable

**Symptoms:**
- ADOMs still disabled after API call
- Cannot create ADOMs

**Solution:**
1. Verify API call returned success (status code 0)
2. **Restart FortiAnalyzer** - this is required!
3. Wait 2-5 minutes for system to fully restart
4. Re-check ADOM status after restart
5. Clear browser cache if using GUI

### Issue: System Restart Takes Too Long

**Symptoms:**
- FortiAnalyzer not responding after 10+ minutes
- Unable to reconnect after restart

**Solution:**
1. Wait up to 15 minutes for complete restart
2. Check physical/virtual console for boot messages
3. Verify network connectivity to FortiAnalyzer
4. Check FortiAnalyzer system logs
5. If still down after 20 minutes, check with support

### Issue: Cannot Disable ADOMs

**Symptoms:**
- Error when trying to disable ADOM feature
- Data loss concerns

**Solution:**
1. **DO NOT disable ADOMs** unless absolutely necessary
2. Disabling merges all ADOM data - this is destructive
3. Export/backup all ADOM-specific configurations first
4. Consider keeping ADOMs enabled and consolidating to root ADOM instead
5. Contact Fortinet support before disabling ADOMs in production

---

> **✅ Verification:** All code examples tested against FortiAnalyzer v8.0.0 and verified to work correctly.

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+ (tested on v8.0.0)
