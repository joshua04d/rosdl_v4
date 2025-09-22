# rosdl/core/file_converter.py

import os
import pandas as pd
from openpyxl import Workbook
from moviepy import VideoFileClip
from pdf2docx import Converter
from docx import Document
from fpdf import FPDF
from PIL import Image


# ------------------------------
# CSV → Excel
# ------------------------------
def csv_to_xlsx(input_csv, output_xlsx=None):
    if output_xlsx is None:
        output_xlsx = os.path.splitext(input_csv)[0] + ".xlsx"

    try:
        df = pd.read_csv(input_csv)
        df.to_excel(output_xlsx, index=False)
        return f"✅ CSV converted to Excel: {output_xlsx}"
    except Exception as e:
        return f"❌ Error converting CSV to Excel: {e}"


# ------------------------------
# Excel → CSV
# ------------------------------
def xlsx_to_csv(input_xlsx, output_csv=None):
    if output_csv is None:
        output_csv = os.path.splitext(input_xlsx)[0] + ".csv"

    try:
        df = pd.read_excel(input_xlsx)
        df.to_csv(output_csv, index=False)
        return f"✅ Excel converted to CSV: {output_csv}"
    except Exception as e:
        return f"❌ Error converting Excel to CSV: {e}"


# ------------------------------
# MP4 → MP3
# ------------------------------
def mp4_to_mp3(input_mp4, output_mp3=None):
    if output_mp3 is None:
        output_mp3 = os.path.splitext(input_mp4)[0] + ".mp3"

    try:
        clip = VideoFileClip(input_mp4)
        clip.audio.write_audiofile(output_mp3)
        clip.close()
        return f"✅ MP4 audio extracted to MP3: {output_mp3}"
    except Exception as e:
        return f"❌ Error converting MP4 to MP3: {e}"


# ------------------------------
# PDF → Word
# ------------------------------
def pdf_to_word(input_pdf, output_docx=None):
    if output_docx is None:
        output_docx = os.path.splitext(input_pdf)[0] + ".docx"

    try:
        cv = Converter(input_pdf)
        cv.convert(output_docx, start=0, end=None)
        cv.close()
        return f"✅ PDF converted to Word: {output_docx}"
    except Exception as e:
        return f"❌ Error converting PDF to Word: {e}"




# ------------------------------
# Image Format Conversion
# ------------------------------
def image_format_convert(input_image, output_image=None):
    try:
        if output_image is None:
            base, _ = os.path.splitext(input_image)
            output_image = base + "_converted.png"  # Default PNG

        img = Image.open(input_image)
        img = img.convert("RGB")  # Normalize mode
        img.save(output_image)
        return f"✅ Image converted: {output_image}"
    except Exception as e:
        return f"❌ Error converting image: {e}"
