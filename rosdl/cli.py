import os
import click
from rosdl import mat, pdf_tools


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


# ---------------- Math Group ----------------
@cli.group()
def mat_group():
    """Math operations"""
    pass


@mat_group.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def addition(a, b):
    """Add two numbers"""
    click.echo(mat.addition(a, b))


@mat_group.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def subtraction(a, b):
    """Subtract two numbers"""
    click.echo(mat.subtraction(a, b))


cli.add_command(mat_group, name="mat")


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


if __name__ == "__main__":
    cli()

