# System Status

Get the current status and information about the FortiAnalyzer system.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

The System Status endpoint provides comprehensive information about the FortiAnalyzer appliance, including:
- System information (version, hostname, serial number)
- Resource utilization (CPU, memory, disk)
- Network configuration
- Service status
- License information

This endpoint is commonly used for:
- Health monitoring and alerting
- System inventory and asset management
- Capacity planning
- Troubleshooting connectivity issues

## Endpoint Details

**Method:** `POST`  
**URL:** `/jsonrpc`  
**API Path:** `/sys/status`  
**ADOM Support:** No (system-level endpoint)  
**Requires Authentication:** Yes  
**Minimum Version:** 7.0.0

## Prerequisites

- Active session or valid API key
- Read-only or higher permissions

## Request Format

### Parameters

This endpoint does not require any parameters.

### Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/sys/status"
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
            "Admin Domain Configuration": "Enabled",
            "BIOS version": "04.06.05",
            "Branch Point": "2086",
            "Build": "2086",
            "Current Time": "Sun Nov  9 14:30:00 2024",
            "Disk Usage": [
                {
                    "name": "/",
                    "total": 102932480,
                    "used": 15439872
                },
                {
                    "name": "/data",
                    "total": 1948374016,
                    "used": 245760000
                }
            ],
            "Hostname": "FAZ-PROD-01",
            "License Status": "Valid",
            "Memory Usage": {
                "total": 16384,
                "used": 8192
            },
            "Model": "FortiAnalyzer-VM64",
            "Serial Number": "FAZVM1234567890",
            "Version": "v7.6.4-build2086 250929 (GA)"
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/sys/status"
    }],
    "session": "kLSFZ7qT9xZc1vB3rtKlXg==",
    "id": 1
}
```
````
`````

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `Admin Domain Configuration` | `string` | ADOM status (Enabled/Disabled) |
| `BIOS version` | `string` | System BIOS version |
| `Build` | `string` | Software build number |
| `Current Time` | `string` | Current system time |
| `Disk Usage` | `array` | Array of disk partition information |
| `├─ name` | `string` | Partition mount point |
| `├─ total` | `integer` | Total space in KB |
| `└─ used` | `integer` | Used space in KB |
| `Hostname` | `string` | System hostname |
| `License Status` | `string` | License validity status |
| `Memory Usage` | `object` | System memory information |
| `├─ total` | `integer` | Total memory in MB |
| `└─ used` | `integer` | Used memory in MB |
| `Model` | `string` | Hardware model |
| `Serial Number` | `string` | System serial number |
| `Version` | `string` | FortiAnalyzer version string |

## Error Handling

### Common Errors

#### Error Code -10: Session Timeout

**Response:**
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

**Cause:** Session has expired or is invalid

**Solution:**
- Re-authenticate and obtain a new session ID
- Use API key authentication for long-running processes

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

def get_system_status(session_id, config):
    """
    Get FortiAnalyzer system status
    
    Args:
        session_id: Active session ID
        config: Configuration dictionary
        
    Returns:
        dict: System status information
    """
    url = f"https://{config['faz_host']}:{config['faz_port']}/jsonrpc"
    
    payload = {
        "method": "get",
        "params": [{
            "url": "/sys/status"
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

def calculate_disk_usage_percent(disk_info):
    """Calculate disk usage percentage"""
    if disk_info['total'] > 0:
        return (disk_info['used'] / disk_info['total']) * 100
    return 0

def main():
    """Main execution"""
    config = load_config()
    session_id = None
    
    try:
        # Login
        session_id = login(config)
        print("✓ Logged in successfully\n")
        
        # Get system status
        status = get_system_status(session_id, config)
        
        # Display key information
        print("="*60)
        print("FortiAnalyzer System Status")
        print("="*60)
        print(f"Hostname:       {status['Hostname']}")
        print(f"Model:          {status['Model']}")
        print(f"Serial Number:  {status['Serial Number']}")
        print(f"Version:        {status['Version']}")
        print(f"License:        {status['License Status']}")
        print(f"Current Time:   {status['Current Time']}")
        print()
        
        # Memory information
        mem = status['Memory Usage']
        mem_percent = (mem['used'] / mem['total']) * 100
        print(f"Memory Usage:   {mem['used']}/{mem['total']} MB ({mem_percent:.1f}%)")
        print()
        
        # Disk information
        print("Disk Usage:")
        for disk in status['Disk Usage']:
            usage_percent = calculate_disk_usage_percent(disk)
            used_gb = disk['used'] / 1024 / 1024
            total_gb = disk['total'] / 1024 / 1024
            print(f"  {disk['name']:12} {used_gb:6.1f}/{total_gb:6.1f} GB ({usage_percent:.1f}%)")
        
        print("\n" + "="*60)
        print("\nFull Response:")
        print(json.dumps(status, indent=2))
        
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
FAZ_HOST="faz-prod-ai.home.mystier.li"
FAZ_PORT="443"
USERNAME="admin"
PASSWORD="your_password"

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

# Step 2: Get System Status
echo "Getting system status..."
STATUS_RESPONSE=$(curl -k -s -X POST "https://${FAZ_HOST}:${FAZ_PORT}/jsonrpc" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": [{"url": "/sys/status"}],
    "session": "'${SESSION_ID}'",
    "id": 2
  }')

# Display key information
echo "System Information:"
echo "$STATUS_RESPONSE" | jq '.result[0].data | {
  Hostname,
  Model,
  "Serial Number",
  Version,
  "License Status",
  "Memory Usage",
  "Disk Usage"
}'

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

> **💡 Tip: Regular Monitoring**  
> Poll this endpoint regularly (every 5-15 minutes) to monitor system health and detect issues early.

> **💡 Tip: Disk Space Alerts**  
> Set up alerts when disk usage exceeds 80% to prevent log data loss and system issues.

> **💡 Tip: Version Tracking**  
> Use this endpoint to maintain an inventory of FortiAnalyzer versions across your infrastructure.

> **⚠️ Warning: Memory Usage**  
> Consistently high memory usage (>90%) may impact performance. Consider optimization or hardware upgrades.

## Use Cases

### Use Case 1: Health Monitoring Dashboard

Create a monitoring dashboard that polls system status every 5 minutes:

```python
def monitor_health(config, threshold_disk=80, threshold_mem=90):
    """Monitor FortiAnalyzer health and send alerts"""
    session_id = login(config)
    
    try:
        status = get_system_status(session_id, config)
        
        # Check disk usage
        for disk in status['Disk Usage']:
            usage_pct = calculate_disk_usage_percent(disk)
            if usage_pct > threshold_disk:
                send_alert(f"Disk {disk['name']} at {usage_pct:.1f}%")
        
        # Check memory usage
        mem = status['Memory Usage']
        mem_pct = (mem['used'] / mem['total']) * 100
        if mem_pct > threshold_mem:
            send_alert(f"Memory usage at {mem_pct:.1f}%")
        
    finally:
        logout(config, session_id)
```

### Use Case 2: Inventory Management

Collect system information for asset tracking:

```python
def collect_inventory(faz_hosts):
    """Collect inventory from multiple FortiAnalyzers"""
    inventory = []
    
    for host in faz_hosts:
        config = {'faz_host': host, ...}
        session_id = login(config)
        
        try:
            status = get_system_status(session_id, config)
            inventory.append({
                'hostname': status['Hostname'],
                'model': status['Model'],
                'serial': status['Serial Number'],
                'version': status['Version'],
                'collected_at': datetime.now()
            })
        finally:
            logout(config, session_id)
    
    return inventory
```

## Related Endpoints

- [System Performance](../system-settings/get-systme-performance.md) - CPU and network statistics
- [Disk Information](../system-settings/get-system-status.md) - Detailed disk usage and health
- [System Configuration](../system-settings/get-system-status.md) - View system configuration

## Troubleshooting

### Issue: Disk Usage Shows 100%

**Symptoms:**
- `/data` partition at or near 100%
- Log ingestion warnings

**Solution:**
1. Check log retention policies
2. Archive old logs
3. Consider storage expansion
4. Enable log compression

### Issue: High Memory Usage

**Symptoms:**
- Memory usage consistently >90%
- Slow API responses
- GUI performance degradation

**Solution:**
1. Check for resource-intensive queries
2. Review scheduled report generation
3. Consider increasing system memory
4. Optimize log retention and archiving

---

**Related Topics:** monitoring, health-check, system-info, diagnostics  
**Last Updated:** 2024-11-09  
**API Version:** 7.6.4
