import frappe
import secrets
from frappe.model.document import Document
from frappe.utils import now, add_days, get_url

class QRLink(Document):
    def before_insert(self):
        """Set defaults before inserting"""
        self.created_on = now()
        
        # Generate URL/content based on QR type
        if self.qr_type == "Document QR":
            # Default url_mode if not set
            if not self.url_mode:
                self.url_mode = "token"
            
            if self.url_mode == "token":
                self.token = secrets.token_urlsafe(32)
                self.qr_url = f"{get_url()}/qr?token={self.token}"
            else:  # direct mode
                # Build direct URL
                base_url = getattr(self, 'custom_url_prefix', None) or get_url()
                action_route = self.get_action_route()
                self.qr_url = f"{base_url}{action_route}"
                
                # Add extra params if specified
                extra_params = getattr(self, 'extra_params', None)
                if extra_params:
                    try:
                        import json
                        params = json.loads(extra_params)
                        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
                        self.qr_url += f"&{param_str}" if "?" in self.qr_url else f"?{param_str}"
                    except:
                        pass
            
            # Set expiry if specified in template but not overridden
            if not self.expires_on and self.qr_template:
                try:
                    template = frappe.get_cached_doc("QR Template", self.qr_template)
                    if hasattr(template, 'token_expiry_days') and template.token_expiry_days and template.token_expiry_days > 0:
                        self.expires_on = add_days(now(), template.token_expiry_days)
                except:
                    pass
        
        elif self.qr_type == "Value QR":
            # For Value QR, ensure qr_content is set
            if not self.qr_content:
                # Try to get from template
                if self.qr_template:
                    try:
                        template = frappe.get_cached_doc("QR Template", self.qr_template)
                        if hasattr(template, 'value_field') and template.value_field:
                            # Get value from the specified field
                            doc = frappe.get_doc(self.target_doctype, self.target_name)
                            field_value = doc.get(template.value_field)
                            if field_value:
                                self.qr_content = str(field_value)
                    except:
                        pass
                
                # Default to target name if still not set
                if not self.qr_content:
                    self.qr_content = self.target_name
        
        # Set initial status
        if not self.status:
            self.status = "Active"
    
    def get_action_route(self):
        """Get the route based on action"""
        # Map actions to routes
        action_routes = {
            "view": f"/app/{self.target_doctype.lower().replace(' ', '-')}/{self.target_name}",
            "edit": f"/app/{self.target_doctype.lower().replace(' ', '-')}/{self.target_name}?edit=1",
            "print": f"/app/print/{self.target_doctype}/{self.target_name}",
            "email": f"/app/email/{self.target_doctype}/{self.target_name}",
            "new_stock_entry": f"/app/stock-entry/new-stock-entry-1?reference_doctype={self.target_doctype}&reference_name={self.target_name}",
            "maintenance_log": f"/app/asset-maintenance-log/new-asset-maintenance-log-1?asset={self.target_name}",
            "asset_repair": f"/app/asset-repair/new-asset-repair-1?asset={self.target_name}",
            "stock_balance": f"/app/query-report/Stock%20Balance?item_code={self.target_name}",
            "view_ledger": f"/app/query-report/Stock%20Ledger?item_code={self.target_name}"
        }
        
        return action_routes.get(self.action, action_routes["view"])
    
    def validate(self):
        """Validate the document"""
        if not self.target_doctype or not self.target_name:
            frappe.throw("Target DocType and Name are required")
        
        # Check if target exists
        if not frappe.db.exists(self.target_doctype, self.target_name):
            frappe.throw(f"{self.target_doctype} {self.target_name} does not exist")
        
        # Validate QR type specific fields
        if self.qr_type == "Document QR":
            if not self.action:
                self.action = "view"
            if not self.url_mode:
                self.url_mode = "token"
        elif self.qr_type == "Value QR":
            if not self.qr_content:
                frappe.throw("QR Content is required for Value QR")
        
        # Set default label text if not provided
        if self.include_label and not self.label_text:
            self.label_text = self.target_name
    
    @frappe.whitelist()
    def generate_qr_code(self):
        """Generate QR code image"""
        from qr_suite.utils.qr_code_generator import generate_qr_image
        
        result = generate_qr_image(self)
        
        if result and result.get("file_url"):
            self.qr_code_image = result["file_url"]
            self.save()
            
            frappe.msgprint("QR Code generated successfully", alert=True)
            return result
        else:
            frappe.throw("Failed to generate QR code")
    
    def is_valid(self):
        """Check if QR link is still valid"""
        if self.status in ["Expired", "Revoked", "Inactive"]:
            return False
            
        if self.expires_on and self.expires_on < now():
            self.status = "Expired"
            self.save()
            return False
            
        return True
    
    @frappe.whitelist()
    def record_scan(self):
        """Record a scan of this QR code"""
        if not self.is_valid():
            frappe.throw("This QR code is no longer valid")
        
        self.scan_count = (self.scan_count or 0) + 1
        self.last_scanned = now()
        self.last_scanned_by = frappe.session.user
        
        # Get IP address if available
        if frappe.local.request:
            self.last_scan_ip = frappe.local.request.remote_addr
        
        self.save()
        
        # Create scan log entry
        frappe.get_doc({
            "doctype": "QR Scan Log",
            "qr_link": self.name,
            "scanned_by": frappe.session.user,
            "scan_timestamp": now(),
            "ip_address": self.last_scan_ip,
            "target_doctype": self.target_doctype,
            "target_name": self.target_name
        }).insert(ignore_permissions=True)
        
        return {"status": "success", "message": "Scan recorded"}
    
    @frappe.whitelist()
    def revoke(self):
        """Revoke this QR code"""
        if self.status == "Revoked":
            frappe.throw("This QR code is already revoked")
        
        self.status = "Revoked"
        self.save()
        
        frappe.msgprint("QR Code has been revoked", indicator="red")
        return {"status": "success", "message": "QR Code revoked"}
    
    @frappe.whitelist()
    def generate_qr_image(self):
        """Generate QR code image (alias for generate_qr_code)"""
        return self.generate_qr_code()
