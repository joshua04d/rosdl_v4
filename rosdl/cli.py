import click
from rosdl.addition import add

@click.group()
def cli():
    """rosdl - Research Oriented Smart Data Library"""
    pass

@cli.command()
def hello():
    """Say Hello from rosdl"""
    click.echo("Hello, World from rosdl!")

@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def add(a, b):
    """Add two numbers"""
    result = add(a, b)
    click.echo(f"The sum of {a} and {b} is {result}")
