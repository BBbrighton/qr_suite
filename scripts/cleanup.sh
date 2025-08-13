#!/bin/bash
# QR Suite Cleanup Script
# This removes all unnecessary files, keeping only essential ones

echo "Cleaning up QR Suite..."

# Remove test and setup scripts from root
rm -f test_qr_manager.py
rm -f setup_qr_suite.py
rm -f setup_qr_suite_v2.py
rm -f fix_qr_permissions.py
rm -f check_qr_suite.py

# Remove backup directories
rm -rf qr_suite_settings_backup
rm -rf qr_doctype_setting_backup

# Remove unnecessary docs (can keep README.md if you want)
rm -f CONTRIBUTING.md
rm -f INSTALL.md
rm -f WORKFLOWS.md
rm -f API.md

# Clean up qr_suite directory
cd qr_suite

# Remove the empty fixtures directory
rm -rf fixtures

# Remove old/duplicate files
rm -f api_fixed.py

# Clean up utils directory
cd utils
rm -f qr_generator.py  # We're using qr_code_generator.py
rm -f qr_manager.py    # No longer needed
cd ..

# Clean up public/js directory
cd public/js
# Keep only qr_injector.js, remove all others
rm -f qr_injector_fixed.js
rm -f warehouse_qr.js
rm -f qr_suite.js
rm -f asset.js
rm -f warehouse.js.backup
rm -f qr_button_injection.js
rm -f qr_injection_new.js
rm -f test.js
rm -f qr_suite_with_settings.js
rm -f warehouse.js
rm -f qr_dynamic.js
rm -f stock_entry.js
rm -f qr_global.js
cd ../..

# Clean up qr_suite/qr_suite directory
cd qr_suite

# Remove QR Manager doctype (no longer needed)
rm -rf doctype/qr_manager

# Remove QR DocType Setting (no longer needed)  
rm -rf doctype/qr_doctype_setting

# Clean up unused utils
rm -rf utils/router.py
rm -rf utils/qr_generator.py
rm -rf utils/qr_manager.py

cd ../..

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

echo "Cleanup complete!"
echo ""
echo "Remaining structure:"
find . -type f -name "*.py" -o -name "*.js" -o -name "*.json" | grep -v __pycache__ | sort
