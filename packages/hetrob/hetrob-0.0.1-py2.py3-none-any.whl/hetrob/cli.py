"""Console script for hetrob."""
import sys
import click


@click.group('hetrob')
def cli():
    pass


@click.group('examples')
def examples():
    pass


@click.command('list')
def list_examples():
    pass


examples.add_command(list_examples)

cli.add_command(examples)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
