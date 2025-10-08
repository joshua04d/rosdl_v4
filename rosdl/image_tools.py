from PIL import Image, ExifTags
import os

resize_templates = {
    "Passport": (400, 600),
    "Instagram Post": (1080, 1080),
    "Instagram Reel": (1080, 1920),
    "Facebook Cover": (820, 312),
    "Twitter Post": (1024, 512),
    "YouTube Thumbnail": (1280, 720),
    "A4 Document (300 DPI)": (2480, 3508),
}

def get_exif_info(path):
    """Return EXIF metadata dict from an image file, or None if not present."""
    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if not exif_data:
            return None
        return {ExifTags.TAGS.get(tag_id, tag_id): val for tag_id, val in exif_data.items()}
    except Exception:
        return None

def resize_image(input_path, output_path, width, height):
    """Resize an image to (width, height)."""
    img = Image.open(input_path)
    img = img.resize((width, height), Image.LANCZOS)
    _save_image(img, output_path)

def upscale_image(input_path, output_path, scale_percent):
    """Upscale image by percentage (e.g. 150 = 1.5x)."""
    img = Image.open(input_path)
    w = int(img.width * (scale_percent / 100))
    h = int(img.height * (scale_percent / 100))
    img = img.resize((w, h), Image.LANCZOS)
    _save_image(img, output_path)

def convert_format(input_path, output_path, output_format):
    """Convert image to another format (JPEG, PNG, etc.)."""
    img = Image.open(input_path)
    if output_format.upper() == "JPEG" and img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_path, output_format)

def remove_exif(input_path, output_path):
    """Remove EXIF metadata from image."""
    img = Image.open(input_path)
    img.save(output_path, exif=b'')

def _save_image(img, output_path):
    """Helper to save with proper JPEG conversion/quality."""
    ext = os.path.splitext(output_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, quality=95)
    else:
        img.save(output_path)
