# Get Event Handlers

Retrieve configured event handlers for automated incident response.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves event handler configurations - useful for:
- Listing all configured automated response rules
- Auditing incident response automation
- Verifying event-triggered workflows
- Documentation and backup
- Compliance reporting

Event handlers automate responses to security events (send alerts, execute scripts, update firewall policies, create tickets).

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
    "method": "get",
    "params": [{
        "url": "/eventmgmt/adom/root/conf-eventhandler"
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
                "name": "Critical_IPS_Alert",
                "description": "Send alert on critical IPS detection",
                "status": "enabled",
                "trigger": "ips-signature",
                "action": "webhook",
                "target": "Splunk_HEC"
            }
        ],
        "status": {
            "code": 0,
            "message": "OK"
        }
    }]
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_event_handlers(session_id, adom="root"):
    """Get all event handlers"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/conf-eventhandler"
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

# Example
handlers = get_event_handlers(session_id="your_session_id")

print(f"Total Event Handlers: {len(handlers)}\n")
for handler in handlers:
    status_icon = "✓" if handler.get('status') == 'enabled' else "✗"
    print(f"{status_icon} {handler['name']}")
    print(f"   Trigger: {handler.get('trigger')}")
    print(f"   Action: {handler.get('action')}")
    print()
```

## Related Endpoints

- [Add Fabric Connector Event Handler](./add-fabric-connector-eventhandler.md) - Create webhook handler
- [Update Event Handler](./update-eventhandler-description.md) - Modify handler settings
- [Disable Event Handler](./disable-eventhandler.md) - Disable automated response

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
