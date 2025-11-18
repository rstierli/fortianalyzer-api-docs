# FortiAnalyzer JSON-RPC API Documentation

**Comprehensive API reference for FortiAnalyzer 7.4.8 - 8.0.0+**

This documentation provides complete coverage of FortiAnalyzer's JSON-RPC API with 108 documented operations, working code examples, and best practices for automation and integration.

```{toctree}
:maxdepth: 2
:caption: Getting Started

getting-started/index
getting-started/authentication
```

```{toctree}
:maxdepth: 2
:caption: Authentication

docs/login-and-logout/login
docs/login-and-logout/logout
docs/fortianalyzercloudlogin/forticloud-token
docs/fortianalyzercloudlogin/get-session-id
```

```{toctree}
:maxdepth: 2
:caption: Device Manager (15 Operations)

docs/device-manager/add-device
docs/device-manager/get-device-list
docs/device-manager/get-device-by-devicename
docs/device-manager/get-device-by-sn
docs/device-manager/update-device
docs/device-manager/delete-device
docs/device-manager/refresh-device
docs/device-manager/get-device-groups
docs/device-manager/install-device
docs/device-manager/preview-install
docs/device-manager/get-install-status
docs/device-manager/set-install-targets
docs/device-manager/get-revision-histry
docs/fabric-viewasset-identity-center/get-ueba-endpoints-by-epid
docs/fabric-viewasset-identity-center/get-ueba-endpoints-by-os
```

```{toctree}
:maxdepth: 2
:caption: Log Management (13 Operations)

docs/logview/create-search-task-for-ip-dst
docs/logview/create-search-task-for-app-ctrl
docs/logview/create-search-task-for-attack---botnet
docs/logview/create-search-task-for-attack---sessionid
docs/logview/create-search-task-for-attack---signature
docs/logview/create-search-task-for-malware---dtypevirus
docs/logview/create-search-task-for-malware---ext-malware-list
docs/logview/create-search-task-for-malware---outbreak
docs/logview/create-search-task-for-webfilter-logs
docs/logview/fetch-log-search-result-by-task-id
docs/logview/cancel-log-search-task
docs/logviewfabric-of-analyzer/create-search-task-for-ip-on-supervisor
docs/logviewfabric-of-analyzer/fetch-log-search-result-by-task-id-on-supervisor
```

```{toctree}
:maxdepth: 2
:caption: FortiView (17 Operations)

docs/fortiviewfortiview-ioc/create-ioc-task
docs/fortiviewfortiview-ioc/fetch-ioc-result-by-task
docs/fortiviewfortiview-ioc/ioc-drilldown-fgt-request
docs/fortiviewioc/set-ioc-rescan
docs/fortiviewtop-sources/create-task
docs/fortiviewtop-sources/fetch-result-by-task
docs/fortiviewtop-applications/topapplications
docs/fortiviewtop-applications/topapplications-w-policyname
docs/fortiviewtop-applications/fetch-result-by-task
docs/fortiviewtop-threats/create-task
docs/fortiviewtop-threats/fetch-result-by-task
docs/fortiviewsecure-sd-wan/create-task-sd-wan-health-overview
docs/fortiviewsecure-sd-wan/create-task-sd-wan-application
docs/fortiviewsecure-sd-wan/create-task-sd-wan-interface-bandwidth-line
docs/fortiviewsecure-sd-wan/create-task-sd-wan-top-talkers
docs/fortiviewsecure-sd-wan/create-task-sd-wan-audio-mos-score
docs/fortiviewsecure-sd-wan/fetch-result-by-task-id
```

```{toctree}
:maxdepth: 2
:caption: Incidents & Events (20 Operations)

docs/incidents-eventsevent-handlers-setup/get-eventhandler
docs/incidents-eventsevent-handlers-setup/add-fabric-connector-eventhandler
docs/incidents-eventsevent-handlers-setup/get-fabric-connector-eventhandler
docs/incidents-eventsevent-handlers-setup/delete-fabric-connector-eventhandler
docs/incidents-eventsevent-handlers-setup/add-subnet-eventhandler
docs/incidents-eventsevent-handlers-setup/update-eventhandler-description
docs/incidents-eventsevent-handlers-setup/update-eventhandler-taget-enable
docs/incidents-eventsevent-handlers-setup/disable-eventhandler
docs/incidents-eventsevent-handlers-setup/upload-eventhandler-rework
docs/incidents-eventsevent-handlers-setupsubnets/get-subnet-list
docs/incidents-eventsevent-handlers-setupsubnets/add-subnet
docs/incidents-eventsevent-handlers-setupsubnets/add-subnet-group
docs/incidents-eventsevent-handlers-setupsubnets/get-subnet-groups
docs/incidents-eventsevent-handlers-setupsubnets/update-subnet-groups
docs/incidents-eventsautomation-connectors/get-fabric-conector
docs/incidents-eventsautomation-connectors/add-fabric-conector
docs/incidents-eventsautomation-connectors/delete-fabric-conector
docs/incidents-eventseventmgmt-alerts/get-ips-alerts
docs/incidents-eventseventmgmt-alerts/get-sdwan-alerts
docs/incidents-eventseventmgmt-alerts/get-events-malicious-by-ep
```

```{toctree}
:maxdepth: 2
:caption: Reports (22 Operations)

docs/reports/run-report
docs/reports/run-report-w-fromgui
docs/reports/download-report
docs/reports/download-report-template
docs/reports/get-report-templates
docs/reports/get-report-layouts
docs/reports/get-report-layouts-no-filters
docs/reports/get-report-layouts-eg-dailysummery
docs/reports/export-report-layout
docs/reports/clone-report-templat
docs/reports/import-report
docs/reports/get-report-charts
docs/reports/add-schedule
docs/reports/add-schedule-w-faz-and-adom-filter
docs/reports/add-schedule-w-faz-and-adom-filter-list
docs/reports/add-schedule-w-srcip-filter
docs/reports/get-report-schedules
docs/reports/enable-hcache-socfilters
docs/reportsfolders/get-report-folder
docs/reportsfolders/add-report-folder-64
docs/reportsfolders/add-report-folder-70
docs/reportsfolders/delete-report-folder
```

```{toctree}
:maxdepth: 2
:caption: System Settings (13 Operations)

docs/system-settings/get-system-status
docs/system-settings/get-systme-performance
docs/system-settings/get-admin-users
docs/system-settings/get-cert
docs/system-settings/get-info-from-managed-devices
docs/system-settings/restart
docs/system-settingsfabric-of-faz/add-farbic-of-faz-group
docs/system-settingsfabric-of-faz/update-farbic-of-faz-group
docs/system-settingsfabric-of-faz/add-farbic-of-faz-group-with-members
docs/system-settingslogforwarding/get-logforward
docs/system-settingslogforwarding/get-logforward-devicefilter
docs/system-settingslogforwarding/add-logforward-devicefilter
docs/system-settingslogforwarding/delete-logforward-devicefilter
```

```{toctree}
:maxdepth: 2
:caption: Examples & Pilots

docs/pilot/system-status
docs/pilot/logview-search
```

---

## Documentation Features

✅ **108 API Operations** fully documented
✅ **Verified against** FortiAnalyzer v7.4.8, v7.6.4, v8.0.0
✅ **Working Python examples** for every endpoint
✅ **Tab-formatted** REQUEST/RESPONSE examples
✅ **Complete parameter documentation** with types and descriptions
✅ **Best practices** and troubleshooting tips

## Quick Links

- [Get System Status](docs/system-settings/get-system-status) - Check FortiAnalyzer version and status
- [Authentication Guide](getting-started/authentication) - Session-based and API key auth
- [Log Search Workflow](docs/pilot/logview-search) - Complete two-step async example
- [Create Event Handler](docs/incidents-eventsevent-handlers-setup/get-eventhandler) - Automation and SOAR integration

## Version Compatibility

All code examples have been tested and verified to work across:
- **FortiAnalyzer v7.4.8** (build2744) - Stable LTS
- **FortiAnalyzer v7.6.4** (build3579) - Latest GA Release
- **FortiAnalyzer v8.0.0** (build0017) - Interim/Beta

No breaking API changes detected between versions.

---

**Last Updated:** November 10, 2025
**Documentation Version:** 1.0
**API Coverage:** FortiAnalyzer 7.4.8 - 8.0.0+
