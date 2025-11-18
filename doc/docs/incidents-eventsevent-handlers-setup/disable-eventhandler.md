# Disable Event Handler

Disable an event handler to stop automated incident response actions.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint disables event handlers - useful for:
- Temporarily stopping automated incident response workflows
- Maintenance and troubleshooting of event handling configurations
- Testing environment changes without affecting production automation
- Preventing event handler execution during system maintenance
- Managing event handler lifecycle

Disabling an event handler stops all automated actions and event forwarding while preserving the configuration for future re-enablement.

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
            "status": "disabled"
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

def disable_event_handler(session_id, adom, handler_name):
    """
    Disable event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        handler_name: Event handler name to disable

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "update",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler/{handler_name}",
            "data": {
                "status": "disabled"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Event handler '{handler_name}' disabled")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

def enable_event_handler(session_id, adom, handler_name):
    """
    Re-enable event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        handler_name: Event handler name to enable

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "update",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler/{handler_name}",
            "data": {
                "status": "enabled"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Event handler '{handler_name}' enabled")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Disable event handler during maintenance
disable_event_handler(
    session_id="your_session_id",
    adom="root",
    handler_name="Critical_IPS_Alert"
)
```

## Use Cases

### Maintenance Mode

```python
# Disable event handler during system maintenance
disable_event_handler(
    session_id=session,
    adom="root",
    handler_name="Critical_IPS_Alert"
)

print("⚠️ Event handler disabled for maintenance window")
print("   Automated responses temporarily suspended")

# ... Perform maintenance ...

# Re-enable after maintenance
enable_event_handler(
    session_id=session,
    adom="root",
    handler_name="Critical_IPS_Alert"
)

print("✓ Event handler re-enabled - automation resumed")
```

### Bulk Disable/Enable

```python
# Disable multiple event handlers for system upgrade
from get_eventhandler import get_event_handlers

handlers = get_event_handlers(session_id=session, adom="root")

print("Disabling all event handlers for system upgrade...\n")

for handler in handlers:
    handler_name = handler.get('name')
    if handler.get('status') == 'enabled':
        disable_event_handler(
            session_id=session,
            adom="root",
            handler_name=handler_name
        )

print("\n✓ All event handlers disabled")
print("   Perform system upgrade...")
print("   Re-enable handlers when complete")
```

### Conditional Disable

```python
# Disable only non-critical event handlers
from get_eventhandler import get_event_handlers

handlers = get_event_handlers(session_id=session, adom="root")

critical_handlers = ["Critical_IPS_Alert", "Ransomware_Detection"]

for handler in handlers:
    handler_name = handler.get('name')

    if handler_name not in critical_handlers:
        disable_event_handler(
            session_id=session,
            adom="root",
            handler_name=handler_name
        )
        print(f"✗ Disabled: {handler_name}")
    else:
        print(f"✓ Kept active: {handler_name} (critical)")
```

### Safe Disable with Verification

```python
# Verify handler exists and is enabled before disabling
from get_eventhandler import get_event_handlers

handler_to_disable = "Test_Event_Handler"

handlers = get_event_handlers(session_id=session, adom="root")
handler_names = {h['name']: h for h in handlers}

if handler_to_disable in handler_names:
    current_status = handler_names[handler_to_disable].get('status')

    if current_status == 'enabled':
        confirm = input(f"Disable event handler '{handler_to_disable}'? (yes/no): ")

        if confirm.lower() == 'yes':
            disable_event_handler(
                session_id=session,
                adom="root",
                handler_name=handler_to_disable
            )
    else:
        print(f"ℹ️ Event handler '{handler_to_disable}' is already disabled")
else:
    print(f"✗ Event handler '{handler_to_disable}' not found")
```

## Best Practices

> **⚠️ Warning:** Disabling an event handler stops ALL automated responses and event forwarding. Ensure alternative alerting mechanisms are in place for critical events.

> **💡 Tip:** Document the reason for disabling in the event handler description field, including expected re-enablement date.

> **💡 Tip:** Use [Update Event Handler Target Status](./update-eventhandler-taget-enable.md) to disable specific targets instead of the entire handler when possible.

> **💡 Tip:** Verify event handler status after maintenance to ensure critical automation is resumed.

> **⚠️ Warning:** Disabled event handlers do not process events. Security incidents may go undetected if critical handlers remain disabled.

## Related Endpoints

- [Get Event Handlers](./get-eventhandler.md) - List and verify handler status
- [Update Event Handler Target Status](./update-eventhandler-taget-enable.md) - Disable specific targets
- [Update Event Handler Description](./update-eventhandler-description.md) - Document status changes
- [Get Fabric Connector Event Handlers](./get-fabric-connector-eventhandler.md) - List configured targets

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
