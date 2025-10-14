# test_text_utils_module.py

import os
from rosdl import text_utils_module as tum

# Initialize the utility class
text_util = tum.TextUtilities()

# -----------------------------
# Sample text for testing
# -----------------------------
sample_text = "Hello World! This is a sample text. It includes numbers like 123 and punctuation!!!"

# 1. Test clean_text
cleaned_text = text_util.clean_text(sample_text)
print("Original Text:\n", sample_text)
print("\nCleaned Text:\n", cleaned_text)

# 2. Test tokenize
tokens = text_util.tokenize(cleaned_text)
print("\nTokens:\n", tokens)

# 3. Test stemming
stems = text_util.stem_words(tokens)
print("\nStems:\n", stems)

# 4. Test keyword extraction
documents = [
    "Data science is an interdisciplinary field.",
    "Machine learning is a part of data science.",
    "Python is a popular language for data science and AI."
]
keywords = text_util.extract_keywords(documents, top_k=5)
print("\nTop Keywords:\n", keywords)

# -----------------------------
# File reading tests
# -----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))

# Test TXT file
txt_path = os.path.join(current_dir, "sample.txt")
if os.path.exists(txt_path):
    txt_content = tum.read_txt_file(txt_path)
    print("\nTXT File Content:\n", txt_content)

# Test DOCX file
docx_path = os.path.join(current_dir, "sample.docx")
if os.path.exists(docx_path):
    docx_content = tum.read_docx_file(docx_path)
    print("\nDOCX File Content:\n", docx_content)

# Test PDF file
pdf_path = os.path.join(current_dir, "sample.pdf")
if os.path.exists(pdf_path):
    pdf_content = tum.read_pdf_file(pdf_path)
    print("\nPDF File Content:\n", pdf_content[:500], "...")  # print first 500 chars
