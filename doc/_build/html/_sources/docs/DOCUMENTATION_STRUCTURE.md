# FortiAnalyzer API Documentation Structure

## Overview

This documentation covers **108 API operations** organized following the FortiAnalyzer GUI structure for intuitive navigation. The structure mirrors how users interact with FortiAnalyzer's web interface, making it easy to find API equivalents of GUI operations.

---

## Proposed Table of Contents

### 1. Getting Started
- **Introduction**
  - About FortiAnalyzer API
  - API Architecture & Design Patterns
  - Version Compatibility (7.4.x - 7.6.x+)
  
- **Quick Start Guide**
  - Prerequisites
  - First API Call
  - Common Use Cases
  
- **Authentication**
  - Session-Based Authentication (login-and-logout/)
  - API Key Authentication
  - FortiCloud Token Authentication (fortianalyzercloudlogin/)
  - Best Practices for Credential Management

---

### 2. Core Concepts

- **Request/Response Format**
  - JSON-RPC Structure
  - Method Types (get, add, update, delete, exec, set)
  - Error Handling & Status Codes
  
- **Asynchronous Operations**
  - Two-Step Workflow Pattern (TID-based)
  - Polling Strategies
  - Timeout Handling
  
- **ADOM Management**
  - Understanding Administrative Domains
  - Multi-Tenancy Considerations
  
- **Pagination & Filtering**
  - Limit and Offset Parameters
  - Filter Expressions
  - Sorting Results

---

### 3. Device Manager
*15 API operations - Managing FortiGate devices and Security Fabric*

#### 3.1 Device Operations (device-manager/)
- Add Managed Device
- Get Device List
- Get Device by Name/Serial
- Update Device Configuration
- Delete Device
- Refresh Device Connection
- Device Authorization
- Device Group Management
- Install Policy to Device
- Preview Config Changes
- Get Install Status
- Install Targets Management
- Revision History

#### 3.2 Asset & Identity (fabric-viewasset-identity-center/)
- Get UEBA Endpoints by Endpoint ID
- Get UEBA Endpoints by Operating System

---

### 4. Log Management (LogView)
*13 API operations - Log search, retrieval, and analysis*

#### 4.1 Log Search & Retrieval (logview/)
- **Core Log Operations**
  - Submit Log Search Task
  - Fetch Search Results by TID
  - Check Search Status
  - Cancel Search Task
  
- **Advanced Search**
  - Log Search with Time Range
  - Log Search with Custom Filters
  - Multi-Device Log Search
  - Log Type Filtering (traffic, event, threat, etc.)
  
- **Log Export**
  - Export to CSV
  - Export to PDF
  - Download Raw Logs

#### 4.2 Fabric of Analyzer (logviewfabric-of-analyzer/)
- Create Distributed Search Task (Supervisor-Member Topology)
- Fetch Fabric Search Results by TID

---

### 5. FortiView
*17 API operations - Real-time and historical visualization data*

#### 5.1 Threat Intelligence (fortiviewfortiview-ioc/, fortiviewioc/)
- Create IOC Analysis Task
- Fetch IOC Results by TID
- IOC Drilldown by FortiGate
- Configure IOC Rescan Settings

#### 5.2 Top Sources (fortiviewtop-sources/)
- Create Top Sources Task
- Fetch Top Sources Results

#### 5.3 Top Applications (fortiviewtop-applications/)
- Create Top Applications Task
- Create Task with Policy Name Filter
- Fetch Results by TID

#### 5.4 Top Threats (fortiviewtop-threats/)
- Create Top Threats Task
- Fetch Top Threats Results

#### 5.5 SD-WAN Analytics (fortiviewsecure-sd-wan/)
- SD-WAN Health Overview
- SD-WAN Application Performance
- SD-WAN Interface Bandwidth
- SD-WAN Top Talkers
- SD-WAN Audio MOS Score
- Fetch SD-WAN Results by TID

---

### 6. Incidents & Events
*20 API operations - Security event management and automation*

#### 6.1 Event Handlers (incidents-eventsevent-handlers-setup/)
- Get Event Handlers
- Add Fabric Connector to Handler
- Get Fabric Connector Handlers
- Delete Fabric Connector Handler
- Add Subnet to Event Handler
- Update Handler Description
- Enable/Disable Handler Targets
- Disable Event Handler
- Upload/Rework Event Handler Config

#### 6.2 Handler Subnets (incidents-eventsevent-handlers-setupsubnets/)
- Get Subnet List
- Add Subnet
- Add Subnet Group
- Get Subnet Groups
- Update Subnet Groups

#### 6.3 Automation Connectors (incidents-eventsautomation-connectors/)
- Get Fabric Connectors (Webhooks/SIEM)
- Add Fabric Connector
- Delete Fabric Connector

#### 6.4 Alert Management (incidents-eventseventmgmt-alerts/)
- Get IPS Alerts
- Get SD-WAN Alerts
- Get Malicious Events by Endpoint

---

### 7. Reports
*22 API operations - Report generation, scheduling, and management*

#### 7.1 Report Configuration (reports/)
- **Templates & Layouts**
  - Get Report Templates
  - Get Report Layouts
  - Get Report Layouts (No Filters)
  - Get Specific Layout (e.g., Daily Summary)
  - Export Report Layout
  - Clone Report Template
  - Import Report Configuration
  
- **Report Charts**
  - Get Report Charts
  
- **Report Scheduling**
  - Add Schedule
  - Add Schedule with FAZ/ADOM Filter
  - Add Schedule with Filter List
  - Add Schedule with Source IP Filter
  - Get Report Schedules
  
- **Report Generation & Download**
  - Run Report (On-Demand)
  - Run Report from GUI Parameters
  - Download Report
  - Download Report Template
  
- **Optimization**
  - Enable HCache & SOC Filters

#### 7.2 Report Organization (reportsfolders/)
- Get Report Folders
- Add Report Folder (v6.4 Format)
- Add Report Folder (v7.0+ Format)
- Delete Report Folder

---

### 8. System Settings
*13 API operations - FortiAnalyzer system configuration*

#### 8.1 System Information (system-settings/)
- Get System Status
- Get System Performance
- Get Admin Users
- Get SSL Certificates
- Get Managed Device Info
- Restart FortiAnalyzer

#### 8.2 Fabric of FortiAnalyzer (system-settingsfabric-of-faz/)
- Add FAZ Fabric Group
- Update FAZ Fabric Group
- Add Members to Fabric Group

#### 8.3 Log Forwarding (system-settingslogforwarding/)
- Get Log Forward Configuration
- Get Log Forward Device Filters
- Add Log Forward Device Filter
- Delete Log Forward Device Filter

---

### 9. Appendices

#### Appendix A: Complete API Reference
- Alphabetical Endpoint Index
- Endpoint Quick Reference Table

#### Appendix B: Examples & Use Cases
- Security Incident Investigation Workflow
- Compliance Reporting Automation
- Multi-Site Log Aggregation
- Automated Threat Response
- Custom Dashboard Integration

#### Appendix C: Code Libraries & SDKs
- Python SDK Examples
- cURL Command Reference
- Postman Collection Usage

#### Appendix D: Troubleshooting
- Common Error Codes
- API Rate Limiting
- Session Management Issues
- Performance Optimization
- Debugging Techniques

#### Appendix E: Migration Guides
- Migrating from v7.4 to v7.6
- Deprecated Features
- Breaking Changes

---

## Documentation Navigation Structure

### Recommended Sidebar Organization

```
├── 📖 Getting Started
│   ├── Introduction
│   ├── Quick Start
│   └── Authentication
│
├── 🎓 Core Concepts
│   ├── Request/Response Format
│   ├── Asynchronous Operations
│   └── ADOM Management
│
├── 🖥️ Device Manager (15)
│   ├── Device Operations
│   └── Asset & Identity (UEBA)
│
├── 📊 Log Management (13)
│   ├── Log Search & Retrieval
│   └── Fabric of Analyzer
│
├── 👁️ FortiView (17)
│   ├── Threat Intelligence (IOC)
│   ├── Top Sources
│   ├── Top Applications
│   ├── Top Threats
│   └── SD-WAN Analytics
│
├── 🚨 Incidents & Events (20)
│   ├── Event Handlers
│   ├── Handler Subnets
│   ├── Automation Connectors
│   └── Alert Management
│
├── 📄 Reports (22)
│   ├── Report Configuration
│   └── Report Organization
│
├── ⚙️ System Settings (13)
│   ├── System Information
│   ├── Fabric of FortiAnalyzer
│   └── Log Forwarding
│
└── 📚 Appendices
    ├── Complete API Reference
    ├── Examples & Use Cases
    ├── Code Libraries
    ├── Troubleshooting
    └── Migration Guides
```

---

## Key Features of This Structure

### 1. GUI-Aligned Navigation
- Mirrors FortiAnalyzer web interface organization
- Users can easily find API equivalents of GUI operations
- Familiar mental model for existing FortiAnalyzer administrators

### 2. Progressive Disclosure
- **Getting Started** → Quick wins for new users
- **Core Concepts** → Deep understanding for power users
- **API Reference** → Organized by functional area
- **Appendices** → Advanced topics and troubleshooting

### 3. Task-Oriented Organization
- Grouped by what users want to accomplish
- Related operations grouped together
- Clear endpoint counts for each section

### 4. Consistent Patterns
- Every endpoint page includes:
  - ✅ Verification badge
  - 📝 Overview with use cases
  - 📋 Parameter tables
  - {tab-item} REQUEST/RESPONSE examples
  - 🐍 Complete Python examples
  - 💡 Best practices & tips
  - 📅 Last updated date

---

## File Structure Mapping

### Current Directory → Documentation Section

```
login-and-logout/                  → Getting Started > Authentication
fortianalyzercloudlogin/           → Getting Started > Authentication

device-manager/                    → Device Manager > Device Operations
fabric-viewasset-identity-center/  → Device Manager > Asset & Identity

logview/                           → Log Management > Log Search & Retrieval
logviewfabric-of-analyzer/         → Log Management > Fabric of Analyzer

fortiviewfortiview-ioc/            → FortiView > Threat Intelligence
fortiviewioc/                      → FortiView > Threat Intelligence
fortiviewtop-sources/              → FortiView > Top Sources
fortiviewtop-applications/         → FortiView > Top Applications
fortiviewtop-threats/              → FortiView > Top Threats
fortiviewsecure-sd-wan/            → FortiView > SD-WAN Analytics

incidents-eventsevent-handlers-setup/      → Incidents & Events > Event Handlers
incidents-eventsevent-handlers-setupsubnets/ → Incidents & Events > Handler Subnets
incidents-eventsautomation-connectors/     → Incidents & Events > Automation Connectors
incidents-eventseventmgmt-alerts/          → Incidents & Events > Alert Management

reports/                           → Reports > Report Configuration
reportsfolders/                    → Reports > Report Organization

system-settings/                   → System Settings > System Information
system-settingsfabric-of-faz/      → System Settings > Fabric of FortiAnalyzer
system-settingslogforwarding/      → System Settings > Log Forwarding

pilot/                             → Appendices > Examples & Use Cases
```

---

## Implementation Notes

### For Read the Docs (Sphinx/MyST)

1. **Create index.md** - Main landing page with overview
2. **Create _toc.yml** - Table of contents structure
3. **Organize by folders** - Group related endpoints
4. **Cross-references** - Link related operations
5. **Search optimization** - Use descriptive titles and keywords

### Recommended Additional Content

#### Landing Page Highlights
- API endpoint count (108 total)
- Version compatibility matrix
- Quick start video/GIF
- Popular endpoint cards (top 10 most used)

#### Getting Started Tutorial
1. Authenticate (obtain session)
2. Submit a log search
3. Poll for results
4. Fetch logs
5. Generate a report
6. Logout

#### Common Workflows
- **Security Investigation**: IOC → Log Search → Report
- **Compliance Audit**: Device List → Log Search → Scheduled Report
- **Automation**: Event Handler → Webhook → External SIEM

---

## Success Metrics

This structure should enable users to:
- ✅ Find any API operation within 2-3 clicks
- ✅ Understand the two-step async pattern
- ✅ Copy working code examples immediately
- ✅ Follow FortiAnalyzer GUI workflow naturally
- ✅ Implement common use cases without external help

---

**Total Documented API Operations: 108**
**Documentation Format: MyST Markdown**
**Target Platform: Read the Docs**
**Alignment: FortiAnalyzer GUI Structure**

---

*Last Updated: 2025-11-10*
*Documentation Version: 1.0*
