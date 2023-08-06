import piexif
import click
import os


@click.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('-a', '--all', is_flag=True, help='Remove all EXIF data from a file.')
@click.option('-d', '--dir', is_flag=True, help='Target is a directory. Remove EXIF data from all files in target '
                                                'directory.')
# @click.option('-k', '--key', type=click.Choice(['0th', 'Exif', 'GPS', 'Interop', '1st'],case_sensitive=False,
# help='Remove EXIF data stored in particular key.')
def cli(target, all, dir):
    """Remove EXIF metadata from file(s)"""
    if dir:
        directory = os.fsencode(target)

        if all:
            no_jpg_found = True
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    no_jpg_found = False
                    piexif.remove(target + '/' + filename)
            if no_jpg_found is True:
                print("Error: No JPG/JPEG files found in the target directory")

    else:
        if all:
            piexif.remove(target)