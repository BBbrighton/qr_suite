import frappe
from frappe.model.document import Document

class QRScanLog(Document):
    def before_insert(self):
        """Before insert operations"""
        if not self.scan_timestamp:
            self.scan_timestamp = frappe.utils.now()
        if not self.scanned_by:
            self.scanned_by = frappe.session.user
