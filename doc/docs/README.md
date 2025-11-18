# FortiAnalyzer API Documentation

Generated from Postman Collection: **FortiAnalyzer_Master_Collection_V1.1**

Total Endpoints: **106**

## API Sections

### [Device Manager](./device-manager/README.md)

13 endpoints

- [enable_ADOM](./device-manager/enable-adom.md)
- [add_ADOM_FOS](./device-manager/add-adom-fos.md)
- [add_ADOM_Fabric](./device-manager/add-adom-fabric.md)
- [get_ADOM_with_fields](./device-manager/get-adom-with-fields.md)
- [get_ADOM_with_no_fields](./device-manager/get-adom-with-no-fields.md)
- ... and 8 more

### [Fabric View/Asset Identity Center](./fabric-viewasset-identity-center/README.md)

2 endpoints

- [get_UEBA_endpoints_by_OS](./fabric-viewasset-identity-center/get-ueba-endpoints-by-os.md)
- [get_UEBA_endpoints_by_epid](./fabric-viewasset-identity-center/get-ueba-endpoints-by-epid.md)

### [FortiAnalyzerCloud/Login](./fortianalyzercloudlogin/README.md)

4 endpoints

- [FortiCloud_Token](./fortianalyzercloudlogin/forticloud-token.md)
- [FortiCloud_Token_ZTP](./fortianalyzercloudlogin/forticloud-token-ztp.md)
- [Get Session_ID](./fortianalyzercloudlogin/get-session-id.md)
- [Logout_API_User](./fortianalyzercloudlogin/logout-api-user.md)

### [FortiView/FortiVIEW IOC](./fortiviewfortiview-ioc/README.md)

3 endpoints

- [Create IOC Task](./fortiviewfortiview-ioc/create-ioc-task.md)
- [IOC Drilldown FGT Request](./fortiviewfortiview-ioc/ioc-drilldown-fgt-request.md)
- [Fetch IOC Result by Task](./fortiviewfortiview-ioc/fetch-ioc-result-by-task.md)

### [FortiView/IOC](./fortiviewioc/README.md)

1 endpoints

- [set_IOC_rescan](./fortiviewioc/set-ioc-rescan.md)

### [FortiView/Secure SD-WAN](./fortiviewsecure-sd-wan/README.md)

6 endpoints

- [Create Task SD-WAN Interface Bandwidth Line](./fortiviewsecure-sd-wan/create-task-sd-wan-interface-bandwidth-line.md)
- [Create Task SD-WAN Health Overview](./fortiviewsecure-sd-wan/create-task-sd-wan-health-overview.md)
- [Create Task SD-WAN Top Talkers](./fortiviewsecure-sd-wan/create-task-sd-wan-top-talkers.md)
- [Create Task SD-WAN Application](./fortiviewsecure-sd-wan/create-task-sd-wan-application.md)
- [Create Task SD-WAN Audio MOS Score](./fortiviewsecure-sd-wan/create-task-sd-wan-audio-mos-score.md)
- ... and 1 more

### [FortiView/Top Applications](./fortiviewtop-applications/README.md)

3 endpoints

- [TopApplications](./fortiviewtop-applications/topapplications.md)
- [TopApplications_w_policyname](./fortiviewtop-applications/topapplications-w-policyname.md)
- [Fetch Result by Task](./fortiviewtop-applications/fetch-result-by-task.md)

### [FortiView/top sources](./fortiviewtop-sources/README.md)

2 endpoints

- [Create Task](./fortiviewtop-sources/create-task.md)
- [Fetch Result by Task](./fortiviewtop-sources/fetch-result-by-task.md)

### [FortiView/top threats](./fortiviewtop-threats/README.md)

2 endpoints

- [Create Task](./fortiviewtop-threats/create-task.md)
- [Fetch Result by Task](./fortiviewtop-threats/fetch-result-by-task.md)

### [Incidents_&_Events/Automation_Connectors](./incidents-eventsautomation-connectors/README.md)

3 endpoints

- [add_fabric_conector](./incidents-eventsautomation-connectors/add-fabric-conector.md)
- [get_fabric_conector](./incidents-eventsautomation-connectors/get-fabric-conector.md)
- [delete_fabric_conector](./incidents-eventsautomation-connectors/delete-fabric-conector.md)

### [Incidents_&_Events/Event_Handlers_Setup](./incidents-eventsevent-handlers-setup/README.md)

9 endpoints

- [upload_EventHandler_rework!!!](./incidents-eventsevent-handlers-setup/upload-eventhandler-rework.md)
- [get_EventHandler](./incidents-eventsevent-handlers-setup/get-eventhandler.md)
- [update_EventHandler_description](./incidents-eventsevent-handlers-setup/update-eventhandler-description.md)
- [update_EventHandler_taget-enable](./incidents-eventsevent-handlers-setup/update-eventhandler-taget-enable.md)
- [add_Fabric-Connector_EventHandler](./incidents-eventsevent-handlers-setup/add-fabric-connector-eventhandler.md)
- ... and 4 more

### [Incidents_&_Events/Event_Handlers_Setup/Subnets](./incidents-eventsevent-handlers-setupsubnets/README.md)

5 endpoints

- [add_subnet](./incidents-eventsevent-handlers-setupsubnets/add-subnet.md)
- [get_subnet_list](./incidents-eventsevent-handlers-setupsubnets/get-subnet-list.md)
- [add_Subnet_group](./incidents-eventsevent-handlers-setupsubnets/add-subnet-group.md)
- [get_Subnet_groups](./incidents-eventsevent-handlers-setupsubnets/get-subnet-groups.md)
- [update_Subnet_groups](./incidents-eventsevent-handlers-setupsubnets/update-subnet-groups.md)

### [Incidents_&_Events/Eventmgmt_Alerts](./incidents-eventseventmgmt-alerts/README.md)

3 endpoints

- [get_IPS_Alerts](./incidents-eventseventmgmt-alerts/get-ips-alerts.md)
- [get_Events_Malicious_by_EP](./incidents-eventseventmgmt-alerts/get-events-malicious-by-ep.md)
- [get_SDWAN_Alerts](./incidents-eventseventmgmt-alerts/get-sdwan-alerts.md)

### [LogView](./logview/README.md)

11 endpoints

- [Create Search Task for IP dst](./logview/create-search-task-for-ip-dst.md)
- [Create Search Task for Webfilter logs](./logview/create-search-task-for-webfilter-logs.md)
- [Create Search Task for Malware - Outbreak](./logview/create-search-task-for-malware---outbreak.md)
- [Create Search Task for Malware - dtype=Virus](./logview/create-search-task-for-malware---dtypevirus.md)
- [Create Search Task for Malware - EXT-Malware-List](./logview/create-search-task-for-malware---ext-malware-list.md)
- ... and 6 more

### [LogView/Fabric of Analyzer](./logviewfabric-of-analyzer/README.md)

2 endpoints

- [Create Search Task for IP on supervisor](./logviewfabric-of-analyzer/create-search-task-for-ip-on-supervisor.md)
- [Fetch Log Search Result by Task ID on supervisor](./logviewfabric-of-analyzer/fetch-log-search-result-by-task-id-on-supervisor.md)

### [Login and Logout](./login-and-logout/README.md)

2 endpoints

- [Login](./login-and-logout/login.md)
- [Logout](./login-and-logout/logout.md)

### [Reports](./reports/README.md)

18 endpoints

- [import_report](./reports/import-report.md)
- [get_Report_layouts](./reports/get-report-layouts.md)
- [get_Report_layouts_no_filters](./reports/get-report-layouts-no-filters.md)
- [get_Report_layouts_eg_DailySummery](./reports/get-report-layouts-eg-dailysummery.md)
- [export_Report_layout](./reports/export-report-layout.md)
- ... and 13 more

### [Reports/Folders](./reportsfolders/README.md)

4 endpoints

- [add_Report_Folder_6.4](./reportsfolders/add-report-folder-64.md)
- [add_Report_Folder_7.0](./reportsfolders/add-report-folder-70.md)
- [get_Report_Folder](./reportsfolders/get-report-folder.md)
- [delete_Report_Folder](./reportsfolders/delete-report-folder.md)

### [System Settings](./system-settings/README.md)

6 endpoints

- [get_admin_users](./system-settings/get-admin-users.md)
- [Restart](./system-settings/restart.md)
- [get_Cert](./system-settings/get-cert.md)
- [get_system_status](./system-settings/get-system-status.md)
- [get_systme_performance](./system-settings/get-systme-performance.md)
- ... and 1 more

### [System Settings/Fabric-of-FAZ](./system-settingsfabric-of-faz/README.md)

3 endpoints

- [add_Farbic-of-FAZ_Group](./system-settingsfabric-of-faz/add-farbic-of-faz-group.md)
- [add_Farbic-of-FAZ_Group with members](./system-settingsfabric-of-faz/add-farbic-of-faz-group-with-members.md)
- [update_Farbic-of-FAZ_Group](./system-settingsfabric-of-faz/update-farbic-of-faz-group.md)

### [System Settings/logforwarding](./system-settingslogforwarding/README.md)

4 endpoints

- [get_logforward](./system-settingslogforwarding/get-logforward.md)
- [get_logforward_devicefilter](./system-settingslogforwarding/get-logforward-devicefilter.md)
- [add_logforward_devicefilter](./system-settingslogforwarding/add-logforward-devicefilter.md)
- [delete_logforward_devicefilter](./system-settingslogforwarding/delete-logforward-devicefilter.md)


## Getting Started

1. [Authentication](../getting-started/authentication.md)
2. [Configuration](../getting-started/index.md)
3. [Quick Start Guide](../getting-started/index.md)

## Documentation Status

This documentation was auto-generated from the Postman collection. Each endpoint requires manual review and completion:

- [ ] Review all parameter descriptions
- [ ] Test all code examples
- [ ] Add use case scenarios
- [ ] Complete error handling sections
- [ ] Add cross-references
