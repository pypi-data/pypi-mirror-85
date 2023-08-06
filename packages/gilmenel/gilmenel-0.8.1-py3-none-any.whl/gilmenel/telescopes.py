from typing import Dict, List, Optional

from astropy import units as u
from matplotlib.artist import Artist
from matplotlib.patches import Circle
from matplotlib.transforms import CompositeGenericTransform

from gilmenel.instruments import BaseInstrument


class Telescope:
    '''The base Gilmenel telescope class, useful as a single place to handle parameters
    that are common to all instruments within a telescope.'''

    def __init__(
        self,
        name: str,
        fov: u.arcmin,
        instruments: Optional[Dict[str, BaseInstrument]] = {},
    ):
        self.name = name
        self.fov = fov  # radius
        self.instruments = instruments

    @property
    def instruments(self):
        return self._instruments

    @instruments.setter
    def instruments(self, value: Dict[str, BaseInstrument]):
        # check if instruments input is a dictionary
        # required for setting the telescope of each instrument
        if not isinstance(value, Dict):
            raise TypeError(f"Instruments '{repr(value)}' is not a dictionary")

        self._instruments = value

        for each in self._instruments.values():
            each.telescope = self

    def get_fiducials(self, ax_transData: CompositeGenericTransform) -> List[Artist]:
        '''Return a list of Artists (lines, circles, patches, etc) to draw
        on Matplotlib diagrams'''

        # Telescope field of view
        telescope_fov = Circle(
            (0, 0), self.fov.to_value(u.deg), color='#444', fill=False
        )

        return [telescope_fov]
