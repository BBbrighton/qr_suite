#!/usr/bin/env python
"""
Verification script for QR Suite Dynamic Hooks
Run this after implementing changes to verify everything works
"""

import frappe

def verify_qr_suite_dynamic():
    """Verify dynamic hooks are working correctly"""
    print("QR Suite Dynamic Hooks Verification")
    print("=" * 40)
    
    # Check 1: Verify hooks.py loads correctly
    try:
        from qr_suite import hooks
        print("✓ hooks.py loads successfully")
        
        # Check if doctype_js is populated
        if hasattr(hooks, 'doctype_js'):
            count = len(hooks.doctype_js)
            print(f"✓ doctype_js contains {count} entries")
            if count > 0:
                print("  Sample entries:", list(hooks.doctype_js.keys())[:3])
        else:
            print("✗ doctype_js not found in hooks")
    except Exception as e:
        print(f"✗ Failed to load hooks: {str(e)}")
        return False
    
    # Check 2: Verify QR Settings exists
    try:
        if frappe.db.exists("QR Settings", "QR Settings"):
            print("✓ QR Settings document exists")
            
            # Get enabled doctypes
            settings = frappe.get_doc("QR Settings", "QR Settings")
            enabled_count = len([d for d in settings.doctype_settings if d.is_enabled])
            print(f"✓ {enabled_count} doctypes enabled in QR Settings")
        else:
            print("! QR Settings document not found - will be created on first use")
    except Exception as e:
        print(f"! Could not check QR Settings: {str(e)}")
    
    # Check 3: Verify cache mechanism
    try:
        # Test cache
        frappe.cache().set_value("qr_suite_test", "test_value", expires_in_sec=60)
        if frappe.cache().get_value("qr_suite_test") == "test_value":
            print("✓ Cache mechanism working")
            frappe.cache().delete_value("qr_suite_test")
        else:
            print("✗ Cache mechanism not working properly")
    except Exception as e:
        print(f"✗ Cache test failed: {str(e)}")
    
    # Check 4: Verify API endpoints
    try:
        from qr_suite.api import get_enabled_doctypes, check_qr_permission
        print("✓ API methods imported successfully")
    except Exception as e:
        print(f"✗ Failed to import API methods: {str(e)}")
    
    print("\n" + "=" * 40)
    print("Verification complete!")
    print("\nTo test the dynamic functionality:")
    print("1. Go to QR Settings in the UI")
    print("2. Enable a new doctype (e.g., 'Lead')")
    print("3. Save and refresh the page")
    print("4. Open any Lead document")
    print("5. You should see QR Suite buttons")
    
    return True

if __name__ == "__main__":
    # Run with: bench --site [sitename] execute qr_suite.verify_qr_dynamic.verify_qr_suite_dynamic
    verify_qr_suite_dynamic()
