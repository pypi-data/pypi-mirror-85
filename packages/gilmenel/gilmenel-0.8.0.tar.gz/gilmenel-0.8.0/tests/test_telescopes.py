from astropy import units as u

from gilmenel.instruments import BaseInstrument
from gilmenel.telescopes import Telescope


class DummyInstrument(BaseInstrument):
    def best_stars(self, stars):
        raise NotImplementedError


dummy = DummyInstrument(
    'Dummy',  # instr_name
    5 * u.arcmin,  # instr_fov, arcminutes radius
    1 * u.arcmin,  # inner_excl_distance, arcminutes
    20 * u.arcsec,  # probe_fov, arcseconds
    10,  # bright limit
    20,  # faint limit
)


class TestTelescope:
    def test_telescope_init(self):
        tel = Telescope("Test", fov=10 * u.arcmin)

        assert tel.name == "Test"
        assert tel.fov == 10 * u.arcmin

    def test_instruments_set(self):
        global dummy

        tel = Telescope("Test", fov=10 * u.arcmin, instruments={"dummy": dummy})
        assert tel._instruments == {"dummy": dummy}
        assert tel._instruments['dummy'].telescope == tel

    def test_instruments_get(self):
        global dummy

        tel = Telescope("Test", fov=10 * u.arcmin, instruments={"dummy": dummy})
        assert tel.instruments == {"dummy": dummy}
