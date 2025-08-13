# QR Link Fixes and Manual Creation Guide

## Issues Fixed

### 1. QR Link Manual Creation
The QR Link doctype was not properly configured for manual creation. Fixed by:
- Changed `target_doctype` from read-only Data to Link field (required)
- Changed `target_name` from Data to Dynamic Link field
- Changed `qr_type` from read-only Data to Select field with options
- Changed `action` from read-only Data to Select field with options

### 2. Enhanced QR Link Form
Added client-side scripts to improve user experience:
- Auto-set defaults for new QR Links
- Dynamic field visibility based on QR type
- Better target document selection

### 3. Missing Methods
Added missing server methods:
- `revoke()` - To revoke QR codes
- `generate_qr_image()` - Alias for generate_qr_code

## Manual QR Link Creation

Users can now create QR Links manually if needed:

1. **Go to QR Link List**
   - Navigate to QR Link list view
   - Click "New"

2. **Fill Required Fields**
   - **Target DocType**: Select the doctype (e.g., Asset, Item)
   - **Target Name**: Select the specific document
   - **QR Type**: Choose "Document QR" or "Value QR"
   - **QR Template**: Optionally select a template

3. **Configure Based on Type**
   - For Document QR:
     - **Action**: Select the action (view, edit, etc.)
     - **Expires On**: Set expiration if needed
   - For Value QR:
     - **QR Content**: Enter the value to encode

4. **Save and Generate**
   - Save the document
   - Click "Generate QR Image" button
   - QR code will be generated and attached

## Recommended Workflow

While manual creation is now possible, the recommended workflow is:
1. Use the "Generate QR Code" button from any document
2. This uses the API and ensures all fields are properly set
3. Manual creation is for special cases or bulk operations

## Testing After Implementation

1. **Restart Bench**: `bench restart`
2. **Clear Cache**: `bench clear-cache`
3. **Test Manual Creation**:
   - Create a new QR Link manually
   - Verify all fields work properly
   - Generate QR image
4. **Test API Generation**:
   - Open any document
   - Click "Generate QR Code"
   - Verify it creates properly

## Troubleshooting

If QR Links still have issues:
1. Check browser console for JavaScript errors
2. Verify user has proper roles (QR User or QR Manager)
3. Ensure the target document exists
4. Check that QR Template (if selected) is active
