# FortiAnalyzer API Documentation

Comprehensive JSON-RPC API documentation for FortiAnalyzer, providing practical examples and integration guides for automation and development.

## 📖 Read the Documentation Online

**Live Documentation:** https://how-to-fortianalyzer-api.readthedocs.io/en/latest/

The documentation is automatically built and published on Read the Docs with every update.

## 🚀 How to Build the HTML Documentation Locally

### Prerequisites

#### Linux/macOS with Python 3

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rstierli/fortianalyzer-api-docs.git
   cd fortianalyzer-api-docs
   ```

2. **Install Sphinx and dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Build the HTML documentation:**
   ```bash
   cd doc
   sphinx-build -b html . _build/html
   ```

4. **Read the HTML documentation:**
   ```bash
   # Open in your browser
   open _build/html/index.html  # macOS
   xdg-open _build/html/index.html  # Linux
   ```

The generated HTML files will be in `doc/_build/html/`

## 📚 What's Covered

This documentation provides comprehensive coverage of:

- **Authentication** - Session-based and API key methods
- **LogView / Log Search** - Two-step search workflow with task IDs
- **Report Generation** - Asynchronous report creation and retrieval
- **Device Management** - ADOM, device registration, and fabric operations
- **FortiView Analytics** - IOC detection, threat analysis, SD-WAN metrics
- **Event Management** - Event handlers, automation connectors, alerts
- **System Operations** - Configuration, monitoring, and administration

Each endpoint includes:
- Complete request/response examples
- Python code samples with error handling
- cURL command examples
- Parameter documentation
- Best practices and troubleshooting tips

## 🔧 Technology Stack

- **Documentation Framework:** Sphinx with MyST Markdown parser
- **Theme:** Sphinx Book Theme
- **Hosting:** Read the Docs
- **Source Format:** Markdown (.md)
- **Build System:** Python 3.11+

## 📝 Documentation Structure

```
doc/
├── docs/
│   ├── login-and-logout/          # Authentication
│   ├── logview/                   # Log search operations
│   ├── reports/                   # Report generation
│   ├── device-manager/            # Device management
│   ├── fortiview*/                # FortiView analytics
│   ├── incidents-events*/         # Event management
│   └── system-settings/           # System operations
├── conf.py                        # Sphinx configuration
└── index.md                       # Documentation homepage
```

## 🛠 Requirements

Python packages required for building (see `requirements.txt`):
- sphinx>=7.0.0
- sphinx-book-theme>=1.0.0
- myst-parser>=2.0.0
- sphinx-copybutton>=0.5.2
- sphinx-design>=0.5.0
- Additional Sphinx extensions

## 📄 License

This documentation is provided as-is for educational and reference purposes.

## 🔗 Related Resources

- **FortiAnalyzer Documentation:** https://docs.fortinet.com/product/fortianalyzer/
- **Fortinet Developer Network:** https://fndn.fortinet.net/
- **FortiManager API Documentation:** https://how-to-fortimanager-api.readthedocs.io/

## ℹ️ About

This documentation project aims to make FortiAnalyzer's JSON-RPC API more accessible through practical examples, clear explanations, and real-world use cases. It complements the official FNDN API reference with how-to guides and integration patterns.

**Maintained by Fortinet.** For official Fortinet documentation, please visit https://docs.fortinet.com/
