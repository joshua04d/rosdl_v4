
import os
import sys
import time
from PIL import Image

SUPPORTED_EXTS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

def check_tesseract_installed():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except ImportError:
        raise ImportError("pytesseract is not installed. Install it with: pip install pytesseract")
    except Exception as e:
        raise RuntimeError("Tesseract is not installed or not found in PATH. "
                           "Installation guide: https://github.com/tesseract-ocr/tesseract") from e

def extract_text(image_path, config=r'--oem 3 --psm 6'):
    """
    Extract text from an image using Tesseract OCR.
    Returns the extracted text.
    """
    import pytesseract
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File '{image_path}' does not exist.")

    ext = os.path.splitext(image_path)[1].lower()
    if ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported file type: {ext}. "
                         f"Supported types: {', '.join(SUPPORTED_EXTS)}")

    pil_img = Image.open(image_path)
    return pytesseract.image_to_string(pil_img, config=config).strip()

def extract_and_save(image_path, output_path):
    """
    Extract text from an image and save to output file.
    """
    text = extract_text(image_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return output_path
