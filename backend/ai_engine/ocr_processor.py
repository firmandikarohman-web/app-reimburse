import cv2
import pytesseract
import re
import os

def process_receipt(image_path: str) -> float:
    """
    Simulates reading a receipt to extract the nominal value using OpenCV and Tesseract.
    """
    try:
        if not os.path.exists(image_path):
            return 0.0

        # 1. Read image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            return 0.0
            
        # 2. Preprocess image (grayscale, threshold)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # 3. Use Tesseract to extract text
        # (Requires tesseract-ocr installed on system)
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        
        # 4. Use Regex to find amounts like Rp 150.000 or 150000
        amounts = re.findall(r'(?:Rp\s*|IDR\s*)?(\d{1,3}(?:\.\d{3})*(?:,\d*)?|\d+)', text)
        
        # 5. Extract the largest number which is usually the total
        max_val = 0.0
        for amt in amounts:
            clean_amt = amt.replace('.', '').replace(',', '.')
            try:
                val = float(clean_amt)
            except ValueError:
                val = 0.0
            if val > max_val:
                max_val = val
                
        return max_val
    except Exception as e:
        print(f"OCR Error: {e}")
        return 0.0
