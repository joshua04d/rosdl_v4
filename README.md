# rosdl

Minimal CLI utilities for small research workflows: simple math helpers and PDF tools (split, merge, extract text, convert to images, OCR, merge-folder).

## Quick install

From the project root:

- Install base package (CLI):
```powershell
python -m pip install -e .
python -m pip install -r requirements.txt
```

- Install optional extras:
  - Math extras:
    ```powershell
    python -m pip install -e ".[mat]"
    ```
  - PDF/OCR extras (requires system packages, see below):
    ```powershell
    python -m pip install -e ".[pdf]"
    ```
  - Or install the PDF packages individually:
    ```powershell
    python -m pip install PyPDF2 pdf2image Pillow pytesseract
    ```

## System requirements (Windows)

- Poppler (for pdf2image / pdftotext): add poppler\bin to PATH.
- Tesseract OCR (for OCR): add tesseract to PATH.
Install via your package manager (Chocolatey) or download installers and add to PATH.

## Usage

Run commands from the repo root (or after installing the package the `rosdl` entrypoint will be available).

Basic
```powershell
rosdl hello
```

Math
```powershell
rosdl mat addition 2 3
rosdl mat subtraction 5 1
```

PDF utilities
```powershell
# split PDF into pages (will prompt for folder name if not provided)
rosdl pdf split input.pdf [out/split_folder]

# merge PDFs (if -o not provided you'll be prompted; default save is next to first input)
rosdl pdf merge file1.pdf file2.pdf ... -o merged.pdf

# extract text -> writes a .txt file next to input by default (will prompt for filename if not provided)
rosdl pdf extract-text input.pdf
rosdl pdf extract-text input.pdf --output out\custom_name.txt

# convert PDF pages to images (requires Poppler)
rosdl pdf to-images input.pdf [out/images_folder]

# OCR an image or PDF page (requires Tesseract)
# will prompt for output filename or use --output
rosdl ocr input.png
rosdl ocr input.png --output out\ocr_output.txt

# merge all PDFs in a folder (will prompt for filename if output omitted)
rosdl pdf merge-folder some_folder [output.pdf]
```

### Default output behavior
- When an output path/folder is omitted, rosdl will:
  - Prompt only for a filename/folder name (not a full path).
  - Save the result in the same directory as the input file (or inside the input folder for merge-folder).
  - This makes running commands on a file from Desktop create outputs on the Desktop by default.
- You may always supply a full path (or use the relevant --output option) to save elsewhere.

## Viewing extracted text
- The extract-text and ocr commands write a .txt file. On Windows:
```powershell
notepad "input.txt"
```
- You can also direct output to stdout or pipe into pagers (Git Bash / WSL) for better preserved layout:
```powershell
rosdl pdf extract-text input.pdf > out\input.txt
less -S out\input.txt
```

## Troubleshooting
- If the CLI fails to import pdf/image/ocr libraries, either:
  - install the pdf extras: python -m pip install -e ".[pdf]" or
  - install missing packages individually.
- If a command requires Poppler or Tesseract install those system tools and add to PATH.
- If `pip install -e .` errors with multiple top-level folders, exclude non-package folders or update package discovery in `pyproject.toml`.

## Contributing
Open a PR or issue with minimal repro steps. Keep helpers small and document any system
