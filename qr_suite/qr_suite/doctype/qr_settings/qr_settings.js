frappe.ui.form.on('QR Settings', {
    refresh: function(frm) {
        // Update counts
        frm.trigger('update_counts');
        
        // Add custom button for smart sync
        frm.add_custom_button(__('Sync Relevant DocTypes'), function() {
            frappe.confirm(
                __('This will add commonly used DocTypes that make sense for QR codes. Continue?'),
                function() {
                    frm.call('sync_doctypes').then(r => {
                        frm.reload_doc();
                    });
                }
            );
        }, __('Actions'));
        
        // Add button to enable all
        frm.add_custom_button(__('Enable All'), function() {
            frm.doc.doctype_settings.forEach(row => {
                if (!row.is_hardcoded || row.is_hardcoded === 0) {
                    frappe.model.set_value(row.doctype, row.name, 'is_enabled', 1);
                }
            });
            frm.trigger('update_counts');
        }, __('Actions'));
        
        // Add button to disable non-hardcoded
        frm.add_custom_button(__('Disable Non-Essential'), function() {
            frm.doc.doctype_settings.forEach(row => {
                if (!row.is_hardcoded || row.is_hardcoded === 0) {
                    frappe.model.set_value(row.doctype, row.name, 'is_enabled', 0);
                }
            });
            frm.trigger('update_counts');
        }, __('Actions'));
    },
    
    update_counts: function(frm) {
        let total = frm.doc.doctype_settings ? frm.doc.doctype_settings.length : 0;
        let enabled = frm.doc.doctype_settings ? frm.doc.doctype_settings.filter(d => d.is_enabled).length : 0;
        
        frm.set_value('total_doctypes', total);
        frm.set_value('enabled_count', enabled);
    },
    
    add_selected_doctype: function(frm) {
        if (!frm.doc.add_doctype_name) {
            frappe.msgprint(__('Please select a DocType to add'));
            return;
        }
        
        frm.call({
            method: 'add_custom_doctype',
            args: {
                doctype_name: frm.doc.add_doctype_name
            },
            callback: function(r) {
                frm.set_value('add_doctype_name', '');
                frm.reload_doc();
            }
        });
    },
    
    sync_now: function(frm) {
        frm.call('sync_doctypes').then(r => {
            frm.reload_doc();
        });
    }
});

frappe.ui.form.on('QR Settings Detail', {
    is_enabled: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.is_hardcoded && !row.is_enabled) {
            frappe.msgprint(__('Cannot disable hardcoded DocType: {0}', [row.doctype_name]));
            frappe.model.set_value(cdt, cdn, 'is_enabled', 1);
        }
        frm.trigger('update_counts');
    },
    
    doctype_settings_add: function(frm) {
        frm.trigger('update_counts');
    },
    
    doctype_settings_remove: function(frm) {
        frm.trigger('update_counts');
    }
});
