# Copyright (c) 2025, Brighton and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime

# Hardcoded doctypes that must always be available
HARDCODED_DOCTYPES = [
    "Asset",
    "Stock Entry", 
    "Serial No",
    "Batch",
    "Item",
    "Warehouse",
    "Purchase Order",
    "Sales Order",
    "Purchase Receipt",
    "Delivery Note",
    "Customer",
    "Supplier",
    "Employee"
]

class QRSettings(Document):
    def validate(self):
        """Validate QR Settings"""
        # Ensure hardcoded doctypes cannot be disabled
        for row in self.doctype_settings:
            if row.is_hardcoded and not row.is_enabled:
                frappe.throw(_("Cannot disable hardcoded doctype: {0}").format(row.doctype_name))
        
        # Update counts
        self.update_counts()
    
    def on_update(self):
        """Clear cache when settings are updated"""
        # Clear the doctype_js cache
        frappe.cache().delete_value("qr_suite_enabled_doctypes_js")
        
        # Clear general cache to ensure hooks are reloaded
        frappe.clear_cache()
        
        # Show message to user
        frappe.msgprint(_("QR Settings updated. Changes will take effect after page refresh."), indicator="green")
    
    def update_counts(self):
        """Update total and enabled counts"""
        self.total_doctypes = len(self.doctype_settings)
        self.enabled_count = len([d for d in self.doctype_settings if d.is_enabled])
    
    @frappe.whitelist()
    def sync_doctypes(self):
        """Sync only relevant doctypes that make sense for QR codes"""
        # Define modules and doctypes that typically need QR codes
        relevant_modules = [
            "Stock", "Buying", "Selling", "Assets", "Manufacturing", 
            "Projects", "CRM", "Support", "HR", "Quality Management"
        ]
        
        # Additional specific doctypes that might be useful
        additional_doctypes = [
            "Payment Entry", "Journal Entry", "Expense Claim",
            "Vehicle", "Location", "Bin", "Package",
            "Maintenance Visit", "Maintenance Schedule"
        ]
        
        # Get relevant doctypes
        relevant_doctypes = frappe.get_list("DocType", 
            filters=[
                ["istable", "=", 0],
                ["issingle", "=", 0],
                ["is_virtual", "=", 0],
                ["custom", "=", 0],  # Exclude custom doctypes by default
                [
                    [
                        ["module", "in", relevant_modules]
                    ],
                    "or",
                    [
                        ["name", "in", HARDCODED_DOCTYPES + additional_doctypes]
                    ]
                ]
            ],
            fields=["name", "module"],
            order_by="module, name"
        )
        
        # Get existing doctype names in settings
        existing_doctypes = {d.doctype_name for d in self.doctype_settings}
        
        # Add missing relevant doctypes
        added = 0
        for dt in relevant_doctypes:
            if dt.name not in existing_doctypes:
                # Check if it's a hardcoded doctype
                is_hardcoded = dt.name in HARDCODED_DOCTYPES
                
                # Get default action based on doctype
                default_action = self.get_default_action(dt.name)
                
                self.append("doctype_settings", {
                    "doctype_name": dt.name,
                    "is_enabled": is_hardcoded,  # Enable by default if hardcoded
                    "is_hardcoded": is_hardcoded,
                    "qr_type_default": "Document QR",
                    "default_action": default_action,
                    "min_role": "QR User"
                })
                added += 1
        
        # Update sync time
        self.last_sync = now_datetime()
        
        # Save (this will trigger on_update and clear cache)
        self.save()
        
        frappe.msgprint(_("Synced relevant DocTypes for QR generation. Added {0} new doctypes.").format(added))
    
    @frappe.whitelist()
    def add_custom_doctype(self, doctype_name):
        """Manually add a specific doctype"""
        # Check if already exists
        existing = [d.doctype_name for d in self.doctype_settings]
        if doctype_name in existing:
            frappe.msgprint(_("DocType {0} already exists in settings").format(doctype_name))
            return
        
        # Verify doctype exists
        if not frappe.db.exists("DocType", doctype_name):
            frappe.throw(_("DocType {0} does not exist").format(doctype_name))
        
        # Add it
        self.append("doctype_settings", {
            "doctype_name": doctype_name,
            "is_enabled": 1,
            "is_hardcoded": 0,
            "qr_type_default": "Document QR",
            "default_action": "view",
            "min_role": "QR User"
        })
        
        # Save (this will trigger on_update and clear cache)
        self.save()
        frappe.msgprint(_("Added {0} to QR Settings").format(doctype_name))
    
    def get_default_action(self, doctype):
        """Get default action for a doctype"""
        action_map = {
            "Asset": "view",
            "Stock Entry": "view", 
            "Serial No": "view",
            "Batch": "view",
            "Item": "stock_balance",
            "Warehouse": "stock_balance",
            "Purchase Order": "view",
            "Sales Order": "view",
            "Purchase Receipt": "view",
            "Delivery Note": "view",
            "Customer": "view",
            "Supplier": "view",
            "Employee": "view"
        }
        return action_map.get(doctype, "view")

@frappe.whitelist()
def get_enabled_doctypes():
    """Get list of enabled doctypes from QR Settings"""
    try:
        # Check if QR Settings exists
        if not frappe.db.exists("QR Settings", "QR Settings"):
            # Create default settings if not exists
            create_default_settings()
        
        settings = frappe.get_cached_doc("QR Settings", "QR Settings")
        
        # Return enabled doctypes
        enabled = []
        for row in settings.doctype_settings:
            if row.is_enabled:
                enabled.append({
                    "name": row.doctype_name,
                    "default_action": row.default_action,
                    "qr_type_default": row.qr_type_default,
                    "min_role": row.min_role
                })
        
        return enabled
    except Exception as e:
        frappe.log_error(f"Error getting enabled doctypes: {str(e)}", "QR Settings")
        # Fallback to hardcoded list
        return [{"name": dt, "default_action": "view", "qr_type_default": "Document QR", "min_role": "QR User"} 
                for dt in HARDCODED_DOCTYPES]

@frappe.whitelist()
def can_generate_qr(doctype, user=None):
    """Check if user can generate QR for given doctype"""
    if not user:
        user = frappe.session.user
    
    # System Manager can always generate
    if "System Manager" in frappe.get_roles(user):
        return True
    
    try:
        settings = frappe.get_cached_doc("QR Settings", "QR Settings")
        
        # Find doctype in settings
        for row in settings.doctype_settings:
            if row.doctype_name == doctype and row.is_enabled:
                # Check role requirement
                if row.min_role == "QR User" and ("QR User" in frappe.get_roles(user) or "QR Manager" in frappe.get_roles(user)):
                    return True
                elif row.min_role == "QR Manager" and "QR Manager" in frappe.get_roles(user):
                    return True
        
        return False
    except:
        # Fallback - check if user has any QR role
        return "QR User" in frappe.get_roles(user) or "QR Manager" in frappe.get_roles(user)

def create_default_settings():
    """Create default QR Settings document"""
    try:
        settings = frappe.new_doc("QR Settings")
        settings.auto_discover = 1
        
        # Add hardcoded doctypes
        for doctype in HARDCODED_DOCTYPES:
            settings.append("doctype_settings", {
                "doctype_name": doctype,
                "is_enabled": 1,
                "is_hardcoded": 1,
                "qr_type_default": "Document QR",
                "default_action": settings.get_default_action(doctype),
                "min_role": "QR User"
            })
        
        settings.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return settings
    except Exception as e:
        frappe.log_error(f"Error creating default QR Settings: {str(e)}", "QR Settings")

def has_permission(doc, ptype, user):
    """Custom permission logic for QR Settings"""
    if ptype == "read":
        # QR User and QR Manager can read
        return "QR User" in frappe.get_roles(user) or "QR Manager" in frappe.get_roles(user) or "System Manager" in frappe.get_roles(user)
    elif ptype in ["write", "create"]:
        # Only QR Manager and System Manager can write
        return "QR Manager" in frappe.get_roles(user) or "System Manager" in frappe.get_roles(user)
    
    return False
