frappe.ui.form.on('QR Template', {
    qr_type: function(frm) {
        // Clear dependent fields when QR type changes
        if (frm.doc.qr_type === 'Value QR') {
            frm.set_value('default_action', '');
            frm.set_value('url_mode', '');
            frm.set_value('token_expiry_days', '');
            frm.set_value('custom_url_prefix', '');
            frm.set_value('extra_params', '');
        }
    },
    
    target_doctype: function(frm) {
        // Clear value field when target doctype changes
        if (frm.doc.qr_type === 'Value QR') {
            frm.set_value('value_field', '');
        }
    }
});
