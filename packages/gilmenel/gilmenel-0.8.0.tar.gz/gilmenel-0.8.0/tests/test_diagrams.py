import pytest

from astropy import units as u
from astropy.coordinates import SkyCoord

from gilmenel.diagrams import produce_ds9_region
from gilmenel.instruments import BaseInstrument, GapInstrument

from tests.mocks import _assert
from tests.mocks import expected
from tests.mocks import mock_star_objects
from tests.mocks import MockCatalog

d = u.deg
m = u.arcmin
s = u.arcsec


class TestDiagrams:
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

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 90.0" # text={1.5 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'circle 50.000000d 75.050000d 2" # text={10.00} color=green width=1\n'
        'circle 50.000000d 75.041667d 2" # text={10.00} color=green width=1\n'
        'circle 50.000000d 75.033333d 2" # text={10.00} color=green width=1\n'
        'circle 50.000000d 75.025000d 2" # text={10.00} color=red width=1\n'
        'circle 50.000000d 75.016667d 2" # text={10.00} color=red width=1\n'
        'circle 50.000000d 75.008333d 2" # text={10.00} color=red width=1\n'
        'circle 50.000000d 75.050000d 10" # text={best star} color=cyan width=2\n'
    )
    def test_produce_ds9_region_0_hrs_radial_vertical(self, expected):
        self.guider_single.point_to(SkyCoord(50 * u.deg, 75 * u.deg), -90 * u.deg)
        stars = mock_star_objects(50, 75, 10, 3 / 60, 6, 1, star_rotation=-90, g_mag=True)
        for star in stars[:3]:
            star.merit = 4
        for star in stars[3:]:
            star.merit = 0
        best_stars = [stars[0]]

        region = produce_ds9_region(self.guider_single, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_single.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 0")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 90.0" # text={1.5 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'circle 50.193185d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.160988d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.096593d 75.000000d 2" # text={10.00} color=red width=1\n'
        'circle 50.064395d 75.000000d 2" # text={10.00} color=red width=1\n'
        'circle 50.032198d 75.000000d 2" # text={10.00} color=red width=1\n'
        'circle 50.193185d 75.000000d 10" # text={best star} color=cyan width=2\n'
    )
    def test_produce_ds9_region_0_hrs_radial_horizontal(self, expected):
        self.guider_single.point_to(SkyCoord(50 * u.deg, 75 * u.deg), 0 * u.deg)
        stars = mock_star_objects(50, 75, 10, 3 / 60, 6, 1, g_mag=True)
        for star in stars[:3]:
            star.merit = 4
        for star in stars[3:]:
            star.merit = 0
        best_stars = [stars[0]]

        region = produce_ds9_region(self.guider_single, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_single.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 0")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 90.0" # text={1.5 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'circle 50.193185d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.096593d 75.043301d 2" # text={10.00} color=green width=1\n'
        'circle 49.903407d 75.043301d 2" # text={10.00} color=green width=1\n'
        'circle 49.806815d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 49.903407d 74.956699d 2" # text={10.00} color=green width=1\n'
        'circle 50.096593d 74.956699d 2" # text={10.00} color=green width=1\n'
        'circle 50.193185d 75.000000d 10" # text={best star} color=cyan width=2\n'
    )
    def test_produce_ds9_region_0_hrs(self, expected):
        self.guider_single.point_to(SkyCoord(50 * u.deg, 75 * u.deg), 0 * u.deg)
        stars = mock_star_objects(50, 75, 10, 3 / 60, 1, 6, g_mag=True)
        for star in stars[:]:
            star.merit = 4
        best_stars = [stars[0]]

        region = produce_ds9_region(self.guider_single, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_single.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 0")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 90.0" # text={1.5 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'circle 50.257580d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.742420d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.257580d 75.000000d 10" # text={best star} color=cyan width=2\n'
    )
    def test_produce_ds9_region_60_hrs(self, expected):
        self.guider_single.point_to(SkyCoord(50 * u.deg, 75 * u.deg), 60 * u.deg)
        stars = mock_star_objects(50, 75, 10, 4 / 60, 1, 6, g_mag=True)
        for star in stars[:]:
            star.merit = 4
        best_stars = [stars[0]]

        region = produce_ds9_region(self.guider_single, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_single.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 60")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 60.0" # text={1.0 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'box 50.0 75.0 1.0\' 10\' 0.0r # fill=0 color=red\n'
        'circle 50.257580d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.742420d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.257580d 75.000000d 10" # text={best star} color=cyan width=2\n'
        'circle 50.128790d 75.057735d 10" # text={best star} color=cyan width=2\n'
    )
    def test_produce_ds9_region_0_rss(self, expected):
        self.guider_dual.point_to(SkyCoord(50 * u.deg, 75 * u.deg), 0 * u.deg)
        stars = mock_star_objects(50, 75, 10, 4 / 60, 1, 6, g_mag=True)
        for star in stars[:]:
            star.merit = 4
        best_stars = stars[:2]

        region = produce_ds9_region(self.guider_dual, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_dual.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 0")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    @expected(
        'global color=white\n'
        'fk5\n'
        'circle 50.000000d 75.000000d 240" # text={4 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 300" # text={5 arcmin} color=green width=1\n'
        'circle 50.000000d 75.000000d 60.0" # text={1.0 arcmin} color=red width=1\n'
        'circle 50.000000d 75.000000d 10" # text={target} color=magenta width=3\n'
        'box 50.0 75.0 1.0\' 10\' 1.0471975511965976r # fill=0 color=red\n'
        'circle 50.257580d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 75.057735d 2" # text={10.00} color=green width=1\n'
        'circle 49.742420d 75.000000d 2" # text={10.00} color=green width=1\n'
        'circle 49.871210d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.128790d 74.942265d 2" # text={10.00} color=green width=1\n'
        'circle 50.257580d 75.000000d 10" # text={best star} color=cyan width=2\n'
        'circle 50.128790d 75.057735d 10" # text={best star} color=cyan width=2\n'
        ''
    )
    def test_produce_ds9_region_60_rss(self, expected):
        self.guider_dual.point_to(SkyCoord(50 * u.deg, 75 * u.deg), 60 * u.deg)
        stars = mock_star_objects(50, 75, 10, 4 / 60, 1, 6, g_mag=True)
        for star in stars[:]:
            star.merit = 4
        best_stars = stars[:2]

        region = produce_ds9_region(self.guider_dual, stars, list(best_stars))

        # with open('stars.reg', "w") as reg:
        #     reg.write(region)

        # # open ds9 and display region file
        # cmd = (f"ds9"
        #        f" -dsseso coord"
        #        f" \"{self.guider_dual.target.to_string('hmsdms', sep=':')}\""
        #        f" -geometry 1400x1200+50+0"
        #        f" -zoom 2"
        #        f" -regions stars.reg"
        #        f" -cmap Cool"
        #        f" -scale mode 99.0"
        #        f" -match frame wcs"
        #        f" -rotate 60")
        # import os
        # os.system(cmd)

        _assert(region, expected)

    # from gilmenel.sources import Star

    # # This test is for development purposes only.
    # @pytest.mark.parametrize(
    #     "stars, best_stars, expected",
    #     [
    #         (
    #             [
    #               Star('', SkyCoord(50.386370 * d, 75.0 * d), radius=6.0 * m, g_mag=15.00, merit=0.000),
    #                 Star('', SkyCoord(50.321975 * d, 75.0 * d), radius=5.0 * m, g_mag=15.00, merit=0.000),
    #                 Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=15.00, merit=1.000),
    #                 Star('', SkyCoord(50.193185 * d, 75.0 * d), radius=3.0 * m, g_mag=15.00, merit=4.000),
    #                 Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=15.00, merit=1.000),
    #                 Star('', SkyCoord(50.064395 * d, 75.0 * d), radius=1.0 * m, g_mag=15.00, merit=0.000),
    #                 Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
    #                 Star('', SkyCoord(49.871210 * d, 75.057735 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
    #                 Star('', SkyCoord(49.871210 * d, 74.942265 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
    #                 Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
    #                 Star('', SkyCoord(49.935605 * d, 75.028868 * d), radius=2.0 * m, g_mag=5.00, merit=0.000),
    #                 Star('', SkyCoord(49.935605 * d, 74.971132 * d), radius=2.0 * m, g_mag=5.00, merit=0.000),
    #             ],
    #             [],
    #             None,
    #         ),
    #     ],
    # )
    # def test_produce_ds9(self, stars, best_stars, expected):
    #     region = produce_ds9_region(self.guider_dual, stars, best_stars)

    #     with open('stars.reg', "w") as reg:
    #         reg.write(region)

    #     # open ds9 and display region file
    #     cmd = (
    #         f"ds9"
    #         f" -dsseso coord"
    #         f" \"{self.guider_dual.target.to_string('hmsdms', sep=':')}\""
    #         f" -geometry 1400x1200+50+0"
    #         f" -zoom 2"
    #         f" -regions stars.reg"
    #         f" -cmap Cool"
    #         f" -scale mode 99.0"
    #         f" -match frame wcs"
    #         f" -rotate 60"
    #     )
    #     import os

    #     os.system(cmd)

    #     assert 0
