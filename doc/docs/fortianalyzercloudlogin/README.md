# FortiAnalyzerCloud/Login

Comprehensive authentication documentation for FortiAnalyzer Cloud and on-premises instances.

## FortiAnalyzer Cloud OAuth Authentication (Recommended)

FortiAnalyzer Cloud uses OAuth 2.0 authentication flow:

### Complete OAuth Guide
- **[OAuth Authentication Overview](./oauth-authentication-overview.md)** - Complete 4-step authentication guide with code examples

### Individual OAuth Steps
1. **[Get OAuth Access Token](./oauth-get-access-token.md)** - Step 1: Request OAuth token from FortiCloud
2. **[Get Session ID (Cloud)](./oauth-get-session-id.md)** - Step 2: Exchange OAuth token for FAZ session
3. [API Operations] - Step 3: Use session for API calls
4. **[Logout API User](./logout-api-user.md)** - Step 4: Terminate session

## On-Premises Authentication

For on-premises FortiAnalyzer instances:

- **[Get Session ID (On-Prem)](./get-session-id.md)** - Username/password authentication
- **[FortiCloud Token](./forticloud-token.md)** - FortiCloud token authentication
- **[FortiCloud Token ZTP](./forticloud-token-ztp.md)** - Zero-touch provisioning
- **[Logout API User](./logout-api-user.md)** - Terminate session

## Quick Start

### FortiAnalyzer Cloud
```python
# OAuth flow (4 steps)
# ⚠️ Replace with YOUR actual values from FortiCloud IAM
auth = FAZCloudAuth(
    faz_fqdn="YOUR-INSTANCE.YOUR-REGION.fortianalyzer.forticloud.com",  # Your FQDN
    api_id="YOUR_API_ID_FROM_IAM",  # From credentials file
    password="YOUR_PASSWORD_FROM_IAM"  # From credentials file
)
session_id = auth.login()
```

### On-Premises
```python
# Direct login (2 steps)
# ⚠️ Replace with YOUR actual on-premises FAZ details
session_id = get_session_id(
    faz_host="faz.example.com",  # Your FAZ hostname
    username="admin",  # Your username
    password="password"  # Your password
)
```

## Key Differences

| Feature | On-Premises | FortiAnalyzer Cloud |
|---------|-------------|---------------------|
| Auth Method | Username/password | OAuth 2.0 (4-step) |
| Auth Endpoint | `/sys/login/user` | `/p/forticloud_jsonrpc_login/` |
| OAuth Required | No | Yes |
| ADOM | Configurable | Always `root` |
| Steps | 1-2 | 4 |

## See Also

- [Device Manager](../device-manager/README.md) - ADOM and device management
- [LogView](../logview/README.md) - Log search and analysis
- [System Settings](../system-settings/README.md) - System configuration
