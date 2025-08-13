import frappe

def execute():
    """Add missing fields to QR Link doctype"""
    
    # Check if QR Link doctype exists
    if not frappe.db.exists("DocType", "QR Link"):
        return
    
    # Check if table exists
    if not frappe.db.table_exists("QR Link"):
        return
    
    # Fields to add if they don't exist
    fields_to_add = [
        {
            "fieldname": "url_mode",
            "fieldtype": "Select",
            "label": "URL Mode",
            "options": "token\ndirect",
            "default": "token"
        },
        {
            "fieldname": "custom_url_prefix",
            "fieldtype": "Data",
            "label": "Custom URL Prefix"
        },
        {
            "fieldname": "extra_params",
            "fieldtype": "Small Text",
            "label": "Extra Parameters"
        },
        {
            "fieldname": "include_label",
            "fieldtype": "Check",
            "label": "Include Label",
            "default": 1
        },
        {
            "fieldname": "label_text",
            "fieldtype": "Data", 
            "label": "Label Text"
        }
    ]
    
    # Get existing columns
    existing_columns = frappe.db.get_table_columns("QR Link")
    
    # Add missing fields
    for field in fields_to_add:
        if field["fieldname"] not in existing_columns:
            try:
                # Add field to database
                frappe.db.sql(f"""
                    ALTER TABLE `tabQR Link` 
                    ADD COLUMN `{field['fieldname']}` {get_column_type(field['fieldtype'])}
                """)
                
                # Set default value if specified
                if "default" in field:
                    default_value = field["default"]
                    if field["fieldtype"] == "Check":
                        default_value = 1 if default_value else 0
                        
                    frappe.db.sql(f"""
                        UPDATE `tabQR Link` 
                        SET `{field['fieldname']}` = %s
                        WHERE `{field['fieldname']}` IS NULL
                    """, (default_value,))
                    
                print(f"Added field: {field['fieldname']}")
            except Exception as e:
                print(f"Error adding field {field['fieldname']}: {str(e)}")
    
    # Commit changes
    frappe.db.commit()
    
    # Clear cache
    frappe.clear_cache(doctype="QR Link")
    
    print("QR Link fields update completed")

def get_column_type(fieldtype):
    """Get MySQL column type for frappe fieldtype"""
    type_map = {
        "Select": "VARCHAR(140)",
        "Data": "VARCHAR(140)", 
        "Small Text": "TEXT",
        "Check": "INT(1) DEFAULT 0"
    }
    return type_map.get(fieldtype, "VARCHAR(140)")
