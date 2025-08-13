// QR Suite DocType Integration - Self-contained version with Full Template Support
frappe.ui.form.on(cur_frm.doctype, {
    refresh: function(frm) {
        // Skip if new document
        if (!frm.doc || frm.is_new() || frm.doc.__islocal) {
            return;
        }
        
        // Skip if already added
        if (frm.qr_suite_buttons_added) {
            return;
        }
        
        // Mark as added to prevent duplicate buttons
        frm.qr_suite_buttons_added = true;
        
        // Check permission before adding buttons
        frappe.call({
            method: 'qr_suite.api.check_qr_permission',
            args: {
                doctype: frm.doctype
            },
            callback: function(r) {
                if (r.message) {
                    // Add Generate QR button
                    frm.add_custom_button(__('Generate QR Code'), function() {
                        show_qr_dialog(frm);
                    }, __('QR Suite'));
                    
                    // Add View QR Codes button
                    frm.add_custom_button(__('View QR Codes'), function() {
                        frappe.set_route('List', 'QR Link', {
                            target_doctype: frm.doctype,
                            target_name: frm.doc.name
                        });
                    }, __('QR Suite'));
                    
                    console.log('QR Suite: Buttons added for', frm.doctype, frm.doc.name);
                } else {
                    console.log('QR Suite: No permission for', frm.doctype);
                }
            },
            error: function(r) {
                console.error('QR Suite: Permission check failed', r);
            }
        });
    }
});

// QR Generation Dialog with Full Template Support
function show_qr_dialog(frm) {
    let d = new frappe.ui.Dialog({
        title: __('Generate QR Code'),
        fields: [
            {
                label: __('QR Template'),
                fieldname: 'qr_template',
                fieldtype: 'Link',
                options: 'QR Template',
                get_query: function() {
                    return {
                        filters: {
                            'is_active': 1,
                            'target_doctype': ['in', ['', frm.doctype]]
                        }
                    }
                },
                onchange: function() {
                    let template_name = d.get_value('qr_template');
                    if (template_name) {
                        // Load template settings
                        frappe.db.get_doc('QR Template', template_name).then(template => {
                            // Apply ALL template settings to dialog fields
                            d.set_value('qr_type', template.qr_type);
                            
                            if (template.qr_type === 'Document QR') {
                                // Apply Document QR specific settings
                                d.set_value('action', template.default_action || 'view');
                                d.set_value('url_mode', template.url_mode || 'token');
                                
                                // Set expiry based on template
                                if (template.token_expiry_days && template.token_expiry_days > 0) {
                                    let expiry = frappe.datetime.add_days(frappe.datetime.now_datetime(), template.token_expiry_days);
                                    d.set_value('expires_on', expiry);
                                } else {
                                    d.set_value('expires_on', '');
                                }
                                
                                // Apply advanced settings
                                d.set_value('custom_url_prefix', template.custom_url_prefix || '');
                                d.set_value('extra_params', template.extra_params || '');
                            } else if (template.qr_type === 'Value QR') {
                                // Apply Value QR specific settings
                                if (template.value_field) {
                                    d.set_value('value_source', 'Field');
                                    d.set_value('value_field', template.value_field);
                                } else {
                                    d.set_value('value_source', 'Document Name');
                                }
                            }
                            
                            // Apply QR appearance settings
                            d.set_value('qr_size', template.qr_size || 'Medium');
                            d.set_value('error_correction', template.error_correction || 'M');
                            d.set_value('image_format', template.image_format || 'PNG');
                            d.set_value('include_label', template.include_readable_text || 1);
                            
                            frappe.show_alert({
                                message: __('Template settings applied. You can modify them as needed.'),
                                indicator: 'blue'
                            }, 3);
                        });
                    }
                },
                description: __('Select a template to pre-fill settings (optional)')
            },
            {
                fieldname: 'template_section_break',
                fieldtype: 'Section Break'
            },
            {
                label: __('QR Type'),
                fieldname: 'qr_type',
                fieldtype: 'Select',
                options: 'Document QR\nValue QR',
                default: 'Document QR',
                reqd: 1,
                onchange: function() {
                    let qr_type = d.get_value('qr_type');
                    // Toggle field visibility based on QR type
                    d.fields_dict.action.df.hidden = (qr_type !== 'Document QR');
                    d.fields_dict.url_mode.df.hidden = (qr_type !== 'Document QR');
                    d.fields_dict.expires_on.df.hidden = (qr_type !== 'Document QR');
                    d.fields_dict.custom_url_prefix.df.hidden = (qr_type !== 'Document QR');
                    d.fields_dict.extra_params.df.hidden = (qr_type !== 'Document QR');
                    
                    d.fields_dict.value_source.df.hidden = (qr_type !== 'Value QR');
                    d.fields_dict.value_field.df.hidden = (qr_type !== 'Value QR' || d.get_value('value_source') !== 'Field');
                    d.fields_dict.custom_value.df.hidden = (qr_type !== 'Value QR' || d.get_value('value_source') !== 'Custom');
                    d.refresh();
                }
            },
            {
                label: __('Action'),
                fieldname: 'action',
                fieldtype: 'Select',
                options: 'view\nedit\nprint\nemail\nnew_stock_entry\nmaintenance_log\nasset_repair\nstock_balance\nview_ledger\nnew_delivery_note\nnew_sales_invoice\nnew_purchase_receipt',
                default: 'view',
                depends_on: "eval:doc.qr_type === 'Document QR'"
            },
            {
                label: __('URL Mode'),
                fieldname: 'url_mode',
                fieldtype: 'Select',
                options: 'token\ndirect',
                default: 'token',
                depends_on: "eval:doc.qr_type === 'Document QR'",
                description: __('Token: Secure URL with token. Direct: Full URL in QR')
            },
            {
                label: __('Expires On'),
                fieldname: 'expires_on',
                fieldtype: 'Datetime',
                depends_on: "eval:doc.qr_type === 'Document QR' && doc.url_mode === 'token'",
                description: __('Leave empty for no expiration')
            },
            {
                label: __('Custom URL Prefix'),
                fieldname: 'custom_url_prefix',
                fieldtype: 'Data',
                depends_on: "eval:doc.qr_type === 'Document QR' && doc.url_mode === 'direct'",
                description: __('Custom domain/prefix instead of site URL')
            },
            {
                label: __('Extra Parameters'),
                fieldname: 'extra_params',
                fieldtype: 'Small Text',
                depends_on: "eval:doc.qr_type === 'Document QR'",
                description: __('Additional URL parameters in JSON format')
            },
            {
                label: __('Value Source'),
                fieldname: 'value_source',
                fieldtype: 'Select',
                options: 'Document Name\nField\nCustom',
                default: 'Document Name',
                hidden: 1,
                onchange: function() {
                    let source = d.get_value('value_source');
                    d.fields_dict.value_field.df.hidden = (source !== 'Field');
                    d.fields_dict.custom_value.df.hidden = (source !== 'Custom');
                    d.refresh();
                }
            },
            {
                label: __('Field'),
                fieldname: 'value_field',
                fieldtype: 'Select',
                hidden: 1,
                get_query: function() {
                    // Get fields from current doctype
                    frappe.call({
                        method: 'qr_suite.api.get_doctype_fields',
                        args: { doctype: frm.doctype },
                        callback: function(r) {
                            if (r.message) {
                                let options = [''];
                                r.message.forEach(field => {
                                    options.push(field.fieldname);
                                });
                                d.fields_dict.value_field.df.options = options.join('\n');
                                d.refresh();
                            }
                        }
                    });
                }
            },
            {
                label: __('Custom Value'),
                fieldname: 'custom_value',
                fieldtype: 'Data',
                hidden: 1
            },
            {
                fieldname: 'appearance_section_break',
                fieldtype: 'Section Break',
                label: __('QR Code Appearance')
            },
            {
                label: __('QR Size'),
                fieldname: 'qr_size',
                fieldtype: 'Select',
                options: 'Small\nMedium\nLarge',
                default: 'Medium'
            },
            {
                label: __('Error Correction'),
                fieldname: 'error_correction',
                fieldtype: 'Select',
                options: 'L\nM\nQ\nH',
                default: 'M',
                description: __('L=7%, M=15%, Q=25%, H=30% error correction')
            },
            {
                label: __('Image Format'),
                fieldname: 'image_format',
                fieldtype: 'Select',
                options: 'PNG\nJPEG',
                default: 'PNG'
            },
            {
                label: __('Include Label'),
                fieldname: 'include_label',
                fieldtype: 'Check',
                default: 1
            },
            {
                label: __('Label Text'),
                fieldname: 'label_text',
                fieldtype: 'Data',
                default: frm.doc.name,
                depends_on: 'include_label'
            },
            {
                fieldname: 'advanced_section',
                fieldtype: 'Section Break',
                collapsible: 1,
                label: __('Save Template'),
                collapsible_depends_on: 'eval:!doc.save_as_template'
            },
            {
                label: __('Save as New Template'),
                fieldname: 'save_as_template',
                fieldtype: 'Check',
                default: 0,
                description: __('Save these settings as a new template for future use')
            },
            {
                label: __('New Template Name'),
                fieldname: 'new_template_name',
                fieldtype: 'Data',
                depends_on: 'save_as_template',
                mandatory_depends_on: 'save_as_template'
            }
        ],
        primary_action_label: __('Generate'),
        primary_action(values) {
            // Save as template if requested
            if (values.save_as_template && values.new_template_name) {
                save_as_template(frm, values);
            }
            
            // Prepare args based on QR type - include ALL settings
            let args = {
                doctype: frm.doctype,
                docname: frm.doc.name,
                qr_type: values.qr_type,
                qr_template: values.qr_template,
                include_label: values.include_label,
                label_text: values.label_text,
                // Include appearance settings
                qr_size: values.qr_size,
                error_correction: values.error_correction,
                image_format: values.image_format
            };
            
            if (values.qr_type === 'Document QR') {
                args.action = values.action;
                args.url_mode = values.url_mode;
                if (values.expires_on) {
                    args.expires_on = values.expires_on;
                }
                if (values.custom_url_prefix) {
                    args.custom_url_prefix = values.custom_url_prefix;
                }
                if (values.extra_params) {
                    args.extra_params = values.extra_params;
                }
            } else {
                if (values.value_source === 'Field' && values.value_field) {
                    args.value_field = values.value_field;
                } else if (values.value_source === 'Custom' && values.custom_value) {
                    args.custom_value = values.custom_value;
                }
            }
            
            frappe.call({
                method: 'qr_suite.api.generate_qr_code',
                args: args,
                callback: function(r) {
                    if (r.message && r.message.success) {
                        d.hide();
                        
                        // Show success message with preview
                        let msg = r.message.message;
                        if (r.message.file_url) {
                            msg += '<br><br><img src="' + r.message.file_url + '" style="max-width: 200px;">';
                        }
                        
                        frappe.msgprint({
                            title: __('QR Code Generated'),
                            message: msg,
                            indicator: 'green'
                        });
                        
                        // Refresh form to show new QR code
                        frm.reload_doc();
                    } else {
                        frappe.msgprint({
                            title: __('Error'),
                            message: r.message.message || __('Failed to generate QR code'),
                            indicator: 'red'
                        });
                    }
                },
                error: function(r) {
                    frappe.msgprint({
                        title: __('Error'),
                        message: __('Failed to generate QR code'),
                        indicator: 'red'
                    });
                }
            });
        },
        secondary_action_label: __('Cancel')
    });
    
    // Load fields if Value QR is selected
    if (d.get_value('qr_type') === 'Value QR') {
        frappe.call({
            method: 'qr_suite.api.get_doctype_fields',
            args: { doctype: frm.doctype },
            callback: function(r) {
                if (r.message) {
                    let options = [''];
                    r.message.forEach(field => {
                        options.push(field.fieldname);
                    });
                    d.fields_dict.value_field.df.options = options.join('\n');
                    d.refresh();
                }
            }
        });
    }
    
    d.show();
}

// Save current settings as a new template
function save_as_template(frm, values) {
    let template_data = {
        doctype: 'QR Template',
        template_name: values.new_template_name,
        description: __('Template for {0}', [frm.doctype]),
        is_active: 1,
        qr_type: values.qr_type,
        target_doctype: frm.doctype,
        include_readable_text: values.include_label,
        // Save appearance settings
        qr_size: values.qr_size,
        error_correction: values.error_correction,
        image_format: values.image_format
    };
    
    if (values.qr_type === 'Document QR') {
        template_data.default_action = values.action;
        template_data.url_mode = values.url_mode;
        if (values.expires_on) {
            // Calculate days from today
            let days = frappe.datetime.get_day_diff(values.expires_on, frappe.datetime.now_datetime());
            template_data.token_expiry_days = Math.max(0, days);
        }
        if (values.custom_url_prefix) {
            template_data.custom_url_prefix = values.custom_url_prefix;
        }
        if (values.extra_params) {
            template_data.extra_params = values.extra_params;
        }
    } else if (values.qr_type === 'Value QR') {
        if (values.value_source === 'Field' && values.value_field) {
            template_data.value_field = values.value_field;
        }
    }
    
    frappe.db.insert(template_data).then(doc => {
        frappe.show_alert({
            message: __('Template "{0}" saved successfully', [doc.template_name]),
            indicator: 'green'
        }, 5);
    }).catch(err => {
        frappe.msgprint({
            title: __('Error'),
            message: __('Failed to save template: {0}', [err.message]),
            indicator: 'red'
        });
    });
}

console.log('QR Suite: DocType integration loaded for', cur_frm.doctype);
