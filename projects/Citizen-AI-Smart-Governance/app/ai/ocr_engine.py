import cv2
import pytesseract
import re
import os

class OCREngine:
    def __init__(self):
        # We can configure tesseract path if needed
        pass

    def preprocess_image(self, image_path):
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            return None
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        return thresh

    def extract_text(self, image_path):
        processed_img = self.preprocess_image(image_path)
        if processed_img is None:
            return ""
            
        text = pytesseract.image_to_string(processed_img)
        return text

    def parse_fields(self, text, document_type):
        fields = {}
        text = text.lower()
        
        # Basic regex parsing based on document type (Prototype Logic)
        if document_type == 'PAN':
            # Try to find PAN format
            pan_match = re.search(r'[a-z]{5}[0-9]{4}[a-z]{1}', text)
            if pan_match:
                fields['document_number'] = pan_match.group(0).upper()
                
            # Date of birth DD/MM/YYYY
            dob_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
            if dob_match:
                fields['dob'] = dob_match.group(0)
                
        return fields

