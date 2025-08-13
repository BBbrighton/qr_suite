// Debug script to check QR Suite loading
console.log("=== QR Suite Debug Info ===");

// Check if frappe.qr_suite exists
if (typeof frappe !== 'undefined' && frappe.qr_suite) {
    console.log("✓ frappe.qr_suite is loaded");
    
    // Check settings
    console.log("Settings loaded:", frappe.qr_suite.settings_loaded);
    console.log("Enabled doctypes:", frappe.qr_suite.enabled_doctypes);
    
    // Check current form
    if (typeof cur_frm !== 'undefined' && cur_frm) {
        console.log("Current form doctype:", cur_frm.doctype);
        console.log("Is enabled:", frappe.qr_suite.enabled_doctypes.includes(cur_frm.doctype));
        console.log("Buttons added:", cur_frm.qr_suite_buttons_added);
    }
} else {
    console.log("✗ frappe.qr_suite NOT loaded");
}

// Check if qr_injector.js is loaded
if (document.querySelector('script[src*="qr_injector.js"]')) {
    console.log("✓ qr_injector.js is in DOM");
} else {
    console.log("✗ qr_injector.js NOT in DOM");
}

// Try to manually trigger button addition
if (typeof frappe !== 'undefined' && frappe.qr_suite && frappe.qr_suite.add_buttons && cur_frm) {
    console.log("Manually triggering button addition...");
    frappe.qr_suite.add_buttons(cur_frm);
}

console.log("=== End Debug Info ===");
