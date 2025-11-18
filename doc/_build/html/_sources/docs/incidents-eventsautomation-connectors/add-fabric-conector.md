# Add Automation Connector (Webhook)

Create a new automation connector (webhook) for incident and event management integrations.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint creates automation connectors - useful for:
- Integrating FortiAnalyzer with SIEM platforms (Splunk, QRadar, Sentinel)
- Connecting to SOAR platforms (Palo Alto XSOAR, Splunk Phantom)
- Creating ticketing system integrations (ServiceNow, Jira)
- Setting up chat notifications (Slack, Microsoft Teams)
- Building custom webhook integrations
- Automating incident response workflows

Automation connectors enable FortiAnalyzer to send real-time security events and alerts to external systems.

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
- Target webhook URL accessible from FortiAnalyzer
- Authentication credentials for target system (if required)

## Request Format

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `adom` | `string` | Yes | - | ADOM name (e.g., "root") |
| `name` | `string` | Yes | - | Unique connector name |
| `uri` | `string` | Yes | - | Webhook endpoint URL |
| `protocol` | `string` | Yes | - | Protocol: "HTTPS" or "HTTP" |
| `port` | `integer` | Yes | - | Port number (e.g., 443, 8088) |
| `title` | `string` | Yes | - | Display title |
| `description` | `string` | Yes | - | Connector description |
| `method` | `integer` | No | `0` | HTTP method: 0=POST, 1=GET, 2=PUT |
| `conn-type` | `integer` | No | `0` | Connection type |
| `auth-status` | `integer` | No | `0` | Authentication: 0=disabled, 1=enabled |
| `status` | `integer` | No | `1` | Status: 0=disabled, 1=enabled |
| `color` | `string` | No | `"#FFFFFF"` | UI color code (hex) |

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/config/adom/root/system/webhook",
        "data": {
            "name": "Splunk_HEC",
            "uri": "https://splunk.example.com:8088/services/collector",
            "protocol": "HTTPS",
            "port": 8088,
            "title": "Splunk SIEM",
            "description": "Splunk HTTP Event Collector Integration",
            "method": 0,
            "conn-type": 0,
            "auth-status": 1,
            "status": 1,
            "color": "#00AA00"
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
        "data": {
            "name": "Splunk_HEC"
        },
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

def add_automation_connector(session_id, adom, name, uri, port, protocol="HTTPS",
                             title=None, description=None, enabled=True):
    """
    Add automation connector (webhook)

    Args:
        session_id: Active session ID
        adom: ADOM name
        name: Unique connector name
        uri: Webhook URL
        port: Port number
        protocol: "HTTPS" or "HTTP" (default: HTTPS)
        title: Display title (default: same as name)
        description: Connector description (default: empty)
        enabled: Enable connector (default: True)

    Returns:
        str: Created connector name
    """
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "add",
        "params": [{
            "url": f"/config/adom/{adom}/system/webhook",
            "data": {
                "name": name,
                "uri": uri,
                "protocol": protocol,
                "port": port,
                "title": title or name,
                "description": description or f"{name} integration",
                "method": 0,  # POST
                "conn-type": 0,
                "auth-status": 0,  # Disabled by default
                "status": 1 if enabled else 0,
                "color": "#FFFFFF"
            }
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    result = response.json()

    if result['result'][0]['status']['code'] == 0:
        print(f"✓ Automation connector '{name}' created successfully")
        return result['result'][0]['data']['name']
    else:
        raise Exception(f"API error: {result['result'][0]['status']['message']}")

# Example: Create Splunk integration
connector_name = add_automation_connector(
    session_id="your_session_id",
    adom="root",
    name="Splunk_HEC",
    uri="https://splunk.example.com:8088/services/collector",
    port=8088,
    protocol="HTTPS",
    title="Splunk SIEM",
    description="Splunk HTTP Event Collector Integration",
    enabled=True
)
```

## Use Cases

### SIEM Integration - Splunk

```python
# Create Splunk HEC webhook connector
add_automation_connector(
    session_id=session,
    adom="root",
    name="Splunk_HEC",
    uri="https://splunk.example.com:8088/services/collector",
    port=8088,
    title="Splunk SIEM",
    description="Forward security events to Splunk",
    enabled=True
)
```

### SIEM Integration - QRadar

```python
# Create IBM QRadar webhook connector
add_automation_connector(
    session_id=session,
    adom="root",
    name="QRadar_API",
    uri="https://qradar.example.com/api/siem/offenses",
    port=443,
    title="IBM QRadar",
    description="Forward security events to QRadar",
    enabled=True
)
```

### Ticketing Integration - ServiceNow

```python
# Create ServiceNow incident webhook
add_automation_connector(
    session_id=session,
    adom="root",
    name="ServiceNow_Incidents",
    uri="https://instance.service-now.com/api/now/table/incident",
    port=443,
    title="ServiceNow",
    description="Create incidents for critical alerts",
    enabled=True
)
```

### Chat Notifications - Slack

```python
# Create Slack webhook for security alerts
add_automation_connector(
    session_id=session,
    adom="root",
    name="Slack_Security_Channel",
    uri="https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
    port=443,
    title="Slack Notifications",
    description="Send critical alerts to Slack #security channel",
    enabled=True
)
```

### Chat Notifications - Microsoft Teams

```python
# Create Microsoft Teams webhook
add_automation_connector(
    session_id=session,
    adom="root",
    name="Teams_SOC_Channel",
    uri="https://outlook.office.com/webhook/YOUR_WEBHOOK_ID",
    port=443,
    title="Microsoft Teams",
    description="Send alerts to Teams SOC channel",
    enabled=True
)
```

## Best Practices

> **💡 Tip:** Always use HTTPS protocol for webhook connectors to ensure secure transmission of security event data.

> **💡 Tip:** Use descriptive names and titles to clearly identify the purpose of each connector.

> **⚠️ Warning:** Test webhook connectivity before enabling the connector to ensure successful event delivery.

> **💡 Tip:** Create separate connectors for different severity levels or event types for better organization.

## Related Endpoints

- [Get Automation Connectors](./get-fabric-conector.md) - List configured webhooks
- [Delete Automation Connector](./delete-fabric-conector.md) - Remove webhook connector

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
