frappe.ui.form.on('QR Link', {
    setup: function(frm) {
        // Set up queries and filters
        frm.set_query('qr_template', function() {
            return {
                filters: {
                    'is_active': 1
                }
            };
        });
    },
    
    onload: function(frm) {
        // Set defaults for new QR Links
        if (frm.is_new()) {
            frm.set_value('status', 'Active');
            frm.set_value('qr_type', 'Document QR');
            frm.set_value('url_mode', 'token');
            frm.set_value('action', 'view');
            frm.set_value('include_label', 1);
            
            // Trigger visibility update
            frm.trigger('update_field_visibility');
        }
    },
    
    refresh: function(frm) {
        // Update field visibility on refresh
        frm.trigger('update_field_visibility');
        
        // Add Generate QR Image button
        if (!frm.doc.__islocal && !frm.doc.qr_code_image) {
            frm.add_custom_button(__('Generate QR Image'), function() {
                frm.trigger('generate_qr_image');
            }, __('Actions'));
        }
        
        // Add Regenerate button if QR image exists
        if (frm.doc.qr_code_image) {
            frm.add_custom_button(__('Regenerate QR'), function() {
                frappe.confirm('This will create a new QR image. Continue?', function() {
                    frm.trigger('generate_qr_image');
                });
            }, __('Actions'));
            
            frm.add_custom_button(__('Download QR'), function() {
                window.open(frm.doc.qr_code_image, '_blank');
            }, __('Actions'));
        }
        
        // Add Revoke button for active QR codes
        if (frm.doc.status === 'Active' && !frm.doc.__islocal) {
            frm.add_custom_button(__('Revoke QR'), function() {
                frappe.confirm(
                    'Are you sure you want to revoke this QR code? This action cannot be undone.',
                    function() {
                        frappe.call({
                            method: 'revoke',
                            doc: frm.doc,
                            callback: function(r) {
                                if (!r.exc) {
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Actions'));
        }
        
        // Add Test button if URL exists
        if (frm.doc.qr_url) {
            frm.add_custom_button(__('Test QR URL'), function() {
                window.open(frm.doc.qr_url, '_blank');
            }, __('Actions'));
        }
        
        // Set status indicator
        if (frm.doc.status) {
            let indicator_map = {
                'Active': 'green',
                'Expired': 'red',
                'Revoked': 'red',
                'Inactive': 'grey'
            };
            let color = indicator_map[frm.doc.status] || 'grey';
            frm.dashboard.set_headline(
                `<span class="indicator ${color}">${frm.doc.status} QR Code</span>`
            );
        }
    },
    
    qr_template: function(frm) {
        // Apply template settings
        if (frm.doc.qr_template) {
            frappe.db.get_doc('QR Template', frm.doc.qr_template).then(template => {
                // Apply template settings
                frm.set_value('qr_type', template.qr_type);
                
                if (template.qr_type === 'Document QR') {
                    frm.set_value('action', template.default_action || 'view');
                    frm.set_value('url_mode', template.url_mode || 'token');
                    
                    if (template.token_expiry_days && template.token_expiry_days > 0) {
                        let expiry = frappe.datetime.add_days(frappe.datetime.now_datetime(), template.token_expiry_days);
                        frm.set_value('expires_on', expiry);
                    }
                    
                    if (template.custom_url_prefix) {
                        frm.set_value('custom_url_prefix', template.custom_url_prefix);
                    }
                    
                    if (template.extra_params) {
                        frm.set_value('extra_params', template.extra_params);
                    }
                }
                
                // Apply appearance settings
                frm.set_value('include_label', template.include_readable_text);
                
                frappe.show_alert({
                    message: __('Template settings applied'),
                    indicator: 'green'
                }, 3);
                
                // Update visibility
                frm.trigger('update_field_visibility');
            });
        }
    },
    
    qr_type: function(frm) {
        // Update visibility and set defaults based on QR type
        frm.trigger('update_field_visibility');
        
        // Clear inappropriate fields when switching types
        if (frm.doc.qr_type === 'Value QR') {
            frm.set_value('action', '');
            frm.set_value('url_mode', '');
            frm.set_value('expires_on', '');
            frm.set_value('custom_url_prefix', '');
            frm.set_value('extra_params', '');
        } else if (frm.doc.qr_type === 'Document QR') {
            frm.set_value('qr_content', '');
            if (!frm.doc.action) {
                frm.set_value('action', 'view');
            }
            if (!frm.doc.url_mode) {
                frm.set_value('url_mode', 'token');
            }
        }
    },
    
    url_mode: function(frm) {
        // Update visibility based on URL mode
        frm.trigger('update_field_visibility');
        
        // Clear inappropriate fields
        if (frm.doc.url_mode === 'direct') {
            frm.set_value('expires_on', '');
        } else if (frm.doc.url_mode === 'token') {
            frm.set_value('custom_url_prefix', '');
        }
    },
    
    target_doctype: function(frm) {
        // Clear target name when doctype changes
        if (frm.doc.target_doctype) {
            frm.set_value('target_name', '');
        }
    },
    
    target_name: function(frm) {
        // Auto-set label text if not manually set
        if (frm.doc.target_name && !frm.doc.label_text) {
            frm.set_value('label_text', frm.doc.target_name);
        }
    },
    
    extra_params: function(frm) {
        // Validate JSON format
        if (frm.doc.extra_params) {
            try {
                JSON.parse(frm.doc.extra_params);
                frm.set_df_property('extra_params', 'description', 'Valid JSON');
            } catch (e) {
                frm.set_df_property('extra_params', 'description', 
                    '<span style="color:red">Invalid JSON format. Example: {"ref": "qr", "campaign": "2024"}</span>');
            }
        }
    },
    
    update_field_visibility: function(frm) {
        // Central function to manage field visibility
        let is_document_qr = frm.doc.qr_type === 'Document QR';
        let is_value_qr = frm.doc.qr_type === 'Value QR';
        let is_token_mode = frm.doc.url_mode === 'token';
        let is_direct_mode = frm.doc.url_mode === 'direct';
        
        // Document QR fields
        frm.toggle_display('action', is_document_qr);
        frm.toggle_display('url_mode', is_document_qr);
        frm.toggle_reqd('action', is_document_qr);
        
        // URL mode dependent fields
        frm.toggle_display('expires_on', is_document_qr && is_token_mode);
        frm.toggle_display('custom_url_prefix', is_document_qr && is_direct_mode);
        frm.toggle_display('extra_params', is_document_qr);
        
        // Value QR fields
        frm.toggle_display('qr_content', is_value_qr);
        frm.toggle_reqd('qr_content', is_value_qr);
        
        // Label fields
        frm.toggle_display('label_text', frm.doc.include_label);
        
        // Refresh field area
        frm.refresh_fields();
    },
    
    generate_qr_image: function(frm) {
        // Generate QR image
        frappe.call({
            method: 'generate_qr_image',
            doc: frm.doc,
            freeze: true,
            freeze_message: __('Generating QR Code...'),
            callback: function(r) {
                if (!r.exc) {
                    frm.reload_doc();
                    frappe.show_alert({
                        message: __('QR Code generated successfully'),
                        indicator: 'green'
                    }, 5);
                }
            }
        });
    },
    
    validate: function(frm) {
        // Validation before save
        
        // Validate QR type specific requirements
        if (frm.doc.qr_type === 'Document QR') {
            if (!frm.doc.action) {
                frappe.msgprint(__('Please select an Action for Document QR'));
                frappe.validated = false;
                return;
            }
            if (!frm.doc.url_mode) {
                frappe.msgprint(__('Please select URL Mode for Document QR'));
                frappe.validated = false;
                return;
            }
        } else if (frm.doc.qr_type === 'Value QR') {
            if (!frm.doc.qr_content) {
                frappe.msgprint(__('Please enter QR Content for Value QR'));
                frappe.validated = false;
                return;
            }
        }
        
        // Validate JSON in extra_params
        if (frm.doc.extra_params) {
            try {
                JSON.parse(frm.doc.extra_params);
            } catch (e) {
                frappe.msgprint(__('Extra Parameters must be valid JSON format'));
                frappe.validated = false;
                return;
            }
        }
        
        // Auto-set label text if empty
        if (frm.doc.include_label && !frm.doc.label_text) {
            frm.set_value('label_text', frm.doc.target_name || 'QR Code');
        }
    },
    
    after_save: function(frm) {
        // Show message to generate QR if not generated
        if (!frm.doc.qr_code_image) {
            frappe.msgprint({
                message: __('QR Link saved. Click "Generate QR Image" to create the QR code.'),
                indicator: 'blue',
                title: __('Generate QR Code')
            });
        }
    }
});
