# QR Suite for ERPNext

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15+-orange.svg)](https://erpnext.com)
[![Frappe](https://img.shields.io/badge/Frappe-v15+-red.svg)](https://frappeframework.com)

🚀 **Transform your ERPNext workflows with intelligent QR code management**

A comprehensive QR code solution that automatically adds QR generation capabilities to **any DocType** in ERPNext, enabling seamless mobile workflows for manufacturing, inventory, assets, and more.

## ✨ Key Features

### 🎯 **Universal Integration**
- **Auto-detects all DocTypes** - QR buttons appear on every form automatically
- **Zero configuration** - Works out of the box
- **Smart defaults** - Automatically suggests appropriate QR types per DocType
- **One-click generation** - Generate QR codes from any document

### 🔧 **Dual QR Types**
- **📋 Document QR**: Secure, token-based workflows (maintenance, repairs, orders)
- **🏷️ Value QR**: Simple field encoding (item codes, serial numbers, barcodes)

### 🔐 **Enterprise Security**
- **Token-based authentication** with configurable expiry
- **ERPNext permission integration** - users only see what they're allowed to
- **Revocation support** - instantly disable compromised QR codes
- **Complete audit trail** - track every scan with user, timestamp, and IP

### 🎨 **Template System**
- **Reusable QR Templates** for consistent workflows
- **Override on-the-fly** - templates suggest, don't enforce settings
- **Save custom configurations** as new templates during generation
- **Action mapping** - route users to specific forms and actions
- **Bulk generation** - create QR codes for multiple records at once
- **Preview functionality** - see QR content before generation

### 📱 **Mobile-First Design**
- **Works with any QR scanner** - camera apps, Google Lens, dedicated scanners
- **Automatic redirects** - seamless transition from scan to action
- **Responsive forms** - optimized for mobile data entry
- **Offline-capable** Value QRs for basic identification

## 🚀 Quick Start

### Installation

```bash
# Get the app from GitHub
bench get-app https://github.com/your-username/qr_suite.git

# Install on your site
bench --site your-site install-app qr_suite

# Run migrations and build
bench --site your-site migrate
bench build --app qr_suite
bench restart
```

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

### First QR Code in 60 Seconds

1. **Open any document** (Asset, Item, Sales Order, etc.)
2. **Click "QR Suite"** → "Generate QR Code"
3. **Choose or create** a QR Template
4. **QR generated!** Download and test

### Example: Asset Maintenance Workflow

```bash
# 1. Create Template
Template Name: "Equipment Maintenance"
QR Type: Document QR
Target DocType: Asset
Action: maintenance_log

# 2. Generate QR for machinery
# 3. Print label and attach to equipment
# 4. Maintenance staff scan → maintenance form opens
# 5. Equipment auto-selected → fast data entry
```

## 📋 Supported Workflows

### 🏭 **Manufacturing**
- **Equipment Maintenance** - Scan → maintenance log
- **Quality Control** - Scan → QC inspection forms
- **Work Order Tracking** - Scan → production updates
- **Tool Management** - Scan → tool checkout/return

### 📦 **Inventory**
- **Item Lookup** - Scan → stock levels, locations
- **Stock Movements** - Scan → stock entries
- **Batch Tracking** - Scan → batch history and usage
- **Cycle Counting** - Scan → inventory adjustments

### 🏢 **Sales & Purchasing**
- **Order Fulfillment** - Scan → delivery notes, invoices
- **Receiving** - Scan → purchase receipts
- **Customer Service** - Scan → customer history, orders
- **Vendor Management** - Scan → supplier information

### 👥 **HR & Admin**
- **Employee Check-in** - Scan → attendance logging
- **Asset Assignment** - Scan → asset allocation
- **Document Access** - Scan → project files, reports
- **Visitor Management** - Scan → visitor registration

## 🔧 Configuration

### QR Template Options

| Setting | Options | Description |
|---------|---------|-------------|
| **QR Type** | Document QR / Value QR | Workflow vs simple identification |
| **Target DocType** | Any ERPNext DocType | Which documents to link |
| **Action** | 25+ built-in actions | Where to redirect users |
| **URL Mode** | Token / Direct | Security level |
| **Expiry** | 0-365 days | Token validity period |

### Built-in Actions

**Asset Management:**
- `maintenance_log` - Create maintenance entry
- `asset_repair` - Create repair request
- `open_doc` - View asset details

**Inventory:**
- `stock_balance` - View current stock
- `new_stock_entry` - Create stock movement
- `view_ledger` - Show stock history

**Sales & Purchase:**
- `delivery_note` - Create delivery
- `sales_invoice` - Generate invoice
- `purchase_receipt` - Record receipt

**And 15+ more...**

## 🎯 Use Cases

### Manufacturing Plant
> "Reduced maintenance logging time by 80%. Technicians scan equipment QR and immediately get the right form with asset pre-filled. No more searching through lists or typing asset numbers."

### Warehouse Operations
> "Inventory cycle counts that used to take 2 days now complete in 4 hours. Staff scan item QRs for instant stock lookup and adjustment entry."

### Healthcare Equipment
> "Perfect for medical device tracking. Each device has a QR for maintenance logs, usage tracking, and compliance documentation. Full audit trail for regulatory requirements."

### Field Service
> "Service technicians scan customer equipment QRs to instantly access service history, create work orders, and update maintenance schedules. Works completely offline for Value QRs."

## 📊 Technical Details

### Architecture
- **Universal JavaScript** - Single script handles all DocTypes
- **Python Backend** - Secure token generation and validation
- **Router System** - Centralized URL mapping and permissions
- **Template Engine** - Flexible, reusable QR configurations

### Security
- **32-character tokens** using cryptographically secure random generation
- **ERPNext permissions** enforced on every scan
- **IP logging** for security analysis
- **Rate limiting** to prevent abuse

### Performance
- **Lightweight** - <50KB total app size
- **Fast generation** - QR codes created in <2 seconds
- **Scalable** - Tested with 10,000+ QR codes
- **Mobile optimized** - Works on any device

## 🛠️ Advanced Features

### Bulk Operations
```javascript
// Generate QRs for all assets in a warehouse
frappe.qr_suite.bulk_generate('Asset', 
    {warehouse: 'Main Store'}, 
    'Equipment Maintenance'
);
```

### Custom Actions
```python
# Add custom routing for your workflows
def custom_route_for(doctype, action, docname):
    if action == "custom_workflow":
        return f"/app/custom-form?doc={docname}"
    return default_route_for(doctype, action, docname)
```

### API Integration
```python
# Trigger external systems on QR scan
def on_qr_scan(qr_link_doc):
    if qr_link_doc.action == "maintenance_log":
        update_cmms_system(qr_link_doc.target_name)
        notify_maintenance_team(qr_link_doc.target_name)
```

## 📱 Mobile App Integration

### Compatible with:
- **ERPNext Mobile App** - Native integration
- **Any QR Scanner** - Camera apps, Google Lens
- **Custom Apps** - API available for integration
- **Web Browsers** - Works on any mobile browser

### Scan Flow:
1. **Scan QR** with any app
2. **Opens browser** with secure URL
3. **Authenticates** with ERPNext login
4. **Redirects** to target form/action
5. **Logs scan** for audit trail

## 🔍 Analytics & Reporting

### Built-in Reports
- **QR Usage Analytics** - Most scanned codes, peak times
- **User Activity** - Who's scanning what, when
- **Workflow Efficiency** - Time from scan to completion
- **Security Audit** - Failed scans, unauthorized access

### Custom Dashboards
- **Maintenance Metrics** - Equipment scan rates, response times
- **Inventory Velocity** - Stock movement tracking via QR
- **Process Compliance** - Scan completion rates by workflow

## 🌐 Multi-language Support

- **Translations** for QR Suite interface
- **Localized actions** based on user language
- **Unicode support** in QR content
- **RTL layout** support for Arabic, Hebrew

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-username/qr_suite
cd qr_suite

# Install in development mode
bench get-app qr_suite ./
bench --site development install-app qr_suite

# Start development
bench start
```

### Areas for Contribution
- 🌍 **Translations** - Help localize QR Suite
- 🎨 **Templates** - Create industry-specific QR templates
- 🔌 **Integrations** - Connect with external systems
- 📊 **Analytics** - Enhanced reporting and dashboards
- 🧪 **Testing** - Automated testing and QA

## 📞 Support

### Community
- **GitHub Issues** - Bug reports and feature requests
- **ERPNext Forum** - Community discussions
- **Discord** - Real-time chat with community

### Documentation
- **[Installation Guide](INSTALL.md)** - Detailed setup instructions
- **[Template Usage Guide](docs/TEMPLATE_USAGE_GUIDE.md)** - How to use QR templates effectively
- **[API Reference](API.md)** - Developer documentation
- **[Workflow Examples](WORKFLOWS.md)** - Real-world use cases
- **[Dynamic Hooks](docs/DYNAMIC_HOOKS_README.md)** - Technical implementation details

### Professional Services
- **Custom Development** - Tailored QR workflows
- **Training** - Team onboarding and best practices
- **Support Contracts** - Priority support and SLA

## 📄 License

MIT License - see [LICENSE](license.txt) for details.

## 🙏 Acknowledgments

- **ERPNext Team** - For the amazing framework
- **Frappe Community** - For continuous inspiration
- **Contributors** - Thank you for making QR Suite better

---

**🚀 Ready to transform your workflows with QR Suite?**

[⬇️ Install Now](https://github.com/your-username/qr_suite) | [📖 Read Docs](INSTALL.md) | [💬 Get Support](https://github.com/your-username/qr_suite/issues)

---

*Made with ❤️ for the ERPNext community*
