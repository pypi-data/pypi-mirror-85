"""Command line interface for primer_2020."""

# Third party modules
import click

# First party modules
import primer_2020


@click.group()
def entry_point():
    """Utility tool for prime numbers."""


@entry_point.command()
@click.argument("number", type=int)
def factorize(number):
    """Factorize the given number."""
    factors = primer_2020.factorize(number)
    factors = [str(factor) for factor in factors]
    factors = " x ".join(factors)
    print(f"{number} = {factors}")
