# [Operation Name]

[One-line description of what this operation does]

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

[Detailed description of the operation including:]

This operation allows you to:
- [Key capability 1]
- [Key capability 2]
- [Key capability 3]

**Use Cases:**
- [Use case 1: scenario description]
- [Use case 2: scenario description]
- [Use case 3: scenario description]

[If async operation:]
This endpoint uses the **two-step asynchronous pattern**:
1. Submit request and receive TID (Task ID)
2. Poll/fetch results using the TID

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/api/endpoint/path`

[If two-step async, add:]
**API Path (Step 1):** `/api/endpoint/path`
**API Path (Step 2):** `/api/endpoint/path/{tid}`

## [Step 1: Submit Request / Create Task]

### Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `device` | `array` | Yes | List of devices to target |
| `param_name` | `string` | Yes | Description of parameter |
| `optional_param` | `integer` | No | Optional parameter (default: value) |

### Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/api/endpoint/path",
        "data": {
            "device": [{"devname": "FGT-01"}],
            "parameter1": "value1",
            "parameter2": 123
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
            "tid": 12345
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/api/endpoint/path"
    }],
    "id": 1
}
```
````
`````

## [Step 2: Fetch Results] (Only for async operations)

### Polling Strategy

Poll the result endpoint every 1-2 seconds until `status` shows completion.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tid` | `integer` | Yes | Task ID from Step 1 |
| `limit` | `integer` | No | Number of results to return |
| `offset` | `integer` | No | Starting position for pagination |

### Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "get",
    "params": [{
        "url": "/api/endpoint/path/12345",
        "data": {
            "limit": 100,
            "offset": 0
        }
    }],
    "session": "{{session_id}}",
    "id": 2
}
```
````
````{tab-item} RESPONSE
```json
{
    "result": [{
        "data": {
            "percentage": 100,
            "status": "done",
            "total_results": 450,
            "results": [
                {
                    "field1": "value1",
                    "field2": "value2"
                }
            ]
        },
        "status": {
            "code": 0,
            "message": "OK"
        }
    }],
    "id": 2
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3
import json
import time

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
FAZ_HOST = "faz.example.com"
FAZ_PORT = 443
API_KEY = "your_api_key_here"
ADOM = "root"

base_url = f"https://{FAZ_HOST}:{FAZ_PORT}/jsonrpc"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Step 1: Submit Request
print("Step 1: Submitting request...")

payload_step1 = {
    "method": "add",
    "params": [{
        "url": f"/api/endpoint/path/adom/{ADOM}",
        "data": {
            "device": [{"devname": "FGT-01"}],
            "parameter1": "value1",
            "parameter2": 123
        }
    }],
    "session": None,
    "id": 1
}

try:
    response = requests.post(
        base_url,
        json=payload_step1,
        headers=headers,
        verify=False,
        timeout=30
    )
    result = response.json()

    if result["result"][0]["status"]["code"] == 0:
        tid = result["result"][0]["data"]["tid"]
        print(f"✅ Request submitted successfully. TID: {tid}")

        # Step 2: Poll for results (if async)
        print("\nStep 2: Fetching results...")

        max_attempts = 30
        for attempt in range(max_attempts):
            payload_step2 = {
                "method": "get",
                "params": [{
                    "url": f"/api/endpoint/path/adom/{ADOM}/{tid}"
                }],
                "session": None,
                "id": 2
            }

            response = requests.post(
                base_url,
                json=payload_step2,
                headers=headers,
                verify=False,
                timeout=30
            )
            result = response.json()

            if result["result"][0]["status"]["code"] == 0:
                data = result["result"][0]["data"]
                percentage = data.get("percentage", 0)
                status = data.get("status", "processing")

                print(f"Progress: {percentage}% - Status: {status}")

                if status == "done" and percentage == 100:
                    print("\n✅ Results ready!")
                    results = data.get("results", [])
                    print(f"Total results: {len(results)}")

                    # Process results
                    for item in results:
                        print(f"  - {item}")

                    break
                elif status == "error":
                    print(f"❌ Task failed: {data.get('message', 'Unknown error')}")
                    break

                time.sleep(2)  # Wait before next poll
            else:
                print(f"❌ Error: {result['result'][0]['status']['message']}")
                break
        else:
            print("❌ Timeout: Task did not complete within expected time")

    else:
        error_msg = result["result"][0]["status"]["message"]
        print(f"❌ Error: {error_msg}")

except requests.exceptions.Timeout:
    print("❌ Request timeout")
except requests.exceptions.ConnectionError:
    print("❌ Connection error")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `tid` | `integer` | Task ID for async operations |
| `field1` | `string` | Description of field |
| `field2` | `integer` | Description of field |
| `results` | `array` | Array of result objects |

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 0 | OK | Success |
| -11 | No permission for the resource | API key lacks required permissions |
| -32600 | Invalid Request | Request format or parameters incorrect |
| -22 | Login fail | Invalid credentials |

## Best Practices

- **Timeout Handling:** Set appropriate timeout values (30s for simple operations, 120s for complex)
- **Retry Logic:** Implement exponential backoff for transient failures
- **Pagination:** Use limit/offset for large result sets
- **Error Handling:** Always check status code before processing data

## Common Issues

### Issue: "No permission for the resource" (-11)

**Cause:** API key user lacks necessary permissions

**Solution:**
```bash
# Grant permissions in FortiAnalyzer:
config system admin user
    edit "api_user"
        set profileid "Super_User"
    next
end
```

### Issue: Request timeout

**Cause:** Operation takes longer than expected

**Solution:** Increase timeout value or check FortiAnalyzer system load

## Related Operations

- [Related Operation 1](#) - Brief description
- [Related Operation 2](#) - Brief description

## See Also

- [Getting Started Guide](../getting-started/index.md)
- [Authentication](../getting-started/authentication.md)

---

**Last Updated:** [Date in format: November 10, 2025]
**Verified Versions:** v7.4.8, v7.6.4, v8.0.0
