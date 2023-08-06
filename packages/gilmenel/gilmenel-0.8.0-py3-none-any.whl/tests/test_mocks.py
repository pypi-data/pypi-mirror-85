from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.utils import diff

from gilmenel.sources import Star

from tests.mocks import _assert
from tests.mocks import catalogue
from tests.mocks import expected
from tests.mocks import mock_query
from tests.mocks import mock_star_objects
from tests.mocks import mock_stars
from tests.mocks import MockCatalog
from tests.mocks import MockSession


class TestMockStars:
    def test_mock_stars_single(self):
        stars = mock_stars(0, 0, 0, 1, 1, 1)
        expected = [('', 1.0, 0.0, 60.0, 0, -0.5)]

        _assert(stars, expected)

    def test_mock_star_objects_single(self):
        stars = mock_star_objects(0, 0, 0, 1, 1, 1)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg))]
        _assert(stars, expected)

        stars = mock_star_objects(0, 0, 0, 1, 1, 1, instr_coord=True)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg))]
        _assert(stars, expected)

        stars = mock_star_objects(0, 0, 0, 1, 1, 1, radius=True)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg), radius=60.0 * u.arcmin)]

        _assert(stars, expected)

        stars = mock_star_objects(0, 0, 0, 1, 1, 1, g_mag=True)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg), g_mag=0.0,)]
        _assert(stars, expected)

        stars = mock_star_objects(0, 0, 0, 1, 1, 1, rp_mag=True)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg), rp_mag=-0.50,)]
        _assert(stars, expected)

        stars = mock_star_objects(0, 0, 0, 1, 1, 1, instr_coord=True, radius=True, g_mag=True, rp_mag=True)
        expected = [Star('', SkyCoord(1.0 * u.deg, 0.0 * u.deg), radius=60.0 * u.arcmin, g_mag=0.0, rp_mag=-0.50,)]
        _assert(stars, expected)

    def test_mock_stars_two_in_ra(self):
        stars = mock_stars(0, 0, 0, 1, 1, 2)
        expected = [('', 1.0, 0.0, 60.0, 0, -0.5), ('', -1.0, 0.0, 60.0, 0, -0.5)]

        _assert(stars, expected)

    def test_mock_stars_four_in_unit_circle(self):
        stars = mock_stars(0, 0, 0, 1, 1, 4)
        expected = [
            ('', 1.0, 0.0, 60.0, 0, -0.5),
            ('', 0.0, 1.0, 60.0, 0, -0.5),
            ('', -1.0, 0.0, 60.0, 0, -0.5),
            ('', -0.0, -1.0, 60.0, 0, -0.5),
        ]

        _assert(stars, expected)

    def test_mock_stars_four_in_unit_circle_offset_ra_dec(self):
        stars = mock_stars(23, 17, 0, 1, 1, 4)
        expected = [
            ('', 24.045692, 17.0, 60.0, 0, -0.5),
            ('', 23.0, 18.0, 60.0, 0, -0.5),
            ('', 21.954308, 17.0, 60.0, 0, -0.5),
            ('', 23.0, 16.0, 60.0, 0, -0.5),
        ]

        _assert(stars, expected)

    def test_mock_stars_four_in_unit_circle_offset_rotate(self):
        stars = mock_stars(0, 0, 0, 1, 1, 4, rotate=45)
        expected = [
            ('', 0.707107, -0.707107, 60.0, 0, -0.5),
            ('', 0.707107, 0.707107, 60.0, 0, -0.5),
            ('', -0.707107, 0.707107, 60.0, 0, -0.5),
            ('', -0.707107, -0.707107, 60.0, 0, -0.5),
        ]

        _assert(stars, expected)

    def test_mock_stars_four_in_unit_circle_offset_ra_dec_rotate(self):
        stars = mock_stars(23, 17, 0, 1, 1, 4, rotate=45)
        expected = [
            ('', 23.739416, 16.292893, 60.0, 0, -0.5),
            ('', 23.739416, 17.707107, 60.0, 0, -0.5),
            ('', 22.260584, 17.707107, 60.0, 0, -0.5),
            ('', 22.260584, 16.292893, 60.0, 0, -0.5),
        ]

        _assert(stars, expected)

    def test_mock_stars_two_in_dec(self):
        stars = mock_stars(0, 0, 0, 1, 1, 4)
        stars = [stars[1]] + [stars[3]]
        expected = [('', 0.0, 1.0, 60.0, 0, -0.5), ('', -0.0, -1.0, 60.0, 0, -0.5)]

        _assert(stars, expected)

    def test_mock_stars_two_in_radius(self):
        stars = mock_stars(0, 0, 0, 2, 2, 1)
        expected = [('', 2.0, 0.0, 120.0, 0, -0.5), ('', 1.0, 0.0, 60.0, 0, -0.5)]

        _assert(stars, expected)

    def test_mock_stars_unit_rounding(self):
        stars = mock_stars(0, 0, 0, 1, 1, 3)
        expected = [
            ('', 1.0, 0.0, 60.0, 0, -0.5),
            ('', -0.5, 0.866025, 60.0, 0, -0.5),
            ('', -0.5, -0.866025, 60.0, 0, -0.5),
        ]

        _assert(stars, expected)

    def test_mock_stars_eight_in_two_rows_unit_circle(self):
        stars = mock_stars(0, 0, 0, 1, 2, 4)
        expected = [
            ('', 1.0, 0.0, 60.0, 0, -0.5),
            ('', 0.0, 1.0, 60.0, 0, -0.5),
            ('', -1.0, 0.0, 60.0, 0, -0.5),
            ('', -0.0, -1.0, 60.0, 0, -0.5),
            ('', 0.5, 0.0, 30.0, 0, -0.5),
            ('', 0.0, 0.5, 30.0, 0, -0.5),
            ('', -0.5, 0.0, 30.0, 0, -0.5),
            ('', -0.0, -0.5, 30.0, 0, -0.5),
        ]
        _assert(stars, expected)


class TestMockCatalog:
    @expected(
        Table(
            rows=[
                ('', 24.045692, 17.0, 60.0, 0, -0.5),
                ('', 23.0, 18.0, 60.0, 0, -0.5),
                ('', 21.954308, 17.0, 60.0, 0, -0.5),
                ('', 23.0, 16.0, 60.0, 0, -0.5),
            ],
            names=('DR2Name', 'RA_ICRS', 'DE_ICRS', '_r', 'Gmag', 'RPmag'),
            units=(None, u.deg, u.deg, u.arcmin, u.mag, u.mag),
        )
    )
    @catalogue(mock_stars(23, 17, 0, 1, 1, 4))
    def test_mock_catalog_mock_star_decorator(self, monkeypatch, expected):
        monkeypatch.setattr("gilmenel.gilmenel.Catalog", MockCatalog)
        from gilmenel.gilmenel import Catalog

        query = Catalog(columns=['Source'])
        result = query.query_region(SkyCoord(30 * u.deg, -72.635 * u.deg), radius=1 * u.deg, catalog="I/345/gaia2")[0]

        _assert(diff.report_diff_values(result, expected), True)


class TestMockSession:
    @expected(
        [
            {'source': '', 'ra': 24.045692, 'dec': 17.0, 'g_mag': 0, 'rp_mag': 0.0},
            {'source': '', 'ra': 23.0, 'dec': 18.0, 'g_mag': 0, 'rp_mag': 0.0},
            {'source': '', 'ra': 21.954308, 'dec': 17.0, 'g_mag': 0, 'rp_mag': 0.0},
            {'source': '', 'ra': 23.0, 'dec': 16.0, 'g_mag': 0, 'rp_mag': 0.0},
        ]
    )
    @mock_query(mock_stars(23, 17, 0, 1, 1, 4))
    def test_mock_catalog_mock_star_decorator(self, monkeypatch, expected):
        query = MockSession().query(None)
        query = query.filter(None)
        query = query.limit(None)

        results = query.all()

        results = [r._asdict() for r in results]

        _assert(results, expected)
