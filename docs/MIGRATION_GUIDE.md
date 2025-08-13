# QR Suite Migration Guide
## Changes Made for Role-Based Permissions and Dynamic DocType Support

### Overview
This update transforms QR Suite from a hardcoded doctype list to a dynamic, role-based permission system with centralized settings.

### New Components Added
1. **QR Settings Detail** (Child Table DocType)
   - Location: `qr_suite/doctype/qr_settings_detail/`
   - Fields: doctype_name, is_enabled, is_hardcoded, qr_type_default, default_action, min_role

2. **QR Settings Python Logic**
   - Location: `qr_suite/doctype/qr_settings/qr_settings.py`
   - Features: Auto-discovery, permission checking, default settings creation

3. **New Roles**
   - QR User: Can generate QR codes for allowed doctypes
   - QR Manager: Can manage QR settings and generate for all doctypes

4. **Tasks Module**
   - Location: `qr_suite/tasks.py`
   - Daily cleanup of expired QR codes

### Modified Components
1. **api.py**
   - Now uses dynamic doctype list from QR Settings
   - Added permission checking (can_generate_qr)
   - Maintains backward compatibility

2. **qr_injector.js**
   - Loads enabled doctypes dynamically
   - Checks permissions before showing buttons
   - Falls back to hardcoded list if settings fail

3. **install.py**
   - Creates roles on install/migrate
   - Initializes QR Settings with hardcoded doctypes
   - Updates permissions for all relevant doctypes

4. **hooks.py**
   - Removed hardcoded doctype_js mappings
   - Added role fixtures
   - Added permission hooks and scheduled tasks

### Migration Steps

#### Step 1: Backup Current Installation
```bash
cd ~/frappe-bench/apps
cp -r qr_suite qr_suite_backup_$(date +%Y%m%d_%H%M%S)
```

#### Step 2: Clear Cache and Migrate
```bash
cd ~/frappe-bench
bench clear-cache
bench build --app qr_suite
bench migrate
```

#### Step 3: Verify Installation
1. Check if roles were created:
   - Go to User List > Roles
   - Look for "QR User" and "QR Manager"

2. Check if QR Settings was created:
   - Go to Awesome Bar and type "QR Settings"
   - Should see all hardcoded doctypes enabled

3. Assign roles to users:
   - Edit users and assign appropriate QR roles
   - System Manager has full access by default

#### Step 4: Test Functionality
1. **As System Manager:**
   - All doctypes should show QR buttons
   - Can access and modify QR Settings

2. **As QR Manager:**
   - All enabled doctypes show QR buttons
   - Can access and modify QR Settings

3. **As QR User:**
   - Only enabled doctypes show QR buttons
   - Can view but not modify QR Settings

4. **As regular user (no QR roles):**
   - No QR buttons should appear

### Rollback Procedure
If anything goes wrong:
```bash
cd ~/frappe-bench/apps
rm -rf qr_suite
cp -r qr_suite_backup_[timestamp] qr_suite
bench clear-cache
bench build --app qr_suite
bench migrate
```

### Post-Migration Tasks
1. **Enable Additional DocTypes:**
   - Go to QR Settings
   - Click "Sync DocTypes Now"
   - Enable any additional doctypes as needed

2. **Customize Permissions:**
   - Adjust min_role for specific doctypes
   - Change default actions as needed

3. **Test QR Generation:**
   - Generate a few test QR codes
   - Verify they work as expected

### Troubleshooting

**Issue: QR buttons not appearing**
- Check browser console for errors
- Verify user has appropriate roles
- Clear browser cache

**Issue: Permission denied errors**
- Check QR Settings to ensure doctype is enabled
- Verify user has required role
- Check if QR Settings document exists

**Issue: Settings not loading**
- Run `bench migrate` again
- Check error logs in `sites/[site]/logs/`
- Manually create QR Settings if needed

### Backward Compatibility
- Old API methods still work
- Hardcoded doctype list used as fallback
- Existing QR Links continue to function
- No data migration required

### Future Enhancements
With this foundation, you can now:
- Add custom doctypes to QR generation
- Set different permission levels per doctype
- Create department-specific QR permissions
- Add more QR types and actions
