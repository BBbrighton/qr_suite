from frappe import _

def get_data():
    return [
        {
            "module_name": "QR Suite",
            "category": "Modules",
            "label": _("QR Suite"),
            "color": "#3498db",
            "icon": "octicon octicon-qrcode",
            "type": "module",
            "description": "Comprehensive QR Code management for ERPNext workflows",
            "onboard_present": 1
        }
    ]
