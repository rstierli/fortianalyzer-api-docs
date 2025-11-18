# Add Fabric Connector to Event Handler

Link an automation connector (webhook) to an event handler for automated incident response.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint associates an automation connector with an event handler - useful for:
- Configuring webhook destinations for event-triggered alerts
- Linking event handlers to SIEM/SOAR platforms
- Setting up automated notifications for security events
- Creating event-driven integration workflows
- Routing specific events to designated external systems

Event handlers trigger automated actions when security events occur. Linking them to automation connectors enables real-time event forwarding to external platforms.

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
    "method": "add",
    "params": [{
        "url": "/eventmgmt/adom/root/config/trigger/1/fabric-connector",
        "data": {
            "name": "Splunk_HEC",
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

def add_fabric_connector_to_event_handler(session_id, adom, event_handler_id, connector_name):
    """
    Link automation connector to event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        event_handler_id: Event handler ID (integer)
        connector_name: Name of automation connector to link

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/config/trigger/{event_handler_id}/fabric-connector",
            "data": {
                "name": connector_name,
                "status": "enabled"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Linked connector '{connector_name}' to event handler {event_handler_id}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Link Splunk connector to critical IPS event handler
add_fabric_connector_to_event_handler(
    session_id="your_session_id",
    adom="root",
    event_handler_id=1,
    connector_name="Splunk_HEC"
)
```

## Use Cases

### Link Multiple Connectors to Event Handler

```python
# Send critical events to multiple destinations
connectors = ["Splunk_HEC", "ServiceNow_Incidents", "Slack_Security_Channel"]

for connector in connectors:
    add_fabric_connector_to_event_handler(
        session_id=session,
        adom="root",
        event_handler_id=1,
        connector_name=connector
    )
    print(f"✓ Linked {connector}")
```

### Configure Severity-Based Routing

```python
# Route different severity levels to different systems
severity_routing = {
    1: ["Splunk_HEC", "ServiceNow_Incidents", "Slack_Security_Channel"],  # Critical
    2: ["Splunk_HEC", "Teams_SOC_Channel"],  # High
    3: ["Splunk_HEC"]  # Medium
}

for handler_id, connectors in severity_routing.items():
    for connector in connectors:
        add_fabric_connector_to_event_handler(
            session_id=session,
            adom="root",
            event_handler_id=handler_id,
            connector_name=connector
        )
```

## Related Endpoints

- [Get Fabric Connector Event Handlers](./get-fabric-connector-eventhandler.md) - List linked connectors
- [Delete Fabric Connector Event Handler](./delete-fabric-connector-eventhandler.md) - Unlink connector
- [Get Automation Connectors](../incidents-eventsautomation-connectors/get-fabric-conector.md) - List available connectors
- [Get Event Handlers](./get-eventhandler.md) - List configured event handlers

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
