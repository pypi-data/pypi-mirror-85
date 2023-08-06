import numpy as np
import pytest

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import MaskedColumn, Table

from gilmenel.sources import Star


# mocked gilmenel.Catalog class to replace query.query_region
class MockCatalog:
    def __init__(self, *args, **kwargs):
        pass

    def query_region(self, coordinates, **kwargs):
        global star_list
        # return an Astropy Table of star data
        if type(star_list) == Table:
            table = star_list
        elif type(star_list) == list:
            if len(star_list) == 0:
                return [[]]  # empty pseudo-Table
            elif type(star_list[0]) == Star:
                star_list = [
                    (
                        s.source_id,
                        s.ra.to_value(u.deg),
                        s.dec.to_value(u.deg),
                        s.radius.to_value(u.arcmin),
                        s.g_mag,
                        s.rp_mag,
                        s.pm_ra_cosdec.to_value(u.mas / u.yr),
                        s.pm_dec.to_value(u.mas / u.yr),
                    )
                    for s in star_list
                ]

            col_names = (
                'DR2Name',
                'RA_ICRS',
                'DE_ICRS',
                '_r',
                'Gmag',
                'RPmag',
                'pmRA',
                'pmDE',
            )
            col_units = (
                None,
                u.deg,
                u.deg,
                u.arcmin,
                u.mag,
                u.mag,
                u.mas / u.yr,
                u.mas / u.yr,
            )
            col_data = zip(*star_list)

            table = Table()
            for name, unit, data in zip(col_names, col_units, col_data):
                table[name] = MaskedColumn(name=name, unit=unit, data=data)
        else:
            raise Exception("Mock data not available")

        return [table]


def _assert(result, expected):
    # print debug output
    if isinstance(result, str):
        print("Received:")
        print(repr(result))
    else:
        print("Expected:")
        print(repr(expected))
        print("Received:")
        print(repr(result))

    assert result == expected

    print("----------")


def expected(expected):  # decorator-factory
    '''
    Calls decorated function with expected result.
    If the expected result is not supplied, an expected result is
    assembled from the query results.
    # Must be used before catalogue decorator.
    '''

    def decorate(func):
        # add expected as a parametrization
        # this allows fixtures to propagate (eg: monkeypatch)
        @pytest.mark.parametrize("expected", [expected])
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__wrapped__ = func

        return wrapper

    return decorate


def mock_stars(ra, dec, g_mag, max_radius, num_radial, num_angular, rotate=0):
    # ra, dec, max_radius, rotate in degrees
    # num_angular, steps_radial as number of stars
    # includes cos(dec) factor
    stars = []
    for radius in np.linspace(max_radius, 0, num=num_radial, endpoint=False):
        for angle in np.linspace(0, 360, num=num_angular, endpoint=False):
            # print(radius, rotate + angle)
            star_dec = dec + radius * np.sin(np.radians(-rotate + angle))
            star_ra = ra + radius * np.cos(np.radians(-rotate + angle)) / np.cos(
                np.radians(dec)
            )

            stars.append(
                (
                    '',  # alternative for incremental source_id numbering: len(stars)
                    np.round(star_ra, decimals=6),
                    np.round(star_dec, decimals=6),
                    radius * 60,  # this is returned in arcminutes
                    g_mag,
                    g_mag - 0.5,
                )
            )

    return stars


def mock_star_objects(
    ra,
    dec,
    *args,
    star_rotation=0,
    instr_rotation=0,
    instr_coord=False,
    radius=False,
    g_mag=False,
    rp_mag=False,
    pm=False
):
    origin_frame = SkyCoord(ra, dec, unit=u.deg).skyoffset_frame(
        rotation=instr_rotation * u.deg
    )
    stars = []
    for (
        star_id,
        star_ra,
        star_dec,
        star_radius,
        star_g_mag,
        star_rp_mag,
    ) in mock_stars(ra, dec, *args, rotate=star_rotation):
        star = Star(star_id, SkyCoord(star_ra, star_dec, unit=u.deg))

        # add parameters as required for each specific test
        if instr_coord:
            star.instr_coord = SkyCoord(star_ra, star_dec, unit=u.deg).transform_to(
                origin_frame
            )
        if radius:
            star.radius = star_radius * u.arcmin
        if g_mag:
            star.g_mag = star_g_mag
        if rp_mag:
            star.rp_mag = star_rp_mag
        if pm:
            star.sky_coord = SkyCoord(
                star_ra,
                star_dec,
                unit=u.deg,
                pm_ra_cosdec=250 * u.mas / u.yr,
                pm_dec=500 * u.mas / u.yr,
                frame='icrs',
                obstime='J2015.5',
            )

        stars.append(star)

    return stars


def catalogue(stars):
    '''
    Decorator to populate query results.
    Must be used after 'expected' decorator.
    '''

    def decorate(func):
        def wrapper(*args, **kwargs):
            global star_list

            star_list = stars

            return func(*args, **kwargs)

        wrapper.__wrapped__ = func

        return wrapper

    return decorate


class MockSession:
    '''
    A mocked Session object that, when queried, returns whatever is provided by
    mock_query below.
    '''

    def query(self, table):
        return self

    def with_entities(self, table):
        return self

    def filter(self, criteria):
        return self

    def limit(self, row_limit):
        return self

    def all(self):
        global sources

        return sources


class MockSource:
    def __init__(self, star):
        (source, ra, dec, radius, g_mag, rp_mag) = star
        self.source = {
            'source': source,
            'ra': ra,
            'dec': dec,
            'g_mag': g_mag,
            'rp_mag': g_mag * (0.9 if hash(ra) % 2 else 1.1),
        }

    def _asdict(self):
        return self.source


def mock_query(stars):
    '''
    Decorator to populate query results.
    Takes in list created by mock_stars and converts to sources
    Must be used after 'expected' decorator.
    '''

    def decorate(func):
        def wrapper(*args, **kwargs):
            global sources

            sources = [MockSource(s) for s in stars]

            return func(*args, **kwargs)

        wrapper.__wrapped__ = func

        return wrapper

    return decorate
