import frappe
from frappe import _

@frappe.whitelist()
def get_enabled_doctypes():
    """Return list of enabled doctypes for QR generation"""
    # Import here to avoid circular import
    from qr_suite.qr_suite.doctype.qr_settings.qr_settings import get_enabled_doctypes as get_from_settings
    
    try:
        # Try to get from QR Settings
        return get_from_settings()
    except Exception as e:
        frappe.log_error(f"Error getting enabled doctypes: {str(e)}", "QR API")
        # Fallback to hardcoded list for backward compatibility
        return get_hardcoded_doctypes()

@frappe.whitelist()
def get_enabled_qr_doctypes():
    """Alias for backward compatibility"""
    return get_enabled_doctypes()

def get_hardcoded_doctypes():
    """Fallback hardcoded list for backward compatibility"""
    ENABLED_DOCTYPES = [
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
    return [{"name": dt, "default_action": "view", "qr_type_default": "Document QR", "min_role": "QR User"} 
            for dt in ENABLED_DOCTYPES]

@frappe.whitelist()
def generate_qr_code(doctype, docname, qr_type="Document QR", qr_template=None, **kwargs):
    """
    Main API method to generate QR codes with full flexibility
    
    Args:
        doctype: Target doctype
        docname: Target document name
        qr_type: "Document QR" or "Value QR"
        qr_template: Optional template name
        **kwargs: Additional options like action, value_field, custom_value, etc.
    """
    try:
        # Validate inputs
        if not doctype or not docname:
            frappe.throw(_("DocType and Document Name are required"))
        
        # Check if document exists
        if not frappe.db.exists(doctype, docname):
            frappe.throw(_("Document {0} {1} not found").format(doctype, docname))
        
        # Check permissions - both document permission and QR generation permission
        if not frappe.has_permission(doctype, "read", docname):
            frappe.throw(_("You don't have permission to access this document"))
        
        # Check QR generation permission
        from qr_suite.qr_suite.doctype.qr_settings.qr_settings import can_generate_qr
        if not can_generate_qr(doctype):
            frappe.throw(_("You don't have permission to generate QR codes for {0}. Required role: QR User or QR Manager").format(doctype))
        
        # Create QR Link document
        qr_link = frappe.new_doc("QR Link")
        qr_link.target_doctype = doctype
        qr_link.target_name = docname
        qr_link.qr_type = qr_type
        qr_link.qr_template = qr_template
        
        # Handle template settings if provided
        if qr_template:
            template = frappe.get_cached_doc("QR Template", qr_template)
            # Apply template's url_mode if not overridden
            if qr_type == "Document QR" and hasattr(template, 'url_mode') and 'url_mode' not in kwargs:
                kwargs['url_mode'] = template.url_mode
        
        # Handle Document QR specific fields
        if qr_type == "Document QR":
            qr_link.action = kwargs.get('action', get_default_action(doctype))
            qr_link.url_mode = kwargs.get('url_mode', 'token')  # Default to token mode
            
            if kwargs.get('expires_on'):
                qr_link.expires_on = kwargs.get('expires_on')
            
            # Handle custom URL prefix for direct mode
            if kwargs.get('custom_url_prefix'):
                qr_link.custom_url_prefix = kwargs.get('custom_url_prefix')
            
            # Handle extra parameters
            if kwargs.get('extra_params'):
                qr_link.extra_params = kwargs.get('extra_params')
        
        # Handle Value QR specific fields
        elif qr_type == "Value QR":
            if kwargs.get('custom_value'):
                # Use custom value directly
                qr_link.qr_content = str(kwargs.get('custom_value'))
            elif kwargs.get('value_field'):
                # Get value from specified field
                doc = frappe.get_doc(doctype, docname)
                field_value = doc.get(kwargs.get('value_field'))
                if field_value:
                    qr_link.qr_content = str(field_value)
                else:
                    qr_link.qr_content = docname
            else:
                # Default to document name
                qr_link.qr_content = docname
        
        # Save with elevated permissions
        qr_link.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Generate QR image with options
        try:
            from qr_suite.utils.qr_code_generator import generate_qr_image
            
            # Pass all relevant options to generator
            generator_kwargs = {
                'qr_size': kwargs.get('qr_size', 'Medium'),
                'error_correction': kwargs.get('error_correction', 'M'),
                'image_format': kwargs.get('image_format', 'PNG')
            }
            
            # Pass label options to generator
            if kwargs.get('include_label'):
                qr_link.include_label = True
                qr_link.label_text = kwargs.get('label_text', docname)
            
            result = generate_qr_image(qr_link, **generator_kwargs)
            
            # Update QR Link with image details
            if result.get("file_url"):
                frappe.db.set_value("QR Link", qr_link.name, {
                    "qr_code_image": result["file_url"],
                    "status": "Active"
                }, update_modified=False)
        except Exception as e:
            frappe.log_error(f"QR image generation failed: {str(e)}", "QR Generation")
            # Don't fail the whole operation if image generation fails
        
        # Reload to get updated values
        qr_link.reload()
        
        return {
            "success": True,
            "qr_link": qr_link.name,
            "file_url": qr_link.qr_code_image,
            "status": qr_link.status,
            "message": _("QR Code generated successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"QR generation error: {str(e)}", "QR API Error")
        return {
            "success": False,
            "message": str(e)
        }

def get_default_action(doctype):
    """Get default action for a doctype from settings or fallback"""
    try:
        # Try to get from settings
        from qr_suite.qr_suite.doctype.qr_settings.qr_settings import get_enabled_doctypes
        enabled = get_enabled_doctypes()
        
        for dt in enabled:
            if dt.get("name") == doctype:
                return dt.get("default_action", "view")
    except:
        pass
    
    # Fallback to hardcoded map
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
def get_doctype_fields(doctype):
    """Get fields suitable for QR encoding from a doctype"""
    try:
        meta = frappe.get_meta(doctype)
        fields = []
        
        # Get fields that make sense to encode in QR
        suitable_fieldtypes = ['Data', 'Link', 'Select', 'Int', 'Float', 'Currency', 'Barcode']
        
        for field in meta.fields:
            if field.fieldtype in suitable_fieldtypes and not field.hidden:
                fields.append({
                    'label': field.label,
                    'fieldname': field.fieldname,
                    'fieldtype': field.fieldtype
                })
        
        return fields
    except Exception as e:
        frappe.log_error(f"Error getting fields: {str(e)}")
        return []

@frappe.whitelist()
def check_qr_permission(doctype):
    """Check if current user can generate QR for doctype"""
    from qr_suite.qr_suite.doctype.qr_settings.qr_settings import can_generate_qr
    return can_generate_qr(doctype)
