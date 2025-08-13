#!/bin/bash
# Quick QR Suite verification script

echo "======================================"
echo "QR Suite Installation Check"
echo "======================================"

# Check roles
echo -e "\n1. Checking Roles..."
bench --site vp mariadb -e "SELECT role_name FROM tabRole WHERE role_name IN ('QR User', 'QR Manager');"

# Check QR Settings
echo -e "\n2. Checking QR Settings..."
bench --site vp mariadb -e "SELECT name, total_doctypes, enabled_count FROM \`tabQR Settings\` LIMIT 1;"

# Check enabled doctypes
echo -e "\n3. Checking Enabled DocTypes..."
bench --site vp mariadb -e "SELECT doctype_name, is_enabled, is_hardcoded FROM \`tabQR Settings Detail\` WHERE is_enabled=1 LIMIT 10;"

echo -e "\n======================================"
echo "Quick checks complete!"
echo "Now please test in the browser:"
echo "1. Go to any Asset, Item, or Customer"
echo "2. Look for 'QR Suite' button group"
echo "3. If missing, hard refresh (Ctrl+Shift+R)"
echo "======================================"
