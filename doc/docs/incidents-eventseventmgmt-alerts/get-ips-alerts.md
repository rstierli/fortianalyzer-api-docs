# Get IPS Alerts

Retrieve IPS (Intrusion Prevention System) event alerts from FortiAnalyzer event management.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves IPS alerts - useful for:
- Monitoring intrusion prevention events
- Investigating security threats and attacks
- Tracking IPS signature matches
- Incident response and threat analysis
- Compliance and security auditing

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/eventmgmt/adom/{adom}/alerts`
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
        "url": "/eventmgmt/adom/root/alerts",
        "apiver": 3,
        "filter": "eventtype=\"ips\"",
        "limit": 100,
        "offset": 0,
        "time-range": {
            "start": "2025-11-10 00:00",
            "end": "2025-11-10 23:59"
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
            "alerts": [
                {
                    "eventtype": "ips",
                    "severity": "critical",
                    "attack": "SQL.Injection",
                    "srcip": "10.0.10.45",
                    "dstip": "192.168.1.100",
                    "timestamp": "2025-11-10 14:32:15"
                }
            ]
        },
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

def get_ips_alerts(session_id, adom, start_time, end_time, limit=100):
    """Get IPS alerts"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{
            "url": f"/eventmgmt/adom/{adom}/alerts",
            "apiver": 3,
            "filter": 'eventtype="ips"',
            "limit": limit,
            "offset": 0,
            "time-range": {
                "start": start_time,
                "end": end_time
            }
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
alerts = get_ips_alerts(
    session_id="your_session_id",
    adom="root",
    start_time="2025-11-10 00:00",
    end_time="2025-11-10 23:59"
)

print(f"Total IPS Alerts: {len(alerts.get('alerts', []))}")
```

## Related Endpoints

- [Get SD-WAN Alerts](./get-sdwan-alerts.md) - SD-WAN event alerts
- [Get Malicious Events by Endpoint](./get-events-malicious-by-ep.md) - Endpoint-based malicious events

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
