import cv2
import numpy as np
from PIL import Image
import io
import os
from app import app

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c + c for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def recolor_product_with_ai(image_path_or_url, target_hex, output_filename):
    """
    Recolors the product using pure OpenCV image processing.
    Avoids heavy ML models (like rembg) to ensure fast, stable live previews.
    """
    input_data = None
    
    # 1. Load image locally
    if image_path_or_url.startswith('http') or image_path_or_url.startswith('/'):
        clean_path = image_path_or_url.split('?')[0].lstrip('/')
        local_path = os.path.join(app.root_path, clean_path)
        img = cv2.imread(local_path)
    else:
        img = cv2.imread(image_path_or_url)
        
    if img is None:
        raise ValueError("Could not read image")

    # 2. Create a mask to separate the object from the white background
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold: anything darker than 240 is object (assuming white background)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Clean up the mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 3. Convert image to HSV for recoloring
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 4. Get target color
    target_r, target_g, target_b = hex_to_rgb(target_hex)
    target_color_bgr = np.uint8([[[target_b, target_g, target_r]]])
    target_color_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0][0]
    
    # 5. Apply hue shift ONLY to the masked area
    # Create a copy of the HSV image
    recolored_hsv = hsv.copy()
    
    # Shift hue and blend saturation, preserve value (lightness/texture)
    recolored_hsv[:, :, 0] = target_color_hsv[0]
    recolored_hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 0.4 + target_color_hsv[1] * 0.6, 0, 255)
    
    # Convert back to BGR
    recolored_bgr = cv2.cvtColor(recolored_hsv, cv2.COLOR_HSV2BGR)
    
    # 6. Blend original and recolored using the mask
    mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
    final_bgr = (recolored_bgr * mask_3d + img * (1 - mask_3d)).astype(np.uint8)
    
    # Convert to RGB for PIL saving
    final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)
    final_img = Image.fromarray(final_rgb)
    
    # Save the output image
    output_dir = os.path.join(app.root_path, 'static', 'images', 'customized')
    os.makedirs(output_dir, exist_ok=True)
    
    full_output_path = os.path.join(output_dir, output_filename)
    final_img.save(full_output_path, quality=90)
    
    return f"/static/images/customized/{output_filename}"
