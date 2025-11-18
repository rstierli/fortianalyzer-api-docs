# Update Event Handler Target Status

Enable or disable specific targets (automation connectors) within an event handler configuration.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint manages the enabled/disabled state of event handler targets - useful for:
- Temporarily disabling event forwarding to specific destinations
- Testing event handler configurations without full deactivation
- Maintenance mode for downstream systems (SIEM, SOAR, ticketing)
- Troubleshooting event forwarding issues
- Gradual rollout of event handler changes

Disabling a target stops event forwarding to that specific destination while keeping the event handler and other targets active.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/conf-eventhandler/{handler_name}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "update",
    "params": [{
        "url": "/eventmgmt/adom/root/conf-eventhandler/Critical_IPS_Alert",
        "data": {
            "target": "Splunk_HEC",
            "status": "enabled"
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
        "url": "/eventmgmt/adom/root/conf-eventhandler/Critical_IPS_Alert"
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_event_handler_target_status(session_id, adom, handler_name, target, enabled=True):
    """
    Enable or disable event handler target

    Args:
        session_id: Active session ID
        adom: ADOM name
        handler_name: Event handler name
        target: Target connector name
        enabled: True to enable, False to disable (default: True)

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    status = "enabled" if enabled else "disabled"

    payload = {
        "method": "update",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler/{handler_name}",
            "data": {
                "target": target,
                "status": status
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Target '{target}' {status} for event handler '{handler_name}'")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Enable Splunk target for critical event handler
update_event_handler_target_status(
    session_id="your_session_id",
    adom="root",
    handler_name="Critical_IPS_Alert",
    target="Splunk_HEC",
    enabled=True
)
```

## Use Cases

### Maintenance Mode - Disable Target

```python
# Temporarily disable Splunk forwarding during SIEM maintenance
update_event_handler_target_status(
    session_id=session,
    adom="root",
    handler_name="Critical_IPS_Alert",
    target="Splunk_HEC",
    enabled=False
)

print("⚠️ Splunk target disabled for maintenance")
print("   Events will continue forwarding to other targets")
```

### Re-enable After Maintenance

```python
# Re-enable Splunk target after maintenance window
update_event_handler_target_status(
    session_id=session,
    adom="root",
    handler_name="Critical_IPS_Alert",
    target="Splunk_HEC",
    enabled=True
)

print("✓ Splunk target re-enabled - event forwarding resumed")
```

### Selective Target Management

```python
# Disable non-critical targets, keep critical ones active
handler_name = "Critical_IPS_Alert"

targets_to_disable = ["Slack_Security_Channel", "Teams_SOC_Channel"]
targets_to_keep = ["Splunk_HEC", "ServiceNow_Incidents"]

print(f"Managing targets for '{handler_name}':\n")

# Disable non-critical chat notifications
for target in targets_to_disable:
    update_event_handler_target_status(
        session_id=session,
        adom="root",
        handler_name=handler_name,
        target=target,
        enabled=False
    )
    print(f"✗ Disabled: {target}")

# Ensure critical targets remain enabled
for target in targets_to_keep:
    update_event_handler_target_status(
        session_id=session,
        adom="root",
        handler_name=handler_name,
        target=target,
        enabled=True
    )
    print(f"✓ Enabled: {target}")
```

### Bulk Target Status Update

```python
# Toggle all targets for an event handler
from get_fabric_connector_eventhandler import get_event_handler_connectors

handler_name = "Critical_IPS_Alert"
new_status = False  # Disable all

connectors = get_event_handler_connectors(
    session_id=session,
    adom="root",
    event_handler_id=1
)

for conn in connectors:
    target_name = conn['name']
    update_event_handler_target_status(
        session_id=session,
        adom="root",
        handler_name=handler_name,
        target=target_name,
        enabled=new_status
    )
    status_icon = "✓" if new_status else "✗"
    print(f"{status_icon} {target_name}: {'enabled' if new_status else 'disabled'}")
```

## Best Practices

> **💡 Tip:** Disable individual targets instead of the entire event handler when performing maintenance on specific downstream systems.

> **💡 Tip:** Document target status changes in event handler descriptions for audit trail and team awareness.

> **⚠️ Warning:** Disabling targets stops event forwarding to those destinations. Ensure alternative alerting is in place if disabling critical targets.

> **💡 Tip:** Use selective targeting for gradual rollout - enable targets one at a time to verify event forwarding works correctly.

## Related Endpoints

- [Get Fabric Connector Event Handlers](./get-fabric-connector-eventhandler.md) - List configured targets
- [Disable Event Handler](./disable-eventhandler.md) - Disable entire event handler
- [Update Event Handler Description](./update-eventhandler-description.md) - Document configuration changes
- [Get Event Handlers](./get-eventhandler.md) - List all event handlers

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
