from . import __version__ as app_version
import frappe

app_name = "qr_suite"
app_title = "QR Suite"
app_publisher = "Brighton"
app_description = "Comprehensive QR Code management for ERPNext workflows"
app_email = "brighton@example.com"
app_license = "MIT"

def get_dynamic_doctype_js():
    """
    Dynamically generate doctype_js based on enabled doctypes in QR Settings
    This function is called during app initialization
    """
    if not frappe.db:
        # During initial setup, database might not be available
        return {}
    
    try:
        # Try to get from cache first
        cache_key = "qr_suite_enabled_doctypes_js"
        cached_doctypes = frappe.cache().get_value(cache_key)
        
        if cached_doctypes is not None:
            return cached_doctypes
        
        # If not in cache, fetch from database
        enabled_doctypes = frappe.get_all(
            "QR Settings Detail",
            filters={
                "parent": "QR Settings",
                "parenttype": "QR Settings", 
                "is_enabled": 1
            },
            pluck="doctype_name"
        )
        
        # Generate doctype_js dictionary
        doctype_js_dict = {}
        for doctype in enabled_doctypes:
            doctype_js_dict[doctype] = "public/js/qr_suite_doctype.js"
        
        # If no enabled doctypes found, fall back to hardcoded list
        if not doctype_js_dict:
            # Hardcoded fallback for initial setup or when QR Settings doesn't exist
            FALLBACK_DOCTYPES = [
                "Asset", "Stock Entry", "Serial No", "Batch", "Item",
                "Warehouse", "Purchase Order", "Sales Order", 
                "Purchase Receipt", "Delivery Note", "Customer",
                "Supplier", "Employee"
            ]
            for doctype in FALLBACK_DOCTYPES:
                doctype_js_dict[doctype] = "public/js/qr_suite_doctype.js"
        
        # Cache for 5 minutes
        frappe.cache().set_value(cache_key, doctype_js_dict, expires_in_sec=300)
        
        return doctype_js_dict
        
    except Exception as e:
        # Log error but don't break the app
        if hasattr(frappe, 'log_error'):
            frappe.log_error(f"Error generating dynamic doctype_js: {str(e)}", "QR Suite Hooks")
        
        # Return hardcoded fallback
        return {
            "Asset": "public/js/qr_suite_doctype.js",
            "Stock Entry": "public/js/qr_suite_doctype.js",
            "Serial No": "public/js/qr_suite_doctype.js",
            "Batch": "public/js/qr_suite_doctype.js",
            "Item": "public/js/qr_suite_doctype.js",
            "Warehouse": "public/js/qr_suite_doctype.js",
            "Purchase Order": "public/js/qr_suite_doctype.js",
            "Sales Order": "public/js/qr_suite_doctype.js",
            "Purchase Receipt": "public/js/qr_suite_doctype.js",
            "Delivery Note": "public/js/qr_suite_doctype.js",
            "Customer": "public/js/qr_suite_doctype.js",
            "Supplier": "public/js/qr_suite_doctype.js",
            "Employee": "public/js/qr_suite_doctype.js"
        }

# Dynamic doctype_js generation
doctype_js = get_dynamic_doctype_js()

# Fixtures - export roles
fixtures = [
    {
        "dt": "Role",
        "filters": [
            ["role_name", "in", ["QR User", "QR Manager"]]
        ]
    }
]

# Hooks to run during lifecycle events
after_install = "qr_suite.install.after_install"
after_migrate = "qr_suite.install.after_migrate"

# Permission hooks
has_permission = {
    "QR Settings": "qr_suite.qr_suite.doctype.qr_settings.qr_settings.has_permission"
}

# Scheduled tasks
scheduler_events = {
    "daily": [
        "qr_suite.tasks.cleanup_expired_qr_codes"
    ]
}

# Website
website_route_rules = [
    {"from_route": "/qr/<path:token>", "to_route": "qr_suite.www.qr.index"}
]

# App configuration
app_color = "blue"
app_email = "brighton@example.com"
app_license = "MIT"

# Clear cache function for use in other modules
def clear_qr_cache():
    """Clear QR Suite cache - can be called when settings change"""
    frappe.cache().delete_value("qr_suite_enabled_doctypes_js")
