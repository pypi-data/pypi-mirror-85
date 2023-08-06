from collections import namedtuple

from astropy import units as u
from astropy.coordinates import SkyCoord
from numpy import array

from matplotlib.patches import Circle

from gilmenel.instruments import BaseInstrument, GapInstrument
from gilmenel.telescopes import Telescope

Frame = namedtuple('Frame', 'coord, frame')


class GuiderSingle(BaseInstrument):
    def best_stars(self, stars):
        return [s for s in stars if s.merit >= 4][:1]

    def get_fiducials(self, ax_transData):
        fiducials = [
            Circle((0, 0), 5 * self.one_arcmin, color='#00ff00', fill=False),  # SCAM
            Circle((0, 0), 4 * self.one_arcmin, color='#00ff00', fill=False),  # RSS
        ]

        return super().get_fiducials(ax_transData) + fiducials


fif = GuiderSingle(
    name='FIF',
    instr_fov=5 * u.arcmin - 20 * u.arcsec,  # iradius
    inner_excl_distance=1.5 * u.arcmin,
    nearby_limit=10 * u.arcsec,  # probe_fov
    bright_limit=8,
    faint_limit=14,
)


class GuiderDual(GapInstrument):
    def _score_star(self, star):
        '''
        rank each star linearly by magnitude and distance from exclusion zone
        favours bright stars at the edge of the field
        '''
        radius = (star.radius - self.inner_excl_distance) / (
            self.instr_fov - self.inner_excl_distance - self.nearby_limit
        )
        mag = 1 - (star.g_mag - self.bright_limit) / (
            self.faint_limit - self.bright_limit
        )
        return radius * mag

    def _group_by_side(self, stars):
        '''
        Groups stars into left and right of gap
        Left is more Westerly at  PA=0 and right is more Easterly at PA=0
        '''
        stars_left = [
            s for s in stars if s.merit >= 4 and s.instr_coord.lon.to_value(u.deg) > 0
        ]
        stars_right = [
            s for s in stars if s.merit >= 4 and s.instr_coord.lon.to_value(u.deg) < 0
        ]

        return stars_left, stars_right

    def _furthest_pair(self, stars_left, stars_right):
        '''
        compare distances between the top 3 stars on each list
        to get longest distance between a star pair
        '''
        furthest_pair = (0, None, None)  # seperation, s, t
        for s in stars_left[:3]:
            for t in stars_right[:3]:
                sep = s.instr_coord.separation(t.instr_coord)
                if sep > furthest_pair[0]:
                    furthest_pair = sep, s, t

        return furthest_pair

    def criteria(self, stars):
        self.filter_geometry(stars)
        self.filter_nearby_pairs([s for s in stars if s.merit == 1])
        self.filter_magnitudes([s for s in stars if s.merit == 2])

        # check if enough stars have been found
        if len([s for s in stars if s.merit >= 4]) > 6:
            return True

    def best_stars(self, stars):
        # split all stars into left and right
        stars_left, stars_right = self._group_by_side(stars)

        # sort in place by star score
        stars_left.sort(key=lambda s: self._score_star(s), reverse=True)
        stars_right.sort(key=lambda s: self._score_star(s), reverse=True)

        if len(stars_left) == 0 and len(stars_right) == 0:
            # no stars available
            return None, None
        elif len(stars_left) == 0:
            # only right star
            return None, stars_right[0]
        elif len(stars_right) == 0:
            # only left stars
            return stars_left[0], None
        else:
            # choose the stars with the greatest seperation
            _, star_left, star_right = self._furthest_pair(stars_left, stars_right)

        return star_left, star_right

    def get_fiducials(self, ax_transData):
        fiducials = [
            Circle((0, 0), 5 * self.one_arcmin, color='#00ff00', fill=False),  # SCAM
            Circle((0, 0), 4 * self.one_arcmin, color='#00ff00', fill=False),  # RSS
        ]

        return super().get_fiducials(ax_transData) + fiducials


origin_scam = Frame(array([2099, 2048.5]) * u.pix, 'SCAM spacial pixels')
origin_longslit = Frame(array([1955, 1800]) * u.pix, 'SCAM spacial pixels')

# pixels to arcsec
plate_scale_scam = 0.138 * u.arcsec / u.pix
offset_longslit = (origin_scam.coord - origin_longslit.coord) * plate_scale_scam

pfgs = GuiderDual(
    name='PFGS',
    instr_fov=5 * u.arcmin - 22 * u.arcsec,  # radius
    inner_excl_distance=0 * u.arcmin,
    nearby_limit=11 * u.arcsec,  # probe_fov
    bright_limit=9,
    faint_limit=16.5,
    slit_gap_radius=0.65 * u.arcmin,
    slit_gap_angle=0 * u.deg,  # degrees relative to PA
    instr_offset=SkyCoord(
        ra=offset_longslit[0],  # ra = X(horizontal)
        dec=offset_longslit[1],  # dec = Y(vertical)
    ),
)
pfgs.inner_excl_shape = 'square'


salt = Telescope(
    'Southern African Large Telescope',
    fov=5.5 * u.arcmin,
    instruments={'pfgs': pfgs, 'fif': fif},
)
