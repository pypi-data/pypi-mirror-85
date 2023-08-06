import warnings

from typing import List

from astropy import units as u
from astropy.coordinates import Distance, SkyCoord
from astropy.table import Table
from astropy.time import Time
from astroquery.vizier import Vizier

from gilmenel import astroquery as asterquery
from gilmenel.exceptions import NoStarsFoundError
from gilmenel.instruments import BaseInstrument
from gilmenel.sources import Star

Catalog = None


def init(use_local_catalogue=False, catalog_url=None):
    global Catalog

    if use_local_catalogue:
        Catalog = asterquery.Local
        asterquery.catalog_url = catalog_url
    else:
        Catalog = Vizier
        print("Using remote Vizier catalogue")


def query_catalogue(instr: BaseInstrument, max_stars: int = -1) -> Table:
    # Query the GAIA DR2 vizier catalogue (catalogue identifier: I/345/gaia2)
    # The '+' in "+Gmag" sorts the list by the brightest first, which is useful
    # for us later when it comes to picking the best candidate stars.

    # Includes proper motion of stars
    global Catalog

    query = Catalog(
        columns=['DR2Name', 'RA_ICRS', 'DE_ICRS', 'pmRA', 'pmDE', '+Gmag', 'RPmag'],
        column_filters={"Gmag": (f"<={instr.faint_limit + 2:.2f}")},
        row_limit=max_stars,
    )
    field_of_view = (
        instr.telescope.fov if instr.telescope is not None else instr.instr_fov
    )
    results = query.query_region(
        instr.origin, radius=field_of_view, catalog="I/345/gaia2"
    )[0]

    # if we find no stars in the field, raise an error
    if len(results) == 0:
        raise NoStarsFoundError(
            f"No stars returned in field "
            f"'{instr.origin.to_string(style='hmsdms')}' "
            f"with radius {instr.instr_fov:.2f}"
        )
    else:
        # print(results)
        return results


def create_stars_from_table(instr: BaseInstrument, results: Table) -> List[Star]:
    # replace unavailable (masked) proper motions with 0
    results['pmRA'] = results['pmRA'].filled(0)
    results['pmDE'] = results['pmDE'].filled(0)

    # obstime of 'J2015.5' is specfic to GAIA DR2:
    # https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/
    # chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html
    sky_coords = SkyCoord(
        results['RA_ICRS'],
        results['DE_ICRS'],
        pm_ra_cosdec=results['pmRA'],
        pm_dec=results['pmDE'],
        frame='icrs',
        obstime='J2015.5',
        distance=Distance(1, u.pc),  # close by, almost to Proxima Centauri
        # distance parameter prevents ErfaWarning:
        # ERFA function "pmsafe" yielded 6 of "distance overridden (Note 6)"
    )

    # immediately perform proper motion calculation
    obstime_now = Time.now()
    with warnings.catch_warnings():
        # ignore warning:
        # ErfaWarning:ERFA function "pmsafe" yielded 6 of "distance overridden (Note 6)"
        warnings.simplefilter("ignore")
        sky_coords = sky_coords.apply_space_motion(obstime_now)

    # set star coordinates relative to instrument frame
    instr_coords = sky_coords.copy().transform_to(instr.instr_frame)
    radii = instr.origin.separation(instr_coords)

    stars = [
        Star(
            source_id=row['DR2Name'],
            sky_coord=sky_coord,
            g_mag=row['Gmag'],
            rp_mag=row['RPmag'],
            instr_coord=instr_coord,
            radius=radius,
        )
        for row, sky_coord, instr_coord, radius in zip(
            results, sky_coords, instr_coords, radii
        )
    ]

    return stars


def view_sky(instr: BaseInstrument, max_stars: int = -1) -> List[Star]:
    results = query_catalogue(instr, max_stars)
    stars = create_stars_from_table(instr, results)

    return stars


def find_best_stars(instr: BaseInstrument, stars: List[Star]) -> List[Star]:
    '''
    Return the best stars as defined by the instrument's best_stars function
    '''
    stars = instr.filter(stars)

    return instr.best_stars(stars)
