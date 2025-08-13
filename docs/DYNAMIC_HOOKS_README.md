# QR Suite Dynamic Hooks Implementation

## Overview
This implementation replaces the static hardcoded doctypes in `hooks.py` with a dynamic system that reads enabled doctypes from QR Settings.

## Changes Made

### 1. Modified `hooks.py`
- Replaced static `doctype_js` dictionary with dynamic `get_dynamic_doctype_js()` function
- Added caching mechanism (5-minute cache) for performance
- Included fallback to hardcoded list for initial setup
- Added `clear_qr_cache()` utility function

### 2. Updated `qr_settings.py`
- Added `on_update()` method to clear cache when settings change
- Added `frappe.clear_cache()` to ensure hooks are reloaded
- User gets notification to refresh page after changes

### 3. Cleaned up `boot.py`
- Removed qr_injector.js loading attempts
- Simplified to only pass configuration data

### 4. Made `qr_suite_doctype.js` self-contained
- Removed dependency on qr_injector.js
- Included all QR dialog functionality directly
- Works independently for each doctype

## How It Works

1. When Frappe loads, `hooks.py` calls `get_dynamic_doctype_js()`
2. The function checks cache first (5-minute TTL)
3. If not cached, queries QR Settings for enabled doctypes
4. Generates doctype_js dictionary dynamically
5. Falls back to hardcoded list if database unavailable
6. When QR Settings are updated, cache is cleared
7. User refreshes page to see changes

## Testing Instructions

1. **Restart Bench** to load new hooks:
   ```bash
   bench restart
   ```

2. **Verify Implementation**:
   ```bash
   bench --site [sitename] execute qr_suite.verify_qr_dynamic.verify_qr_suite_dynamic
   ```

3. **Test Dynamic Functionality**:
   - Go to QR Settings
   - Add a new doctype (e.g., "Purchase Invoice", "Lead")
   - Save settings
   - Refresh the page (you'll see a green notification)
   - Open any document of that doctype
   - QR Suite buttons should appear

## Benefits

1. **No Code Changes Required**: Add/remove doctypes through UI
2. **Immediate Effect**: Changes apply after page refresh
3. **Performance**: 5-minute cache prevents repeated DB queries
4. **Backward Compatible**: Falls back to hardcoded list if needed
5. **Clean Architecture**: Uses native Frappe mechanisms

## Troubleshooting

If QR buttons don't appear after adding a doctype:
1. Check browser console for errors
2. Ensure you refreshed the page after saving QR Settings
3. Verify the user has "QR User" or "QR Manager" role
4. Run the verification script
5. Check if `bench restart` was executed after implementation

## Files Modified
- `/apps/qr_suite/qr_suite/hooks.py`
- `/apps/qr_suite/qr_suite/qr_suite/doctype/qr_settings/qr_settings.py`
- `/apps/qr_suite/qr_suite/boot.py`
- `/apps/qr_suite/qr_suite/public/js/qr_suite_doctype.js`

## Files Added
- `/apps/qr_suite/test_dynamic_hooks.py`
- `/apps/qr_suite/verify_qr_dynamic.py`
- `/apps/qr_suite/DYNAMIC_HOOKS_README.md` (this file)
