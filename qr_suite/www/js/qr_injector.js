// Copy of qr_injector.js
// QR Suite Universal Button Injector - Enhanced Dynamic Version
console.log('QR Suite: Loading enhanced injector...');

frappe.provide('frappe.qr_suite');

// Store enabled doctypes
frappe.qr_suite.enabled_doctypes = [];
frappe.qr_suite.settings_loaded = false;
frappe.qr_suite.injected_doctypes = new Set();

// Load settings from server
frappe.qr_suite.load_settings = function() {
    if (frappe.qr_suite.settings_loaded) {
        return Promise.resolve();
    }
    
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'qr_suite.api.get_enabled_doctypes',
            callback: function(r) {
                if (r.message) {
                    frappe.qr_suite.enabled_doctypes = r.message.map(dt => dt.name);
                    frappe.qr_suite.settings_loaded = true;
                    console.log('QR Suite: Loaded enabled doctypes:', frappe.qr_suite.enabled_doctypes);
                    
                    // Inject buttons for all enabled doctypes
                    frappe.qr_suite.inject_all_doctypes();
                    resolve();
                }
            },
            error: function() {
                console.error('QR Suite: Failed to load settings');
                reject();
            }
        });
    });
};

// Inject buttons for all enabled doctypes
frappe.qr_suite.inject_all_doctypes = function() {
    frappe.qr_suite.enabled_doctypes.forEach(doctype => {
        if (!frappe.qr_suite.injected_doctypes.has(doctype)) {
            frappe.qr_suite.inject_for_doctype(doctype);
        }
    });
};

// Inject buttons for a specific doctype
frappe.qr_suite.inject_for_doctype = function(doctype) {
    console.log(`QR Suite: Injecting buttons for ${doctype}`);
    
    try {
        frappe.ui.form.on(doctype, {
            refresh: function(frm) {
                // Skip if new document
                if (!frm.doc || frm.is_new() || frm.doc.__islocal) {
                    return;
                }
                
                // Skip if already added
                if (frm.qr_suite_buttons_added) {
                    return;
                }
                
                // Check if doctype is in enabled list
                if (!frappe.qr_suite.enabled_doctypes.includes(frm.doctype)) {
                    console.log(`QR Suite: ${frm.doctype} not in enabled list`);
                    return;
                }
                
                // Check permission
                frappe.call({
                    method: 'qr_suite.api.check_qr_permission',
                    args: { doctype: frm.doctype },
                    callback: function(r) {
                        if (r.message) {
                            frm.qr_suite_buttons_added = true;
                            
                            // Add buttons
                            frm.add_custom_button(__('Generate QR Code'), function() {
                                frappe.qr_suite.show_qr_dialog(frm);
                            }, __('QR Suite'));
                            
                            frm.add_custom_button(__('View QR Codes'), function() {
                                frappe.set_route('List', 'QR Link', {
                                    target_doctype: frm.doctype,
                                    target_name: frm.doc.name
                                });
                            }, __('QR Suite'));
                            
                            console.log(`QR Suite: Buttons added for ${frm.doctype} - ${frm.doc.name}`);
                        } else {
                            console.log(`QR Suite: No permission for ${frm.doctype}`);
                        }
                    }
                });
            }
        });
        
        frappe.qr_suite.injected_doctypes.add(doctype);
        console.log(`QR Suite: Successfully injected for ${doctype}`);
        
    } catch(e) {
        console.log(`QR Suite: Could not inject for ${doctype}:`, e);
    }
};

// Dialog function (simplified version)
frappe.qr_suite.show_qr_dialog = function(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __('Generate QR Code'),
        fields: [
            {
                fieldtype: 'HTML',
                options: `<div class="alert alert-info">
                    <p><strong>Generate QR Code for ${frm.doctype}: ${frm.doc.name}</strong></p>
                </div>`
            },
            {
                fieldname: 'qr_type',
                fieldtype: 'Select',
                label: 'QR Type',
                options: 'Document QR\nValue QR',
                default: 'Document QR',
                reqd: 1
            },
            {
                fieldname: 'qr_template',
                fieldtype: 'Link',
                label: 'QR Template (Optional)',
                options: 'QR Template'
            }
        ],
        primary_action_label: __('Generate'),
        primary_action: function(values) {
            frappe.call({
                method: 'qr_suite.api.generate_qr_code',
                args: {
                    doctype: frm.doctype,
                    docname: frm.doc.name,
                    qr_type: values.qr_type,
                    qr_template: values.qr_template
                },
                freeze: true,
                freeze_message: __('Generating QR Code...'),
                callback: function(r) {
                    if (r.message && r.message.success) {
                        frappe.show_alert({
                            message: __('QR Code generated successfully'),
                            indicator: 'green'
                        });
                        
                        if (r.message.file_url) {
                            window.open(r.message.file_url, '_blank');
                        }
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message.message || __('Failed to generate QR code'),
                            indicator: 'red'
                        });
                    }
                }
            });
            dialog.hide();
        }
    });
    dialog.show();
};

// Check and inject when navigating to a form
frappe.qr_suite.check_and_inject = function() {
    if (window.cur_frm && cur_frm.doctype) {
        const doctype = cur_frm.doctype;
        
        // If settings not loaded, load them
        if (!frappe.qr_suite.settings_loaded) {
            frappe.qr_suite.load_settings();
            return;
        }
        
        // Check if this doctype is enabled and not yet injected
        if (frappe.qr_suite.enabled_doctypes.includes(doctype) && 
            !frappe.qr_suite.injected_doctypes.has(doctype)) {
            frappe.qr_suite.inject_for_doctype(doctype);
            
            // Trigger refresh to show buttons immediately
            setTimeout(() => {
                if (cur_frm && cur_frm.doctype === doctype) {
                    cur_frm.trigger('refresh');
                }
            }, 100);
        }
    }
};

// Initialize on page load
frappe.ready(function() {
    console.log('QR Suite: Ready, loading settings...');
    frappe.qr_suite.load_settings();
});

// Monitor route changes
frappe.router.on('change', () => {
    setTimeout(() => {
        frappe.qr_suite.check_and_inject();
    }, 500);
});

// Also monitor form loads
$(document).on('form-refresh', function() {
    frappe.qr_suite.check_and_inject();
});

// Periodically check for new forms (failsafe)
setInterval(() => {
    if (window.cur_frm && cur_frm.doctype && !cur_frm.is_new()) {
        frappe.qr_suite.check_and_inject();
    }
}, 2000);

console.log('QR Suite: Enhanced injector loaded');
