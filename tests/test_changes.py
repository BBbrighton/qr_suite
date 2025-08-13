#!/usr/bin/env python
# Test script to verify QR Suite changes

import json

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    try:
        # Test API imports
        from qr_suite.api import get_enabled_doctypes, generate_qr_code, check_qr_permission
        print("✓ API imports successful")
        
        # Test settings imports
        from qr_suite.qr_suite.doctype.qr_settings.qr_settings import (
            get_enabled_doctypes as get_from_settings,
            can_generate_qr,
            create_default_settings,
            HARDCODED_DOCTYPES
        )
        print("✓ QR Settings imports successful")
        
        # Test install imports
        from qr_suite.install import (
            after_install,
            after_migrate,
            create_qr_roles,
            update_qr_link_permissions,
            create_default_qr_settings
        )
        print("✓ Install imports successful")
        
        # Test utils imports
        from qr_suite.utils.qr_code_generator import generate_qr_image
        print("✓ Utils imports successful")
        
        # Test tasks imports
        from qr_suite.tasks import cleanup_expired_qr_codes
        print("✓ Tasks imports successful")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def check_json_validity():
    """Check if all JSON files are valid"""
    print("\nChecking JSON files...")
    json_files = [
        "qr_suite/qr_suite/doctype/qr_settings/qr_settings.json",
        "qr_suite/qr_suite/doctype/qr_settings_detail/qr_settings_detail.json"
    ]
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            print(f"✓ {file_path} is valid JSON")
        except Exception as e:
            print(f"✗ {file_path} has JSON error: {e}")
            return False
    
    return True

def check_backwards_compatibility():
    """Check if changes maintain backwards compatibility"""
    print("\nChecking backwards compatibility...")
    
    # Check if old API methods still exist
    checks = [
        ("get_enabled_doctypes", "API method"),
        ("get_enabled_qr_doctypes", "API alias method"),
        ("generate_qr_code", "Main generation method"),
        ("get_doctype_fields", "Field getter method")
    ]
    
    from qr_suite import api
    for method_name, desc in checks:
        if hasattr(api, method_name):
            print(f"✓ {desc} '{method_name}' exists")
        else:
            print(f"✗ {desc} '{method_name}' missing!")
            return False
    
    return True

def main():
    """Run all tests"""
    print("QR Suite Change Verification")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_imports()
    all_passed &= check_json_validity()
    all_passed &= check_backwards_compatibility()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All checks passed! Changes appear to be safe.")
    else:
        print("✗ Some checks failed. Please review the errors above.")
    
    print("\nNext steps:")
    print("1. Run: bench clear-cache")
    print("2. Run: bench migrate")
    print("3. Test in browser with different user roles")

if __name__ == "__main__":
    main()
