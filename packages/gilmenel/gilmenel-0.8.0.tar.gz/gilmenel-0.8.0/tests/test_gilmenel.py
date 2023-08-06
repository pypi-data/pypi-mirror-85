import pytest

from datetime import datetime

from astropy import units as u
from astropy.coordinates import SkyCoord
from freezegun import freeze_time

from gilmenel import gilmenel
from gilmenel.exceptions import GilmenelError
from gilmenel.instruments import BaseInstrument, GapInstrument
from gilmenel.sources import Star

from tests.mocks import _assert
from tests.mocks import catalogue
from tests.mocks import mock_star_objects
from tests.mocks import MockCatalog

d = u.deg
m = u.arcmin
s = u.arcsec
maspyr = u.mas / u.yr


class TestGilmenel:
    @staticmethod
    @pytest.fixture(autouse=True)
    def patch_catalog(monkeypatch):
        monkeypatch.setattr("gilmenel.gilmenel.Catalog", MockCatalog)

    def setup(self):
        class TestInstrument(BaseInstrument):
            def best_stars(self, stars):
                '''Return first star in list of stars that have been checked'''
                return [s for s in stars if s.merit > 0][:1]

        self.instr = TestInstrument(
            'Test',  # instr_name
            5 * m,  # instr_fov, arcminutes radius
            1 * m,  # inner_excl_distance, arcminutes
            20 * s,  # probe_fov, arcseconds
            10,  # bright limit
            20,  # faint limit
        )
        self.instr.point_to(SkyCoord(50 * d, -30 * d), 0 * d)

        class GuiderSingle(BaseInstrument):
            def best_stars(self, stars):
                '''Return first star in list of filtered stars'''
                return [s for s in stars if s.merit >= 4][:1]

        self.guider_single = GuiderSingle(
            'Single Probe',  # instr_name
            5 * u.arcmin - 20 * u.arcsec,  # instr_fov, arcminutes radius
            1.5 * u.arcmin,  # inner_excl_distance, arcminutes
            10 * u.arcsec,  # probe_fov, arcseconds
            8,  # bright limit
            14,  # faint limit
        )
        self.guider_single.point_to(SkyCoord(50 * d, 75 * d), 0 * d)

        class GuiderDual(GapInstrument):
            def best_stars(self, stars):
                '''Return first two stars in list of filtered stars'''
                return [s for s in stars if s.merit >= 4][:2]

        self.guider_dual = GuiderDual(
            'Two Probes',  # instr_name
            5 * u.arcmin - 22 * u.arcsec,  # instr_fov, arcminutes radius
            1.0 * u.arcmin,  # inner_excl_distance, arcminutes
            11 * u.arcsec,  # probe_fov, arcseconds
            9,  # bright limit
            15,  # faint limit
            0.5 * u.arcmin,  # arcmin
            0 * u.deg,  # degrees
        )
        self.guider_dual.point_to(SkyCoord(50 * d, 75 * d), 0 * d)

    @freeze_time("2020-01-01")
    @catalogue(mock_star_objects(50, -30, 15, 4 / 60, 1, 6, radius=True, g_mag=True, rp_mag=True, pm=True))
    def test_view_sky_proper_motions(self):
        results = gilmenel.view_sky(self.instr)
        expected = [
            Star(
                '',
                SkyCoord(
                    50.077341 * d,
                    -29.999375 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=4.019 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
            Star(
                '',
                SkyCoord(
                    50.038851 * d,
                    -29.941640 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=4.042 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
            Star(
                '',
                SkyCoord(
                    49.961871 * d,
                    -29.941640 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=4.024 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
            Star(
                '',
                SkyCoord(
                    49.923381 * d,
                    -29.999375 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=3.981 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
            Star(
                '',
                SkyCoord(
                    49.961871 * d,
                    -30.057110 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=3.958 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
            Star(
                '',
                SkyCoord(
                    50.038851 * d,
                    -30.057110 * d,
                    pm_ra_cosdec=250.0 * maspyr,
                    pm_dec=500.0 * maspyr,
                    obstime=datetime(2020, 1, 1),
                ),
                radius=3.977 * m,
                g_mag=15.00,
                rp_mag=14.50,
            ),
        ]

        _assert(results, expected)

    @catalogue([])
    def test_view_sky_failed(self):
        with pytest.raises(GilmenelError):
            assert gilmenel.view_sky(self.instr)

    def test_find_best_stars(self):
        stars = mock_star_objects(50, -30, 15, 4 / 60, 1, 6, instr_coord=True, radius=True, g_mag=True)
        results = gilmenel.find_best_stars(self.instr, stars)
        expected = [Star('', SkyCoord(50.076980 * d, -30.0 * d), radius=4.0 * m, g_mag=15.00, merit=4.000)]

        _assert(results, expected)
