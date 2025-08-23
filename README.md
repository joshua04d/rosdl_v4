# rosdl

Minimal CLI utilities for small research workflows: simple math helpers and PDF tools (split, merge, extract text, convert to images, OCR, merge-folder).

## Quick install

From the project root:

```powershell
python -m pip install -e .
python -m pip install -r requirements.txt
```

Notes:
- On Windows you may need to install system packages for some features:
  - Poppler (for pdf2image / pdftotext). Add poppler\bin to PATH.
  - Tesseract OCR. Add tesseract to PATH.

## Usage

Run commands from the repo root (or after install the `rosdl` entrypoint will be available).


1.PDF utilities:
```powershell
# split PDF into pages (creates folder with page_1.pdf, page_2.pdf, ...)
rosdl pdf split input.pdf out/split

# merge PDFs (use -o to specify output path)
rosdl pdf merge file1.pdf file2.pdf -o merged.pdf

# extract text -> writes a .txt file next to PDF (e.g. input.pdf -> input.txt) and prints the path
rosdl pdf extract-text input.pdf

# convert PDF pages to images (requires Poppler)
rosdl pdf to-images input.pdf out/images

# OCR a PDF (requires Tesseract)
rosdl pdf ocr input.pdf

# merge all PDFs in a folder
rosdl pdf merge-folder some_folder output.pdf
```

Viewing extracted text:
- The extract-text / ocr commands write a .txt file. On Windows:
```powershell
notepad input.txt
```

## Troubleshooting

- If a CLI command complains about missing system tools, install Poppler or Tesseract and add them to PATH.
- If `pip install -e .` fails due to extra top-level folders, remove or exclude any non-package folders (e.g. `out_dir`) from the project root or update package discovery in `pyproject.toml`.

## Contributing

Open a PR or issue with minimal repro steps.
