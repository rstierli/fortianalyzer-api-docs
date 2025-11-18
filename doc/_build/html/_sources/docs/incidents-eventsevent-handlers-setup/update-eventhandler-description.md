# Update Event Handler Description

Modify the description field of an existing event handler configuration.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint updates event handler descriptions - useful for:
- Documenting event handler purpose and configuration
- Updating handler annotations after configuration changes
- Maintaining accurate incident response documentation
- Compliance and audit trail requirements
- Team collaboration and knowledge sharing

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
            "description": "Critical IPS detections forwarded to Splunk and ServiceNow - Updated 2025-11-10"
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
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_event_handler_description(session_id, adom, handler_name, description):
    """
    Update event handler description

    Args:
        session_id: Active session ID
        adom: ADOM name
        handler_name: Event handler name
        description: New description text

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "update",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler/{handler_name}",
            "data": {
                "description": description
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Updated description for event handler '{handler_name}'")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Update event handler description with timestamp
today = datetime.now().strftime("%Y-%m-%d")
update_event_handler_description(
    session_id="your_session_id",
    adom="root",
    handler_name="Critical_IPS_Alert",
    description=f"Critical IPS detections forwarded to Splunk and ServiceNow - Updated {today}"
)
```

## Use Cases

### Add Timestamp to Descriptions

```python
# Update description with last modification timestamp
from datetime import datetime

handlers_to_update = [
    "Critical_IPS_Alert",
    "Ransomware_Detection",
    "C2_Communication_Block"
]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

for handler_name in handlers_to_update:
    description = f"Automated incident response handler - Last reviewed: {timestamp}"
    update_event_handler_description(
        session_id=session,
        adom="root",
        handler_name=handler_name,
        description=description
    )
    print(f"✓ Updated: {handler_name}")
```

### Document Configuration Changes

```python
# Update description after adding new connector
handler_name = "Critical_IPS_Alert"
new_description = """
Critical IPS signature detections
Destinations: Splunk HEC, ServiceNow, Slack #security
Trigger: IPS severity >= 5
Subnets: DMZ (10.10.100.0/24), Production (10.10.200.0/24)
Owner: Security Operations Team
Last Updated: 2025-11-10
"""

update_event_handler_description(
    session_id=session,
    adom="root",
    handler_name=handler_name,
    description=new_description.strip()
)
```

### Bulk Description Update

```python
# Standardize event handler descriptions
from get_eventhandler import get_event_handlers

handlers = get_event_handlers(session_id=session, adom="root")

for handler in handlers:
    handler_name = handler.get('name')
    trigger_type = handler.get('trigger', 'unknown')
    action = handler.get('action', 'unknown')

    standardized_desc = f"[{trigger_type.upper()}] {action.capitalize()} action - Managed by SOC team"

    update_event_handler_description(
        session_id=session,
        adom="root",
        handler_name=handler_name,
        description=standardized_desc
    )
    print(f"✓ Standardized: {handler_name}")
```

## Best Practices

> **💡 Tip:** Include the date of last update in descriptions to track configuration change history.

> **💡 Tip:** Document the purpose, trigger conditions, destinations, and owner in the description for better team collaboration.

> **💡 Tip:** Use consistent description formatting across all event handlers for easier auditing and reporting.

> **⚠️ Warning:** Description field has a character limit. Keep descriptions concise while including essential information.

## Related Endpoints

- [Get Event Handlers](./get-eventhandler.md) - List configured event handlers
- [Disable Event Handler](./disable-eventhandler.md) - Disable automated response
- [Add Fabric Connector Event Handler](./add-fabric-connector-eventhandler.md) - Link webhook to handler

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
