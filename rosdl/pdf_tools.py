# rosdl/core/pdf_tools.py

import os
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path # type: ignore
import pytesseract
from PIL import Image


# 1. Split PDF
def split_pdf(input_pdf, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PdfReader(input_pdf)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_path = os.path.join(output_dir, f"page_{i+1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
    return f"✅ Split {len(reader.pages)} pages into {output_dir}"


# 2. Merge PDFs
def merge_pdfs(pdf_list, output_pdf):
    writer = PdfWriter()
    for pdf in pdf_list:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_pdf, "wb") as f:
        writer.write(f)
    return f"✅ Merged {len(pdf_list)} PDFs into {output_pdf}"


# 3. Extract text from PDF
def extract_text(input_pdf, output_txt: str | None = None):
    """
    Extract text from a PDF and save it to a .txt file.
    If output_txt is None the txt file will be created next to the PDF
    with the same base name (e.g. foo.pdf -> foo.txt).
    Returns the path to the created .txt file.
    """
    reader = PdfReader(input_pdf)
    text_parts = []
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    text = "\n".join(text_parts).strip()

    if output_txt is None:
        base = os.path.splitext(input_pdf)[0]
        output_txt = base + ".txt"

    os.makedirs(os.path.dirname(output_txt) or ".", exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)
    return output_txt


# 4. PDF to Images
def pdf_to_images(input_pdf, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images = convert_from_path(input_pdf)
    paths = []
    for i, img in enumerate(images):
        path = os.path.join(output_dir, f"page_{i+1}.png")
        img.save(path, "PNG")
        paths.append(path)
    return f"✅ Saved {len(paths)} images to {output_dir}"



# 6. OCR Entire PDF
def ocr_pdf(input_pdf, output_txt: str | None = None):
    """
    Run OCR on each page of the PDF and save combined text to a .txt file.
    If output_txt is None the txt file will be created next to the PDF
    with the same base name (e.g. foo.pdf -> foo.txt).
    Returns the path to the created .txt file.
    """
    images = convert_from_path(input_pdf)
    parts = []
    for img in images:
        parts.append(pytesseract.image_to_string(img))
    text = "\n".join(parts).strip()

    if output_txt is None:
        base = os.path.splitext(input_pdf)[0]
        output_txt = base + ".txt"

    os.makedirs(os.path.dirname(output_txt) or ".", exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)
    return output_txt


# 7. Merge all PDFs in a folder
def merge_pdfs_in_folder(folder_path, output_pdf):
    pdf_list = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")
    ]
    pdf_list.sort()
    return merge_pdfs(pdf_list, output_pdf)
