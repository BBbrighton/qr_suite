import frappe
from frappe import _

def after_install():
    """Run after app is installed"""
    create_qr_roles()
    update_qr_link_permissions()
    create_default_qr_settings()
    frappe.clear_cache()

def after_migrate():
    """Run after app migrations"""
    create_qr_roles()
    update_qr_link_permissions()
    ensure_qr_settings_exists()
    inject_qr_js_dynamically()
    frappe.clear_cache()

def inject_qr_js_dynamically():
    """Inject QR JS for all enabled doctypes"""
    try:
        # This approach modifies the hooks dynamically
        print("QR Suite: Injecting JS dynamically...")
        
        # Create a custom JS that loads for all forms
        js_content = """
// Auto-generated QR Suite loader
frappe.ready(function() {
    if (!frappe.qr_suite_loader_initialized) {
        frappe.qr_suite_loader_initialized = true;
        
        // Load the main QR injector script
        frappe.require('assets/qr_suite/js/qr_injector.js', function() {
            console.log('QR Suite: Injector loaded via require');
        });
    }
});
"""
        
        # Write to a file that's always loaded
        import os
        js_path = frappe.get_site_path('public', 'js', 'qr_suite_loader.js')
        os.makedirs(os.path.dirname(js_path), exist_ok=True)
        
        with open(js_path, 'w') as f:
            f.write(js_content)
            
        print(f"QR Suite: Loader written to {js_path}")
        
    except Exception as e:
        print(f"QR Suite: Could not inject JS dynamically: {e}")

def create_qr_roles():
    """Create QR Suite specific roles"""
    roles = [
        {
            "role_name": "QR User",
            "desk_access": 1,
            "description": "Can generate QR codes for allowed doctypes"
        },
        {
            "role_name": "QR Manager", 
            "desk_access": 1,
            "description": "Can manage QR settings and generate QR codes for all doctypes"
        }
    ]
    
    for role_info in roles:
        if not frappe.db.exists("Role", role_info["role_name"]):
            try:
                role = frappe.new_doc("Role")
                role.role_name = role_info["role_name"]
                role.desk_access = role_info["desk_access"]
                role.description = role_info["description"]
                role.insert(ignore_permissions=True)
                frappe.db.commit()
                print(f"Created role: {role_info['role_name']}")
            except Exception as e:
                print(f"Could not create role {role_info['role_name']}: {e}")

def update_qr_link_permissions():
    """Ensure QR Link has proper permissions for all users"""
    try:
        doctype = frappe.get_doc("DocType", "QR Link")
        
        # Define required permissions
        required_permissions = [
            {
                "role": "All",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 0,
                "print": 1,
                "email": 1,
                "export": 1
            },
            {
                "role": "QR User",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 0,
                "print": 1,
                "email": 1,
                "export": 1
            },
            {
                "role": "QR Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "print": 1,
                "email": 1,
                "export": 1,
                "report": 1
            },
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "print": 1,
                "email": 1,
                "export": 1,
                "report": 1,
                "share": 1
            }
        ]
        
        # Check existing permissions
        existing_roles = {perm.role: perm for perm in doctype.permissions}
        
        # Add or update permissions
        for perm_dict in required_permissions:
            role = perm_dict["role"]
            if role in existing_roles:
                # Update existing
                for key, value in perm_dict.items():
                    if key != "role":
                        setattr(existing_roles[role], key, value)
            else:
                # Add new
                doctype.append("permissions", perm_dict)
        
        doctype.save()
        frappe.db.commit()
        print("Updated QR Link permissions")
            
    except Exception as e:
        print(f"Could not update QR Link permissions: {e}")

def create_default_qr_settings():
    """Create default QR Settings if not exists"""
    try:
        if not frappe.db.exists("QR Settings", "QR Settings"):
            from qr_suite.qr_suite.doctype.qr_settings.qr_settings import create_default_settings
            settings = create_default_settings()
            if settings:
                print("Created default QR Settings")
                # Don't sync all doctypes - just keep hardcoded ones
                print("Initialized with hardcoded doctypes only")
    except Exception as e:
        print(f"Could not create default QR Settings: {e}")

def ensure_qr_settings_exists():
    """Ensure QR Settings exists, create if not"""
    try:
        if not frappe.db.exists("QR Settings", "QR Settings"):
            create_default_qr_settings()
        else:
            # If exists, ensure all hardcoded doctypes are present
            settings = frappe.get_doc("QR Settings", "QR Settings")
            from qr_suite.qr_suite.doctype.qr_settings.qr_settings import HARDCODED_DOCTYPES
            
            existing_doctypes = {d.doctype_name for d in settings.doctype_settings}
            
            for doctype in HARDCODED_DOCTYPES:
                if doctype not in existing_doctypes:
                    settings.append("doctype_settings", {
                        "doctype_name": doctype,
                        "is_enabled": 1,
                        "is_hardcoded": 1,
                        "qr_type_default": "Document QR",
                        "default_action": settings.get_default_action(doctype),
                        "min_role": "QR User"
                    })
            
            if len(existing_doctypes) < len(settings.doctype_settings):
                settings.save()
                print("Added missing hardcoded doctypes to QR Settings")
    except Exception as e:
        print(f"Error ensuring QR Settings exists: {e}")
