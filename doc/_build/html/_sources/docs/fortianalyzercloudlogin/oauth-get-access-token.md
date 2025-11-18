# Get OAuth Access Token (FAZ Cloud Step 1)

Request OAuth access token from FortiCloud authentication server.

> **✅ All code examples tested:** Verified against FortiAnalyzer Cloud v7.4.2+

## Overview

This is **Step 1** of the FortiAnalyzer Cloud OAuth authentication flow. You must obtain an OAuth access token before you can authenticate to your FAZ Cloud instance.

## Prerequisites

You must have FortiCloud IAM credentials from the **credentials file**:
- `apiID` (username in OAuth terms)
- `password`
- `client_id` (always "FortiAnalyzer" for FAZ Cloud)

> 📋 **How to get credentials**: See [OAuth Authentication Overview](./oauth-authentication-overview.md#prerequisites)

## Endpoint Details

**Method:** `POST`
**URL:** `https://customerapiauth.fortinet.com/api/v1/oauth/token/`
**Authentication Required:** No (this IS the authentication step)
**SSL Verification:** Yes (FortiCloud uses valid certificates)

## Request Format

`````{tab-set}
````{tab-item} REQUEST
```json
{
  "username": "D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50",
  "password": "e00632a71cdd405fe6118ca7b2edb0f5!1Aa",
  "client_id": "FortiAnalyzer",
  "grant_type": "password"
}
```
````

````{tab-item} RESPONSE
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2N1c3RvbWVyYXBpYXV0aC5mb3J0aW5ldC5jb20iLCJzdWIiOiJEMEZBQkE4Qy1GRTVELTRB...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "read write"
}
```
````
`````

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `username` | string | Yes | The `apiID` from your FortiCloud IAM credentials file (UUID format) |
| `password` | string | Yes | The `password` from your FortiCloud IAM credentials file |
| `client_id` | string | Yes | Always `"FortiAnalyzer"` for FAZ Cloud |
| `grant_type` | string | Yes | Always `"password"` for this OAuth flow |

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT token used to authenticate to FAZ Cloud (valid for ~1 hour) |
| `token_type` | string | Always `"Bearer"` |
| `expires_in` | integer | Token validity in seconds (typically 3600 = 1 hour) |
| `scope` | string | Granted permissions |

## Complete Python Example

```python
import requests
import json
from datetime import datetime, timedelta

def get_oauth_access_token(api_id, password, client_id="FortiAnalyzer"):
    """
    Get OAuth access token from FortiCloud

    Args:
        api_id: The apiID from FortiCloud IAM credentials file
        password: The password from FortiCloud IAM credentials file
        client_id: Always "FortiAnalyzer" for FAZ Cloud

    Returns:
        dict: Contains access_token, expires_in, etc.
    """
    endpoint = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    payload = {
        "username": api_id,
        "password": password,
        "client_id": client_id,
        "grant_type": "password"
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

        # Calculate token expiration time
        expires_in = result.get('expires_in', 3600)
        expiry_time = datetime.now() + timedelta(seconds=expires_in)

        print(f"✓ OAuth access token received")
        print(f"  Token type: {result.get('token_type')}")
        print(f"  Expires in: {expires_in} seconds ({expires_in // 60} minutes)")
        print(f"  Expires at: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")

        return result

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        raise


# Example usage
if __name__ == "__main__":
    # ⚠️ EXAMPLES - Replace these with values from YOUR FortiCloud IAM credentials file
    API_ID = "D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50"  # Your actual apiID
    PASSWORD = "e00632a71cdd405fe6118ca7b2edb0f5!1Aa"  # Your actual password
    CLIENT_ID = "FortiAnalyzer"  # Always "FortiAnalyzer" for FAZ Cloud

    # Get OAuth token
    token_info = get_oauth_access_token(
        api_id=API_ID,
        password=PASSWORD,
        client_id=CLIENT_ID
    )

    # Extract the access token for next step
    access_token = token_info['access_token']
    print(f"\n📋 Access Token (first 50 chars): {access_token[:50]}...")

    # Next step: Exchange this token for FAZ session ID
    # See: oauth-get-session-id.md
```

## Using Environment Variables (Best Practice)

```python
import os
import requests

def get_oauth_access_token_secure():
    """Get OAuth token using environment variables (secure)"""

    # Load from environment variables
    api_id = os.getenv('FAZ_CLOUD_API_ID')
    password = os.getenv('FAZ_CLOUD_PASSWORD')
    client_id = os.getenv('FAZ_CLOUD_CLIENT_ID', 'FortiAnalyzer')

    if not api_id or not password:
        raise ValueError("Missing credentials in environment variables")

    endpoint = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    payload = {
        "username": api_id,
        "password": password,
        "client_id": client_id,
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

    return response.json()


# Set environment variables first:
# export FAZ_CLOUD_API_ID="D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50"
# export FAZ_CLOUD_PASSWORD="e00632a71cdd405fe6118ca7b2edb0f5!1Aa"
# export FAZ_CLOUD_CLIENT_ID="FortiAnalyzer"

token_info = get_oauth_access_token_secure()
```

## cURL Example

```bash
# ⚠️ Replace username/password with values from YOUR FortiCloud IAM credentials file
curl -X POST https://customerapiauth.fortinet.com/api/v1/oauth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "YOUR_API_ID_FROM_IAM",
    "password": "YOUR_PASSWORD_FROM_IAM",
    "client_id": "FortiAnalyzer",
    "grant_type": "password"
  }'
```

## Token Expiration and Refresh

Access tokens typically expire after **3600 seconds (1 hour)**. For long-running applications, implement token refresh logic:

```python
import time
from datetime import datetime, timedelta

class OAuthTokenManager:
    """Manage OAuth token with automatic refresh"""

    def __init__(self, api_id, password, client_id="FortiAnalyzer"):
        self.api_id = api_id
        self.password = password
        self.client_id = client_id
        self.access_token = None
        self.expiry_time = None

    def get_token(self):
        """Get valid token (refresh if expired)"""
        if self.is_token_expired():
            self.refresh_token()
        return self.access_token

    def is_token_expired(self, buffer_seconds=300):
        """Check if token is expired (with 5-minute buffer)"""
        if not self.expiry_time or not self.access_token:
            return True
        return datetime.now() >= (self.expiry_time - timedelta(seconds=buffer_seconds))

    def refresh_token(self):
        """Request new access token"""
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

        expires_in = result.get('expires_in', 3600)
        self.expiry_time = datetime.now() + timedelta(seconds=expires_in)

        print(f"✓ Token refreshed (expires at {self.expiry_time.strftime('%H:%M:%S')})")


# Usage (⚠️ Replace with your actual credentials from FortiCloud IAM)
token_manager = OAuthTokenManager(
    api_id="YOUR_API_ID_FROM_IAM",
    password="YOUR_PASSWORD_FROM_IAM"
)

# Always get valid token (automatically refreshes if needed)
access_token = token_manager.get_token()
```

## Common Errors

### 401 Unauthorized
```json
{
  "error": "invalid_grant",
  "error_description": "Invalid credentials"
}
```
**Cause**: Incorrect apiID or password
**Solution**:
- Verify credentials match the downloaded credentials file
- Re-download credentials from FortiCloud IAM
- Check if API user is still active in IAM

### 403 Forbidden
```json
{
  "error": "access_denied",
  "error_description": "User does not have required permissions"
}
```
**Cause**: Permission profile doesn't include FortiAnalyzer Cloud access
**Solution**:
- Update permission profile in FortiCloud IAM
- Ensure FortiAnalyzer Cloud service is selected
- Verify user is linked to correct permission profile

### Connection Timeout
**Cause**: Network issue or firewall blocking FortiCloud
**Solution**:
- Allow HTTPS (443) to `customerapiauth.fortinet.com`
- Check corporate proxy settings
- Verify DNS resolution

### SSL Certificate Error
**Cause**: System missing CA certificates
**Solution**:
```bash
# Update CA certificates (Ubuntu/Debian)
sudo apt-get update && sudo apt-get install ca-certificates

# Update CA certificates (CentOS/RHEL)
sudo yum install ca-certificates

# Update CA certificates (macOS)
# Usually not needed, uses system keychain
```

## Security Best Practices

1. **Never hardcode credentials**
   ```python
   # ❌ BAD
   api_id = "D6FA8A8C-FE5D-448E-A0E3-683D6DC24A50"

   # ✅ GOOD
   api_id = os.getenv('FAZ_CLOUD_API_ID')
   ```

2. **Store credentials securely**
   - Use environment variables
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Encrypt configuration files

3. **Rotate credentials regularly**
   - Generate new API user every 90 days
   - Disable old API users after rotation

4. **Never log tokens**
   ```python
   # ❌ BAD
   print(f"Token: {access_token}")

   # ✅ GOOD
   print(f"Token: {access_token[:10]}... (truncated)")
   ```

5. **Monitor API usage**
   - Review FortiCloud IAM audit logs
   - Alert on unusual API patterns
   - Track failed authentication attempts

## Next Steps

After obtaining the access token, proceed to:
- **Step 2**: [Get Session ID](./oauth-get-session-id.md) - Exchange token for FAZ session
- **Complete Guide**: [OAuth Authentication Overview](./oauth-authentication-overview.md)

---

**Last Updated:** 2025-01-14
**FAZ Cloud Version:** 7.4.2+
**OAuth Endpoint:** customerapiauth.fortinet.com
