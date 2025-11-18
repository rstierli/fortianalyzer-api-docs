# Get FAZ Cloud Session ID (OAuth Step 2)

Exchange OAuth access token for FortiAnalyzer Cloud session ID.

> **✅ All code examples tested:** Verified against FortiAnalyzer Cloud v7.4.2+

## Overview

This is **Step 2** of the FortiAnalyzer Cloud OAuth authentication flow. After obtaining an OAuth access token from FortiCloud, you must exchange it for a FortiAnalyzer session ID.

## Prerequisites

You must have an **OAuth access token** from Step 1:
- See [Get OAuth Access Token](./oauth-get-access-token.md)

## Endpoint Details

**Method:** `POST`
**URL:** `https://{your-faz-cloud-fqdn}/p/forticloud_jsonrpc_login/`
**Authentication Required:** No (uses access_token in body)
**SSL Verification:** Yes (FortiCloud uses valid certificates)

> ⚠️ **Note**: This endpoint is **different** from on-premises FAZ login

## FQDN Format

Your FAZ Cloud FQDN follows this pattern:
```
{account_id}.{region}.fortianalyzer.forticloud.com
```

> **⚠️ IMPORTANT**: The examples below are **NOT real instances**. You must replace them with your actual FAZ Cloud FQDN.

**Example FQDNs (for reference only):**
- `123456.ca-west-1.fortianalyzer.forticloud.com` ← Example format
- `789012.us-east-1.fortianalyzer.forticloud.com` ← Example format
- `345678.eu-central-1.fortianalyzer.forticloud.com` ← Example format

**Find your actual FQDN in:**
1. FortiCloud portal → FortiAnalyzer Cloud → Instance details
2. Your FAZ Cloud welcome email
3. FortiCloud IAM console

## Request Format

`````{tab-set}
````{tab-item} REQUEST
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2N1c3RvbWVyYXBpYXV0aC5mb3J0aW5ldC5jb20iLCJzdWIiOiJEMEZBQkE4Qy1GRTVELTRB..."
}
```
````

````{tab-item} RESPONSE
```json
{
  "session": "4gs1dS37E4cw0mP0VWR5JLsPTzf6b4r6JcsbH9MxbsU+c0vF9E94qsci3h0YvWe49yCxJIz4DK24E3ZgeThA70nPQUiEp5WDkA=="
}
```
````
`````

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | string | Yes | The OAuth access token from Step 1 |

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `session` | string | FortiAnalyzer session ID - use this for all subsequent API calls |

## Complete Python Example

```python
import requests
import json

def get_faz_session_id(faz_fqdn, access_token):
    """
    Exchange OAuth access token for FAZ Cloud session ID

    Args:
        faz_fqdn: Your FAZ Cloud FQDN (e.g., "123456.ca-west-1.fortianalyzer.forticloud.com")
        access_token: OAuth access token from Step 1

    Returns:
        str: FortiAnalyzer session ID
    """
    endpoint = f"https://{faz_fqdn}/p/forticloud_jsonrpc_login/"

    payload = {
        "access_token": access_token
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            verify=True,  # Always verify SSL for FortiCloud
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        session_id = result['session']

        print(f"✓ FAZ Cloud session ID received")
        print(f"  Session (first 40 chars): {session_id[:40]}...")

        return session_id

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        raise
    except KeyError:
        print(f"❌ No 'session' field in response")
        raise


# Example usage
if __name__ == "__main__":
    # From Step 1
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."

    # Your FAZ Cloud FQDN (⚠️ EXAMPLE - Replace with your actual FQDN)
    faz_fqdn = "123456.ca-west-1.fortianalyzer.forticloud.com"

    # Get FAZ session ID
    session_id = get_faz_session_id(
        faz_fqdn=faz_fqdn,
        access_token=access_token
    )

    print(f"\n✓ Ready to make API calls with session ID")

    # Next step: Use this session_id for API calls
    # See: OAuth Authentication Overview
```

## Complete 2-Step Authentication Flow

```python
import requests

class FAZCloudAuth:
    """Complete FAZ Cloud OAuth authentication"""

    def __init__(self, faz_fqdn, api_id, password, client_id="FortiAnalyzer"):
        self.faz_fqdn = faz_fqdn
        self.api_id = api_id
        self.password = password
        self.client_id = client_id
        self.access_token = None
        self.session_id = None

    def step1_get_oauth_token(self):
        """Step 1: Get OAuth access token"""
        endpoint = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

        payload = {
            "username": self.api_id,
            "password": self.password,
            "client_id": self.client_id,
            "grant_type": "password"
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            verify=True,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        self.access_token = result['access_token']
        print("✓ Step 1: OAuth access token received")
        return self.access_token

    def step2_get_session_id(self):
        """Step 2: Exchange token for session ID"""
        if not self.access_token:
            self.step1_get_oauth_token()

        endpoint = f"https://{self.faz_fqdn}/p/forticloud_jsonrpc_login/"

        payload = {
            "access_token": self.access_token
        }

        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            verify=True,
            timeout=30
        )
        response.raise_for_status()

        result = response.json()
        self.session_id = result['session']
        print("✓ Step 2: FAZ session ID received")
        return self.session_id

    def login(self):
        """Complete login flow (Steps 1 & 2)"""
        print("🔐 Starting FAZ Cloud authentication...")
        self.step1_get_oauth_token()
        self.step2_get_session_id()
        print("✅ Authentication complete!")
        return self.session_id


# Usage (⚠️ Replace example values with your actual credentials)
auth = FAZCloudAuth(
    faz_fqdn="123456.ca-west-1.fortianalyzer.forticloud.com",  # Your actual FQDN
    api_id="D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50",  # From IAM credentials file
    password="e00632a71cdd405fe6118ca7b2edb0f5!1Aa"  # From IAM credentials file
)

session_id = auth.login()

# Now use session_id for API calls
```

## cURL Example

```bash
# Step 1: Get OAuth token (save to file)
curl -X POST https://customerapiauth.fortinet.com/api/v1/oauth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50",
    "password": "e00632a71cdd405fe6118ca7b2edb0f5!1Aa",
    "client_id": "FortiAnalyzer",
    "grant_type": "password"
  }' | jq -r '.access_token' > token.txt

# Step 2: Exchange token for session ID (⚠️ Replace FQDN with your actual instance)
ACCESS_TOKEN=$(cat token.txt)
curl -X POST https://YOUR-INSTANCE-ID.YOUR-REGION.fortianalyzer.forticloud.com/p/forticloud_jsonrpc_login/ \
  -H "Content-Type: application/json" \
  -d "{\"access_token\": \"$ACCESS_TOKEN\"}" | jq -r '.session'
```

## Postman Example

### Step 1: Setup Environment Variables
Create environment in Postman with:
- `faz_fqdn`: `YOUR-INSTANCE.YOUR-REGION.fortianalyzer.forticloud.com` ← Replace with actual FQDN
- `api_id`: Your apiID from FortiCloud IAM credentials file
- `password`: Your password from FortiCloud IAM credentials file
- `client_id`: `FortiAnalyzer`

### Step 2: OAuth Token Request
```
POST https://customerapiauth.fortinet.com/api/v1/oauth/token/

Body (JSON):
{
  "username": "{{api_id}}",
  "password": "{{password}}",
  "client_id": "{{client_id}}",
  "grant_type": "password"
}

Tests (save token to variable):
pm.environment.set("access_token", pm.response.json().access_token);
```

### Step 3: Get Session ID
```
POST https://{{faz_fqdn}}/p/forticloud_jsonrpc_login/

Body (JSON):
{
  "access_token": "{{access_token}}"
}

Tests (save session to variable):
pm.environment.set("session_id", pm.response.json().session);
```

## Using the Session for API Calls

Once you have the session ID, use it for all FAZ API calls:

```python
import requests

def faz_api_call(faz_fqdn, session_id, method, url, data=None):
    """
    Make FAZ Cloud API call with session

    Args:
        faz_fqdn: Your FAZ Cloud FQDN
        session_id: Session ID from Step 2
        method: API method (get, add, update, delete, exec)
        url: API endpoint URL
        data: Optional request data

    Returns:
        dict: API response
    """
    endpoint = f"https://{faz_fqdn}/jsonrpc"

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": [{
            "url": url,
            "apiver": 3
        }],
        "session": session_id,
        "id": 1
    }

    if data:
        payload["params"][0]["data"] = data

    response = requests.post(
        endpoint,
        json=payload,
        headers={"Content-Type": "application/json"},
        verify=True,
        timeout=30
    )
    response.raise_for_status()

    return response.json()


# Example: Get ADOM list (⚠️ Replace FQDN with your actual instance)
result = faz_api_call(
    faz_fqdn="YOUR-INSTANCE.YOUR-REGION.fortianalyzer.forticloud.com",
    session_id=session_id,
    method="get",
    url="/dvmdb/adom"
)

print(f"ADOMs: {result}")

# Example: Get IPS alerts (⚠️ Replace FQDN with your actual instance)
result = faz_api_call(
    faz_fqdn="YOUR-INSTANCE.YOUR-REGION.fortianalyzer.forticloud.com",
    session_id=session_id,
    method="get",
    url="/eventmgmt/adom/root/alerts",
    data={
        "filter": "eventtype=\"ips\"",
        "limit": 10
    }
)

print(f"IPS Alerts: {result}")
```

## Common Errors

### Invalid access_token
```json
{
  "error": "invalid_token",
  "error_description": "The access token is invalid or has expired"
}
```
**Cause**: OAuth token expired (>1 hour old) or invalid
**Solution**:
- Request new access token (Step 1)
- Verify access_token is being passed correctly
- Check for extra whitespace or line breaks in token

### Invalid FQDN
```
ConnectionError: Failed to establish a new connection
```
**Cause**: Incorrect FAZ Cloud FQDN
**Solution**:
- Verify FQDN in FortiCloud portal
- Check DNS resolution: `nslookup your-fqdn.forticloud.com`
- Ensure format: `{id}.{region}.fortianalyzer.forticloud.com`

### 403 Forbidden
```json
{
  "status": {
    "code": 403,
    "message": "Permission denied"
  }
}
```
**Cause**: API user lacks FortiAnalyzer Cloud permissions
**Solution**:
- Update permission profile in FortiCloud IAM
- Ensure "FortiAnalyzer Cloud" service is enabled
- Verify permission level (Read, Write, Admin)

### SSL Certificate Error
**Cause**: System doesn't trust FortiCloud certificates
**Solution**:
- Update CA certificates on your system
- Ensure Python `requests` library is up-to-date
- Do not set `verify=False` for FortiCloud (security risk)

## Session Management

### Session Lifetime
- FAZ Cloud sessions typically last **15-30 minutes** of inactivity
- No explicit expiration time returned
- Implement session refresh logic for long-running apps

### Session Refresh Pattern
```python
import time
from datetime import datetime, timedelta

class FAZCloudSession:
    """Manage FAZ Cloud session with auto-refresh"""

    def __init__(self, faz_fqdn, api_id, password):
        self.faz_fqdn = faz_fqdn
        self.api_id = api_id
        self.password = password
        self.session_id = None
        self.last_activity = None

    def get_session(self, max_idle_minutes=20):
        """Get valid session (refresh if idle too long)"""
        if self._is_session_stale(max_idle_minutes):
            self.refresh_session()
        self.last_activity = datetime.now()
        return self.session_id

    def _is_session_stale(self, max_idle_minutes):
        """Check if session might be expired"""
        if not self.session_id or not self.last_activity:
            return True

        idle_time = datetime.now() - self.last_activity
        return idle_time > timedelta(minutes=max_idle_minutes)

    def refresh_session(self):
        """Get new session (Steps 1 & 2)"""
        print("♻️ Refreshing FAZ Cloud session...")

        # Step 1: Get OAuth token
        oauth_response = requests.post(
            "https://customerapiauth.fortinet.com/api/v1/oauth/token/",
            json={
                "username": self.api_id,
                "password": self.password,
                "client_id": "FortiAnalyzer",
                "grant_type": "password"
            },
            verify=True,
            timeout=30
        )
        oauth_response.raise_for_status()
        access_token = oauth_response.json()['access_token']

        # Step 2: Get session ID
        session_response = requests.post(
            f"https://{self.faz_fqdn}/p/forticloud_jsonrpc_login/",
            json={"access_token": access_token},
            verify=True,
            timeout=30
        )
        session_response.raise_for_status()
        self.session_id = session_response.json()['session']

        self.last_activity = datetime.now()
        print("✓ Session refreshed")


# Usage (⚠️ Replace with your actual credentials)
session_mgr = FAZCloudSession(
    faz_fqdn="YOUR-INSTANCE.YOUR-REGION.fortianalyzer.forticloud.com",
    api_id="YOUR_API_ID_FROM_IAM",
    password="YOUR_PASSWORD_FROM_IAM"
)

# Always get fresh session
for i in range(100):
    session_id = session_mgr.get_session()
    # Make API call...
    time.sleep(60)  # Wait 1 minute between calls
```

## Security Best Practices

1. **Never log session IDs**
   ```python
   # ❌ BAD
   print(f"Session: {session_id}")

   # ✅ GOOD
   print(f"Session: {session_id[:20]}... (truncated)")
   ```

2. **Always logout when done**
   ```python
   try:
       # Your API operations
       pass
   finally:
       # Logout (see logout-api-user.md)
       logout_faz_cloud(faz_fqdn, session_id)
   ```

3. **Validate session before use**
   ```python
   if not session_id or len(session_id) < 20:
       raise ValueError("Invalid session ID")
   ```

4. **Handle session expiration gracefully**
   ```python
   try:
       result = faz_api_call(...)
   except requests.exceptions.HTTPError as e:
       if e.response.status_code == 401:
           # Session expired, re-authenticate
           session_id = auth.login()
           result = faz_api_call(...)
   ```

## Next Steps

- **Step 3**: Use session_id for [API calls](./oauth-authentication-overview.md#step-3-use-session-for-api-calls)
- **Step 4**: [Logout](./logout-api-user.md) when done
- **Complete Guide**: [OAuth Authentication Overview](./oauth-authentication-overview.md)

---

**Last Updated:** 2025-01-14
**FAZ Cloud Version:** 7.4.2+
**Endpoint:** `/p/forticloud_jsonrpc_login/`
