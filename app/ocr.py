import pytesseract
from PIL import Image

# Tesseract executable 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe' 

def perform_ocr(image_path):
    return pytesseract.image_to_string(Image.open(image_path))
