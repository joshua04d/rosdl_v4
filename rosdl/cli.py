import click
from rosdl.addition import add
from rosdl import mat  # import module instead of functions


@click.group()
def cli():
    """rosdl - Research Oriented Smart Data Library"""
    pass


# ----- Basic Commands -----
@cli.command()
def hello():
    """Say Hello from rosdl"""
    click.echo("Hello, World from rosdl!")


@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def add_numbers(a, b):
    """Add two numbers (from addition.py)"""
    result = add(a, b)
    click.echo(f"The sum of {a} and {b} is {result}")


# ----- Math Group -----
@cli.group()
def mat_group():
    """Math operations"""
    pass


@mat_group.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def addition(a, b):
    """Add two numbers (from mat.py)"""
    result = mat.addition(a, b)
    click.echo(result)


@mat_group.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def subtraction(a, b):
    """Subtract two numbers (from mat.py)"""
    result = mat.subtraction(a, b)
    click.echo(result)


# Register the math group under "mat"
cli.add_command(mat_group, name="mat")
if __name__ == "__main__":
    cli()


