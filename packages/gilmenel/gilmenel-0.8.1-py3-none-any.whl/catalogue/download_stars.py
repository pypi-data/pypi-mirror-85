#!.venv/bin/python3

import numpy as np

from collections import deque

from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.vizier import Vizier

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from tqdm import tqdm, trange

from models import (
    GAIA_DR2,
    Source,
)

session = None
waiting_sources = deque()


def open_session():
    global session

    engine = create_engine('sqlite:///catalogue/gaia_dr2_salt.db', poolclass=NullPool,)

    Session = sessionmaker(bind=engine)
    session = Session()

    # use local Vizier mirror
    Vizier.VIZIER_SERVER = 'vizieridia.saao.ac.za'


def download_sources(target: SkyCoord, faint_limit: float):
    # Query the GAIA DR2 vizier catalogue
    # (vizier catalogue identifier: I/345/gaia2)
    # The '+' in "+Gmag" sorts the list by the brightest first

    # The proper motion (pmRA and pmDE) filter is needed to remove some stars
    # that may be fast moving e.g. block_id 78169 is an interesting test!
    # -there's a 13.5 mag star with high proper motion!
    # This is not so much a problem *now*, soon after GAIA catalogue was made,
    # but is more important for future proofing this code...
    # Limits of +-50mas/yr are selected in RA and Dec.
    vquery = Vizier(
        columns=['DR2Name', 'RA_ICRS', 'DE_ICRS', 'Gmag', 'RPmag',],
        column_filters={
            "Gmag": (f"<={faint_limit:.2f}"),
            "pmRA": ("> -50 && < 50"),
            "pmDE": ("> -50 && < 50"),
        },
        row_limit=-1,
    )
    vquery.TIMEOUT = 120  # 2 mins
    target.field = 'icrs'
    results = vquery.query_region(
        target,
        width=1.0 * np.cos(target.dec) * u.deg,
        height=1.0 * u.deg,
        catalog="I/345/gaia2",
        cache=False,
    )[0]

    # if we find no stars in the field, raise an error
    if len(results) == 0:
        raise Exception("No stars found in field")
    else:
        # for r in results:
        #     print(type(r['Source']), r['Source'])
        return results


def write_to_db(sources):
    global session

    for s in tqdm(sources, mininterval=1.0, leave=False):
        source = Source(
            source=s['DR2Name'][9:],
            catalog=GAIA_DR2,
            ra=float(s['RA_ICRS']),
            dec=float(s['DE_ICRS']),
            g_mag=float(s['Gmag']),
            rp_mag=(
                float(s['RPmag'])
                if not isinstance(s['RPmag'], np.ma.core.MaskedConstant)
                else np.nan
            ),
        )
        session.add(source)

    session.commit()


def queue_to_write(sources):
    global session
    global waiting_sources

    for s in sources:
        waiting_sources.append(
            Source(
                source=s['DR2Name'][9:],
                catalog=GAIA_DR2,
                ra=float(s['RA_ICRS']),
                dec=float(s['DE_ICRS']),
                g_mag=float(s['Gmag']),
                rp_mag=(
                    float(s['RPmag'])
                    if not isinstance(s['RPmag'], np.ma.core.MaskedConstant)
                    else np.nan
                ),
            )
        )
    if len(waiting_sources) >= 30000:
        for _ in trange(len(waiting_sources), leave=False):
            session.add(waiting_sources.popleft())
        session.commit()


def write_checkpoint():
    # add remaining sources
    for _ in trange(len(waiting_sources), leave=False):
        session.add(waiting_sources.popleft())
    session.commit()

    # commit all WAL changes
    session.execute('PRAGMA wal_checkpoint;')


def download(target: SkyCoord, faint_limit: float = 21):
    sources = download_sources(target, faint_limit)
    print(f"[{target.ra}, {target.dec}] returned {len(sources)} sources")
    write_to_db(sources)


if __name__ == '__main__':
    open_session()
    target = SkyCoord(193.5 * u.deg, -60.5 * u.deg)  # Jewel Box
    # target = SkyCoord(165 * u.deg, -56 * u.deg)  # debug
    # target = SkyCoord(165.5 * u.deg, -55.5 * u.deg)  # debug
    # target = SkyCoord(0 * u.deg, 0 * u.deg)  # Null Island
    # target = SkyCoord(120 * u.deg, -30 * u.deg)  # somewhere South
    download(target, faint_limit=18.5)
