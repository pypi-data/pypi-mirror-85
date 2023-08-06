from astropy import units as u
from astropy.coordinates import SkyCoord

from gilmenel.sources import Star

from tests.mocks import _assert

d = u.deg
m = u.arcmin
s = u.arcsec


class TestStar:
    def test_init(self):
        star = Star("star1", SkyCoord(23 * d, 17 * d), radius=2 * d, g_mag=9.5)

        _assert(star.source_id, "star1")
        _assert(star.sky_coord.ra.to_value(d), 23)
        _assert(star.sky_coord.dec.to_value(d), 17)
        _assert(star.radius, 2 * d)
        _assert(star.g_mag, 9.5)

    def test_eq(self):
        star_0 = Star("1", SkyCoord(23 * d, 17 * d), radius=2 * d, g_mag=9.5)
        star_1 = Star("1", SkyCoord(23 * d, 17 * d), radius=2 * d, g_mag=9.5)
        star_2 = Star("2", SkyCoord(23 * d, 17 * d), radius=2 * d, g_mag=9.5)

        star_3 = Star("3", SkyCoord(24 * d, 17 * d), radius=2 * d, g_mag=9.5)
        star_4 = Star("4", SkyCoord(24 * d, 17 * d), radius=2 * d, g_mag=9)

        _assert(star_0 == star_1, True)
        _assert(star_0 == star_2, False)
        _assert(star_0 == star_3, False)
        _assert(star_0 == star_4, False)
