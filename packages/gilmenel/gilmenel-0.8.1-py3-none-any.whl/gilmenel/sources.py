import re

from typing import Optional

from astropy import units as u
from astropy.coordinates import SkyCoord
from numpy import cos

maspyr = u.mas / u.yr


class Star(object):
    def __init__(
        self,
        source_id: str,
        sky_coord: SkyCoord,
        instr_coord: Optional[SkyCoord] = None,
        radius: Optional[u.Quantity] = None,  # u.arcmin
        g_mag: Optional[float] = None,
        rp_mag: Optional[float] = None,
        merit: Optional[int] = None,
    ):
        self.source_id = str(source_id)  # a unique star identifier
        self.sky_coord = sky_coord  # the celestial position of the star in RA and Dec

        self.instr_coord = instr_coord  # the star position relative to the instrument
        self.radius = radius  # the distance from the instrument's origin to the star

        self.g_mag = g_mag  # star magnitude in green
        self.rp_mag = rp_mag  # star magnitude in red

        # at first, all sources have a merit of -1
        # as they pass each filter, the merit value increases
        # this will allow for operations in marginal conditions
        if merit is None:
            self.merit = -1
        else:
            self.merit = merit

    @property
    def ra(self):
        return self.sky_coord.ra

    @property
    def dec(self):
        return self.sky_coord.dec

    @property
    def pm_ra_cosdec(self):
        try:
            return self.sky_coord.pm_ra_cosdec
        except AttributeError:
            return self.sky_coord.pm_ra * cos(self.dec)
        except TypeError:  # pm_ra_cosdec value is not defined
            return 0 * u.mas / u.yr

    @property
    def pm_ra(self):
        try:
            return self.sky_coord.pm_ra
        except AttributeError:
            try:
                return self.sky_coord.pm_ra_cosdec / cos(self.dec)
            except TypeError:  # pm_ra_cosdec value is not defined
                return 0 * u.mas / u.yr
        except TypeError:  # pm_ra value is not defined
            return 0 * u.mas / u.yr

    @property
    def pm_dec(self):
        try:
            return self.sky_coord.pm_dec
        except AttributeError:  # pm_dec value is masked
            return 0 * u.mas / u.yr
        except TypeError:  # pm_dec not defined
            return 0 * u.mas / u.yr

    @property
    def obstime(self):
        return self.sky_coord.obstime

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Star):
            return (
                self.source_id == other.source_id
                and u.isclose(self.ra, other.ra, rtol=1e-6)
                and u.isclose(self.dec, other.dec, rtol=1e-6)
                and u.isclose(self.pm_ra, other.pm_ra, rtol=1e-2)
                and u.isclose(self.pm_dec, other.pm_dec, rtol=1e-2)
                and self.obstime == other.obstime
                and self.g_mag == other.g_mag
                and self.rp_mag == other.rp_mag
                and u.isclose(self.merit, other.merit, rtol=1e-3)
            )
        return False  # pragma: no cover

    def __repr__(self):
        # compile non-default parameters
        parameters = [
            f"\nStar("
            f"'{self.source_id}',"
            f" SkyCoord({self.ra.to_value(u.deg):.6f} * d,"
            f" {self.dec.to_value(u.deg):.6f} * d",
            None
            if self.pm_ra_cosdec == 0
            else f' pm_ra_cosdec={self.pm_ra_cosdec.to_value(maspyr):.1f} * maspyr',
            None
            if self.pm_dec == 0
            else f' pm_dec={self.pm_dec.to_value(maspyr):.1f} * maspyr',
            None
            if self.obstime is None
            else (
                f'obstime=datetime('
                f'{self.obstime.datetime.year}, '
                f'{self.obstime.datetime.month}, '
                f'{self.obstime.datetime.day}'
                f')'
            ),
            ")",
            None
            if self.radius is None
            else f'radius={self.radius.to_value(u.arcmin):.3f} * m',
            None if self.g_mag is None else f'g_mag={self.g_mag:.2f}',
            None if self.rp_mag is None else f'rp_mag={self.rp_mag:.2f}',
            None if self.merit == -1 else f'merit={self.merit:.3f}',
        ]
        # filter out defaults
        parameters = [each for each in parameters if each is not None]
        # combine
        parameters = ", ".join(parameters) + ")"

        return re.sub(r'0+ ', '0 ', parameters)  # replace extra zeros
