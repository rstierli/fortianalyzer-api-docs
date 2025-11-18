# Delete Automation Connector (Webhook)

Delete an existing automation connector (webhook) from incident and event management integrations.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint deletes automation connectors - useful for:
- Removing deprecated or unused webhook integrations
- Cleaning up test connectors
- Decommissioning retired SIEM/SOAR/ticketing integrations
- Managing connector lifecycle
- Security auditing and connector inventory management

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/config/adom/{adom}/system/webhook`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Administrative access to system configuration in specified ADOM
- Connector name to delete

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `filter` | `array` | Yes | - | Filter array: ["name", "in", "connector_name"] |
| `confirm` | `integer` | Yes | - | Confirmation: 1 to proceed with deletion |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "delete",
    "params": [{
        "url": "/config/adom/root/system/webhook",
        "confirm": 1,
        "filter": ["name", "in", "Splunk_HEC"]
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
        "url": "/config/adom/root/system/webhook"
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

def delete_automation_connector(session_id, adom, connector_name):
    """
    Delete automation connector (webhook)

    Args:
        session_id: Active session ID
        adom: ADOM name
        connector_name: Name of connector to delete

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "delete",
        "params": [{
            "url": f"/config/adom/{adom}/system/webhook",
            "confirm": 1,
            "filter": ["name", "in", connector_name]
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Automation connector '{connector_name}' deleted successfully")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Delete specific connector
delete_automation_connector(
    session_id="your_session_id",
    adom="root",
    connector_name="Splunk_HEC"
)
```

## Use Cases

### Remove Deprecated Connector

```python
# Delete old test connector
delete_automation_connector(
    session_id=session,
    adom="root",
    connector_name="Test_Webhook_Old"
)
```

### Cleanup Multiple Connectors

```python
# Delete multiple unused connectors
deprecated_connectors = [
    "Old_Splunk_Test",
    "Deprecated_QRadar",
    "Test_ServiceNow"
]

for connector in deprecated_connectors:
    try:
        delete_automation_connector(
            session_id=session,
            adom="root",
            connector_name=connector
        )
        print(f"✓ Deleted: {connector}")
    except Exception as e:
        print(f"✗ Failed to delete {connector}: {e}")
```

### Safe Delete with Verification

```python
# Verify connector exists before deleting
from get_fabric_conector import get_automation_connectors

connectors = get_automation_connectors(session_id=session, adom="root")
connector_names = [c['name'] for c in connectors]

connector_to_delete = "Old_Integration"

if connector_to_delete in connector_names:
    # Confirm deletion
    confirm = input(f"Delete connector '{connector_to_delete}'? (yes/no): ")

    if confirm.lower() == 'yes':
        delete_automation_connector(
            session_id=session,
            adom="root",
            connector_name=connector_to_delete
        )
else:
    print(f"✗ Connector '{connector_to_delete}' not found")
```

## Best Practices

> **⚠️ Warning:** Deletion is permanent and cannot be undone. Verify the connector name before deletion.

> **💡 Tip:** List all connectors first using [Get Automation Connectors](./get-fabric-conector.md) to ensure you're deleting the correct one.

> **💡 Tip:** Export connector configuration before deletion for backup purposes.

> **⚠️ Warning:** Deleting an active connector will immediately stop event forwarding to that system.

## Related Endpoints

- [Get Automation Connectors](./get-fabric-conector.md) - List configured webhooks
- [Add Automation Connector](./add-fabric-conector.md) - Create new webhook connector

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
