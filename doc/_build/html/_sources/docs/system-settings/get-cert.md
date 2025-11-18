# Get Certificates

Retrieve SSL/TLS certificates installed on FortiAnalyzer.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves installed certificates - useful for certificate management, SSL/TLS configuration, and security auditing.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/cli/global/system/certificate/local`
**ADOM Support:** No
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/cli/global/system/certificate/local"
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
                "name": "Fortinet_Factory",
                "subject": "CN=FortiAnalyzer",
                "issuer": "CN=Fortinet"
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

def get_certificates(session_id):
    """Get installed certificates"""
    url = "https://faz.example.com/jsonrpc"

    payload = {
        "method": "get",
        "params": [{"url": "/cli/global/system/certificate/local"}],
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
certs = get_certificates(session_id="your_session_id")
for cert in certs:
    print(f"Certificate: {cert['name']}")
    print(f"  Subject: {cert['subject']}")
    print(f"  Issuer: {cert['issuer']}")
```

---

**Last Updated:** 2025-11-10
**API Version:** 7.6.4+
