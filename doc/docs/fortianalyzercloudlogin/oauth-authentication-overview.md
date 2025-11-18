# FortiAnalyzer Cloud OAuth Authentication - Complete Guide

Comprehensive guide for authenticating to FortiAnalyzer Cloud using OAuth 2.0 flow.

> **✅ All code examples tested:** Verified against FortiAnalyzer Cloud v7.4.2+

## Overview

FortiAnalyzer Cloud uses a **4-step OAuth 2.0 authentication flow**, which is fundamentally different from on-premises FortiAnalyzer authentication. This guide walks through the complete process.

## Authentication Flow Comparison

### On-Premises FortiAnalyzer
```
1. Direct login with username/password OR API key
2. Receive session ID
3. Use session for API calls
```

### FortiAnalyzer Cloud (OAuth Flow)
```
1. Obtain OAuth credentials from FortiCloud IAM
2. Request OAuth access token from FortiCloud
3. Exchange access token for FAZ session ID
4. Use session for API calls
```

## Prerequisites

### Step 0: Setup FortiCloud IAM Credentials

Before you can authenticate, you must create API credentials in FortiCloud IAM:

#### A. Create Permission Profile
1. Log into FortiCloud portal: https://support.fortinet.com
2. Navigate to **IAM** → **Permission Profiles**
3. Click **Add New** permission profile
4. Configure:
   - **Name**: `FAZ_Cloud_API`
   - **Service**: Select **FortiAnalyzer Cloud**
   - **Access Type**: **Admin** (or as required)
5. Save the permission profile

#### B. Create API User
1. Navigate to **IAM** → **Users**
2. Click **Add User** → Select **API User**
3. Configure:
   - **User Type**: API User
   - **Description**: `FAZ Cloud API Access`
   - **Permission Profile**: Select `FAZ_Cloud_API` (from step A)
4. Click **Create**

#### C. Download Credentials
1. After creating the API user, click **Download Credentials**
2. Save the credentials file - it contains:
   - **apiID**: UUID format (e.g., `D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50`)
   - **password**: Generated password (e.g., `e00632a71cdd405fe6118ca7b2edb0f5!1Aa`)
   - **client_id**: Always `FortiAnalyzer` for FAZ Cloud

> **⚠️ IMPORTANT**: Credentials are only shown once! Store them securely.

---

## The 4-Step OAuth Authentication Process

### Step 1: Get OAuth Access Token

**Endpoint**: `https://customerapiauth.fortinet.com/api/v1/oauth/token/`

Exchange your API credentials for an OAuth access token.

```json
{
  "username": "D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50",  // apiID from credentials
  "password": "e00632a71cdd405fe6118ca7b2edb0f5!1Aa",  // password from credentials
  "client_id": "FortiAnalyzer",                         // client_id from credentials
  "grant_type": "password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read write"
}
```

> 📝 **Note**: Access tokens expire in ~1 hour

### Step 2: Exchange Access Token for Session ID

**Endpoint**: `https://{your-faz-cloud-fqdn}/p/forticloud_jsonrpc_login/`

Exchange the OAuth access token for a FortiAnalyzer session ID.

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "session": "4gs1dS37E4cw0mP0VWR5JLsPTzf6b4r6JcsbH9MxbsU+c0vF9E94q..."
}
```

### Step 3: Use Session for API Calls

**Endpoint**: `https://{your-faz-cloud-fqdn}/jsonrpc`

Now use the standard FortiAnalyzer JSON-RPC API with your session ID.

```json
{
  "jsonrpc": "2.0",
  "method": "get",
  "params": [{
    "url": "/dvmdb/adom",
    "apiver": 3
  }],
  "session": "4gs1dS37E4cw0mP0VWR5JLsPTzf6b4r6...",
  "id": 1
}
```

> **⚠️ IMPORTANT**: For FAZ Cloud, ADOM is **always** `root`

### Step 4: Logout

**Endpoint**: `https://{your-faz-cloud-fqdn}/jsonrpc`

Always logout when done to free resources.

```json
{
  "id": 1,
  "method": "exec",
  "params": [{
    "url": "/sys/logout"
  }],
  "session": "4gs1dS37E4cw0mP0VWR5JLsPTzf6b4r6..."
}
```

---

## Complete Python Example

```python
import requests
import json

class FAZCloudAuth:
    """FortiAnalyzer Cloud OAuth Authentication"""

    def __init__(self, faz_fqdn, api_id, password, client_id="FortiAnalyzer"):
        """
        Initialize FAZ Cloud authentication

        Args:
            faz_fqdn: Your FAZ Cloud FQDN (e.g., "123456.ca-west-1.fortianalyzer.forticloud.com")
            api_id: apiID from FortiCloud IAM credentials file
            password: password from FortiCloud IAM credentials file
            client_id: Always "FortiAnalyzer" for FAZ Cloud
        """
        self.faz_fqdn = faz_fqdn
        self.api_id = api_id
        self.password = password
        self.client_id = client_id
        self.access_token = None
        self.session_id = None

        self.oauth_endpoint = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"
        self.login_endpoint = f"https://{faz_fqdn}/p/forticloud_jsonrpc_login/"
        self.api_endpoint = f"https://{faz_fqdn}/jsonrpc"

    def get_oauth_token(self):
        """Step 1: Get OAuth access token from FortiCloud"""
        payload = {
            "username": self.api_id,
            "password": self.password,
            "client_id": self.client_id,
            "grant_type": "password"
        }

        response = requests.post(
            self.oauth_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            verify=True  # FortiCloud always uses valid SSL certificates
        )
        response.raise_for_status()

        result = response.json()
        self.access_token = result['access_token']
        print(f"✓ OAuth access token received (expires in {result.get('expires_in', 'N/A')}s)")
        return self.access_token

    def get_session_id(self):
        """Step 2: Exchange access token for FAZ session ID"""
        if not self.access_token:
            self.get_oauth_token()

        payload = {
            "access_token": self.access_token
        }

        response = requests.post(
            self.login_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            verify=True
        )
        response.raise_for_status()

        result = response.json()
        self.session_id = result['session']
        print(f"✓ FAZ session ID received")
        return self.session_id

    def login(self):
        """Complete login flow (Steps 1 & 2)"""
        print("🔐 Authenticating to FortiAnalyzer Cloud...")
        self.get_oauth_token()
        self.get_session_id()
        print("✓ Authentication complete!")
        return self.session_id

    def api_call(self, method, url, data=None):
        """Step 3: Make API call with session"""
        if not self.session_id:
            self.login()

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": [{
                "url": url,
                "apiver": 3
            }],
            "session": self.session_id,
            "id": 1
        }

        if data:
            payload["params"][0]["data"] = data

        response = requests.post(
            self.api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            verify=True
        )
        response.raise_for_status()
        return response.json()

    def logout(self):
        """Step 4: Logout and terminate session"""
        if not self.session_id:
            return

        payload = {
            "id": 1,
            "method": "exec",
            "params": [{
                "url": "/sys/logout"
            }],
            "session": self.session_id
        }

        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                verify=True
            )
            print("✓ Logged out successfully")
        except:
            pass  # Best effort logout


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

# Load credentials from FortiCloud IAM credentials file
faz_cloud = FAZCloudAuth(
    faz_fqdn="123456.ca-west-1.fortianalyzer.forticloud.com",  # ⚠️ EXAMPLE - Replace with your actual FQDN
    api_id="D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50",  # From FortiCloud IAM credentials file
    password="e00632a71cdd405fe6118ca7b2edb0f5!1Aa",  # From FortiCloud IAM credentials file
    client_id="FortiAnalyzer"
)

try:
    # Login (Steps 1 & 2)
    faz_cloud.login()

    # Make API calls (Step 3)
    # Example 1: Get ADOM list
    result = faz_cloud.api_call("get", "/dvmdb/adom")
    print(f"\n📊 ADOMs: {result}")

    # Example 2: Get IPS alerts
    result = faz_cloud.api_call(
        method="get",
        url="/eventmgmt/adom/root/alerts",
        data={
            "filter": "eventtype=\"ips\"",
            "limit": 10,
            "time-range": {
                "start": "2024-01-01 00:00:00",
                "end": "2024-12-31 23:59:59"
            }
        }
    )
    print(f"\n🛡️ IPS Alerts: {result}")

finally:
    # Always logout (Step 4)
    faz_cloud.logout()
```

---

## Key Differences: Cloud vs On-Premises

| Aspect | On-Premises | FortiAnalyzer Cloud |
|--------|-------------|---------------------|
| **Authentication** | Username/password OR API key | OAuth 2.0 (4-step flow) |
| **OAuth Endpoint** | N/A | `customerapiauth.fortinet.com` |
| **Login Endpoint** | `/jsonrpc` with `/sys/login/user` | `/p/forticloud_jsonrpc_login/` |
| **Credentials** | Username + password OR API key | apiID + password + client_id |
| **ADOM** | Can be custom | **Always `root`** |
| **FQDN Format** | Custom (e.g., `faz.mystier.li`) | `*.fortianalyzer.forticloud.com` |
| **SSL Verification** | Often disabled (self-signed) | Always enabled (valid certs) |
| **Auth Steps** | 1-2 steps | **4 steps** |

---

## Security Best Practices

### Credential Management
1. **Never hardcode credentials** - use environment variables or secrets management
2. **Rotate credentials regularly** - regenerate API users periodically
3. **Use minimal permissions** - assign least-privilege permission profiles
4. **Store credentials securely** - use encrypted storage (e.g., HashiCorp Vault)
5. **Monitor API user activity** - review audit logs in FortiCloud IAM

### Token Handling
1. **Access tokens expire** - default is 3600 seconds (1 hour)
2. **Implement token refresh** - for long-running applications
3. **Never log tokens** - redact from logs and error messages
4. **Invalidate on completion** - always logout when done

### Network Security
1. **Use HTTPS only** - FortiCloud enforces SSL/TLS
2. **Whitelist IP addresses** - if possible in FortiCloud IAM
3. **Monitor for anomalies** - unusual API call patterns
4. **Rate limiting** - implement backoff for API errors

---

## Troubleshooting

### Error: 401 Unauthorized (OAuth Endpoint)
**Cause**: Invalid apiID or password
**Solution**:
- Verify credentials match the downloaded credentials file
- Re-download credentials from FortiCloud IAM
- Check if API user is still active

### Error: Invalid access_token
**Cause**: Token expired (>1 hour old)
**Solution**:
- Request new access token (Step 1)
- Implement token refresh logic for long-running apps

### Error: 403 Forbidden (FAZ API)
**Cause**: Permission profile lacks required permissions
**Solution**:
- Update permission profile in FortiCloud IAM
- Assign correct FortiAnalyzer Cloud access level
- Verify user is linked to correct permission profile

### Error: Connection timeout (customerapiauth.fortinet.com)
**Cause**: Firewall blocking OAuth endpoint
**Solution**:
- Allow HTTPS (443) to `*.fortinet.com`
- Check corporate proxy settings
- Verify DNS resolution

### Error: Session not found
**Cause**: Session expired or invalid
**Solution**:
- Re-authenticate (Steps 1 & 2)
- Check session_id is being passed correctly
- Verify FAZ Cloud FQDN is correct

---

## API Rate Limits

FortiCloud may enforce rate limits:
- **OAuth endpoint**: ~100 requests/minute
- **FAZ API**: Varies by subscription tier
- **Best practice**: Implement exponential backoff

```python
import time

def api_call_with_retry(func, max_retries=3):
    """API call with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt
                print(f"⚠️ Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## Additional Resources

- **FortiCloud IAM**: https://support.fortinet.com
- **FAZ Cloud Documentation**: https://docs.fortinet.com/product/fortianalyzer
- **API Reference**: See individual endpoint documentation
- **Support**: FortiCare portal for enterprise support

---

## Related Documentation

- [Step 1: Get OAuth Access Token](./oauth-get-access-token.md)
- [Step 2: Get Session ID](./oauth-get-session-id.md)
- [Step 4: Logout API User](./logout-api-user.md)

---

**Last Updated:** 2025-01-14
**FAZ Cloud Version:** 7.4.2+
**Author:** Based on Fortinet FortiAnalyzer Cloud API Guide
