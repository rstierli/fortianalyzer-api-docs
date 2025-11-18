# Contributing New API Endpoints

## Workflow: From Postman to Documentation

### Step 1: Create & Test in Postman

1. **Create new request** in Postman Collection
2. **Test against FortiAnalyzer** (7.4.8, 7.6.4, or 8.0.0)
3. **Verify response** is correct
4. **Save to collection** with descriptive name
5. **Export examples** (right-click → Add Example)

### Step 2: Create Documentation File

**File Location:**
```
doc/docs/{category}/{operation-name}.md
```

**Categories:**
- `device-manager/` - Device operations
- `logview/` - Log search operations
- `fortiview*/` - Analytics operations
- `reports/` - Report operations
- `system-settings*/` - System configuration
- `incidents-events*/` - Event handlers and alerts

**Naming Convention:**
- Use lowercase with hyphens
- Be descriptive: `create-log-search-task.md`
- Match Postman request name (slugified)

### Step 3: Use Documentation Template

```markdown
# [Operation Name]

[Brief description of what this operation does]

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

[Detailed description including:]
- What the operation does
- When to use it
- Common use cases (3-5 bullet points)

[If async operation, mention the two-step pattern]

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path:** `/path/to/endpoint`

[If two-step async:]
**API Path (Step 1):** `/path/to/endpoint`
**API Path (Step 2):** `/path/to/endpoint/{tid}`

## [Step 1: Create Task / Submit Request]

### Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adom` | `string` | Yes | ADOM name (e.g., "root") |
| `device` | `array` | Yes | Device list |
| `param_name` | `type` | Yes/No | Description |

````{tab-item} REQUEST
```json
{
    "method": "add|get|exec|set|delete",
    "params": [{
        "url": "/api/path/here",
        "data": {
            "field": "value"
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
        "url": "/api/path/here"
    }],
    "id": 1
}
```
````

## [Step 2: Fetch Results] (if async)

[Repeat tab-item format for step 2]

## Complete Python Example

```python
import requests
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
FAZ_HOST = "faz.example.com"
FAZ_PORT = 443
API_KEY = "your_api_key_here"

base_url = f"https://{FAZ_HOST}:{FAZ_PORT}/jsonrpc"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Step 1: [Action]
payload = {
    "method": "add",
    "params": [{
        "url": "/api/path",
        "data": {
            "field": "value"
        }
    }],
    "session": None,
    "id": 1
}

try:
    response = requests.post(base_url, json=payload, headers=headers, verify=False, timeout=30)
    result = response.json()

    if result["result"][0]["status"]["code"] == 0:
        # Handle success
        print("Success!")
    else:
        print(f"Error: {result['result'][0]['status']['message']}")

except Exception as e:
    print(f"Error: {e}")
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `field_name` | `type` | Description |

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 0 | OK | Success |
| -11 | No permission | API key lacks required permissions |

## Best Practices

- [Tip 1]
- [Tip 2]
- [Tip 3]

## Common Issues

### Issue 1: [Problem]
**Solution:** [Fix]

### Issue 2: [Problem]
**Solution:** [Fix]

## Related Operations

- [Related Operation 1](../category/operation.md)
- [Related Operation 2](../category/operation.md)

---

**Last Updated:** [Date]
**Verified Versions:** v7.4.8, v7.6.4, v8.0.0
```

### Step 4: Add to Index File

**Update the appropriate index file:**

```
doc/index.md
```

**Add entry in correct toctree section:**

```markdown
\```{toctree}
:maxdepth: 2
:caption: [Category Name]

docs/category/existing-operation
docs/category/your-new-operation    <-- ADD HERE
\```
```

### Step 5: Test Locally

```bash
cd doc/
make clean
make livehtml
```

**Verify:**
- [ ] Page renders correctly
- [ ] Tab-items work (REQUEST/RESPONSE)
- [ ] Code blocks have syntax highlighting
- [ ] Links to related operations work
- [ ] Navigation sidebar shows new operation

### Step 6: Build & Deploy

```bash
make clean
make html
make upload
```

**Verify on S3:**
```
https://cmm-doc.s3.eu-west-1.amazonaws.com/FortiAnalyzer_API_Documentation/index.html
```

---

## Quick Checklist

**Before committing:**
- [ ] Tested API call in Postman against all 3 versions (7.4.8, 7.6.4, 8.0.0)
- [ ] Created markdown file in correct category folder
- [ ] Used template structure with all required sections
- [ ] Added verification badge with all 3 versions
- [ ] Included working Python example
- [ ] Added tab-item REQUEST/RESPONSE examples
- [ ] Updated doc/index.md with new operation
- [ ] Tested local build with `make livehtml`
- [ ] Verified page renders correctly
- [ ] Committed to git
- [ ] Deployed to S3 with `make upload`

---

## File Organization

```
doc/
├── index.md                          # Main TOC - ADD NEW OPERATIONS HERE
├── docs/
│   ├── device-manager/
│   │   ├── operation1.md
│   │   └── new-operation.md         # Your new file
│   ├── logview/
│   ├── fortiview*/
│   ├── reports/
│   └── system-settings*/
└── getting-started/
```

---

## Tips for Quality Documentation

### 1. **Clear Descriptions**
- Explain WHAT the operation does
- Explain WHEN to use it
- Explain WHY it's useful

### 2. **Real Examples**
- Use realistic data (not "foo", "bar")
- Include actual filter expressions
- Show practical use cases

### 3. **Complete Code**
- Include error handling
- Show timeout handling for async operations
- Add comments explaining key sections

### 4. **Helpful Context**
- Link to related operations
- Mention prerequisites
- Warn about common pitfalls

### 5. **Test Thoroughly**
- Test against all 3 versions
- Test with different parameters
- Verify error scenarios work

---

## Version Testing

**Required:** Test new operations against all 3 versions before documenting

```bash
# Use test configs
python3 test_api_versions.py
```

Or manually test with configs:
- `.faz-env-7.4.8.json`
- `.faz-env-7.6.4.json`
- `.faz-env-8.0.0.json`

**If behavior differs between versions:**
Add version-specific notes:

```markdown
## Version Differences

### FortiAnalyzer 7.4.8
- [Specific behavior or limitation]

### FortiAnalyzer 7.6.4+
- [Enhanced behavior or new parameters]

### FortiAnalyzer 8.0.0+
- [Latest features]
```

---

## Automation Helper Script (Optional)

Create `scripts/new-endpoint.sh`:

```bash
#!/bin/bash
# Helper script to create new endpoint documentation

echo "Category (device-manager, logview, reports, etc.):"
read category

echo "Operation name (e.g., create-log-search-task):"
read operation

mkdir -p "doc/docs/$category"
cp "doc/docs/TEMPLATE.md" "doc/docs/$category/$operation.md"

echo "Created: doc/docs/$category/$operation.md"
echo "Next steps:"
echo "1. Edit the file with your API details"
echo "2. Add to doc/index.md in the $category section"
echo "3. Test with 'make livehtml'"
```

---

## Questions?

Contact: Roland Stierli
Documentation System: Sphinx + MyST Markdown + sphinx_book_theme
Deployment: AWS S3 (cmm-doc bucket)
