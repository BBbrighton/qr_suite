# QR Template Usage Guide

## Overview
QR Templates in QR Suite allow you to pre-configure QR code generation settings for consistent and efficient QR code creation across your organization.

## What are QR Templates?

QR Templates are reusable configurations that define:
- QR code type (Document QR or Value QR)
- Default actions and behaviors
- Visual settings (size, error correction, format)
- Expiration rules
- Field mappings for Value QR codes

## When to Use Templates

### Use Templates When:
1. **Standardization is needed** - Multiple users generate QR codes with same settings
2. **Specific workflows** - Different departments need different QR configurations
3. **Compliance requirements** - Certain QR codes must follow specific rules
4. **Time savings** - Avoid reconfiguring common settings repeatedly

### Direct Generation When:
1. **One-off QR codes** - Quick generation with custom settings
2. **Testing** - Trying different configurations
3. **Special cases** - Unique requirements not covered by templates

## Creating Templates

### Example 1: Asset Tracking Template
```
Template Name: Asset QR Standard
QR Type: Document QR
Target DocType: Asset
Default Action: view
Token Expiry: 0 (no expiry)
Include Readable Text: Yes
```

### Example 2: Serial Number Template
```
Template Name: Serial Number Value QR
QR Type: Value QR
Target DocType: Serial No
Value Field: serial_no
Include Readable Text: Yes
```

### Example 3: Temporary Access Template
```
Template Name: Visitor Asset Access
QR Type: Document QR
Target DocType: Asset
Default Action: view
Token Expiry: 1 day
Include Readable Text: Yes
```

## Using Templates in QR Generation

1. **Select Template**: In the QR generation dialog, choose a template from the dropdown
2. **Review Settings**: Template settings are automatically applied
3. **Override if Needed**: Modify any setting as required for this specific QR
4. **Generate**: Create the QR with template-based or modified settings

## Template Inheritance and Override

Templates work on a "suggest, don't enforce" principle:
- Templates **suggest** default values
- Users can **override** any setting during generation
- Original template remains unchanged
- Overrides apply only to current QR generation

## Best Practices

### 1. Naming Conventions
Use clear, descriptive names:
- ✅ "Asset Tracking - Warehouse"
- ✅ "Serial No - Manufacturing"
- ❌ "Template 1"
- ❌ "QR Config"

### 2. Template Organization
Group templates by:
- **Department**: "HR Employee QR", "Finance Asset QR"
- **Use Case**: "Visitor Access", "Inventory Check"
- **Duration**: "Permanent Asset QR", "Temporary Access QR"

### 3. Documentation
Add descriptions to templates explaining:
- Purpose and use case
- Any special requirements
- Contact person for questions

### 4. Regular Review
- Review templates quarterly
- Remove unused templates
- Update settings as processes change

## Advanced Features

### Dynamic Templates
Templates can use field mappings:
```javascript
// Value Field can reference any field from the doctype
Value Field: "serial_no"  // Uses the serial_no field
Value Field: "item_code"  // Uses the item_code field
```

### Template Permissions
- **System Manager**: Create, edit, delete all templates
- **QR Manager**: Create and edit templates
- **QR User**: Use templates (cannot create/edit)

### Save as Template
During QR generation, users can:
1. Configure custom settings
2. Check "Save as New Template"
3. Provide template name
4. Settings are saved for future use

## Common Scenarios

### Scenario 1: Multi-location Business
Create location-specific templates:
- "Asset QR - New York Office"
- "Asset QR - London Warehouse"
- "Asset QR - Tokyo Branch"

### Scenario 2: Time-bound Access
Create expiry-based templates:
- "Contractor Access - 1 Day"
- "Visitor Pass - 4 Hours"
- "Temporary Employee - 30 Days"

### Scenario 3: Department Standards
Create department templates:
- "IT Equipment QR" (includes custom URL for IT portal)
- "HR Document QR" (30-day expiry for confidential docs)
- "Finance Asset QR" (permanent, high error correction)

## Troubleshooting

### Template Not Appearing
- Check if template is marked as "Active"
- Verify Target DocType matches or is blank
- Ensure user has permission to view templates

### Settings Not Applied
- Confirm template was selected before generation
- Check browser console for errors
- Verify template settings are saved correctly

### Cannot Save Template
- Ensure "QR Manager" or "System Manager" role
- Check for duplicate template names
- Verify all required fields are filled

## Tips and Tricks

1. **Default Templates**: Name your most-used template with "Default" prefix for easy finding
2. **Test Templates**: Create test templates for trying new configurations
3. **Export/Import**: Templates can be exported as fixtures for deployment across instances
4. **Bulk Updates**: Use Data Import Tool to update multiple templates at once
