import frappe
from frappe.utils import now_datetime, add_days

def cleanup_expired_qr_codes():
    """Mark expired QR codes as expired"""
    try:
        # Get all active QR Links with expiry date passed
        expired_qr_links = frappe.get_all("QR Link",
            filters={
                "status": "Active",
                "expires_on": ["<", now_datetime()]
            },
            fields=["name"]
        )
        
        # Update status
        for qr_link in expired_qr_links:
            frappe.db.set_value("QR Link", qr_link.name, "status", "Expired")
        
        if expired_qr_links:
            frappe.db.commit()
            print(f"Marked {len(expired_qr_links)} QR codes as expired")
    
    except Exception as e:
        frappe.log_error(f"Error in QR cleanup: {str(e)}", "QR Cleanup Task")
