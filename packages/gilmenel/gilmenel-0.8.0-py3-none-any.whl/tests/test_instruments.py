import numpy as np
import pytest

from typing import List

from astropy import units as u
from astropy.coordinates import SkyCoord

from gilmenel.instruments import BaseInstrument, GapInstrument
from gilmenel.sources import Star

from tests.mocks import _assert
from tests.mocks import mock_star_objects

d = u.deg
m = u.arcmin
s = u.arcsec


class TestBaseInstrument:
    instr = None

    def setup(self):
        class TestInstrument(BaseInstrument):
            def best_stars(self, stars: List[Star]) -> List[Star]:
                raise NotImplementedError

        self.instr = TestInstrument(
            'Test',  # instr_name
            5 * m,  # instr_fov, arcminutes radius
            1 * m,  # inner_excl_distance, arcminutes
            20 * s,  # probe_fov, arcseconds
            10,  # bright limit
            20,  # faint limit
        )
        self.instr.point_to(SkyCoord(50 * d, -30 * d), 0 * d)

    def test_instantiate_instr(self):
        _assert(self.instr.inner_excl_shape, "circle")

        expected = SkyCoord(50 * d, -30 * d)
        _assert(self.instr.target.ra, expected.ra)
        _assert(self.instr.target.dec, expected.dec)

    def test_instr_best_stars_abstract(self):
        with pytest.raises(Exception):
            assert self.instr.best_stars([])

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (Star('', SkyCoord(50 * d + 0.5 * m, -30 * d), radius=0.5 * m), False),  # star too close
            (Star('', SkyCoord(50 * d + 1.0 * m, -30 * d), radius=1.0 * m), False),  # star too close
            (Star('', SkyCoord(50 * d + 2.0 * m, -30 * d), radius=2.0 * m), True),  # good star
            (Star('', SkyCoord(50 * d + 5.0 * m, -30 * d), radius=5.0 * m), True),  # good star
            (Star('', SkyCoord(50 * d + 10.0 * m, -30 * d), radius=10.0 * m), False),  # star too far
        ],
    )
    def test_star_available_circle(self, test_input, expected):
        print(test_input)
        _assert(self.instr.star_available(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (mock_star_objects(50, -30, 0, 0.5 / 60, 1, 1, instr_coord=True, radius=True)[0], False,),  # star too close
            (
                mock_star_objects(50, -30, 0, 0.999 / 60, 1, 1, instr_coord=True, radius=True)[0],
                False,
            ),  # star too close
            (mock_star_objects(50, -30, 0, 1.000 / 60, 1, 1, instr_coord=True, radius=True)[0], False,),  # border-line
            (
                mock_star_objects(50, -30, 0, 1.001 / 60, 1, 1, instr_coord=True, radius=True)[0],
                True,
            ),  # good star just
            (mock_star_objects(50, -30, 0, 2.0 / 60, 1, 1, instr_coord=True, radius=True)[0], True),  # good star
            (mock_star_objects(50, -30, 0, 5.0 / 60, 1, 1, instr_coord=True, radius=True)[0], True),  # good star
            (mock_star_objects(50, -30, 0, 10.0 / 60, 1, 1, instr_coord=True, radius=True)[0], False,),  # star too far
        ],
    )
    def test_star_available_square(self, test_input, expected):
        self.instr.inner_excl_shape = 'square'
        _assert(self.instr.star_available(test_input), expected)

    def test_star_available_not_implemented(self):
        self.instr.inner_excl_shape = 'does not exist'
        star = Star('', SkyCoord(50 * d, -30 * d), radius=2 * m)
        with pytest.raises(NotImplementedError):
            assert self.instr.star_available(star)

    def test_point_to_without_offset(self):
        target = SkyCoord(50 * d, -30 * d)
        self.instr.point_to(target, 0 * u.deg)

        print("Target:", self.instr.target)
        print("Offset:", self.instr.instr_offset)
        print("Origin:", self.instr.origin)

        assert self.instr.target == SkyCoord(50 * d, -30 * d)
        assert self.instr.instr_offset == SkyCoord(0, 0, unit=u.deg)
        assert self.instr.origin == SkyCoord(50 * d, -30 * d)

    def test_point_to_with_offset(self):
        target = SkyCoord(50 * d, -30 * d)
        offset = SkyCoord(180 * s, 0 * s)
        self.instr.point_to(target, 0 * u.deg, instr_offset=offset)

        print("Target:", self.instr.target)
        print("Offset:", self.instr.instr_offset)
        print("Origin:", self.instr.origin)

        assert self.instr.target == SkyCoord(50 * d, -30 * d)
        assert self.instr.instr_offset == SkyCoord(180 * u.arcsec, 0 * u.arcsec)
        assert (
            self.instr.origin.separation(SkyCoord((50 + 0.050 / np.cos(np.radians(-30))) * d, -30 * d)).to_value(
                u.arcsec
            )
            < 0.05  # arcsec
        )

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (  # check for inner and outer radii, including cos(dec) factor
                mock_star_objects(50, 75, 15, 5.5 / 60, 11, 4, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.354173 * d, 75.0 * d), radius=5.50 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 75.091667 * d), radius=5.50 * m, merit=0.000),
                    Star('', SkyCoord(49.645827 * d, 75.0 * d), radius=5.50 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 74.908333 * d), radius=5.50 * m, merit=0.000),
                    Star('', SkyCoord(50.321975 * d, 75.0 * d), radius=5.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.083333 * d), radius=5.0 * m, merit=1.000),
                    Star('', SkyCoord(49.678025 * d, 75.0 * d), radius=5.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.916667 * d), radius=5.0 * m, merit=1.000),
                    Star('', SkyCoord(50.289778 * d, 75.0 * d), radius=4.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.0750 * d), radius=4.50 * m, merit=1.000),
                    Star('', SkyCoord(49.710222 * d, 75.0 * d), radius=4.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.9250 * d), radius=4.50 * m, merit=1.000),
                    Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.066667 * d), radius=4.0 * m, merit=1.000),
                    Star('', SkyCoord(49.742420 * d, 75.0 * d), radius=4.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.933333 * d), radius=4.0 * m, merit=1.000),
                    Star('', SkyCoord(50.225383 * d, 75.0 * d), radius=3.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.058333 * d), radius=3.50 * m, merit=1.000),
                    Star('', SkyCoord(49.774617 * d, 75.0 * d), radius=3.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.941667 * d), radius=3.50 * m, merit=1.000),
                    Star('', SkyCoord(50.193185 * d, 75.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.050 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(49.806815 * d, 75.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.950 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.160988 * d, 75.0 * d), radius=2.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.041667 * d), radius=2.50 * m, merit=1.000),
                    Star('', SkyCoord(49.839012 * d, 75.0 * d), radius=2.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.958333 * d), radius=2.50 * m, merit=1.000),
                    Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.033333 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(49.871210 * d, 75.0 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.966667 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(50.096593 * d, 75.0 * d), radius=1.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 75.0250 * d), radius=1.50 * m, merit=1.000),
                    Star('', SkyCoord(49.903407 * d, 75.0 * d), radius=1.50 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, 74.9750 * d), radius=1.50 * m, merit=1.000),
                    Star('', SkyCoord(50.064395 * d, 75.0 * d), radius=1.0 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 75.016667 * d), radius=1.0 * m, merit=0.000),
                    Star('', SkyCoord(49.935605 * d, 75.0 * d), radius=1.0 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 74.983333 * d), radius=1.0 * m, merit=0.000),
                    Star('', SkyCoord(50.032198 * d, 75.0 * d), radius=0.50 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 75.008333 * d), radius=0.50 * m, merit=0.000),
                    Star('', SkyCoord(49.967802 * d, 75.0 * d), radius=0.50 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, 74.991667 * d), radius=0.50 * m, merit=0.000),
                ],
            ),
        ],
    )
    def test_filter_geometry(self, test_input, expected):
        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, 75, 15, 75 / 3600, 3, 1, instr_coord=True, g_mag=True),
                [
                    Star('', SkyCoord(50.080494 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                    Star('', SkyCoord(50.053663 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                    Star('', SkyCoord(50.026831 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                ],
            ),
            (
                mock_star_objects(50, 75, 15, 45 / 3600, 3, 1, instr_coord=True, g_mag=True),
                [
                    Star('', SkyCoord(50.048296 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.032198 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.016099 * d, 75.0 * d), g_mag=15.00),
                ],
            ),
            (
                mock_star_objects(50, 75, 15, 45 / 3600, 3, 1, instr_coord=True, g_mag=True)
                + mock_star_objects(50, 75, 13, 0, 1, 1, instr_coord=True, g_mag=True),
                [
                    Star('', SkyCoord(50.048296 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.032198 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.016099 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.0 * d, 75.0 * d), g_mag=13.00, merit=2.000),
                ],
            ),
        ],
    )
    def test_filter_nearby_pairs(self, test_input, expected):
        _assert(self.instr.filter_nearby_pairs(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                [
                    Star('', SkyCoord(51.0 * d, 75.0 * d), g_mag=25),
                    Star('', SkyCoord(50.8 * d, 75.0 * d), g_mag=20),
                    Star('', SkyCoord(50.6 * d, 75.0 * d), g_mag=15),
                    Star('', SkyCoord(50.4 * d, 75.0 * d), g_mag=10),
                    Star('', SkyCoord(50.2 * d, 75.0 * d), g_mag=5),
                ],
                [
                    Star('', SkyCoord(51.0 * d, 75.0 * d), g_mag=25, merit=-1),
                    Star('', SkyCoord(50.8 * d, 75.0 * d), g_mag=20, merit=4),
                    Star('', SkyCoord(50.6 * d, 75.0 * d), g_mag=15, merit=4),
                    Star('', SkyCoord(50.4 * d, 75.0 * d), g_mag=10, merit=4),
                    Star('', SkyCoord(50.2 * d, 75.0 * d), g_mag=5, merit=3),
                ],
            ),
        ],
    )
    def test_filter_magnitudes(self, test_input, expected):
        _assert(self.instr.filter_magnitudes(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, 75, 15, 6 / 60, 6, 1, instr_coord=True, radius=True, g_mag=True)
                + mock_star_objects(50, 75, 5, 4 / 60, 2, 3, instr_coord=True, radius=True, g_mag=True)
                + mock_star_objects(
                    50, 75, 21, 2 / 60, 2, 1, star_rotation=180, instr_coord=True, radius=True, g_mag=True
                ),
                [
                    Star('', SkyCoord(50.386370 * d, 75.0 * d), radius=6.0 * m, g_mag=15.00, merit=0.000),
                    Star('', SkyCoord(50.321975 * d, 75.0 * d), radius=5.0 * m, g_mag=15.00, merit=0.000),
                    Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=15.00, merit=1.000),
                    Star('', SkyCoord(50.193185 * d, 75.0 * d), radius=3.0 * m, g_mag=15.00, merit=4.000),
                    Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=15.00, merit=1.000),
                    Star('', SkyCoord(50.064395 * d, 75.0 * d), radius=1.0 * m, g_mag=15.00, merit=4.000),
                    Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.871210 * d, 75.057735 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.871210 * d, 74.942265 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.935605 * d, 75.028868 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.935605 * d, 74.971132 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                ],
            ),
        ],
    )
    def test_filter(self, test_input, expected):
        _assert(self.instr.filter(test_input), expected)


class TestGapInstrument:
    instr = None

    def setup(self):
        class TestInstrument(GapInstrument):
            pass

        self.instr = TestInstrument(
            'Test',  # instr_name
            5 * m,  # instr_fov, arcminutes radius
            1 * m,  # inner_excl_distance, arcminutes
            20 * s,  # probe_fov, arcseconds
            10,  # bright limit
            20,  # faint limit
            0.5 * m,  # slit_gap, arcminutes
            0 * d,  # slit angle
        )
        self.instr.point_to(SkyCoord(50 * d, -30 * d), 0 * d)

    def test_instantiate_instr(self):
        _assert(self.instr.inner_excl_shape, "circle")

        expected = SkyCoord(50 * d, -30 * d)
        _assert(self.instr.target.ra, expected.ra)
        _assert(self.instr.target.dec, expected.dec)

    def test_instr_best_stars_abstract(self):
        with pytest.raises(NotImplementedError):
            assert self.instr.best_stars([])

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, -30, 15, 3 / 60, 1, 4, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.057735 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -29.950 * d), radius=3.0 * m, merit=0.000),
                    Star('', SkyCoord(49.942265 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -30.050 * d), radius=3.0 * m, merit=0.000),
                ],
            ),
        ],
    )
    def test_star_available_gap_0(self, test_input, expected):
        self.instr.point_to(SkyCoord(50 * d, -30 * d), 0 * u.deg)

        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, -30, 15, 3 / 60, 1, 4, instr_rotation=30, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.057735 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -29.950 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(49.942265 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -30.050 * d), radius=3.0 * m, merit=1.000),
                ],
            ),
        ],
    )
    def test_star_available_gap_30(self, test_input, expected):
        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, -30, 15, 3 / 60, 1, 4, instr_rotation=60, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.057735 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -29.950 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(49.942265 * d, -30.0 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -30.050 * d), radius=3.0 * m, merit=1.000),
                ],
            ),
        ],
    )
    def test_star_available_gap_60(self, test_input, expected):
        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, -30, 15, 3 / 60, 1, 4, instr_rotation=90, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.057735 * d, -30.0 * d), radius=3.0 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, -29.950 * d), radius=3.0 * m, merit=1.000),
                    Star('', SkyCoord(49.942265 * d, -30.0 * d), radius=3.0 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, -30.050 * d), radius=3.0 * m, merit=1.000),
                ],
            ),
        ],
    )
    def test_star_available_gap_90(self, test_input, expected):
        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, -30, 15, 2 / 60, 3, 4, instr_coord=True, radius=True),
                [
                    Star('', SkyCoord(50.038490 * d, -30.0 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -29.966667 * d), radius=2.0 * m, merit=0.000),
                    Star('', SkyCoord(49.961510 * d, -30.0 * d), radius=2.0 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -30.033333 * d), radius=2.0 * m, merit=0.000),
                    Star('', SkyCoord(50.025660 * d, -30.0 * d), radius=1.333 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -29.977778 * d), radius=1.333 * m, merit=0.000),
                    Star('', SkyCoord(49.974340 * d, -30.0 * d), radius=1.333 * m, merit=1.000),
                    Star('', SkyCoord(50.0 * d, -30.022222 * d), radius=1.333 * m, merit=0.000),
                    Star('', SkyCoord(50.012830 * d, -30.0 * d), radius=0.667 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, -29.988889 * d), radius=0.667 * m, merit=0.000),
                    Star('', SkyCoord(49.987170 * d, -30.0 * d), radius=0.667 * m, merit=0.000),
                    Star('', SkyCoord(50.0 * d, -30.011111 * d), radius=0.667 * m, merit=0.000),
                ],
            ),
        ],
    )
    def test_filter_geometry(self, test_input, expected):
        _assert(self.instr.filter_geometry(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, 75, 15, 75 / 3600, 3, 1, instr_coord=True, g_mag=True),
                [
                    Star('', SkyCoord(50.080494 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                    Star('', SkyCoord(50.053663 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                    Star('', SkyCoord(50.026831 * d, 75.0 * d), g_mag=15.00, merit=2.000),
                ],
            ),
            (
                mock_star_objects(50, 75, 15, 45 / 3600, 3, 1, instr_coord=True, g_mag=True),
                [
                    Star('', SkyCoord(50.048296 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.032198 * d, 75.0 * d), g_mag=15.00),
                    Star('', SkyCoord(50.016099 * d, 75.0 * d), g_mag=15.00),
                ],
            ),
        ],
    )
    def test_filter_nearby_pairs(self, test_input, expected):
        _assert(self.instr.filter_nearby_pairs(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                [
                    Star('', SkyCoord(51.0 * d, 75.0 * d), g_mag=25, radius=1.0 * m),
                    Star('', SkyCoord(50.8 * d, 75.0 * d), g_mag=20, radius=0.8 * m),
                    Star('', SkyCoord(50.6 * d, 75.0 * d), g_mag=15, radius=0.6 * m),
                    Star('', SkyCoord(50.4 * d, 75.0 * d), g_mag=10, radius=0.4 * m),
                    Star('', SkyCoord(50.2 * d, 75.0 * d), g_mag=5, radius=0.2 * m),
                ],
                [
                    Star('', SkyCoord(51.0 * d, 75.0 * d), g_mag=25, merit=-1),
                    Star('', SkyCoord(50.8 * d, 75.0 * d), g_mag=20, merit=4),
                    Star('', SkyCoord(50.6 * d, 75.0 * d), g_mag=15, merit=4),
                    Star('', SkyCoord(50.4 * d, 75.0 * d), g_mag=10, merit=4),
                    Star('', SkyCoord(50.2 * d, 75.0 * d), g_mag=5, merit=3),
                ],
            ),
        ],
    )
    def test_filter_magnitudes(self, test_input, expected):
        _assert(self.instr.filter_magnitudes(test_input), expected)

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (
                mock_star_objects(50, 75, 15, 6 / 60, 6, 1, instr_coord=True, radius=True, g_mag=True)
                + mock_star_objects(50, 75, 5, 4 / 60, 2, 3, instr_coord=True, radius=True, g_mag=True)
                + mock_star_objects(
                    50, 75, 21, 2 / 60, 2, 1, star_rotation=180, instr_coord=True, radius=True, g_mag=True
                ),
                [
                    Star('', SkyCoord(50.386370 * d, 75.0 * d), radius=6.0 * m, g_mag=15.00, merit=0.000),
                    Star('', SkyCoord(50.321975 * d, 75.0 * d), radius=5.0 * m, g_mag=15.00, merit=0.000),
                    Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=15.00, merit=1.000),
                    Star('', SkyCoord(50.193185 * d, 75.0 * d), radius=3.0 * m, g_mag=15.00, merit=4.000),
                    Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=15.00, merit=1.000),
                    Star('', SkyCoord(50.064395 * d, 75.0 * d), radius=1.0 * m, g_mag=15.00, merit=4.000),
                    Star('', SkyCoord(50.257580 * d, 75.0 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.871210 * d, 75.057735 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.871210 * d, 74.942265 * d), radius=4.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(50.128790 * d, 75.0 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.935605 * d, 75.028868 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                    Star('', SkyCoord(49.935605 * d, 74.971132 * d), radius=2.0 * m, g_mag=5.00, merit=3.000),
                ],
            ),
        ],
    )
    def test_filter(self, test_input, expected):
        self.instr.point_to(SkyCoord(50 * d, 75 * d, frame='icrs'), 0 * d)

        _assert(self.instr.filter(test_input), expected)
