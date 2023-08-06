#!.venv/bin/python3

import os.path as path
import pickle
import threading
import sys

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

import numpy as np

import config

from concurrent.futures import ProcessPoolExecutor as PoolExecutor
from itertools import tee
from time import strftime
from tqdm import tqdm
from typing import List, Tuple

from sqlalchemy import (
    and_,
    create_engine,
    func,
)
from sqlalchemy.orm import sessionmaker

from models import Source

session = None


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def open_session():
    global session

    engine = create_engine(f"sqlite:///{config.catalogue_db_path}")

    Session = sessionmaker(bind=engine)  # noqa
    session = Session()


def query_source_ids(spread: Tuple[int, int]):
    start, stop = spread

    star_grid_sky = np.zeros((180, 360))  # whole sky
    star_grid_deg = np.zeros((100, 100))  # per degree

    query = session.query(Source)
    query = query.filter(Source.source_id >= start)
    query = query.filter(Source.source_id < stop)

    for i, s in enumerate(query.yield_per(128)):
        # increment count in grid of source locations on sky
        star_grid_sky[s.dec_square][s.ra_square] += 1

        # increment count in grid of source locations per deg
        star_grid_deg[s.dec_deg_dist][s.ra_deg_dist] += 1

    return star_grid_sky, star_grid_deg


def query_grid():
    # ID_MAX = 104259626
    ID_MAX = (
        session.query(Source.source_id)
        .order_by(Source.source_id.desc())
        .limit(1)
        .one()[0]
    )  # index of last record in table
    ID_STEP = 10 ** 4
    WORKERS = 12

    star_ids = ((p1, p2) for p1, p2 in pairwise(range(0, ID_MAX, ID_STEP)))
    star_grid_sky = np.zeros((180, 360))
    star_grid_deg = np.zeros((100, 100))

    print(f"Expecting {ID_MAX:,} sources")

    try:
        # create a thread pool of WORKERS threads
        with PoolExecutor(max_workers=WORKERS) as executor:
            # distribute all star_ids between the workers in the pool
            # grid is the response of query_source_ids
            for grid_sky, grid_deg in tqdm(
                executor.map(query_source_ids, star_ids),
                total=round(ID_MAX / ID_STEP),
                desc="Loading sources",
                unit=" kilostars",
            ):
                star_grid_sky = [
                    [s + g for s, g in zip(s_row, g_row)]
                    for s_row, g_row in zip(star_grid_sky, grid_sky)
                ]

                star_grid_deg = [
                    [s + g for s, g in zip(s_row, g_row)]
                    for s_row, g_row in zip(star_grid_deg, grid_deg)
                ]

    except KeyboardInterrupt:
        print("Keyboard interrupt - query incomplete")

        return star_grid_sky, star_grid_deg

    return star_grid_sky, star_grid_deg


def plot_stars(stars):
    matfig = plt.figure(figsize=(20, 10))
    im = plt.matshow(
        stars,
        aspect="equal",
        origin="lower",
        extent=[0, 360, -90, 90],
        norm=colors.LogNorm(vmin=10 ** 2, vmax=10 ** 6),
        fignum=matfig.number,
    )
    plt.colorbar(im).ax.set_ylabel("Source Density per deg²", rotation=270)
    plt.gca().xaxis.tick_bottom()
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(30))
    # x-axis relabelling from degrees to hours
    plt.gca().set_xlim(360, 0)
    plt.gca().set_xticks(np.arange(0, 360 + 1, 360 / 12))
    plt.gca().set_xticklabels(np.arange(0, 24 + 1, 2))
    plt.xlabel("RA [hours]")
    # add second x-axis in degrees
    ax2 = plt.gca().secondary_xaxis("top", functions=(lambda x: x, lambda x: x),)
    ax2.set_ticks(np.arange(0, 360 + 1, 30))
    ax2.set_xlabel("RA [degrees]")
    # continue with y-axis
    plt.ylabel("Dec [degrees]")
    plt.title("Downloaded Catalogue Source Density (Gmag < 18.5)", pad=20)
    plot_path = (
        path.splitext(config.catalogue_db_path)[0]
        + f'_sky_{strftime("%Y-%m-%dT%H-%M-%S")}.png'
    )
    plt.savefig(plot_path, bbox_inches="tight")
    plt.show()
    plt.close()


def plot_dist(stars):
    matfig = plt.figure(figsize=(10, 10))
    im = plt.matshow(
        stars,
        aspect="equal",
        origin="lower",
        # extent=[0, 360, -90, 90],
        norm=colors.LogNorm(vmin=10 ** 0, vmax=10 ** 6),
        fignum=matfig.number,
    )
    plt.colorbar(im).ax.set_ylabel("Source Density per deg²", rotation=270)
    plt.gca().xaxis.tick_bottom()
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
    # x-axis relabelling from degrees to hours
    # plt.gca().set_xlim(360, 0)
    # plt.gca().set_xticks(np.arange(0, 360 + 1, 360 / 12))
    # plt.gca().set_xticklabels(np.arange(0, 24 + 1, 2))
    plt.xlabel("RA [degrees x10^2]")
    # add second x-axis in degrees
    ax2 = plt.gca().secondary_xaxis("top", functions=(lambda x: x, lambda x: x),)
    # ax2.set_ticks(np.arange(0, 360 + 1, 30))
    ax2.set_xlabel("RA [degrees x10^2]")
    # continue with y-axis
    plt.ylabel("Dec [degrees x10^2]")
    plt.title("Downloaded Catalogue Source Density (Gmag < 18.5)", pad=20)
    plot_path = (
        path.splitext(config.catalogue_db_path)[0]
        + f'_deg_{strftime("%Y-%m-%dT%H-%M-%S")}.png'
    )
    plt.savefig(plot_path, bbox_inches="tight")
    plt.show()
    plt.close()


if __name__ == "__main__":

    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        debug = True

    pickle_path = path.splitext(config.catalogue_db_path)[0] + "_summary.pickle"

    if debug:
        print("Loading pickle")
        stars_sky, stars_deg = pickle.load(open(pickle_path, "rb"))
    else:
        print("Querying database...")
        open_session()
        stars_sky, stars_deg = query_grid()
        # pickle to save results from expensive query
        pickle.dump((stars_sky, stars_deg), open(pickle_path, "wb"))

    print("Plotting stars...")
    plot_stars(stars_sky)
    plot_dist(stars_deg)
    print("Complete.")
