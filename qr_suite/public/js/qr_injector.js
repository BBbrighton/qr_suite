// QR Suite Universal Injector - Clean Unified Version
console.log('QR Suite: Loading universal injector...');

frappe.provide('frappe.qr_suite');

// Initialize
frappe.qr_suite.initialized = false;
frappe.qr_suite.enabled_doctypes = [];
frappe.qr_suite.enabled_map = {}; // For faster lookup
frappe.qr_suite.user_has_permission = false;

// Load settings once
frappe.qr_suite.init = function() {
    if (frappe.qr_suite.initialized) return;
    
    console.log('QR Suite: Initializing...');
    
    // Load enabled doctypes
    frappe.call({
        method: 'qr_suite.api.get_enabled_doctypes',
        callback: function(r) {
            if (r.message) {
                frappe.qr_suite.enabled_doctypes = r.message.map(dt => dt.name);
                // Create map for faster lookup
                r.message.forEach(dt => {
                    frappe.qr_suite.enabled_map[dt.name] = dt;
                });
                console.log('QR Suite: Loaded enabled doctypes:', frappe.qr_suite.enabled_doctypes);
            }
        }
    });
    
    // Check user permission once
    if (frappe.user_roles.includes('System Manager') || 
        frappe.user_roles.includes('QR Manager') || 
        frappe.user_roles.includes('QR User')) {
        frappe.qr_suite.user_has_permission = true;
    }
    
    frappe.qr_suite.initialized = true;
};

// Add buttons to form
frappe.qr_suite.add_buttons = function(frm) {
    // Skip if new document
    if (!frm || !frm.doc || frm.is_new() || frm.doc.__islocal) {
        return;
    }
    
    // Skip if already added (by any method)
    if (frm.qr_suite_buttons_added || frm.qr_suite_dynamic_buttons_added) {
        return;
    }
    
    // Skip if user has no permission
    if (!frappe.qr_suite.user_has_permission) {
        return;
    }
    
    // Check if doctype is enabled
    if (!frappe.qr_suite.enabled_doctypes.includes(frm.doctype)) {
        return;
    }
    
    // Double-check permission for this specific doctype
    frappe.call({
        method: 'qr_suite.api.check_qr_permission',
        args: { doctype: frm.doctype },
        callback: function(r) {
            if (r.message && !frm.qr_suite_buttons_added && !frm.qr_suite_dynamic_buttons_added) {
                // Mark as added
                frm.qr_suite_buttons_added = true;
                
                // Add Generate QR button
                frm.add_custom_button(__('Generate QR Code'), function() {
                    frappe.qr_suite.show_qr_dialog(frm);
                }, __('QR Suite'));
                
                // Add View QR Codes button
                frm.add_custom_button(__('View QR Codes'), function() {
                    frappe.set_route('List', 'QR Link', {
                        target_doctype: frm.doctype,
                        target_name: frm.doc.name
                    });
                }, __('QR Suite'));
                
                console.log(`QR Suite: Buttons dynamically added for ${frm.doctype}`);
            }
        }
    });
};

// QR Dialog function
frappe.qr_suite.show_qr_dialog = function(frm) {
    // Get available fields for value QR
    const fields = frm.meta.fields
        .filter(df => ['Data', 'Link', 'Select', 'Int', 'Float', 'Currency', 'Barcode'].includes(df.fieldtype) && !df.hidden)
        .map(df => ({ label: df.label, value: df.fieldname }));
    
    const dialog = new frappe.ui.Dialog({
        title: __('Generate QR Code'),
        fields: [
            {
                fieldtype: 'HTML',
                options: `
                    <div class="alert alert-info">
                        <p><strong>Generate QR Code for ${frm.doctype}: ${frm.doc.name}</strong></p>
                    </div>
                `
            },
            {
                fieldname: 'qr_type',
                fieldtype: 'Select',
                label: 'QR Type',
                options: 'Document QR\nValue QR',
                default: 'Document QR',
                reqd: 1,
                change: function() {
                    const qr_type = dialog.get_value('qr_type');
                    dialog.fields_dict.action.df.hidden = qr_type !== 'Document QR';
                    dialog.fields_dict.value_field.df.hidden = qr_type !== 'Value QR';
                    dialog.fields_dict.custom_value.df.hidden = qr_type !== 'Value QR';
                    dialog.refresh();
                }
            },
            {
                fieldname: 'qr_template',
                fieldtype: 'Link',
                label: 'QR Template',
                options: 'QR Template',
                description: 'Optional: Use a template for settings'
            },
            {
                fieldtype: 'Section Break'
            },
            {
                fieldname: 'action',
                fieldtype: 'Select',
                label: 'Action',
                options: [
                    'view',
                    'edit',
                    'print',
                    'email',
                    'new_stock_entry',
                    'maintenance_log',
                    'asset_repair',
                    'stock_balance',
                    'view_ledger',
                    'new_delivery_note',
                    'new_sales_invoice',
                    'new_purchase_receipt'
                ].join('\n'),
                default: frappe.qr_suite.enabled_map[frm.doctype]?.default_action || 'view',
                depends_on: "eval:doc.qr_type=='Document QR'",
                description: 'What should happen when QR is scanned'
            },
            {
                fieldname: 'value_field',
                fieldtype: 'Select',
                label: 'Value Field',
                options: fields.map(f => f.value).join('\n'),
                depends_on: "eval:doc.qr_type=='Value QR'",
                description: 'Which field value to encode',
                change: function() {
                    const field = dialog.get_value('value_field');
                    if (field && frm.doc[field]) {
                        dialog.set_value('custom_value', frm.doc[field]);
                    }
                }
            },
            {
                fieldname: 'custom_value',
                fieldtype: 'Data',
                label: 'Custom Value',
                depends_on: "eval:doc.qr_type=='Value QR'",
                description: 'Override the value to encode',
                default: frm.doc.name
            },
            {
                fieldtype: 'Section Break',
                label: 'Advanced Options'
            },
            {
                fieldname: 'include_label',
                fieldtype: 'Check',
                label: 'Include Label on QR',
                default: 0,
                description: 'Add text label below QR code'
            },
            {
                fieldname: 'label_text',
                fieldtype: 'Data',
                label: 'Label Text',
                depends_on: 'include_label',
                description: 'Text to show below QR (leave empty for document name)'
            },
            {
                fieldname: 'expires_on',
                fieldtype: 'Datetime',
                label: 'Expires On',
                depends_on: "eval:doc.qr_type=='Document QR'",
                description: 'Optional: Set expiry for Document QR'
            }
        ],
        primary_action_label: __('Generate'),
        primary_action: function(values) {
            frappe.qr_suite.generate_qr_code(frm, values);
            dialog.hide();
        }
    });
    
    dialog.show();
};

// Generate QR Code
frappe.qr_suite.generate_qr_code = function(frm, values) {
    const args = {
        doctype: frm.doctype,
        docname: frm.doc.name,
        qr_type: values.qr_type,
        qr_template: values.qr_template
    };
    
    // Add type-specific args
    if (values.qr_type === 'Document QR') {
        args.action = values.action || 'view';
        args.expires_on = values.expires_on;
    } else if (values.qr_type === 'Value QR') {
        if (values.custom_value) {
            args.custom_value = values.custom_value;
        } else if (values.value_field && frm.doc[values.value_field]) {
            args.value_field = values.value_field;
            args.custom_value = frm.doc[values.value_field];
        } else {
            args.custom_value = frm.doc.name;
        }
    }
    
    // Add label options
    if (values.include_label) {
        args.include_label = 1;
        args.label_text = values.label_text || frm.doc.name;
    }
    
    frappe.call({
        method: 'qr_suite.api.generate_qr_code',
        args: args,
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
                
                if (r.message.qr_link) {
                    frappe.msgprint({
                        title: __('QR Code Generated'),
                        message: __('QR Code has been generated successfully.'),
                        primary_action: {
                            label: __('View QR Link'),
                            action: function() {
                                frappe.set_route('Form', 'QR Link', r.message.qr_link);
                            }
                        }
                    });
                }
            } else {
                frappe.msgprint({
                    title: __('Error'),
                    message: r.message.message || __('Failed to generate QR code'),
                    indicator: 'red'
                });
            }
        },
        error: function(r) {
            console.error('QR generation error:', r);
            frappe.msgprint({
                title: __('Error'),
                message: __('An error occurred while generating the QR code'),
                indicator: 'red'
            });
        }
    });
};

// MAIN HOOK: Override the form refresh handler
$(document).ready(function() {
    // Initialize QR Suite
    frappe.qr_suite.init();
    
    // Method 1: Hook into form refresh prototype
    if (frappe.ui.form.Form) {
        const original_refresh = frappe.ui.form.Form.prototype.refresh;
        frappe.ui.form.Form.prototype.refresh = function() {
            // Call original refresh
            original_refresh.apply(this, arguments);
            
            // Add QR buttons if applicable
            if (this.doctype && this.doc && !this.is_new()) {
                frappe.qr_suite.add_buttons(this);
            }
        };
        console.log('QR Suite: Hooked into Form.refresh');
    }
    
    // Method 2: Listen to form events (backup)
    $(document).on('form-refresh', function(e, frm) {
        if (frm && frm.doctype && frm.doc && !frm.is_new()) {
            frappe.qr_suite.add_buttons(frm);
        }
    });
    
    // Method 3: Monitor route changes (another backup)
    frappe.router.on('change', function() {
        setTimeout(function() {
            if (window.cur_frm && cur_frm.doctype && cur_frm.doc && !cur_frm.is_new()) {
                frappe.qr_suite.add_buttons(cur_frm);
            }
        }, 1000);
    });
});

// Also make functions available globally for hardcoded doctypes compatibility
window.show_qr_dialog = frappe.qr_suite.show_qr_dialog;
window.generate_qr_code = frappe.qr_suite.generate_qr_code;

console.log('QR Suite: Universal injector loaded successfully');
