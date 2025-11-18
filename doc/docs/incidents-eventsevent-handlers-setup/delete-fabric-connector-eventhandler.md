# Delete Fabric Connector from Event Handler

Unlink an automation connector from an event handler.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint removes automation connector associations from event handlers - useful for:
- Removing deprecated webhook integrations from event handlers
- Changing event routing configurations
- Decommissioning retired SIEM/SOAR connections
- Troubleshooting event forwarding issues
- Managing event handler lifecycle

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/config/trigger/{eid}/fabric-connector/{connector_name}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/eventmgmt/adom/root/config/trigger/1/fabric-connector/Splunk_HEC"
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
        "url": "/eventmgmt/adom/root/config/trigger/1/fabric-connector/Splunk_HEC"
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

def delete_fabric_connector_from_event_handler(session_id, adom, event_handler_id, connector_name):
    """
    Unlink automation connector from event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        event_handler_id: Event handler ID (integer)
        connector_name: Name of connector to unlink

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "delete",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/config/trigger/{event_handler_id}/fabric-connector/{connector_name}"
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Unlinked connector '{connector_name}' from event handler {event_handler_id}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Remove Slack connector from event handler
delete_fabric_connector_from_event_handler(
    session_id="your_session_id",
    adom="root",
    event_handler_id=1,
    connector_name="Slack_Security_Channel"
)
```

## Use Cases

### Remove Deprecated Connector

```python
# Remove old test connector from event handler
delete_fabric_connector_from_event_handler(
    session_id=session,
    adom="root",
    event_handler_id=1,
    connector_name="Old_Test_Webhook"
)
```

### Cleanup Multiple Connectors

```python
# Remove multiple deprecated connectors from handler
deprecated_connectors = ["Old_Splunk_Test", "Deprecated_Teams", "Test_Webhook"]

for connector in deprecated_connectors:
    try:
        delete_fabric_connector_from_event_handler(
            session_id=session,
            adom="root",
            event_handler_id=1,
            connector_name=connector
        )
        print(f"✓ Removed: {connector}")
    except Exception as e:
        print(f"✗ Failed to remove {connector}: {e}")
```

### Safe Delete with Verification

```python
# Verify connector exists before deleting
from get_fabric_connector_eventhandler import get_event_handler_connectors

connectors = get_event_handler_connectors(
    session_id=session,
    adom="root",
    event_handler_id=1
)

connector_names = [c['name'] for c in connectors]
connector_to_delete = "Old_Integration"

if connector_to_delete in connector_names:
    confirm = input(f"Remove connector '{connector_to_delete}' from event handler? (yes/no): ")

    if confirm.lower() == 'yes':
        delete_fabric_connector_from_event_handler(
            session_id=session,
            adom="root",
            event_handler_id=1,
            connector_name=connector_to_delete
        )
else:
    print(f"✗ Connector '{connector_to_delete}' not linked to this handler")
```

## Best Practices

> **⚠️ Warning:** Unlinking a connector immediately stops event forwarding to that destination. Verify the connector is no longer needed before removal.

> **💡 Tip:** List connectors using [Get Fabric Connector Event Handlers](./get-fabric-connector-eventhandler.md) before deletion to ensure you're removing the correct association.

> **💡 Tip:** The connector itself (webhook configuration) remains intact after unlinking. Only the association to the event handler is removed.

## Related Endpoints

- [Get Fabric Connector Event Handlers](./get-fabric-connector-eventhandler.md) - List linked connectors
- [Add Fabric Connector Event Handler](./add-fabric-connector-eventhandler.md) - Link connector to handler
- [Get Event Handlers](./get-eventhandler.md) - List all event handlers
- [Get Automation Connectors](../incidents-eventsautomation-connectors/get-fabric-conector.md) - List available connectors

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
