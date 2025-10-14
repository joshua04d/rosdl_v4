import os
import click
from rosdl import ocr_module
from rosdl import pdf_tools
import inspect
from rosdl import metadata_extractor
from rosdl import file_converter
from rosdl import image_tools
from rosdl import data_generator


# Customizing the help headers
class CustomHelpGroup(click.Group):
    def format_help(self, ctx, formatter):
        click.echo(click.style("\n✨ Rosdl - Research Oriented Smart Data Library ✨\n", fg="cyan", bold=True))
        super().format_help(ctx, formatter)


@click.group(cls=CustomHelpGroup)
def cli():
    """Rosdl - Research Oriented Smart Data Library"""
    pass


# ---------------- Basic ----------------
@cli.command()
def hello():
    """Say Hello from rosdl"""
    click.echo(click.style("👋 Hello, World from rosdl!", fg="green", bold=True))


# # ---------------- Math Group ----------------
# @cli.group()
# def mat_group():
#     """Math operations"""
#     pass
# @mat_group.command()
# @click.argument("a", type=int)
# @click.argument("b", type=int)
# def addition(a, b):
#     """Add two numbers"""
#     click.echo(mat.addition(a, b))


# @mat_group.command()
# @click.argument("a", type=int)
# @click.argument("b", type=int)
# def subtraction(a, b):
#     """Subtract two numbers"""
#     click.echo(mat.subtraction(a, b))
# cli.add_command(mat_group, name="mat")


# ---------------- PDF Group -----------------
@cli.group()
def pdf():
    """PDF utilities: split, merge, extract-text, pdf-to-images, ocr, merge-folder"""
    pass

@pdf.command("split")
@click.argument("input_pdf", type=click.Path(exists=True))
@click.argument("output_base", required=False, type=click.Path())
def split_pdf(input_pdf, output_base):
    """Split PDF into individual pages."""
    if not output_base:
        input_dir = os.path.dirname(os.path.abspath(input_pdf)) or "."
        default_folder = os.path.splitext(os.path.basename(input_pdf))[0] + "_split"
        folder_name = click.prompt(
            click.style("Output folder name (will be created next to input PDF)", fg="cyan"),
            default=default_folder
        )
        output_base = os.path.join(input_dir, folder_name)

    files = pdf_tools.split_pdf(input_pdf, output_base)
    if isinstance(files, (list, tuple)):
        click.echo(click.style(f"✅ Split into {len(files)} pages: {files}", fg="green"))
    elif isinstance(files, str):
        click.echo(files)
    else:
        click.echo(click.style("✅ Split completed.", fg="green"))

@pdf.command("merge")
@click.argument("pdfs", nargs=-1, type=click.Path(exists=True))
@click.option("--output", "-o", required=False, type=click.Path())
def merge_pdfs(pdfs, output):
    """Merge multiple PDFs into one."""
    if not output:
        if not pdfs:
            raise click.ClickException("No input PDFs provided.")
        first_dir = os.path.dirname(os.path.abspath(pdfs[0])) or "."
        default_name = "merged.pdf"
        name = click.prompt(
            click.style(f"Output filename (will be saved in {first_dir})", fg="cyan"),
            default=default_name
        )
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        output = os.path.join(first_dir, name)

    pdf_tools.merge_pdfs(list(pdfs), output)
    click.echo(click.style(f"✅ Merged {len(pdfs)} files into {output}", fg="green"))

@pdf.command("extract-text")
@click.argument("input_pdf", type=click.Path(exists=True))
@click.option("--output-name", "-n", required=False, help="Only the filename; saved next to input PDF.")
def extract_text(input_pdf, output_name):
    """Extract text from a PDF."""
    input_dir = os.path.dirname(os.path.abspath(input_pdf)) or "."
    default_name = os.path.splitext(os.path.basename(input_pdf))[0] + ".txt"

    if not output_name:
        name = click.prompt(click.style(f"Output filename (saved next to input PDF)", fg="cyan"), default=default_name)
    else:
        name = output_name

    if not name.lower().endswith(".txt"):
        name += ".txt"

    output_path = os.path.join(input_dir, name)
    # call the pdf_tools function which writes the file
    if hasattr(pdf_tools, "extract_text"):
        result = pdf_tools.extract_text(input_pdf, output_path)
    elif hasattr(pdf_tools, "extract_text_from_pdf"):
        result = pdf_tools.extract_text_from_pdf(input_pdf, output_path)
    else:
        raise click.ClickException("pdf_tools has no extract_text function")
    click.echo(click.style(result, fg="green"))

@pdf.command("to-images")
@click.argument("input_pdf", type=click.Path(exists=True))
@click.argument("output_folder", required=False, type=click.Path())
def pdf_to_images(input_pdf, output_folder):
    """Convert PDF pages to images."""
    if not output_folder:
        input_dir = os.path.dirname(os.path.abspath(input_pdf)) or "."
        default_folder = os.path.splitext(os.path.basename(input_pdf))[0] + "_images"
        folder_name = click.prompt(
            click.style("Output folder name for images (will be created next to input PDF)", fg="cyan"),
            default=default_folder
        )
        output_folder = os.path.join(input_dir, folder_name)

    files = pdf_tools.pdf_to_images(input_pdf, output_folder)
    if isinstance(files, (list, tuple)):
        click.echo(click.style(f"✅ Saved {len(files)} images in {output_folder}", fg="green"))
    elif isinstance(files, str):
        click.echo(files)
    else:
        click.echo(click.style("✅ Saved images.", fg="green"))

@pdf.command("ocr")
@click.argument("input_pdf", type=click.Path(exists=True))
def ocr(input_pdf):
    """Run OCR on a PDF."""
    text = pdf_tools.ocr_pdf(input_pdf)
    click.echo(click.style(text, fg="yellow"))

@pdf.command("merge-folder")
@click.argument("input_folder", type=click.Path(exists=True))
@click.argument("output", required=False, type=click.Path())
def merge_pdfs_in_folder(input_folder, output):
    """Merge all PDFs in a folder."""
    if not output:
        default_name = "merged.pdf"
        name = click.prompt(click.style(f"Output filename (saved inside {input_folder})", fg="cyan"), default=default_name)
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        output = os.path.join(input_folder, name)

    pdf_tools.merge_pdfs_in_folder(input_folder, output)
    click.echo(click.style(f"✅ Merged PDFs in {input_folder} into {output}", fg="green"))

cli.add_command(pdf, name="pdf")

# Add OCR command
# Add/modify OCR command
@cli.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Full path to save OCR .txt. If omitted you'll be prompted; default is same folder as input.")
def ocr(image_path, output):
    """Run OCR on an image file or PDF page and save text.

    If --output is provided it is used directly. If omitted the CLI will ask whether
    to save next to the input file (default) and prompt for a filename, or let you
    provide a full path.
    """
    input_dir = os.path.dirname(os.path.abspath(image_path)) or "."
    default_name = os.path.splitext(os.path.basename(image_path))[0] + ".txt"

    if output:
        output_path = output
    else:
        save_next = click.confirm("Save next to input file? (Yes = same folder, No = specify full path)", default=True)
        if save_next:
            name = click.prompt(click.style("Output filename (saved next to input file)", fg="cyan"), default=default_name)
            if not name.lower().endswith(".txt"):
                name += ".txt"
            output_path = os.path.join(input_dir, name)
        else:
            path = click.prompt(click.style("Full output path (including filename)", fg="cyan"),
                                default=os.path.join(input_dir, default_name))
            if not path.lower().endswith(".txt"):
                path += ".txt"
            output_path = path

    # Attempt to use ocr_module if it has a usable function, otherwise fallback to pytesseract
    func = None
    for name in ("extract_text", "extract_text_from_image", "ocr", "ocr_image", "image_to_text"):
        if hasattr(ocr_module, name):
            func = getattr(ocr_module, name)
            break

    result_text = None
    if func:
        try:
            sig = inspect.signature(func)
            # call either (path, out_path) or (path) depending on signature
            if len(sig.parameters) == 2:
                res = func(image_path, output_path)
                # if function returned a path, treat it as done
                if isinstance(res, str) and os.path.exists(res):
                    click.echo(click.style(f"✅ OCR saved to {res}", fg="green"))
                    return
                # otherwise fall through to read result if it's text
                result_text = res
            else:
                result_text = func(image_path)
        except Exception as e:
            raise click.ClickException(f"Error calling ocr_module function: {e}") from e
    else:
        try:
            from PIL import Image
            import pytesseract
        except Exception:
            raise click.ClickException(
                "ocr_module has no OCR function and pytesseract is not installed. "
                "Install optional pdf extras or add an extract function to ocr_module."
            )
        try:
            img = Image.open(image_path)
            result_text = pytesseract.image_to_string(img)
        except Exception as e:
            raise click.ClickException(f"OCR failed: {e}") from e

    result_text = (result_text or "").strip()
    if not result_text:
        click.echo(click.style("⚠️ No text extracted.", fg="yellow"))
        return

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result_text)
    click.echo(click.style(f"✅ OCR saved to {output_path}", fg="green"))

# ---------------- Metadata Group -----------------
@cli.group()
def meta():
    """File metadata utilities"""
    pass


@meta.command("file")
@click.argument("filepath", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Custom output path for report")
def meta_file(filepath, output):
    """Extract metadata for a single file (always exports a .txt report)."""
    out = metadata_extractor.extract_file(filepath, output=output, interactive=(output is None))
    click.echo(click.style(f"✅ Metadata report saved at: {out}", fg="green"))


@meta.command("folder")
@click.argument("folder_path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recursively scan subfolders")
@click.option("-o", "--output", type=click.Path(), help="Custom output path for report")
def meta_folder(folder_path, recursive, output):
    """Extract metadata for all files in a folder (always exports a .txt report)."""
    out = metadata_extractor.extract_folder(folder_path, output=output, recursive=recursive, interactive=(output is None))
    click.echo(click.style(f"✅ Metadata report saved at: {out}", fg="green"))


cli.add_command(meta, name="meta")

# =========================
# FILE CONVERTER COMMANDS
# =========================
@cli.group()
def convert():
    """File format converters: PDF ⇄ Word, CSV ⇄ XLSX, MP4 ⇨ MP3, Images ⇄ Formats"""
    pass


def _resolve_output(input_file, output_file, default_ext, prompt_msg):
    """Resolve output path with interactive prompt + defaults."""
    input_dir = os.path.dirname(os.path.abspath(input_file)) or "."
    default_name = os.path.splitext(os.path.basename(input_file))[0] + default_ext
    default_path = os.path.join(input_dir, default_name)

    if output_file:
        out = output_file
        if not out.lower().endswith(default_ext):
            out += default_ext
        return out

    save_next = click.confirm(
        click.style("Save next to input file? (Yes = same folder, No = specify full path)", fg="cyan"),
        default=True
    )
    if save_next:
        name = click.prompt(click.style(prompt_msg, fg="cyan"), default=default_name)
        if not name.lower().endswith(default_ext):
            name += default_ext
        return os.path.join(input_dir, name)
    else:
        path = click.prompt(click.style("Full output path (including filename)", fg="cyan"), default=default_path)
        if not path.lower().endswith(default_ext):
            path += default_ext
        return path


# -------------------------
# PDF → Word
# -------------------------
@convert.command("pdf-to-word")
@click.argument("input_pdf", type=click.Path(exists=True))
@click.argument("output_docx", required=False)
def pdf_to_word_cmd(input_pdf, output_docx):
    """Convert PDF to Word (DOCX)"""
    output_path = _resolve_output(input_pdf, output_docx, ".docx", "Output DOCX filename")
    msg = file_converter.pdf_to_word(input_pdf, output_path)
    click.echo(click.style(f"✅ {msg}", fg="green"))


# -------------------------
# XLSX → CSV
# -------------------------
@convert.command("xlsx-to-csv")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", required=False)
def xlsx_to_csv_cmd(input_file, output_file):
    """Convert XLSX to CSV"""
    output_path = _resolve_output(input_file, output_file, ".csv", "Output CSV filename")
    msg = file_converter.xlsx_to_csv(input_file, output_path)
    click.echo(click.style(f"✅ {msg}", fg="green"))


# -------------------------
# CSV → XLSX
# -------------------------
@convert.command("csv-to-xlsx")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", required=False)
def csv_to_xlsx_cmd(input_file, output_file):
    """Convert CSV to XLSX"""
    output_path = _resolve_output(input_file, output_file, ".xlsx", "Output XLSX filename")
    msg = file_converter.csv_to_xlsx(input_file, output_path)
    click.echo(click.style(f"✅ {msg}", fg="green"))


# -------------------------
# MP4 → MP3
# -------------------------
@convert.command("mp4-to-mp3")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", required=False)
def mp4_to_mp3_cmd(input_file, output_file):
    """Extract audio from MP4 → MP3"""
    output_path = _resolve_output(input_file, output_file, ".mp3", "Output MP3 filename")
    msg = file_converter.mp4_to_mp3(input_file, output_path)
    click.echo(click.style(f"✅ {msg}", fg="green"))


# -------------------------
# Image Format Conversion
# -------------------------
@convert.command("image-format")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", required=False)
def image_format_cmd(input_file, output_file):
    """Convert images between formats (e.g. JPG → PNG, PNG → WEBP)"""
    # Here, we don’t know the default ext — so infer from user’s choice
    input_ext = os.path.splitext(input_file)[1].lower() or ".png"
    prompt_ext = ".png" if input_ext != ".png" else ".jpg"

    output_path = _resolve_output(
        input_file, output_file, prompt_ext, f"Output image filename (e.g. {prompt_ext})"
    )
    msg = file_converter.image_format_convert(input_file, output_path)
    click.echo(click.style(f"✅ {msg}", fg="green"))

# =========================
# IMAGE TOOLS COMMANDS
# =========================
@click.group()
def image():
    """Image processing tools: resize, upscale, convert, exif, strip metadata"""
    pass


def _resolve_output(input_file, output_file, default_ext, prompt_msg):
    """Resolve output path with interactive prompt + default to source folder."""
    input_dir = os.path.dirname(os.path.abspath(input_file)) or "."
    default_name = os.path.splitext(os.path.basename(input_file))[0] + default_ext
    default_path = os.path.join(input_dir, default_name)

    if output_file:
        out = output_file
        if not out.lower().endswith(default_ext):
            out += default_ext
        return out

    save_next = click.confirm(
        click.style("Save next to input file? (Yes = same folder, No = specify full path)", fg="cyan"),
        default=True
    )
    if save_next:
        name = click.prompt(click.style(prompt_msg, fg="cyan"), default=default_name)
        if not name.lower().endswith(default_ext):
            name += default_ext
        return os.path.join(input_dir, name)
    else:
        path = click.prompt(click.style("Full output path (including filename)", fg="cyan"), default=default_path)
        if not path.lower().endswith(default_ext):
            path += default_ext
        return path


@image.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Path to save resized image")
@click.option("--width", type=int, help="Target width in pixels")
@click.option("--height", type=int, help="Target height in pixels")
@click.option(
    "--template",
    type=click.Choice(list(image_tools.resize_templates.keys())),
    help="Predefined resize template.\n" +
         "\n".join([f"  {name}: {w}x{h}" for name, (w, h) in image_tools.resize_templates.items()])
)
def resize(input_path, output, width, height, template):
    """Resize image using width/height or template."""
    if template:
        width, height = image_tools.resize_templates[template]
    if not width or not height:
        raise click.UsageError("Either provide --template or both --width and --height")

    output_path = _resolve_output(input_path, output, ".png", "Output filename for resized image")
    image_tools.resize_image(input_path, output_path, width, height)
    click.echo(click.style(f"✅ Resized image saved at {output_path}", fg="green"))




@image.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Path to save upscaled image")
@click.option("--scale", type=int, required=True, help="Upscale percentage (e.g., 150 = 1.5x)")
def upscale(input_path, output, scale):
    """Upscale image by percentage."""
    output_path = _resolve_output(input_path, output, ".png", "Output filename for upscaled image")
    image_tools.upscale_image(input_path, output_path, scale)
    click.echo(click.style(f"✅ Upscaled image saved at {output_path}", fg="green"))


@image.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Path to save converted image")
@click.option("--format", "output_format", required=True, help="Output format (JPEG, PNG, etc.)")
def convert(input_path, output, output_format):
    """Convert image to another format."""
    ext = "." + output_format.lower()
    output_path = _resolve_output(input_path, output, ext, "Output filename for converted image")
    image_tools.convert_format(input_path, output_path, output_format)
    click.echo(click.style(f"✅ Converted image saved at {output_path}", fg="green"))


@image.command()
@click.argument("input_path", type=click.Path(exists=True))
def exif(input_path):
    """Show EXIF metadata of an image."""
    exif_data = image_tools.get_exif_info(input_path)
    if not exif_data:
        click.echo("ℹ️ No EXIF metadata found.")
    else:
        click.echo("\n".join(f"{k}: {v}" for k, v in exif_data.items()))


@image.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Path to save image without EXIF")
def strip(input_path, output):
    """Remove EXIF metadata and save clean image."""
    output_path = _resolve_output(input_path, output, ".png", "Output filename for image without EXIF")
    image_tools.remove_exif(input_path, output_path)
    click.echo(click.style(f"✅ Image saved without EXIF at {output_path}", fg="green"))


# Register in main CLI
cli.add_command(image)


# =========================
# TEXT UTILITIES COMMANDS
# =========================
from rosdl import text_utils_module as tu

@cli.group()
def text():
    """Text utilities: clean, tokenize, stem, keywords, info"""
    pass

# -----------------------------
# Helper to load text (file or string)
# -----------------------------
def _load_text(input_text):
    if not input_text:
        input_text = click.prompt("Enter text or file path")
    return tu.load_text(input_text)

# -----------------------------
# Clean Text
# -----------------------------
@text.command("clean")
@click.argument("input_text", required=False)
@click.option("--remove-stopwords/--keep-stopwords", default=True, help="Remove stopwords or not")
def clean_text(input_text, remove_stopwords):
    """Clean input text or file content."""
    text_content = _load_text(input_text)
    tu_util = tu.TextUtilities()
    cleaned = tu_util.clean_text(text_content, remove_stopwords)
    click.echo(cleaned)

# -----------------------------
# Tokenize Text
# -----------------------------
@text.command("tokenize")
@click.argument("input_text", required=False)
def tokenize(input_text):
    """Tokenize input text or file content into words."""
    text_content = _load_text(input_text)
    tu_util = tu.TextUtilities()
    tokens = tu_util.tokenize(text_content)
    click.echo(tokens)

# -----------------------------
# Stem Text
# -----------------------------
@text.command("stem")
@click.argument("input_text", required=False)
def stem(input_text):
    """Stem input text or file content."""
    text_content = _load_text(input_text)
    tu_util = tu.TextUtilities()
    tokens = tu_util.tokenize(text_content)
    stemmed = tu_util.stem_words(tokens)
    click.echo(stemmed)

# -----------------------------
# Extract Keywords
# -----------------------------
@text.command("keywords")
@click.argument("input_text", required=False)
@click.option("--top-k", default=10, help="Number of keywords to extract")
def keywords(input_text, top_k):
    """Extract top keywords from input text or file using TF-IDF."""
    text_content = _load_text(input_text)
    tu_util = tu.TextUtilities()
    cleaned = tu_util.clean_text(text_content)
    kws = tu_util.extract_keywords([cleaned], top_k)
    click.echo(kws)

# -----------------------------
# Text Info
# -----------------------------
@text.command("info")
@click.argument("input_text", required=False)
def info(input_text):
    """Get basic info/stats about text or file content."""
    text_content = _load_text(input_text)
    tu_util = tu.TextUtilities()
    stats = tu_util.get_text_info(text_content)
    
    click.echo("📊 Text Statistics:")
    click.echo(f"Characters: {stats['characters']}")
    click.echo(f"Words: {stats['words']}")
    click.echo(f"Unique Words: {stats['unique_words']}")
    click.echo(f"Sentences: {stats['sentences']}")
    click.echo("Top 10 Frequent Words:")
    for word, freq in stats['top_words']:
        click.echo(f"  {word}: {freq}")

# Register the text group
cli.add_command(text)





# =========================
# EDA & Drift CLI Commands with Interactive Save
# =========================
import pandas as pd
from rosdl import eda_drift_module as eda

@cli.group()
def eda_cli():
    """Quick EDA & Data Drift Analysis"""
    pass


def _resolve_output_interactive(input_file, output_file, default_ext, prompt_msg):
    """Resolve output path interactively if --output is not provided."""
    input_dir = os.path.dirname(os.path.abspath(input_file)) or "."
    default_name = os.path.splitext(os.path.basename(input_file))[0] + default_ext
    default_path = os.path.join(input_dir, default_name)

    if output_file:
        if not output_file.lower().endswith(default_ext):
            output_file += default_ext
        return output_file

    # Interactive prompt
    save_next = click.confirm(
        click.style("Save next to input file? (Yes = same folder, No = specify full path)", fg="cyan"),
        default=True
    )
    if save_next:
        name = click.prompt(click.style(prompt_msg, fg="cyan"), default=default_name)
        if not name.lower().endswith(default_ext):
            name += default_ext
        return os.path.join(input_dir, name)
    else:
        path = click.prompt(click.style("Full output path (including filename)", fg="cyan"), default=default_path)
        if not path.lower().endswith(default_ext):
            path += default_ext
        return path


@eda_cli.command("quick")
@click.argument("csv_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Optional path to save report as CSV")
def quick(csv_file, output):
    """Perform quick EDA on a CSV file."""
    df = pd.read_csv(csv_file)
    report = eda.quick_eda(df)

    # Convert report to DataFrame for saving
    df_report = pd.DataFrame({
        "Column": list(report['dtypes'].keys()),
        "DataType": list(report['dtypes'].values()),
        "Missing": [report['missing'][c] for c in report['dtypes'].keys()],
        "Unique": [report['unique_values'][c] for c in report['dtypes'].keys()]
    })

    click.echo("\n--- Quick EDA Report ---")
    click.echo(df_report.to_string(index=False))

    # Resolve output interactively if not provided
    output_path = _resolve_output_interactive(csv_file, output, ".csv", "Output EDA report filename")
    df_report.to_csv(output_path, index=False)
    click.echo(click.style(f"✅ EDA report saved to {output_path}", fg="green"))


@eda_cli.command("drift")
@click.argument("csv1", type=click.Path(exists=True))
@click.argument("csv2", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Optional path to save drift report as CSV")
def drift(csv1, csv2, output):
    """Compare two CSV files for data drift."""
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    drift_report = eda.detect_drift(df1, df2)

    # Convert drift report to DataFrame
    df_report = pd.DataFrame(drift_report, columns=["Column", "Type", "p_value"])
    df_report["Drift_Detected"] = df_report.apply(
        lambda row: "YES" if row["p_value"] < 0.05 and row["Type"] != "No Change" else "NO", axis=1
    )

    click.echo("\n--- Data Drift Report ---")
    click.echo(df_report.to_string(index=False))

    # Resolve output interactively if not provided
    output_path = _resolve_output_interactive(csv1, output, ".csv", "Output drift report filename")
    df_report.to_csv(output_path, index=False)
    click.echo(click.style(f"✅ Drift report saved to {output_path}", fg="green"))

# Register CLI group
cli.add_command(eda_cli, name="eda_cli")


# =========================
# SYNTHETIC DATA GENERATION COMMANDS
# =========================

@cli.group()
def synth():
    """Synthetic data utilities: generate, augment, prompt"""
    pass


@synth.command("schema")
@click.argument("schema_file", type=click.Path(exists=True))
@click.option("-n", "--rows", default=100, help="Number of rows to generate.")
@click.option("-o", "--output", type=click.Path(), help="Output CSV file.")
def synth_schema(schema_file, rows, output):
    """Generate synthetic data from a JSON/YAML schema."""
    import json
    with open(schema_file) as f:
        schema = json.load(f)
    fname = data_generator.generate_from_schema(schema, rows, output)
    click.echo(click.style(f"✅ Generated data saved as {fname}", fg="green"))


@synth.command("prompt")
@click.argument("prompt", type=str)
@click.option("-o", "--output", type=click.Path(), help="Output CSV file.")
def synth_prompt(prompt, output):
    """Generate synthetic data from text prompt."""
    fname = data_generator.generate_from_prompt(prompt, output)
    click.echo(click.style(f"✅ Generated data saved as {fname}", fg="green"))


@synth.command("augment")
@click.argument("dataset", type=click.Path(exists=True))
@click.option("-n", "--add", default=50, help="Number of rows to add.")
@click.option("-o", "--output", type=click.Path(), help="Output CSV file.")
def synth_augment(dataset, add, output):
    """Augment existing dataset with synthetic rows."""
    fname = data_generator.augment_dataset(dataset, add, output)
    click.echo(click.style(f"✅ Augmented dataset saved as {fname}", fg="green"))


cli.add_command(synth, name="synth")


if __name__ == "__main__":
    cli()

