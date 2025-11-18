# Add Subnet to Event Handler

Configure subnet-based event triggering for automated incident response.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint adds subnet-based triggers to event handlers - useful for:
- Creating network-segmented event monitoring
- Configuring location-specific automated responses
- Setting up subnet-aware security alerting
- Implementing zone-based incident escalation
- Managing distributed network event handling

Event handlers can be configured to trigger only for events originating from or destined to specific subnets, enabling precise network-based automation rules.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/config/trigger/{eid}/subnet`
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
        "url": "/eventmgmt/adom/root/config/trigger/1/subnet",
        "data": {
            "subnet": "10.10.100.0/24",
            "description": "Production DMZ subnet"
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
        "url": "/eventmgmt/adom/root/config/trigger/1/subnet"
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

def add_subnet_to_event_handler(session_id, adom, event_handler_id, subnet, description=""):
    """
    Add subnet trigger to event handler

    Args:
        session_id: Active session ID
        adom: ADOM name
        event_handler_id: Event handler ID (integer)
        subnet: Subnet in CIDR notation (e.g., "10.0.0.0/24")
        description: Optional description of subnet

    Returns:
        bool: True if successful
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/config/trigger/{event_handler_id}/subnet",
            "data": {
                "subnet": subnet,
                "description": description or f"Subnet {subnet}"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Added subnet '{subnet}' to event handler {event_handler_id}")
        return True
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Add DMZ subnet to critical event handler
add_subnet_to_event_handler(
    session_id="your_session_id",
    adom="root",
    event_handler_id=1,
    subnet="10.10.100.0/24",
    description="Production DMZ subnet"
)
```

## Use Cases

### Configure Zone-Based Alerting

```python
# Different event handlers for different network zones
network_zones = {
    1: {  # Critical handler
        "subnets": ["10.10.100.0/24", "10.10.200.0/24"],
        "description": "DMZ and production subnets"
    },
    2: {  # Medium handler
        "subnets": ["192.168.10.0/24", "192.168.20.0/24"],
        "description": "Internal corporate networks"
    },
    3: {  # Low handler
        "subnets": ["172.16.0.0/16"],
        "description": "Guest and IoT networks"
    }
}

for handler_id, config in network_zones.items():
    for subnet in config['subnets']:
        add_subnet_to_event_handler(
            session_id=session,
            adom="root",
            event_handler_id=handler_id,
            subnet=subnet,
            description=config['description']
        )
        print(f"✓ Handler {handler_id}: Added {subnet}")
```

### Multi-Site Security Monitoring

```python
# Configure subnet-based event handlers for distributed sites
sites = {
    "HQ": ["10.0.0.0/16"],
    "Branch_Office_1": ["10.1.0.0/16"],
    "Branch_Office_2": ["10.2.0.0/16"],
    "Cloud_DMZ": ["172.31.0.0/16"]
}

for site_name, subnets in sites.items():
    for subnet in subnets:
        add_subnet_to_event_handler(
            session_id=session,
            adom="root",
            event_handler_id=1,
            subnet=subnet,
            description=f"{site_name} network"
        )
        print(f"✓ {site_name}: Added {subnet}")
```

### High-Value Asset Monitoring

```python
# Monitor specific subnets containing critical infrastructure
critical_subnets = [
    ("10.10.10.0/28", "Database servers"),
    ("10.10.20.0/28", "Domain controllers"),
    ("10.10.30.0/28", "Payment processing systems"),
    ("10.10.40.0/28", "Management network")
]

for subnet, desc in critical_subnets:
    add_subnet_to_event_handler(
        session_id=session,
        adom="root",
        event_handler_id=1,
        subnet=subnet,
        description=desc
    )
    print(f"✓ Monitoring: {desc} ({subnet})")
```

## Best Practices

> **💡 Tip:** Use specific subnet masks (e.g., /24, /28) rather than broad ranges to reduce false positives and focus on relevant network segments.

> **💡 Tip:** Add descriptive labels to subnet entries to make event handler configurations self-documenting and easier to audit.

> **⚠️ Warning:** Overlapping subnets in different event handlers may cause duplicate event processing. Ensure subnet assignments are mutually exclusive when possible.

## Related Endpoints

- [Get Event Handlers](./get-eventhandler.md) - List configured event handlers
- [Update Event Handler Description](./update-eventhandler-description.md) - Modify handler settings
- [Disable Event Handler](./disable-eventhandler.md) - Disable automated response

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
