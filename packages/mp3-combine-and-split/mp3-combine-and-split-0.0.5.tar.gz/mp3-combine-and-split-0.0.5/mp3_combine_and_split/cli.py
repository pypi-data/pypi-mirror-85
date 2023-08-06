"""Console script for mp3_combine_and_split."""
import os
import sys
import click
from mp3_combine_and_split.lib import MP3CombineAndSplit


@click.command()
@click.option(
    "-i",
    "--input-directory",
    "input_directory",
    required=True,
    help="Specify the directory containing the mp3s",
    type=click.Path(exists=True),
)
@click.option(
    "-o",
    "--out-directory",
    "output_directory",
    required=False,
    help="Specify the directory to save the created mp3s to. If not "
    "specified this will default to the same as the input "
    "directory",
    default=None,
    type=click.Path(exists=True),
)
@click.option(
    "-d",
    "--duration",
    "duration",
    required=False,
    help="Specify the duration in seconds that the resulting "
    "MP3s should be. Default is 44 mins 50 seconds "
    "(2690 seconds)",
    default=2690,
    type=click.INT,
)
def main(input_directory, output_directory, duration):
    """Console script for mp3_combine_and_split."""
    if output_directory is None:
        output_directory = input_directory

    mp3_combine_and_split_obj = MP3CombineAndSplit(
        input_directory, output_directory, duration
    )

    combined_mp3 = mp3_combine_and_split_obj.combine_mp3s()
    split_mps = mp3_combine_and_split_obj.split_mp3(combined_mp3)
    # the combined mp3 is no longer required now
    os.remove(combined_mp3)
    click.echo(split_mps)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
