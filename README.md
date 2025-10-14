# rosdl
**Rosdl: Rapid Open Source Data Library**

rosdl is a lightweight Python library that streamlines research and data workflows by combining essential utilities into one package. It provides tools for handling PDFs (split, merge, extract), performing OCR, managing archives, cleaning CSVs, converting file formats, processing images, extracting metadata, running quick EDA with drift detection, and generating synthetic data. With both Python APIs and a simple CLI, rosdl helps researchers, students, and developers save time and focus on insights instead of struggling with scattered tools.

---

## Quick Install

From the project root:

**Install base package (CLI):**
```powershell
python -m pip install -e .
python -m pip install -r requirements.txt
```

**Install optional extras:**
- Math:
    ```powershell
    python -m pip install -e ".[mat]"
    ```
- PDF (requires system packages, see below):
    ```powershell
    python -m pip install -e ".[pdf]"
    ```
- OCR:
    ```powershell
    python -m pip install -e ".[ocr]"
    ```
- Metadata:
    ```powershell
    python -m pip install -e ".[meta]"
    ```
- Or install PDF packages individually:
    ```powershell
    python -m pip install PyPDF2 pdf2image Pillow pytesseract
    ```

---

## System Requirements (Windows)

- **Poppler** (for pdf2image / pdftotext): add `poppler\bin` to PATH.
- **Tesseract OCR** (for OCR): add `tesseract` to PATH.

Install via your package manager (Chocolatey) or download installers and add to PATH.

---

## Usage

Run commands from the repo root (or after installing the package, the `rosdl` entrypoint will be available).

### Basic

```powershell
rosdl hello
```

---

### PDF Utilities

```powershell
# Split PDF into pages (will prompt for folder name if not provided)
rosdl pdf split input.pdf [out/split_folder]

# Merge PDFs (if -o not provided you'll be prompted; default save is next to first input)
rosdl pdf merge file1.pdf file2.pdf ... -o merged.pdf

# Extract text -> writes a .txt file next to input by default (will prompt for filename if not provided)
rosdl pdf extract-text input.pdf
rosdl pdf extract-text input.pdf --output out\custom_name.txt

# Convert PDF pages to images (requires Poppler)
rosdl pdf to-images input.pdf [out/images_folder]
```

---

### OCR Utilities

```powershell
# OCR an image or PDF page (requires Tesseract)
# Will prompt for output filename or use --output
rosdl ocr input.png
rosdl ocr input.png --output out\ocr_output.txt
```

---

### Metadata Extractor

```powershell
# Extract metadata for a single file
rosdl meta file sample.pdf

# Extract metadata for a folder
rosdl meta folder "path_to_folder"

# Export metadata (json or csv)
rosdl meta export some_folder -e json -o out\metadata.json
rosdl meta export some_folder -e csv -o out\metadata.csv
```

---

### Text Utilities

```powershell
# Load and read text from files
rosdl text load input.txt
rosdl text read-pdf input.pdf
rosdl text read-docx input.docx

# Tokenization
rosdl text tokenize input.txt  # splits into words
rosdl text sent-tokenize input.txt  # splits into sentences
```
*Note: NLTK’s punkt resource is required for sentence tokenization:*
```python
import nltk
nltk.download('punkt')
```

---

### Image Utilities

```powershell
# Convert image format
rosdl img convert input.png --to jpg --output out\converted.jpg

# Resize image
rosdl img resize input.png --width 800 --height 600 --output out\resized.png

# Remove EXIF metadata
rosdl img remove-exif input.jpg --output out\clean.jpg

# Upscale image
rosdl img upscale input.png --scale 2 --output out\upscaled.png
```

---

### CSV / XLSX / File Conversion

```powershell
# Convert CSV -> XLSX
rosdl convert csv-to-xlsx input.csv --output out\output.xlsx

# Convert XLSX -> CSV
rosdl convert xlsx-to-csv input.xlsx --output out\output.csv

# Convert PDF -> Word
rosdl convert pdf-to-word input.pdf --output out\output.docx

# Convert video/audio
rosdl convert mp4-to-mp3 input.mp4 --output out\output.mp3
```

---

### EDA & Drift Detection

```powershell
# Quick exploratory data analysis
rosdl eda quick input.csv

# Detect drift between two datasets
rosdl eda drift old_data.csv new_data.csv
```
*Note: Ensure numeric columns are correctly detected; missing or non-numeric data may cause errors.*

---

### Synthetic Data Generation

```powershell
# Generate a realistic name
rosdl gen name 10  # generates 10 names

# Generate realistic phone numbers or cities
rosdl gen phone 5
rosdl gen city 5

# Generate custom string, int, float, or PID columns
rosdl gen string 10 --prefix "item"
rosdl gen int 10 --min 1 --max 100
rosdl gen float 10 --min 0 --max 1

# Generate dataset from schema or prompt
rosdl gen schema schema.json --rows 50
rosdl gen prompt "columns: name, age, city" --rows 20
```

---

## Default Output Behavior

- When an output path/folder is omitted, rosdl will:
    - Prompt only for a filename/folder name (not a full path).
    - Save the result in the same directory as the input file (or inside the input folder for merge-folder).
    - This makes running commands on a file from Desktop create outputs on the Desktop by default.
- You may always supply a full path (or use the relevant `--output` option) to save elsewhere.

---

## Viewing Extracted Text

- The extract-text and ocr commands write a `.txt` file. On Windows:
    ```powershell
    notepad "input.txt"
    ```
- You can also direct output to stdout or pipe into pagers (Git Bash / WSL):
    ```powershell
    rosdl pdf extract-text input.pdf > out\input.txt
    less -S out\input.txt
    ```

---

## Troubleshooting

- If the CLI fails to import PDF/image/OCR libraries, either:
    - Install the PDF extras: `python -m pip install -e ".[pdf]"`
    - Or install missing packages individually.
- If a command requires Poppler or Tesseract, install those system tools and add to PATH.
- If `pip install -e .` errors with multiple top-level folders, exclude non-package folders or update package discovery in `pyproject.toml`.

---

## Contributing

Open a PR or issue with minimal repro steps. Keep helpers small and document any system dependencies clearly.

---

## License

Include your project license here (e.g. MIT) or remove this section if not applicable.