# Get Automation Connectors (Webhooks)

Retrieve configured automation connectors (webhooks) for incident and event management integrations.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves automation connector configurations - useful for:
- Listing all configured webhooks and integrations
- Auditing automation connector settings
- Verifying SIEM/SOAR/ticketing system integrations
- Checking webhook status and connectivity
- Documentation and configuration backup

Automation connectors enable FortiAnalyzer to send events and alerts to external systems (Splunk, QRadar, ServiceNow, Slack, Microsoft Teams, custom webhooks).

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/system/webhook`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to system configuration in specified ADOM
- Administrative permissions for automation connector management

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/config/adom/root/system/webhook"
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
                "name": "Splunk_SIEM",
                "uri": "https://splunk.example.com:8088/services/collector",
                "protocol": "HTTPS",
                "port": 8088,
                "method": 0,
                "conn-type": 0,
                "auth-status": 1,
                "status": 1,
                "description": "Splunk HEC Integration",
                "title": "Splunk SIEM",
                "color": "#00AA00"
            },
            {
                "name": "ServiceNow_Tickets",
                "uri": "https://yourinstance.service-now.com/api/now/table/incident",
                "protocol": "HTTPS",
                "port": 443,
                "method": 0,
                "conn-type": 0,
                "auth-status": 1,
                "status": 1,
                "description": "ServiceNow Incident Creation",
                "title": "ServiceNow",
                "color": "#62D84E"
            }
        ],
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/config/adom/root/system/webhook"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Connector name (unique identifier) |
| `uri` | `string` | Webhook URL endpoint |
| `protocol` | `string` | Protocol: "HTTPS", "HTTP" |
| `port` | `integer` | Port number |
| `method` | `integer` | HTTP method: 0=POST, 1=GET, 2=PUT |
| `conn-type` | `integer` | Connection type |
| `auth-status` | `integer` | Authentication status: 0=disabled, 1=enabled |
| `status` | `integer` | Connector status: 0=disabled, 1=enabled |
| `description` | `string` | Connector description |
| `title` | `string` | Display title |
| `color` | `string` | UI color code (hex) |

## Complete Python Example

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_automation_connectors(session_id, adom="root"):
    """
    Get all automation connectors (webhooks)

    Args:
        session_id: Active session ID
        adom: ADOM name (default: "root")

    Returns:
        list: Automation connector configurations
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/config/adom/{adom}/system/webhook"
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        return result['result'][0]['data']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example usage
connectors = get_automation_connectors(session_id="your_session_id")

print(f"Total Automation Connectors: {len(connectors)}\n")

for conn in connectors:
    status_icon = "✓" if conn['status'] == 1 else "✗"
    print(f"{status_icon} {conn['name']} ({conn['title']})")
    print(f"   URL: {conn['uri']}")
    print(f"   Protocol: {conn['protocol']}:{conn['port']}")
    print(f"   Status: {'Enabled' if conn['status'] == 1 else 'Disabled'}")
    print()
```

## Use Cases

### Audit Webhook Configurations

```python
# Audit all configured webhooks
connectors = get_automation_connectors(session_id=session)

print("Webhook Configuration Audit:\n")
enabled_count = sum(1 for c in connectors if c['status'] == 1)
disabled_count = len(connectors) - enabled_count

print(f"Total Connectors: {len(connectors)}")
print(f"  Enabled: {enabled_count}")
print(f"  Disabled: {disabled_count}\n")

# Check for insecure HTTP connectors
insecure = [c for c in connectors if c['protocol'] == 'HTTP']
if insecure:
    print("⚠️ Insecure HTTP Connectors Detected:")
    for conn in insecure:
        print(f"  - {conn['name']}: {conn['uri']}")
```

### Export Connector Configuration

```python
# Export webhook configurations to JSON
import json
from datetime import datetime

connectors = get_automation_connectors(session_id=session)

backup = {
    "export_date": datetime.now().isoformat(),
    "adom": "root",
    "connectors": connectors
}

filename = f"webhooks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, 'w') as f:
    json.dump(backup, f, indent=2)

print(f"✓ Exported {len(connectors)} connectors to {filename}")
```

## Related Endpoints

- [Add Automation Connector](./add-fabric-conector.md) - Create new webhook connector
- [Delete Automation Connector](./delete-fabric-conector.md) - Remove webhook connector

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
