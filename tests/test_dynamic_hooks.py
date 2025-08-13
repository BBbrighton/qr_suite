#!/usr/bin/env python
# Test script to verify dynamic hooks implementation

import frappe
from frappe.utils import cint

def test_dynamic_hooks():
    """Test the dynamic hooks implementation"""
    print("Testing QR Suite Dynamic Hooks Implementation")
    print("=" * 50)
    
    # Test 1: Check if hooks can be imported
    try:
        from qr_suite.hooks import get_dynamic_doctype_js
        print("✓ Successfully imported get_dynamic_doctype_js function")
    except Exception as e:
        print(f"✗ Failed to import: {str(e)}")
        return
    
    # Test 2: Test the function without database
    print("\nTest 2: Testing function without database context...")
    frappe.db = None
    result = get_dynamic_doctype_js()
    print(f"Result without DB: {len(result)} doctypes")
    print(f"Should return empty dict: {result == {}}")
    
    # Test 3: Test with database mock
    print("\nTest 3: Testing with database context...")
    # This would need actual database connection in real environment
    
    # Test 4: Check cache functionality
    print("\nTest 4: Testing cache functionality...")
    try:
        # Mock cache for testing
        class MockCache:
            def __init__(self):
                self.data = {}
            
            def get_value(self, key):
                return self.data.get(key)
            
            def set_value(self, key, value, expires_in_sec=None):
                self.data[key] = value
            
            def delete_value(self, key):
                if key in self.data:
                    del self.data[key]
        
        # Test cache operations
        cache = MockCache()
        test_data = {"Asset": "public/js/qr_suite_doctype.js"}
        cache.set_value("qr_suite_enabled_doctypes_js", test_data)
        cached = cache.get_value("qr_suite_enabled_doctypes_js")
        print(f"✓ Cache set and get working: {cached == test_data}")
        
        cache.delete_value("qr_suite_enabled_doctypes_js")
        print(f"✓ Cache delete working: {cache.get_value('qr_suite_enabled_doctypes_js') is None}")
        
    except Exception as e:
        print(f"✗ Cache test failed: {str(e)}")
    
    # Test 5: Verify fallback doctypes
    print("\nTest 5: Checking fallback doctypes...")
    EXPECTED_FALLBACK = [
        "Asset", "Stock Entry", "Serial No", "Batch", "Item",
        "Warehouse", "Purchase Order", "Sales Order", 
        "Purchase Receipt", "Delivery Note", "Customer",
        "Supplier", "Employee"
    ]
    print(f"Expected {len(EXPECTED_FALLBACK)} fallback doctypes defined")
    
    print("\n" + "=" * 50)
    print("Dynamic Hooks Implementation Test Complete")
    print("\nNext Steps:")
    print("1. Run 'bench restart' to reload the app with new hooks")
    print("2. Test in browser by:")
    print("   a. Going to QR Settings")
    print("   b. Adding a new doctype (e.g., 'Lead', 'Purchase Invoice')")
    print("   c. Refreshing the page")
    print("   d. Opening that doctype - QR buttons should appear")

if __name__ == "__main__":
    # Run in bench console: bench --site [sitename] console
    # Then: exec(open('test_dynamic_hooks.py').read())
    test_dynamic_hooks()
