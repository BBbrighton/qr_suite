# QR Link Manual Creation Guide

## Quick Start - Manual QR Link Creation

### 1. Navigate to QR Link List
- Go to: **QR Suite > QR Link**
- Click: **New**

### 2. Basic Information
- **QR Type**: Select "Document QR" or "Value QR"
- **QR Template**: (Optional) Select a template to auto-fill settings
- **Status**: Automatically set to "Active"

### 3. Target Document
- **Target DocType**: Select the doctype (e.g., "Asset", "Item")
- **Target Document**: Select the specific document

### 4. For Document QR
- **Action**: Choose what happens on scan (view, edit, print, etc.)
- **URL Mode**: 
  - "token" = Secure URL with expiring token
  - "direct" = Full URL encoded in QR

#### If Token Mode:
- **Expires On**: Set expiration date (optional)

#### If Direct Mode:
- **Custom URL Prefix**: Use custom domain (optional)
- **Extra Parameters**: Add URL params in JSON format

### 5. For Value QR
- **QR Content**: Enter the value to encode
  - Can be item code, serial number, or any text
  - If using template, this can be auto-filled from a field

### 6. QR Appearance
- **Include Label**: Check to add text below QR code
- **Label Text**: Text to display (auto-fills from target name)

### 7. Save and Generate
1. Click **Save**
2. Click **Generate QR Image** button
3. QR code will be generated and attached

## Example Scenarios

### Document QR - Asset with Token
```
QR Type: Document QR
Target DocType: Asset
Target Document: COMP-001
Action: view
URL Mode: token
Expires On: [30 days from now]
Include Label: ✓
Label Text: Computer COMP-001
```

### Document QR - Direct URL for Item
```
QR Type: Document QR
Target DocType: Item
Target Document: WIDGET-A
Action: stock_balance
URL Mode: direct
Custom URL Prefix: https://inventory.example.com
Extra Parameters: {"warehouse": "Main"}
```

### Value QR - Serial Number
```
QR Type: Value QR
Target DocType: Serial No
Target Document: SN-2024-001
QR Content: SN-2024-001
Include Label: ✓
Label Text: Serial: SN-2024-001
```

## Tips

1. **Use Templates**: Create templates for common configurations
2. **Test First**: Use "Test QR URL" button to verify before printing
3. **JSON Format**: For extra params, use proper JSON: `{"key": "value"}`
4. **Bulk Creation**: Use Data Import for multiple QR Links

## Troubleshooting

### "Target Document not found"
- Ensure the document exists in the selected doctype
- Check permissions on the target document

### "Invalid JSON format"
- Extra Parameters must be valid JSON
- Use double quotes for keys and string values
- Example: `{"ref": "qr", "year": 2024}`

### QR Image not generating
- Save the document first
- Click "Generate QR Image" button
- Check browser console for errors

### Fields not showing
- QR Type determines which fields are visible
- URL Mode affects token/direct specific fields
- Refresh the form if fields don't update
