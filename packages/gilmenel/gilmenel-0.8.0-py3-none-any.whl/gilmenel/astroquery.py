import operator
import re

import numpy as np

from collections import OrderedDict

from astropy import units as u
from astropy.table import Table

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from gilmenel.exceptions import CatalogUnavailableError

from catalogue.models import Source


catalog_url = 'sqlite://file::memory:'


def to_astrotable(data, names):
    '''Return an Astropy Table of data'''
    if len(data) == 0:
        return Table(names=names)  # empty Table

    # if data elements are of type Base used in the ORM model
    rows = [d._asdict() for d in data]
    table = Table(data=rows, names=names)

    return table


class Local:
    '''
    A mocked Vizier class to replace vquery.query_region

    Usage:
        query = Local(
            columns=["_r", 'Source', 'RA_ICRS', 'DE_ICRS', '+Gmag'],
            column_filters={
                "Gmag": (f"<=15"),
            },
            row_limit=max_stars)

        results = query.query_region(instr.target,
                                     radius=instr.instr_fov,
                                     catalog="I/345/gaia2")[0]
    '''

    def __init__(
        self, columns=None, column_filters={'Gmag': "<=10"}, row_limit=5, **kwargs,
    ):

        self.columns = columns  # not used
        self.column_filters = column_filters
        self.row_limit = row_limit

        engine = create_engine(catalog_url)

        Session = sessionmaker(bind=engine)  # noqa
        self.session = Session()

    def query_region(self, target, radius=1 * u.arcmin, catalog="I/345/gaia2"):

        if catalog != "I/345/gaia2":
            raise CatalogUnavailableError(
                f"Specified catalog '{catalog}' is not available"
            )

        comps = {
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne,
            ">=": operator.ge,
            ">": operator.gt,
        }

        # transform to equatorial equivalent target
        equi_radius_ra = radius / np.cos(target.dec)

        ra_min = target.ra - equi_radius_ra
        ra_max = target.ra + equi_radius_ra

        dec_min = target.dec - radius
        dec_max = target.dec + radius

        # first do a box filter
        ra_filter = and_(
            Source.ra <= ra_max.to_value(u.deg), (Source.ra >= ra_min.to_value(u.deg))
        )
        dec_filter = and_(
            Source.dec <= dec_max.to_value(u.deg),
            (Source.dec >= dec_min.to_value(u.deg)),
        )

        # Gmag filter
        if 'Gmag' in self.column_filters:
            # remove comparators
            g_mag_number = re.sub(r'[!=<>]+', '', self.column_filters['Gmag'])
            # remove digits and points
            g_mag_comp = re.sub(r'[\d\.]+', '', self.column_filters['Gmag'])
            # limit queries by magnitude
            g_mag_filter = comps[g_mag_comp](Source.g_mag, g_mag_number)
        else:
            g_mag_filter = None

        query = self.session.query(Source)
        # query = query.with_entities(
        #     Source.source_name, Source.ra, Source.dec, Source.g_mag, Source.rp_mag,
        # )  # for testing, these are overridden in mocks.MockSouce
        query = query.filter(ra_filter)
        query = query.filter(dec_filter)
        query = query.filter(g_mag_filter)
        query = query.limit(self.row_limit)

        results = query.all()

        # inject regular grid for testing
        # from tests.mocks import MockSource
        # results = []
        # for ra in np.linspace(ra_min, ra_max, num=10):
        #     ra = ra.to_value(u.deg)
        #     for dec in np.linspace(dec_min, dec_max, num=10):
        #         dec = dec.to_value(u.deg)
        #         source = MockSource(int(ra * 100 + dec), (
        #             ra,
        #             dec,
        #             None,
        #             float(g_mag_number),
        #         ))
        #         results.append(source)

        # used for column renaming
        labels = OrderedDict(
            source='DR2Name',  # unique catalog designation
            ra='RA_ICRS',
            dec='DE_ICRS',
            g_mag='Gmag',
            rp_mag='RPmag',
        )

        # extract names of columns for correct ordering
        names = [k for k, _ in labels.items()]

        table = to_astrotable(results, names)

        # rename columns to match output from Vizier
        for old, new in labels.items():
            table.rename_column(old, new)

        # equator equivalent radius calculation
        target_ra = target.ra.to_value(u.deg)
        target_dec = target.dec.to_value(u.deg)
        candidates_ra = table['RA_ICRS']
        candidates_dec = table['DE_ICRS']

        ra_diff = target_ra - candidates_ra
        dec_scale = np.cos(np.radians(candidates_dec))

        # calculate radius in degrees
        table['_r'] = np.hypot(ra_diff * dec_scale, candidates_dec - target_dec)

        # degrees -> arcmin
        table['_r'] *= 60

        # round result to reasonable number of decimal places
        table['_r'] = np.around(table['_r'], 4)

        # then filter in place by radius
        mask = table['_r'] <= radius.to_value(u.arcmin)
        table = table[mask]

        # print(table)

        return [table]
