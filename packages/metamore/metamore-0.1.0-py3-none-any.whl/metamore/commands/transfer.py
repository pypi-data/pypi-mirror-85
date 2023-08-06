import piexif
import click


@click.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('target', type=click.Path(exists=True))
def cli(source, target):
    """Transfer EXIF metadata from one file to another"""
    piexif.transplant(source, target)
