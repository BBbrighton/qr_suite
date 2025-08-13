import frappe
import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont
from frappe.utils import get_url
from frappe.utils.file_manager import save_file

def generate_qr_image(qr_link_doc, **kwargs):
    """
    Generate QR code image for a QR Link document
    Returns dict with file_url and other details
    """
    try:
        # Get content to encode
        content = get_qr_content(qr_link_doc)
        
        if not content:
            frappe.throw("No content to encode in QR code")
        
        # Get QR settings from kwargs or defaults
        qr_size = kwargs.get('qr_size', 'Medium')
        error_correction = kwargs.get('error_correction', 'M')
        image_format = kwargs.get('image_format', 'PNG')
        
        # Map size to box_size
        size_map = {
            'Small': 8,
            'Medium': 10,
            'Large': 12
        }
        box_size = size_map.get(qr_size, 10)
        
        # Map error correction
        error_map = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
        error_level = error_map.get(error_correction, qrcode.constants.ERROR_CORRECT_M)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=None,  # Auto-size
            error_correction=error_level,
            box_size=box_size,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Add label if requested
        if hasattr(qr_link_doc, 'include_label') and qr_link_doc.include_label:
            label_text = getattr(qr_link_doc, 'label_text', qr_link_doc.target_name)
            img = add_label_to_qr(img, label_text)
        elif qr_link_doc.qr_type == "Value QR":
            # For Value QR, always add label showing what's encoded
            label_text = qr_link_doc.qr_content or qr_link_doc.target_name
            img = add_label_to_qr(img, label_text)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Save as file
        filename = f"QR-{qr_link_doc.target_doctype}-{qr_link_doc.target_name}.png"
        file_doc = save_file(
            filename, 
            img_byte_arr, 
            "QR Link", 
            qr_link_doc.name,
            is_private=0
        )
        
        return {
            "file_url": file_doc.file_url,
            "file_name": file_doc.file_name,
            "base64": base64.b64encode(img_byte_arr).decode('utf-8')
        }
        
    except Exception as e:
        frappe.log_error(f"Error generating QR image: {str(e)}", "QR Image Generation")
        frappe.throw(f"Error generating QR image: {str(e)}")

def get_qr_content(qr_link_doc):
    """Get the content to encode in the QR code"""
    if qr_link_doc.qr_type == "Document QR":
        # For Document QR, use the pre-generated qr_url
        if hasattr(qr_link_doc, 'qr_url') and qr_link_doc.qr_url:
            return qr_link_doc.qr_url
        # Fallback to token-based URL
        elif qr_link_doc.token:
            return f"{get_url()}/qr?token={qr_link_doc.token}"
        else:
            # Build URL based on action
            action = getattr(qr_link_doc, 'action', 'view')
            doctype_slug = frappe.scrub(qr_link_doc.target_doctype).replace("_", "-")
            
            if action == 'view':
                return f"{get_url()}/app/{doctype_slug}/{qr_link_doc.target_name}"
            elif action == 'edit':
                return f"{get_url()}/app/{doctype_slug}/{qr_link_doc.target_name}?edit=1"
            elif action == 'print':
                return f"{get_url()}/app/{doctype_slug}/{qr_link_doc.target_name}?print=1"
            elif action == 'new_stock_entry':
                return f"{get_url()}/app/stock-entry/new-stock-entry?{doctype_slug}={qr_link_doc.target_name}"
            elif action == 'maintenance_log':
                return f"{get_url()}/app/maintenance-log/new-maintenance-log?asset={qr_link_doc.target_name}"
            elif action == 'asset_repair':
                return f"{get_url()}/app/asset-repair/new-asset-repair?asset={qr_link_doc.target_name}"
            elif action == 'stock_balance':
                return f"{get_url()}/app/query-report/Stock Balance?item_code={qr_link_doc.target_name}"
            else:
                # Default to view
                return f"{get_url()}/app/{doctype_slug}/{qr_link_doc.target_name}"
    else:
        # For Value QR, use the pre-set content or target name
        return getattr(qr_link_doc, 'qr_content', qr_link_doc.target_name)

def add_label_to_qr(img, text):
    """Add a text label below the QR code"""
    if not text:
        return img
        
    # Create a new image with extra space for text
    width, height = img.size
    
    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
    
    # Calculate text size
    draw = ImageDraw.Draw(img)
    text = str(text)
    
    # Handle long text by wrapping
    max_width = width - 20
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width or not current_line:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Calculate total height needed
    line_height = 20
    text_height = len(lines) * line_height + 20
    
    # Create new image with space for text
    new_height = height + text_height
    new_img = Image.new('RGB', (width, new_height), 'white')
    
    # Paste the QR code
    new_img.paste(img, (0, 0))
    
    # Add text
    draw = ImageDraw.Draw(new_img)
    y_offset = height + 10
    
    for line in lines:
        # Center each line
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, y_offset), line, fill='black', font=font)
        y_offset += line_height
    
    return new_img
