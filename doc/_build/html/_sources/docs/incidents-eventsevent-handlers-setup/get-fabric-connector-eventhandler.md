# Get Fabric Connector Event Handlers

Retrieve automation connectors linked to a specific event handler.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves automation connector associations for event handlers - useful for:
- Auditing event handler webhook configurations
- Verifying event routing destinations
- Documenting incident response workflows
- Troubleshooting event forwarding issues
- Compliance reporting and configuration backup

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/config/trigger/{eid}/fabric-connector`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/eventmgmt/adom/root/config/trigger/1/fabric-connector"
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
                "name": "Splunk_HEC",
                "status": "enabled"
            },
            {
                "name": "ServiceNow_Incidents",
                "status": "enabled"
            }
        ],
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/eventmgmt/adom/root/config/trigger/1/fabric-connector"
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

def get_event_handler_connectors(session_id, adom, event_handler_id):
    """
    Get automation connectors linked to event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        event_handler_id: Event handler ID (integer)

    Returns:
        list: Linked automation connectors
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/config/trigger/{event_handler_id}/fabric-connector"
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

# Example: Get connectors for event handler 1
connectors = get_event_handler_connectors(
    session_id="your_session_id",
    adom="root",
    event_handler_id=1
)

print(f"Event Handler 1 - Linked Connectors:\n")
for conn in connectors:
    status_icon = "✓" if conn.get('status') == 'enabled' else "✗"
    print(f"{status_icon} {conn['name']}")
```

## Use Cases

### Audit All Event Handler Configurations

```python
# Audit all event handlers and their connector associations
from get_eventhandler import get_event_handlers

handlers = get_event_handlers(session_id=session, adom="root")

print("Event Handler Audit:\n")
for handler in handlers:
    handler_id = handler.get('id', 'unknown')
    connectors = get_event_handler_connectors(
        session_id=session,
        adom="root",
        event_handler_id=handler_id
    )

    print(f"Handler: {handler.get('name')}")
    print(f"  Connectors: {len(connectors)}")
    for conn in connectors:
        print(f"    - {conn['name']} ({conn.get('status', 'unknown')})")
    print()
```

### Verify Critical Event Routing

```python
# Verify critical event handlers have required connectors
critical_handler_id = 1
required_connectors = ["Splunk_HEC", "ServiceNow_Incidents", "Slack_Security_Channel"]

connectors = get_event_handler_connectors(
    session_id=session,
    adom="root",
    event_handler_id=critical_handler_id
)

configured_names = [c['name'] for c in connectors if c.get('status') == 'enabled']

missing = set(required_connectors) - set(configured_names)

if missing:
    print(f"⚠️ Critical handler missing connectors: {', '.join(missing)}")
else:
    print(f"✓ All required connectors configured and enabled")
```

## Related Endpoints

- [Add Fabric Connector Event Handler](./add-fabric-connector-eventhandler.md) - Link connector to handler
- [Delete Fabric Connector Event Handler](./delete-fabric-connector-eventhandler.md) - Unlink connector
- [Get Event Handlers](./get-eventhandler.md) - List all event handlers
- [Get Automation Connectors](../incidents-eventsautomation-connectors/get-fabric-conector.md) - List available connectors

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
