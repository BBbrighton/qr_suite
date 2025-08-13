
from __future__ import annotations
import frappe
from frappe.utils import now_datetime, get_url_to_form

try:
    from qr_suite.utils.router import get_redirect_url as _router_redirect  # optional
except Exception:
    _router_redirect = None

class QRNotFound(Exception): pass
class QRExpired(Exception): pass

def get_context(context):
    params = frappe.local.form_dict or {}
    try:
        link = _resolve_qr_link(params)
        _validate_qr_link(link)
        target = _compute_redirect_url(link, params)
        _safe_log_scan(link)
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = target
        return
    except QRNotFound as e:
        _set_error(context, 404, str(e))
    except QRExpired as e:
        _set_error(context, 410, str(e))
    except Exception:
        frappe.log_error(title="QR Suite: unexpected error at /qr", message=frappe.get_traceback())
        _set_error(context, 500, "Unexpected error while processing QR code.")

def _resolve_qr_link(params):
    token = params.get("token") or params.get("t")
    if token:
        row = frappe.get_all("QR Link", filters={"token": token}, fields=["name"], limit=1)
        if row:
            return frappe.get_doc("QR Link", row[0].name)
        if frappe.db.exists("QR Link", token):
            return frappe.get_doc("QR Link", token)
        raise QRNotFound("Invalid or unknown QR token.")

    dt = params.get("doctype") or params.get("target_doctype")
    dn = params.get("name") or params.get("target_name")
    if dt and dn:
        rows = frappe.get_all("QR Link",
            filters={"target_doctype": dt, "target_name": dn},
            fields=["name"], order_by="modified desc", limit=1)
        if rows:
            return frappe.get_doc("QR Link", rows[0].name)
        raise QRNotFound("No QR Link found for the given document.")
    raise QRNotFound("Missing token or document reference.")

def _validate_qr_link(link):
    status = (link.get("status") or "").lower()
    if status in {"disabled", "cancelled", "inactive"}:
        raise QRExpired("This QR code is disabled.")
    now = now_datetime()
    expiry_dt = link.get("expiry_datetime") or link.get("expires_on") or None
    expiry_date = link.get("expiry_date") or None
    if expiry_dt and now > expiry_dt:
        raise QRExpired("This QR code has expired.")
    if expiry_date and now.date() > expiry_date:
        raise QRExpired("This QR code has expired.")

def _compute_redirect_url(link, params):
    if callable(_router_redirect):
        try:
            url = _router_redirect(link)
            if url:
                return _absolutize(url)
        except Exception:
            frappe.log_error("QR Suite: router.get_redirect_url failed", frappe.get_traceback())

    for field in ("redirect_url", "url", "qr_url", "target_url"):
        val = link.get(field)
        if val:
            return _absolutize(val)

    dt = link.get("target_doctype")
    dn = link.get("target_name")
    if dt and dn:
        return get_url_to_form(dt, dn)

    return frappe.utils.get_url("/app")

def _absolutize(url: str) -> str:
    if isinstance(url, str) and (url.startswith("http://") or url.startswith("https://")):
        return url
    return frappe.utils.get_url(url or "/")

def _safe_log_scan(link):
    try:
        ua = frappe.get_request_header("User-Agent")
        ip = getattr(frappe.local, "request_ip", None)
        frappe.get_doc({
            "doctype": "QR Scan Log",
            "qr_link": link.name,
            "scanned_by": frappe.session.user,
            "ip_address": ip,
            "user_agent": ua,
            "scan_time": now_datetime(),
        }).insert(ignore_permissions=True)
    except Exception:
        try:
            frappe.db.rollback()
        except Exception:
            pass
        frappe.log_error("QR Suite: scan log insert failed", frappe.get_traceback())

def _set_error(context, http_status: int, message: str):
    frappe.local.response["http_status_code"] = http_status
    context.no_cache = 1
    titles = {404: "QR Code Not Found", 410: "QR Code Expired", 500: "QR Error"}
    context.error_title = titles.get(http_status, "QR Error")
    context.error_message = message
    frappe.local.response["message"] = f"{context.error_title}: {message}"
