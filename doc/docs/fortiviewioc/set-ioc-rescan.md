# Configure IOC Rescan Settings

Configure Indicator of Compromise (IOC) rescan settings for UEBA threat analysis.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint configures IOC rescan settings for UEBA - useful for:
- Enabling automated historical log rescanning for new IOC signatures
- Configuring rescan time range to balance thoroughness vs. performance
- Adjusting IOC detection sensitivity across log types
- Retroactive threat detection after IOC database updates
- Compliance requirements for historical threat analysis
- Identifying previously undetected compromises

IOC rescanning allows FortiAnalyzer to reanalyze historical logs when new threat indicators are added, helping identify compromises that occurred before the IOC was known.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/ueba/ioc-rescan`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Administrative access to ADOM configuration
- UEBA feature enabled on FortiAnalyzer
- IOC feature enabled
- Sufficient storage for historical log analysis

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `last-ndays` | `integer` | Yes | - | Number of days to rescan (1-365) |
| `logtype` | `integer` | Yes | - | Log type to scan (see Log Types table) |
| `status` | `integer` | Yes | - | Enable (1) or disable (0) IOC rescan |

### Log Types

| Value | Log Type | Description |
|-------|----------|-------------|
| `1` | Traffic | Firewall traffic logs |
| `2` | Event | System and security events |
| `4` | Virus | Antivirus detection logs |
| `7` | All Logs | All available log types |
| `8` | Web Filter | Web filtering logs |
| `16` | IPS | Intrusion prevention logs |

> **💡 Tip:** Use `logtype: 7` to scan all log types for comprehensive IOC detection.

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "set",
    "params": [{
        "url": "/config/adom/root/ueba/ioc-rescan",
        "data": {
            "last-ndays": 7,
            "logtype": 7,
            "status": 1
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
        },
        "url": "/config/adom/root/ueba/ioc-rescan"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

## Response Fields

The endpoint returns an empty data object on success. Check the status code:

| Status Code | Meaning |
|-------------|---------|
| `0` | Success - IOC rescan settings updated |
| `-10` | Session timeout or invalid |
| `-3` | Permission denied |
| `-1` | Generic error (check message) |

## Complete Python Example

```python
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def set_ioc_rescan(session_id, adom, days=7, logtype=7, enabled=True):
    """
    Configure IOC rescan settings for UEBA

    Args:
        session_id: Active session ID
        adom: ADOM name
        days: Number of days to rescan (1-365, default: 7)
        logtype: Log type to scan (1-7, default: 7 for all logs)
        enabled: Enable (True) or disable (False) IOC rescan

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "set",
        "params": [{
            "url": f"/config/adom/{adom}/ueba/ioc-rescan",
            "data": {
                "last-ndays": days,
                "logtype": logtype,
                "status": 1 if enabled else 0
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        status_msg = "enabled" if enabled else "disabled"
        print(f"✓ IOC rescan {status_msg} for last {days} days (logtype: {logtype})")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Enable IOC rescan for last 7 days, all log types
success = set_ioc_rescan(
    session_id="your_session_id",
    adom="root",
    days=7,
    logtype=7,  # All logs
    enabled=True
)

if success:
    print("IOC rescan configuration updated successfully")
```

## Use Cases

### Enable Comprehensive IOC Scanning

```python
# Enable IOC rescan for last 30 days across all log types
set_ioc_rescan(
    session_id=session,
    adom="root",
    days=30,
    logtype=7,  # All logs
    enabled=True
)
print("✓ Enabled comprehensive IOC scanning for 30-day history")
```

### Targeted IPS Log Scanning

```python
# Scan only IPS logs for last 14 days
set_ioc_rescan(
    session_id=session,
    adom="root",
    days=14,
    logtype=16,  # IPS logs only
    enabled=True
)
print("✓ Enabled IPS log IOC scanning for 14-day history")
```

### Disable IOC Rescan

```python
# Disable IOC rescan to reduce system load
set_ioc_rescan(
    session_id=session,
    adom="root",
    days=7,
    logtype=7,
    enabled=False
)
print("✓ IOC rescan disabled")
```

### Graduated Scanning Strategy

```python
# Implement graduated scanning based on log criticality
log_configs = [
    {"type": 16, "days": 30, "name": "IPS"},      # IPS: 30 days
    {"type": 4, "days": 30, "name": "Virus"},     # Virus: 30 days
    {"type": 1, "days": 7, "name": "Traffic"},    # Traffic: 7 days
    {"type": 8, "days": 7, "name": "WebFilter"}   # WebFilter: 7 days
]

for config in log_configs:
    set_ioc_rescan(
        session_id=session,
        adom="root",
        days=config['days'],
        logtype=config['type'],
        enabled=True
    )
    print(f"✓ Configured {config['name']} logs: {config['days']} days")
```

### Post-IOC-Update Scanning

```python
# After importing new IOC signatures, rescan recent history
def trigger_ioc_rescan_after_update(session_id, adom):
    """
    Enable aggressive IOC rescan after IOC database update
    """
    # Enable 90-day comprehensive scan
    set_ioc_rescan(
        session_id=session_id,
        adom=adom,
        days=90,
        logtype=7,  # All logs
        enabled=True
    )
    print("✓ IOC rescan enabled for 90-day retrospective analysis")
    print("⚠️ Note: This may impact system performance")

    # Recommendation: Monitor system load
    print("Monitor FortiAnalyzer system load during rescan")

# Usage after IOC update
trigger_ioc_rescan_after_update(session, "root")
```

## Error Handling

`````{tab-set}
````{tab-item} ERROR RESPONSE - Invalid Parameter
```json
{
    "result": [{
        "status": {
            "code": -1,
            "message": "Invalid parameter value"
        }
    }]
}
```
````
`````

**Common causes:**
- `last-ndays` outside valid range (1-365)
- Invalid `logtype` value
- UEBA or IOC feature not enabled
- ADOM does not exist

`````{tab-set}
````{tab-item} ERROR RESPONSE - Permission Denied
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

**Common causes:**
- Insufficient administrative privileges
- ADOM access restrictions
- Read-only user account

## Best Practices

> **💡 Tip:** Start with shorter rescan periods (7 days) and increase gradually to avoid performance impact.

> **⚠️ Warning:** Scanning 365 days of logs can significantly impact FortiAnalyzer performance. Schedule during maintenance windows.

> **💡 Tip:** Use targeted log type scanning (e.g., IPS only) when investigating specific threat types.

> **💡 Tip:** Disable IOC rescan when not needed to conserve system resources.

## Performance Considerations

| Rescan Period | Performance Impact | Recommended Use Case |
|---------------|-------------------|---------------------|
| 1-7 days | Low | Daily operations |
| 8-30 days | Moderate | Weekly security reviews |
| 31-90 days | High | Post-incident investigations |
| 91-365 days | Very High | Annual compliance audits |

## Configuration Strategy

**Recommended approach:**

1. **Normal Operations:** 7-day rescan, all logs
2. **Security Incident:** Extend to 30-90 days temporarily
3. **Compliance Audit:** 365 days, schedule during off-hours
4. **Resource Constrained:** IPS + Virus logs only, 7 days

## Monitoring Rescan Impact

After enabling IOC rescan:

1. Monitor FortiAnalyzer CPU and disk I/O
2. Check UEBA dashboard for new IOC detections
3. Review system logs for rescan completion
4. Adjust timeframe if performance degrades

## Related Endpoints

- [Get UEBA Endpoints by EPID](../fabric-viewasset-identity-center/get-ueba-endpoints-by-epid.md) - Query UEBA endpoint data
- [Search Attack Logs](../logview/create-search-task-for-attack---signature.md) - Search IPS detection logs
- [Top Threats](../fortiviewtop-threats/create-task.md) - Analyze threat patterns

## IOC Rescan Workflow

**Typical workflow after enabling:**

1. **Enable rescan** - Configure settings via this endpoint
2. **Monitor progress** - Check FortiAnalyzer system dashboard
3. **Review detections** - Check UEBA IOC alerts
4. **Investigate hits** - Analyze any historical compromises detected
5. **Adjust settings** - Fine-tune based on results and performance

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
