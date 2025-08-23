import click
from rosdl import mat, pdf_tools


@click.group()
def cli():
    """rosdl - Research Oriented Smart Data Library"""
    pass


# ---------------- Basic ----------------
@cli.command()
def hello():
    """Say Hello from rosdl"""
    click.echo("Hello, World from rosdl!")


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
@click.argument("output_base", type=click.Path())
def split_pdf(input_pdf, output_base):
    """Split PDF into individual pages"""
    files = pdf_tools.split_pdf(input_pdf, output_base)
    if isinstance(files, (list, tuple)):
        click.echo(f"✅ Split into {len(files)} pages: {files}")
    elif isinstance(files, str):
        click.echo(files)
    else:
        click.echo("✅ Split completed.")


@pdf.command("merge")
@click.argument("pdfs", nargs=-1, type=click.Path(exists=True))
@click.option("--output", "-o", required=True, type=click.Path())
def merge_pdfs(pdfs, output):
    """Merge multiple PDFs into one"""
    pdf_tools.merge_pdfs(list(pdfs), output)
    click.echo(f"✅ Merged {len(pdfs)} files into {output}")


@pdf.command("extract-text")
@click.argument("input_pdf", type=click.Path(exists=True))
def extract_text(input_pdf):
    """Extract text from a PDF"""
    if hasattr(pdf_tools, "extract_text"):
        text = pdf_tools.extract_text(input_pdf)
    elif hasattr(pdf_tools, "extract_text_from_pdf"):
        text = pdf_tools.extract_text_from_pdf(input_pdf)
    else:
        raise click.ClickException("pdf_tools has no extract_text function")
    click.echo(text)


@pdf.command("to-images")
@click.argument("input_pdf", type=click.Path(exists=True))
@click.argument("output_folder", type=click.Path())
def pdf_to_images(input_pdf, output_folder):
    """Convert PDF pages to images"""
    files = pdf_tools.pdf_to_images(input_pdf, output_folder)
    if isinstance(files, (list, tuple)):
        click.echo(f"✅ Saved {len(files)} images in {output_folder}")
    elif isinstance(files, str):
        click.echo(files)
    else:
        click.echo("✅ Saved images.")




@pdf.command("merge-folder")
@click.argument("input_folder", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
def merge_pdfs_in_folder(input_folder, output):
    """Merge all PDFs in a folder"""
    pdf_tools.merge_pdfs_in_folder(input_folder, output)
    click.echo(f"✅ Merged PDFs in {input_folder} into {output}")


cli.add_command(pdf, name="pdf")


if __name__ == "__main__":
    cli()

