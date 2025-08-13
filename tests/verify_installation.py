#!/usr/bin/env python
"""
QR Suite Installation Verification Script
Run this from frappe-bench directory: bench execute qr_suite.verify_installation
"""

import frappe

def verify_installation():
    """Verify QR Suite installation and configuration"""
    print("\n" + "="*60)
    print("QR Suite Installation Verification")
    print("="*60)
    
    # Check 1: Roles
    print("\n1. Checking Roles...")
    roles = ["QR User", "QR Manager"]
    for role_name in roles:
        exists = frappe.db.exists("Role", role_name)
        if exists:
            print(f"   ✓ Role '{role_name}' exists")
        else:
            print(f"   ✗ Role '{role_name}' NOT FOUND")
    
    # Check 2: QR Settings
    print("\n2. Checking QR Settings...")
    if frappe.db.exists("QR Settings", "QR Settings"):
        print("   ✓ QR Settings document exists")
        
        # Get settings details
        settings = frappe.get_doc("QR Settings", "QR Settings")
        print(f"   - Total DocTypes: {settings.total_doctypes}")
        print(f"   - Enabled DocTypes: {settings.enabled_count}")
        
        # Check hardcoded doctypes
        from qr_suite.qr_suite.doctype.qr_settings.qr_settings import HARDCODED_DOCTYPES
        existing_doctypes = {d.doctype_name for d in settings.doctype_settings}
        
        missing = set(HARDCODED_DOCTYPES) - existing_doctypes
        if missing:
            print(f"   ⚠ Missing hardcoded doctypes: {missing}")
        else:
            print("   ✓ All hardcoded doctypes present")
    else:
        print("   ✗ QR Settings NOT FOUND")
    
    # Check 3: Permissions
    print("\n3. Checking Permissions...")
    try:
        # Check QR Link permissions
        doctype = frappe.get_doc("DocType", "QR Link")
        role_perms = {perm.role: perm for perm in doctype.permissions}
        
        for role in ["All", "QR User", "QR Manager", "System Manager"]:
            if role in role_perms:
                print(f"   ✓ QR Link permissions set for '{role}'")
            else:
                print(f"   ⚠ QR Link permissions missing for '{role}'")
    except Exception as e:
        print(f"   ✗ Error checking permissions: {e}")
    
    # Check 4: API availability
    print("\n4. Checking API Methods...")
    try:
        from qr_suite.api import get_enabled_doctypes, generate_qr_code, check_qr_permission
        print("   ✓ API methods imported successfully")
        
        # Try calling get_enabled_doctypes
        enabled = get_enabled_doctypes()
        if enabled:
            print(f"   ✓ get_enabled_doctypes() returned {len(enabled)} doctypes")
        else:
            print("   ⚠ get_enabled_doctypes() returned empty list")
    except Exception as e:
        print(f"   ✗ API error: {e}")
    
    # Check 5: JavaScript files
    print("\n5. Checking JavaScript Files...")
    js_file = frappe.get_app_path("qr_suite", "public", "js", "qr_injector.js")
    import os
    if os.path.exists(js_file):
        print("   ✓ qr_injector.js exists")
        # Check if it has the dynamic loading code
        with open(js_file, 'r') as f:
            content = f.read()
            if "load_settings" in content:
                print("   ✓ qr_injector.js has dynamic loading code")
            else:
                print("   ⚠ qr_injector.js might be old version")
    else:
        print("   ✗ qr_injector.js NOT FOUND")
    
    print("\n" + "="*60)
    print("Verification Complete")
    print("="*60)
    
    # Recommendations
    print("\nRecommendations:")
    print("1. If any checks failed, run: bench migrate")
    print("2. Clear browser cache and hard refresh (Ctrl+Shift+R)")
    print("3. Assign QR roles to users who need QR functionality")
    print("4. Test with different user roles to verify permissions")

if __name__ == "__main__":
    verify_installation()
