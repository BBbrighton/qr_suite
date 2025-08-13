#!/bin/bash
# Final cleanup script for QR Suite

echo "QR Suite Final Cleanup"
echo "====================="

# Remove duplicate and unnecessary files
echo "Removing duplicate files..."
rm -f qr_suite/www/js/qr_injector.js
rm -f qr_suite/verify_installation.py
rm -f qr_suite/public/js/qr_injector.js
rm -f qr_suite/public/js/qr_debug.js

# Remove old shell scripts
echo "Removing old scripts..."
rm -f scripts/cleanup.sh
rm -f scripts/cleanup_final.sh
rm -f scripts/check_installation.sh

# Remove temporary files
echo "Removing temporary files..."
rm -f qr_suite.zip
rm -f .cleanup_list
rm -rf qr_suite_backup_*

# Remove empty directories
echo "Removing empty directories..."
rmdir qr_suite/www/js 2>/dev/null || true
rmdir qr_suite/public/css 2>/dev/null || true
rmdir qr_suite/templates/includes 2>/dev/null || true

# Remove all __pycache__ directories
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove the deep_clean.py script after running
rm -f deep_clean.py

echo ""
echo "Cleanup completed!"
echo ""
echo "The QR Suite app is now ready for GitHub!"
echo ""
echo "Next steps:"
echo "1. git add -A"
echo "2. git commit -m 'feat: Complete QR Suite v1.0.0 - Ready for production'"
echo "3. git remote add origin https://github.com/your-username/qr_suite.git"
echo "4. git push -u origin main"
echo ""
echo "Installation from GitHub:"
echo "bench get-app https://github.com/your-username/qr_suite.git"
