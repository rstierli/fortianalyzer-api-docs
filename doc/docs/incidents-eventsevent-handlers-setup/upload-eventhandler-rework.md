# Upload Event Handler Configuration

Upload or import event handler configurations for bulk deployment and configuration management.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint uploads event handler configurations - useful for:
- Bulk deployment of event handlers across multiple ADOMs
- Configuration backup and restore operations
- Migrating event handler settings between systems
- Implementing configuration as code workflows
- Standardizing incident response automation across environments

Uploading event handler configurations enables consistent automated incident response deployment and simplified configuration management.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/conf-eventhandler`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "set",
    "params": [{
        "url": "/eventmgmt/adom/root/conf-eventhandler",
        "data": [
            {
                "name": "Critical_IPS_Alert",
                "description": "Critical IPS detections forwarded to Splunk and ServiceNow",
                "status": "enabled",
                "trigger": "ips-signature",
                "action": "webhook",
                "target": "Splunk_HEC"
            },
            {
                "name": "Ransomware_Detection",
                "description": "Ransomware indicators trigger immediate alerting",
                "status": "enabled",
                "trigger": "threat-signature",
                "action": "webhook",
                "target": "ServiceNow_Incidents"
            }
        ]
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
        "url": "/eventmgmt/adom/root/conf-eventhandler"
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def upload_event_handler_config(session_id, adom, handlers):
    """
    Upload event handler configurations

    Args:
        session_id: Active session ID
        adom: ADOM name
        handlers: List of event handler configuration dictionaries

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "set",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler",
            "data": handlers
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Uploaded {len(handlers)} event handler configurations")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Upload multiple event handlers
event_handlers = [
    {
        "name": "Critical_IPS_Alert",
        "description": "Critical IPS detections forwarded to Splunk and ServiceNow",
        "status": "enabled",
        "trigger": "ips-signature",
        "action": "webhook",
        "target": "Splunk_HEC"
    },
    {
        "name": "Ransomware_Detection",
        "description": "Ransomware indicators trigger immediate alerting",
        "status": "enabled",
        "trigger": "threat-signature",
        "action": "webhook",
        "target": "ServiceNow_Incidents"
    },
    {
        "name": "C2_Communication_Block",
        "description": "Command and control traffic detection and blocking",
        "status": "enabled",
        "trigger": "botnet-detection",
        "action": "webhook",
        "target": "Slack_Security_Channel"
    }
]

upload_event_handler_config(
    session_id="your_session_id",
    adom="root",
    handlers=event_handlers
)
```

## Use Cases

### Configuration Backup and Restore

```python
# Export existing event handlers
from get_eventhandler import get_event_handlers
import json
from datetime import datetime

# Backup: Export current configuration
handlers = get_event_handlers(session_id=session, adom="root")

backup_filename = f"event_handlers_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(backup_filename, 'w') as f:
    json.dump(handlers, f, indent=2)

print(f"✓ Backed up {len(handlers)} event handlers to {backup_filename}")

# Restore: Upload saved configuration
with open(backup_filename, 'r') as f:
    handlers_to_restore = json.load(f)

upload_event_handler_config(
    session_id=session,
    adom="root",
    handlers=handlers_to_restore
)

print(f"✓ Restored {len(handlers_to_restore)} event handlers")
```

### Multi-ADOM Deployment

```python
# Deploy standard event handlers across multiple ADOMs
standard_handlers = [
    {
        "name": "Critical_Security_Events",
        "description": "Critical security event forwarding",
        "status": "enabled",
        "trigger": "ips-signature",
        "action": "webhook",
        "target": "Splunk_HEC"
    },
    {
        "name": "Compliance_Alerts",
        "description": "Compliance violation notifications",
        "status": "enabled",
        "trigger": "policy-violation",
        "action": "webhook",
        "target": "ServiceNow_Incidents"
    }
]

adoms = ["root", "Production", "Development", "DMZ"]

for adom in adoms:
    try:
        upload_event_handler_config(
            session_id=session,
            adom=adom,
            handlers=standard_handlers
        )
        print(f"✓ {adom}: Deployed {len(standard_handlers)} handlers")
    except Exception as e:
        print(f"✗ {adom}: Failed - {e}")
```

### Configuration as Code

```python
# Load event handler definitions from YAML/JSON configuration file
import json

# Load configuration template
with open('event_handlers_config.json', 'r') as f:
    config = json.load(f)

# Customize for environment
env = "production"
handlers = []

for handler_template in config['event_handlers']:
    handler = handler_template.copy()
    handler['name'] = f"{env}_{handler['name']}"
    handler['description'] = f"[{env.upper()}] {handler['description']}"
    handlers.append(handler)

# Deploy to environment
upload_event_handler_config(
    session_id=session,
    adom="root",
    handlers=handlers
)

print(f"✓ Deployed {len(handlers)} event handlers for {env} environment")
```

### Migrate Between FortiAnalyzer Systems

```python
# Export from source FortiAnalyzer
source_session = login_to_faz("source-faz.example.com", "admin", "password")
source_handlers = get_event_handlers(session_id=source_session, adom="root")

print(f"✓ Exported {len(source_handlers)} handlers from source system")

# Import to destination FortiAnalyzer
dest_session = login_to_faz("dest-faz.example.com", "admin", "password")
upload_event_handler_config(
    session_id=dest_session,
    adom="root",
    handlers=source_handlers
)

print(f"✓ Imported {len(source_handlers)} handlers to destination system")
```

### Template-Based Deployment

```python
# Create event handlers from templates with variable substitution
handler_templates = {
    "ips_alert": {
        "name": "{severity}_IPS_Alert",
        "description": "{severity} IPS detections - {destination}",
        "status": "enabled",
        "trigger": "ips-signature",
        "action": "webhook",
        "target": "{destination}"
    },
    "threat_detection": {
        "name": "{threat_type}_Detection",
        "description": "{threat_type} threat detection - {destination}",
        "status": "enabled",
        "trigger": "threat-signature",
        "action": "webhook",
        "target": "{destination}"
    }
}

# Generate handlers from templates
deployments = [
    {"template": "ips_alert", "severity": "Critical", "destination": "Splunk_HEC"},
    {"template": "ips_alert", "severity": "High", "destination": "ServiceNow_Incidents"},
    {"template": "threat_detection", "threat_type": "Ransomware", "destination": "Slack_Security_Channel"},
    {"template": "threat_detection", "threat_type": "Botnet", "destination": "Splunk_HEC"}
]

handlers = []
for deploy in deployments:
    template = handler_templates[deploy['template']]
    handler = {k: v.format(**deploy) for k, v in template.items()}
    handlers.append(handler)

upload_event_handler_config(
    session_id=session,
    adom="root",
    handlers=handlers
)

print(f"✓ Deployed {len(handlers)} handlers from templates")
```

## Best Practices

> **💡 Tip:** Always backup existing event handler configurations before uploading new ones. The `set` method may overwrite existing configurations.

> **💡 Tip:** Validate event handler configurations in a test environment before deploying to production.

> **💡 Tip:** Use version control (Git) for event handler configuration files to track changes and enable rollback.

> **⚠️ Warning:** Ensure all referenced automation connectors (targets) exist in the destination ADOM before uploading event handlers.

> **💡 Tip:** Include timestamps and environment identifiers in event handler descriptions for better tracking and auditing.

## Related Endpoints

- [Get Event Handlers](./get-eventhandler.md) - Export existing configurations
- [Add Fabric Connector Event Handler](./add-fabric-connector-eventhandler.md) - Link connectors
- [Disable Event Handler](./disable-eventhandler.md) - Disable uploaded handlers
- [Get Automation Connectors](../incidents-eventsautomation-connectors/get-fabric-conector.md) - Verify target connectors exist

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
