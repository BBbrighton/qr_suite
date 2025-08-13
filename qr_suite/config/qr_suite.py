from frappe import _

def get_data():
    return {
        "QR Suite": {
            "color": "#3498db",
            "icon": "octicon octicon-qrcode",
            "label": _("QR Suite"),
            "link": "Modules/QR Suite",
            "category": "Modules",
            "type": "module"
        }
    }
