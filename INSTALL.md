# QR Suite Installation Guide

## Prerequisites

- ERPNext v15+ installed and running
- Frappe Framework v15+
- Python 3.10+
- Administrator or System Manager access

## Installation Methods

### Method 1: From GitHub (Recommended)

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from GitHub
bench get-app https://github.com/your-username/qr_suite.git

# Install the app on your site(s)
bench --site your-site-name install-app qr_suite

# Run migrations
bench --site your-site-name migrate

# Build assets
bench build --app qr_suite

# Restart bench
bench restart
```

### Method 2: From Git with Branch

```bash
# Get specific branch
bench get-app --branch develop https://github.com/your-username/qr_suite.git

# Install and setup
bench --site your-site-name install-app qr_suite
bench --site your-site-name migrate
bench build --app qr_suite
bench restart
```

### Method 3: Manual Installation

```bash
# Clone the repository
cd ~/frappe-bench/apps
git clone https://github.com/your-username/qr_suite.git

# Install dependencies
cd qr_suite
pip install -r requirements.txt

# Install on site
cd ~/frappe-bench
bench --site your-site-name install-app qr_suite
bench --site your-site-name migrate
bench build --app qr_suite
bench restart
```

## Post-Installation Setup

### 1. Assign Roles

QR Suite creates two roles:
- **QR User**: Can generate and view QR codes
- **QR Manager**: Can manage QR settings and templates

Assign these roles to appropriate users:
1. Go to User List
2. Select a user
3. In Roles section, add "QR User" or "QR Manager"
4. Save

### 2. Configure QR Settings

1. Go to **QR Suite > QR Settings**
2. Click **Sync DocTypes** to populate available doctypes
3. Enable/disable doctypes as needed
4. Set permissions per doctype
5. Save

### 3. Create QR Templates (Optional)

1. Go to **QR Suite > QR Template**
2. Create templates for common use cases
3. Configure default settings
4. Save

### 4. Test Installation

```bash
# Run verification script
bench --site your-site-name execute qr_suite.tests.verify_installation.verify_installation
```

## Updating QR Suite

```bash
# Update the app
cd ~/frappe-bench/apps/qr_suite
git pull

# Run migrations
cd ~/frappe-bench
bench --site your-site-name migrate
bench build --app qr_suite
bench restart
```

## Uninstallation

```bash
# Remove from site
bench --site your-site-name uninstall-app qr_suite

# Remove app files (optional)
bench remove-app qr_suite
```

## Troubleshooting

### QR buttons not appearing

1. Clear browser cache (Ctrl+Shift+R)
2. Check browser console for errors
3. Verify user has QR roles assigned
4. Run `bench restart`

### Permission errors

1. Ensure user has appropriate QR role
2. Check doctype permissions in QR Settings
3. Verify ERPNext permissions for target doctypes

### Migration issues

```bash
# Force reinstall doctypes
bench --site your-site-name reinstall-doctype "QR Link" "QR Template" "QR Settings"

# Clear cache
bench --site your-site-name clear-cache
```

### JavaScript errors

```bash
# Rebuild assets
bench build --app qr_suite

# Clear static files
bench clear-cache
```

## Support

- GitHub Issues: https://github.com/your-username/qr_suite/issues
- ERPNext Forum: https://discuss.erpnext.com
- Documentation: https://github.com/your-username/qr_suite/wiki

## License

MIT License - see LICENSE file for details
