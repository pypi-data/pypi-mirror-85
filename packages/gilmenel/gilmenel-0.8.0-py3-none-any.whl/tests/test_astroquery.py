from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.utils import diff

from tests.mocks import _assert
from tests.mocks import expected
from tests.mocks import mock_query
from tests.mocks import mock_stars
from tests.mocks import MockSession

from gilmenel.astroquery import Local


class TestLocal:
    @expected(
        Table(
            rows=[
                ('', 270.57735, -30.0, 10, 11.0, 30),
                ('', 270.0, -29.5, 10, 11.0, 30.0),
                ('', 269.42265, -30.0, 10, 9.0, 30),
                ('', 270.0, -30.5, 10, 11.0, 30.0),
            ],
            names=('DR2Name', 'RA_ICRS', 'DE_ICRS', 'Gmag', 'RPmag', '_r',),
        )
    )
    @mock_query(mock_stars(270, -30, 10, 0.5, 1, 4))
    def test_query_region_defaults(self, monkeypatch, expected):
        monkeypatch.setattr("gilmenel.astroquery.create_engine", lambda _: None)
        monkeypatch.setattr("gilmenel.astroquery.sessionmaker", lambda **_: MockSession)

        coordinates = SkyCoord(270 * u.deg, -30 * u.deg)

        query = Local()
        result = query.query_region(coordinates, radius=0.5 * u.deg)[0]

        _assert(diff.report_diff_values(result, expected), True)

    @expected(
        Table(
            rows=[
                ('', 270.57735, -30.0, 10, 11.0, 30),
                ('', 270.0, -29.5, 10, 11.0, 30.0),
                ('', 269.42265, -30.0, 10, 9.0, 30),
                ('', 270.0, -30.5, 10, 11.0, 30.0),
            ],
            names=('DR2Name', 'RA_ICRS', 'DE_ICRS', 'Gmag', 'RPmag', '_r',),
        )
    )
    @mock_query(mock_stars(270, -30, 10, 0.5, 1, 4) + mock_stars(270, -30, 10, 0.6, 1, 4))
    def test_query_region_parameters(self, monkeypatch, expected):
        monkeypatch.setattr("gilmenel.astroquery.create_engine", lambda _: None)
        monkeypatch.setattr("gilmenel.astroquery.sessionmaker", lambda **_: MockSession)

        coordinates = SkyCoord(270 * u.deg, -30 * u.deg)

        query = Local(column_filters={"Gmag": "<=15",}, row_limit=100,)
        result = query.query_region(coordinates, radius=0.5 * u.deg)[0]

        _assert(diff.report_diff_values(result, expected), True)


if __name__ == '__main__':
    TestLocal().test_query_region_defaults()
    TestLocal().test_query_region_parameters()
