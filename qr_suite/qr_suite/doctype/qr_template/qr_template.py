import frappe
from frappe.model.document import Document

class QRTemplate(Document):
    def validate(self):
        """Validate QR Template"""
        self.validate_doctype_exists()
        self.validate_field_name()
        
    def validate_doctype_exists(self):
        """Validate that target doctype exists"""
        if self.target_doctype:
            if not frappe.db.exists("DocType", self.target_doctype):
                frappe.throw(f"DocType '{self.target_doctype}' does not exist")
                
    def validate_field_name(self):
        """Validate field name for Value QR"""
        if self.qr_type == "Value QR" and self.value_field and self.target_doctype:
            # Check if field exists in the doctype
            meta = frappe.get_meta(self.target_doctype)
            if not meta.has_field(self.value_field):
                frappe.throw(f"Field '{self.value_field}' does not exist in DocType '{self.target_doctype}'")
    
    def get_qr_size_pixels(self):
        """Get QR code size in pixels"""
        size_map = {
            "Small": 150,
            "Medium": 250,
            "Large": 400
        }
        return size_map.get(self.qr_size, 250)
    
    def get_error_correction_level(self):
        """Get QR error correction level"""
        import qrcode
        level_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        return level_map.get(self.error_correction, qrcode.constants.ERROR_CORRECT_M)
