"""Console script for rmcalyse."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for rmcalyse."""
    click.echo("Replace this message by putting your code into "
               "rmcalyse.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
