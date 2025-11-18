# Documentation Workflow: Postman → Published Docs

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     1. POSTMAN: CREATE & TEST                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  • Create new API request in Postman Collection                     │
│  • Test against v7.4.8, v7.6.4, v8.0.0                              │
│  • Verify response is correct                                        │
│  • Save examples (right-click → Add Example)                        │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│              2. CREATE DOCUMENTATION FILE (3 Options)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Option A: Manual                                                    │
│  • Copy doc/docs/TEMPLATE.md                                        │
│  • Rename to operation-name.md                                       │
│  • Place in appropriate category folder                              │
│                                                                       │
│  Option B: Script (Automated)                                        │
│  • Run: ./scripts/new-endpoint.sh                                   │
│  • Follow prompts                                                    │
│  • File created automatically                                        │
│                                                                       │
│  Option C: Ask Claude                                                │
│  • Provide Postman request/response                                 │
│  • Claude generates complete markdown                                │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   3. FILL IN DOCUMENTATION                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Required Sections:                                                  │
│  ✓ Title & one-line description                                     │
│  ✓ Verification badge (v7.4.8, v7.6.4, v8.0.0)                     │
│  ✓ Overview with use cases                                          │
│  ✓ Endpoint details (method, path)                                  │
│  ✓ Key parameters table                                             │
│  ✓ Tab-item REQUEST/RESPONSE examples                               │
│  ✓ Complete Python example                                          │
│  ✓ Error codes table                                                │
│  ✓ Best practices                                                   │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  4. UPDATE MAIN INDEX                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  File: doc/index.md                                                 │
│                                                                       │
│  Add to appropriate toctree section:                                │
│                                                                       │
│  ```{toctree}                                                        │
│  :maxdepth: 2                                                        │
│  :caption: [Category Name]                                          │
│                                                                       │
│  docs/category/existing-operation                                    │
│  docs/category/your-new-operation    <-- ADD HERE                   │
│  ```                                                                 │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    5. TEST LOCALLY                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Terminal:                                                           │
│  $ cd doc/                                                          │
│  $ make livehtml                                                    │
│                                                                       │
│  Browser: http://localhost:8088                                     │
│                                                                       │
│  Verify:                                                            │
│  ✓ Page renders without errors                                      │
│  ✓ Tab-items work (REQUEST/RESPONSE)                                │
│  ✓ Code syntax highlighting works                                   │
│  ✓ Navigation shows new operation                                   │
│  ✓ Links to related operations work                                 │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  6. BUILD & DEPLOY                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Terminal:                                                           │
│  $ make clean                                                       │
│  $ make html                                                        │
│  $ make upload                                                      │
│                                                                       │
│  Published URL:                                                     │
│  https://cmm-doc.s3.eu-west-1.amazonaws.com/                       │
│         FortiAnalyzer_API_Documentation/index.html                  │
│                                                                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      7. GIT COMMIT                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  $ git add doc/docs/category/new-operation.md                      │
│  $ git add doc/index.md                                            │
│  $ git commit -m "Add: [Operation Name] API documentation"         │
│  $ git push                                                         │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

### Create New Endpoint (Fast Track)

```bash
# 1. Run helper script
./scripts/new-endpoint.sh

# 2. Edit the generated file
# Fill in: Overview, Parameters, Examples, Error codes

# 3. Add to index
# Edit doc/index.md - add line in appropriate toctree

# 4. Test & Deploy
cd doc/
make livehtml    # Test at localhost:8088
make clean
make html
make upload      # Deploy to S3

# 5. Commit
git add doc/docs/[category]/[operation].md doc/index.md
git commit -m "Add: [Operation] documentation"
git push
```

### File Locations

```
FortiAnalyzer_API_Documentation/
├── WORKFLOW.md                    ← This file
├── CONTRIBUTING.md                ← Detailed guide
├── scripts/
│   └── new-endpoint.sh           ← Automation script
└── doc/
    ├── index.md                  ← Main TOC (add new ops here)
    ├── docs/
    │   ├── TEMPLATE.md           ← Copy this for new endpoints
    │   ├── device-manager/       ← Device operations
    │   ├── logview/              ← Log search
    │   ├── fortiview*/           ← Analytics
    │   ├── reports/              ← Reports
    │   ├── system-settings*/     ← System config
    │   └── incidents-events*/    ← Event handlers
    └── getting-started/          ← Guides
```

### Categories & Their Purpose

| Category | Operations | Purpose |
|----------|-----------|---------|
| `device-manager/` | 15 | Device lifecycle, authorization, policy install |
| `logview/` | 11 | Log search and retrieval |
| `logviewfabric-of-analyzer/` | 2 | Distributed log search (Supervisor/Member) |
| `fortiviewfortiview-ioc/` | 3 | IOC threat intelligence |
| `fortiviewioc/` | 1 | IOC configuration |
| `fortiviewtop-sources/` | 2 | Top traffic sources analytics |
| `fortiviewtop-applications/` | 3 | Top applications analytics |
| `fortiviewtop-threats/` | 2 | Top threats analytics |
| `fortiviewsecure-sd-wan/` | 6 | SD-WAN performance analytics |
| `reports/` | 18 | Report generation, templates, scheduling |
| `reportsfolders/` | 4 | Report organization |
| `system-settings/` | 6 | System info, admin users, certificates |
| `system-settingsfabric-of-faz/` | 3 | Fabric of FortiAnalyzer setup |
| `system-settingslogforwarding/` | 4 | Log forwarding configuration |
| `incidents-eventsevent-handlers-setup/` | 9 | Event handler automation |
| `incidents-eventsevent-handlers-setupsubnets/` | 5 | Subnet filtering for handlers |
| `incidents-eventsautomation-connectors/` | 3 | Webhook/SIEM connectors |
| `incidents-eventseventmgmt-alerts/` | 3 | Alert retrieval |
| `fortianalyzercloudlogin/` | 4 | FortiCloud authentication |
| `fabric-viewasset-identity-center/` | 2 | UEBA endpoints |
| `login-and-logout/` | 2 | Basic authentication |

---

## Time Estimates

| Task | Time |
|------|------|
| Test API in Postman | 5-10 min |
| Create documentation file | 2 min (script) / 5 min (manual) |
| Write documentation | 20-30 min |
| Update index | 2 min |
| Test locally | 5 min |
| Build & deploy | 3 min |
| Git commit | 2 min |
| **Total** | **~40-60 min** |

With practice, can be reduced to 20-30 minutes for simple operations.

---

## Tips for Speed

### 1. **Reuse Similar Operations**
Instead of starting from TEMPLATE.md, copy a similar operation:
```bash
cp doc/docs/logview/create-search-task-for-ip-dst.md \
   doc/docs/logview/create-search-task-for-new-field.md
```

### 2. **Use Postman Examples**
Export request/response from Postman directly into tab-items.

### 3. **Batch Updates**
Document multiple related operations at once, then deploy together.

### 4. **Keep Make Running**
Use `make livehtml` - it auto-rebuilds on file changes.

---

## Troubleshooting

### Build fails with "Unknown directive: tab-item"
**Solution:** `sphinx_design` extension is required (already in conf.py)

### Links don't work in local preview
**Solution:** Use relative paths: `../category/operation.md` not absolute paths

### Operation not appearing in navigation
**Solution:** Ensure it's added to `doc/index.md` in the correct toctree section

### Tab-items not rendering
**Solution:** Use four backticks for outer fence, three for inner code block:
````markdown
````{tab-item} REQUEST
```json
{ ... }
```
````
````

---

## Questions?

See detailed guide: [CONTRIBUTING.md](CONTRIBUTING.md)

Contact: Roland Stierli
