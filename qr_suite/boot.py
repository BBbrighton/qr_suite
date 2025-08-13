import frappe

def inject_qr_js(bootinfo):
    """
    Boot session hook - now only used for passing configuration data
    The actual QR button injection is handled via dynamic doctype_js in hooks.py
    """
    # Add enabled doctypes to bootinfo for reference
    try:
        from qr_suite.qr_suite.doctype.qr_settings.qr_settings import get_enabled_doctypes
        enabled = get_enabled_doctypes()
        bootinfo.qr_enabled_doctypes = [dt["name"] for dt in enabled]
    except:
        # If QR Settings doesn't exist yet, use empty list
        bootinfo.qr_enabled_doctypes = []
