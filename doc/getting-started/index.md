# Getting Started

Welcome to FortiAnalyzer API! This guide will help you make your first API calls and understand the basics.

## Introduction

The FortiAnalyzer API is a JSON-RPC interface that provides programmatic access to all major FortiAnalyzer functions. Whether you're building automation scripts, integrating with SIEM platforms, or creating custom dashboards, this API gives you complete control.

### Key Characteristics

- **Protocol**: JSON-RPC 2.0 over HTTPS
- **Authentication**: Session-based or API key
- **Format**: JSON request/response
- **Versioning**: URL-based API versioning
- **Rate Limiting**: Configurable per-user limits

### What You Can Do

- 🔍 Search and analyze millions of log records
- 📊 Generate and schedule security reports  
- 🖥️ Manage FortiGate devices and policies
- 🚨 Configure automated incident response
- 📈 Access real-time threat intelligence
- ⚙️ Monitor and configure FortiAnalyzer system

## Prerequisites

Before you begin, ensure you have:

1. **FortiAnalyzer Access**
   - FortiAnalyzer 7.4.0 or higher
   - HTTPS access to FortiAnalyzer (default port 443)
   - Administrative or API user credentials

2. **Development Environment**
   - Python 3.7+ (recommended)
   - `requests` library (`pip install requests`)
   - Or any HTTP client (cURL, Postman, etc.)

3. **Network Access**
   - Network connectivity to FortiAnalyzer
   - Firewall rules allowing HTTPS traffic
   - SSL certificate trust (or disable verification for testing)

## Your First API Call

Let's authenticate and get system status:

```python
import requests
import urllib3

# Disable SSL warnings (for self-signed certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# FortiAnalyzer connection details
FAZ_HOST = "faz.example.com"
FAZ_PORT = "443"
USERNAME = "admin"
PASSWORD = "your_password"

# Step 1: Login
url = f"https://{FAZ_HOST}:{FAZ_PORT}/jsonrpc"

login_payload = {
    "method": "exec",
    "params": [{
        "url": "/sys/login/user",
        "data": {
            "user": USERNAME,
            "passwd": PASSWORD
        }
    }],
    "session": None,
    "id": 1
}

response = requests.post(url, json=login_payload, verify=False)
result = response.json()

if result['result'][0]['status']['code'] == 0:
    session_id = result['session']
    print(f"✓ Logged in! Session ID: {session_id}")
else:
    print(f"✗ Login failed: {result['result'][0]['status']['message']}")
    exit(1)

# Step 2: Get system status
status_payload = {
    "method": "get",
    "params": [{
        "url": "/sys/status"
    }],
    "session": session_id,
    "id": 2
}

response = requests.post(url, json=status_payload, verify=False)
status = response.json()['result'][0]['data']

print(f"\nFortiAnalyzer Information:")
print(f"  Hostname: {status['Hostname']}")
print(f"  Version: {status['Version']}")
print(f"  Model: {status['Model']}")

# Step 3: Logout
logout_payload = {
    "method": "exec",
    "params": [{"url": "/sys/logout"}],
    "session": session_id,
    "id": 3
}

requests.post(url, json=logout_payload, verify=False)
print("\n✓ Logged out successfully")
```

## Authentication Methods

FortiAnalyzer supports two authentication methods:

### Session-Based Authentication

Best for: Interactive applications, scripts with defined lifecycle

```python
# Login to get session ID
login_response = requests.post(url, json={
    "method": "exec",
    "params": [{
        "url": "/sys/login/user",
        "data": {"user": "admin", "passwd": "password"}
    }],
    "session": None,
    "id": 1
}, verify=False)

session_id = login_response.json()['session']

# Use session ID in subsequent requests
# ... API calls ...

# Always logout when done
requests.post(url, json={
    "method": "exec",
    "params": [{"url": "/sys/logout"}],
    "session": session_id,
    "id": 999
}, verify=False)
```

**Detailed guide**: [Session Authentication](authentication.md#session-based-authentication)

### API Key Authentication

Best for: Long-running services, automation, CI/CD pipelines

```python
# Use API key in Authorization header
headers = {
    "Authorization": "Bearer your_api_key_here",
    "Content-Type": "application/json"
}

response = requests.post(url, json={
    "method": "get",
    "params": [{"url": "/sys/status"}],
    "session": None,
    "id": 1
}, headers=headers, verify=False)
```

**Detailed guide**: [API Key Authentication](authentication.md#api-key-authentication)

## Request Structure

All FortiAnalyzer API requests follow this JSON-RPC format:

```json
{
    "method": "get|add|update|delete|exec|set",
    "params": [{
        "url": "/api/endpoint/path",
        "data": {
            "param1": "value1",
            "param2": "value2"
        }
    }],
    "session": "session_id_or_null",
    "id": 1
}
```

### Key Components

| Field | Description |
|-------|-------------|
| `method` | Operation type: `get`, `add`, `update`, `delete`, `exec`, `set` |
| `params` | Array of parameter objects (usually one element) |
| `url` | API endpoint path |
| `data` | Request parameters (optional, depends on endpoint) |
| `session` | Session ID from login, or `null` when using API key |
| `id` | Request ID (any integer, used for tracking) |

## Response Structure

Successful responses follow this format:

```json
{
    "result": [{
        "data": {
            // Response data here
        },
        "status": {
            "code": 0,
            "message": "OK"
        },
        "url": "/api/endpoint/path"
    }],
    "session": "session_id",
    "id": 1
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `-1` | Generic error |
| `-3` | Invalid parameter or object not found |
| `-10` | Session timeout or invalid |
| `-11` | Permission denied |

## Common Patterns

### Two-Step Asynchronous Operations

Many operations (log searches, report generation) use a two-step pattern:

```python
# Step 1: Submit task → Get TID (Task ID)
submit_response = requests.post(url, json={
    "method": "add",
    "params": [{
        "url": "/logview/adom/root/logsearch",
        "apiver": 3,
        "device": [{"devid": "All_FortiGate"}],
        "filter": "srcip==10.0.1.100",
        "logtype": "traffic",
        "time-range": {"last-n-hours": 24}
    }],
    "session": session_id,
    "id": 2
})

tid = submit_response.json()['result'][0]['data']['tid']
print(f"Task ID: {tid}")

# Step 2: Poll for results using TID
import time

while True:
    status_response = requests.post(url, json={
        "method": "get",
        "params": [{
            "url": f"/logview/adom/root/logsearch/{tid}"
        }],
        "session": session_id,
        "id": 3
    })
    
    data = status_response.json()['result'][0]['data']
    
    if data['percentage'] == 100 and data['status'] == 'done':
        print(f"✓ Search complete! Found {data['total_lines']} logs")
        logs = data['logs']
        break
    
    print(f"  Progress: {data['percentage']}%")
    time.sleep(2)
```

**Learn more**: [Asynchronous Operations](./authentication.md)

## Next Steps

### 📚 Learn Core Concepts
Understand [ADOM management](./authentication.md), [filtering](./authentication.md), and [pagination](./authentication.md).

### 🔍 Explore Log Management
Start with [log searches](../docs/logview/README.md) - the most commonly used API feature.

### 📄 Generate Reports
Learn to [run reports](../docs/reports/run-report.md) and [schedule automated delivery](../docs/reports/add-schedule.md).

### 🚨 Configure Automation
Set up [event handlers](../docs/incidents-eventsevent-handlers-setup/README.md) and [webhook integrations](../docs/incidents-eventsautomation-connectors/README.md).

### 💻 Browse Examples
Check the [Use Cases](./index.md) for complete workflow examples.

## Quick Reference

| Task | API Operation | Doc Link |
|------|----------|----------|
| Login | `/sys/login/user` | [Authentication](authentication.md) |
| System Status | `/sys/status` | [System Status](../docs/system-settings/get-system-status.md) |
| Log Search | `/logview/adom/{adom}/logsearch` | [Log Search](../docs/logview/README.md) |
| Run Report | `/report/adom/{adom}/run` | [Run Report](../docs/reports/run-report.md) |
| Get Devices | `/dvmdb/adom/{adom}/device` | [Device List](../docs/device-manager/README.md) |

---

**Need Help?** Check [Troubleshooting](./index.md) or [Common Errors](./index.md).
