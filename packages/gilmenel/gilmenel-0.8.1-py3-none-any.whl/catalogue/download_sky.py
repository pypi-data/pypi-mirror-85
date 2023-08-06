#!.venv/bin/python3

import itertools
import sys

import click
import requests

from astropy import units as u
from astropy.coordinates import SkyCoord

from tqdm import tqdm

import download_stars

SUCCESS_FILE = "catalogue/succeeded.tsv"
FAILED_FILE = "catalogue/failed.tsv"


def download_degree2(target):
    attempts = 0
    success = False
    sources = None

    while success is False:
        try:
            sources = download_stars.download_sources(target, faint_limit=18.5)
            success = True

            with open(SUCCESS_FILE, 'a') as f:
                # append coords to tsv file
                f.write(f"{target.ra}\t{target.dec}\t{len(sources)}\n")
        except requests.exceptions.ConnectionError:
            # try again
            attempts += 1
            tqdm.write(f"ConnectionError, occurrance {attempts} - retrying")
        except requests.exceptions.ReadTimeout:
            # try again
            attempts += 1
            tqdm.write(f"ReadTimeout, occurrance {attempts} - retrying")
        except Exception as e:

            with open(FAILED_FILE, 'a') as f:
                # append coords to tsv file
                f.write(f"{target.ra}\t{target.dec}\t{e}\n")

    return sources


def main(start_ra=0, start_dec=-90, size=360 * 180):
    RA_POS = 360
    RA_NEG = 0

    DEC_POS = 11
    DEC_NEG = -76

    start_ra = max(start_ra, RA_NEG)
    start_dec = max(start_dec, DEC_NEG)

    # create grid covering telescope range
    full_grid = (
        (ra, dec) for ra in range(RA_NEG, RA_POS) for dec in range(DEC_NEG, DEC_POS)
    )

    # remove section excluded by starting ra and dec
    partial_grid = (
        (ra, dec)
        for ra, dec in full_grid
        if (ra > start_ra or (ra == start_ra and dec >= start_dec))
    )

    # create SkyCoords from remaining grid
    targets = (
        SkyCoord((ra + 0.5) * u.deg, (dec + 0.5) * u.deg) for ra, dec in partial_grid
    )

    size = min(
        ((RA_POS - start_ra - 1) * (DEC_POS - DEC_NEG) + (DEC_POS - start_dec)), size
    )

    print(f"Total patches: {size}")

    with open(SUCCESS_FILE, 'w') as f:
        # clear success file
        f.write(f"RA\tDec\tSources\n")

    with open(FAILED_FILE, 'w') as f:
        # clear failure file
        f.write(f"RA\tDec\tReason\n")

    download_stars.open_session()

    # limit size of iterator based on size
    targets = itertools.islice(targets, size)

    print("Executing...")

    for t in tqdm(targets, total=size, desc="Downloads", unit=" patches",):
        # download stars and add to database
        download_stars.queue_to_write(download_degree2(t))

    download_stars.write_checkpoint()


@click.command()
@click.option('--ra', '-r', type=click.INT, default=0, help="The RA to start from.")
@click.option('--dec', '-d', type=click.INT, default=-90, help="The DEC to start from.")
@click.option(
    '--size',
    '-s',
    type=click.INT,
    default=360 * 180,
    help="The number of square degrees to download.",
)
def cli(ra, dec, size):
    main(start_ra=ra, start_dec=dec, size=size)


if __name__ == '__main__':
    cli()
