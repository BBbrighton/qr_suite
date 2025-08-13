#!/bin/bash
# Quick migration script for QR Suite fields

echo "Migrating QR Suite fields..."

# Run the patch
bench --site all run-patch qr_suite.patches.add_qr_link_fields

# Migrate the doctype
bench --site all migrate

# Clear cache
bench --site all clear-cache

# Restart workers
bench restart

echo "Migration complete! QR Link fields should now be available."
