from collections import namedtuple
from typing import (
    Any,
    List,
)

import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from astropy.visualization.wcsaxes import WCSAxes
from astropy import units as u
from astropy.coordinates import (
    Longitude,
    Latitude,
    SkyCoord,
)
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Patch
from matplotlib.transforms import Affine2D

from gilmenel.instruments import (
    Star,
    BaseInstrument,
    GapInstrument,
)

Circle9 = namedtuple('Circle9', 'x y radius width color label')
Box9 = namedtuple('Box9', 'x y width height rotation color label')


def create_drawing(
    instr: BaseInstrument, stars: List[Star], best_stars: List[Star]
) -> List[Any]:
    # TODO: add hooks to BaseInstrument class so that each instrument and
    # telescope can define its own debug output

    target_ra = instr.origin.ra.to_value(u.deg)
    target_dec = instr.origin.dec.to_value(u.deg)

    shapes = []

    # setup some fiducials as guides, these are specific to SALT
    # 4.0 arcmin
    shapes.append(Circle9(target_ra, target_dec, 240, 1, 'green', '4 arcmin'))
    # 5.0 arcmin
    shapes.append(Circle9(target_ra, target_dec, 300, 1, 'green', '5 arcmin'))

    # draw inner exclusion distance
    radius = instr.inner_excl_distance.to_value(u.arcmin)
    label = f"{radius} arcmin"
    shapes.append(Circle9(target_ra, target_dec, radius * 60, 1, 'red', label))

    # the actual target/centre of search; in pink so it stands out!
    shapes.append(Circle9(target_ra, target_dec, 10, 3, 'magenta', "target"))

    # a line near the target to make sure the slit gap width is OK
    if isinstance(instr, GapInstrument):
        gap_width = instr.slit_gap_radius.to_value(u.arcmin) * 2
        pa = instr.slit_gap_angle.to_value(u.rad)
        shapes.append(Box9(target_ra, target_dec, gap_width, 10, pa, 'red', ""))

    # TODO: make these colours editable too
    merit_colours = {
        -1: "grey",  # not processed
        0: "red",  # out of range
        1: "orange",  # nearby stars
        2: "yellow",  # too dim
        3: "yellow",  # too bright
        4: "green",  # good candidate
    }

    for s in stars:
        if s.merit > -1:  # exclude faint stars that were not evaluated
            # the colour reflects the star's suitability
            colour = merit_colours[s.merit]
            shapes.append(
                Circle9(
                    s.ra.to_value(u.deg),
                    s.dec.to_value(u.deg),
                    2,
                    1,
                    colour,
                    f"{s.g_mag:.2f}",
                )
            )

    # indicate the best stars
    for s in best_stars:
        if s is not None:
            shapes.append(
                Circle9(
                    s.ra.to_value(u.deg),
                    s.dec.to_value(u.deg),
                    10,
                    2,
                    'cyan',
                    "best star",
                )
            )

    return shapes


def produce_ds9_region(
    instr: BaseInstrument, stars: List[Star], best_stars: List[Star]
) -> str:
    # create a ds9 region to help visualise things - for testing purposes...
    # note this must be written to disk as a region file that must be loaded
    # from file by ds9 later with a system command

    def draw_circle(r, label, c, x, y, width):
        rline = (
            f"circle {x:.6f}d {y:.6f}d {r}\" "
            f"# text={{{label}}} color={c} width={width}\n"
        )
        return rline

    shapes = create_drawing(instr, stars, best_stars)

    output = "global color=white\n"
    output += "fk5\n"

    # draw shapes
    for sh in shapes:
        if isinstance(sh, Circle9):
            output += draw_circle(sh.radius, sh.label, sh.color, sh.x, sh.y, sh.width)

        elif isinstance(sh, Box9):
            output += (
                f"box {sh.x} {sh.y} {sh.width}' {sh.height}' {sh.rotation}r #"
                f" fill=0 color={sh.color}\n"
            )

    return output


def produce_png(
    instr: BaseInstrument,
    stars: List[Star],
    best_stars: List[Star],
    merit_colours={
        -1: "grey",  # not processed
        0: "#DD2C00",  # out of range   - Deep Orange A700
        1: "#FF9800",  # nearby stars   - Orange 500
        2: "#A1887F",  # too dim        - Brown 400
        3: "#FFFF00",  # too bright     - Yellow A200
        4: "#76FF03",  # good           - Light Green  A400
    },
    merit_names={
        -1: "Not processed",
        0: "Not reachable",
        1: "Double stars",
        2: "Too dim",
        3: "Too bright",
        4: "Good",
    },
) -> matplotlib.figure.Figure:
    def red_or_blue(star):
        # calculate an approximate colour for the star
        # ideal: C = BP - RP -> 0.5 = blue, 2.0 = green/grey, 3.5 = red

        if star.rp_mag:
            return star.g_mag - star.rp_mag - 0.9  # more positive = more red

        return 0

    def equitorial(target, coords):
        ''' Convert ICRS coordinates in degrees to
            equitorially equivalent coordinates
        '''
        delta_ra = coords.ra - target.ra
        delta_dec = coords.dec - target.dec

        # implement wrap-around at equinox
        if target.ra.deg > 300 and coords.ra.deg < 60:
            delta_ra += 360 * u.deg
        elif target.ra.deg < 60 and coords.ra.deg > 300:
            delta_ra -= 360 * u.deg

        delta_ra = delta_ra * np.cos(coords.dec.radian)

        return delta_ra.to_value(u.deg), delta_dec.to_value(u.deg)

    def icrs(target, coords):
        ''' Convert equitorially equivalent coordinates in degrees to
            ICRS coordinates
        '''
        ra = coords.ra / np.cos(coords.dec.radian) + target.ra
        dec = coords.dec + target.dec

        return ra.wrap_at(360 * u.deg).degree, dec.degree

    ra, dec = zip(*[equitorial(instr.origin, s) for s in stars])
    colour = [red_or_blue(s) for s in stars]
    g_mag = [s.g_mag for s in stars]
    merit = [s.merit for s in stars]

    # 'brightness' for star size on scatter plot
    # 20 -> 1
    # 15 -> 5
    # 10 -> 25
    # = 5 ** ((20 - g) / 5)
    brightness = [(3 ** ((20 - s.g_mag) / 5)) ** 2.0 for s in stars]
    halo = [(3 ** ((20 - s.g_mag) / 5)) ** 2.5 for s in stars]

    # Set up an affine transformation
    transform_target = Affine2D()
    transform_target.translate(instr.origin.ra.deg, instr.origin.dec.deg)

    # Set up an affine transformation
    transform_position_angle = Affine2D()
    transform_position_angle.rotate(instr.position_angle.to_value(u.rad))  # radians

    # Set up metadata dictionary
    coord_meta = {}
    coord_meta['name'] = 'lon', 'lat'
    coord_meta['type'] = 'longitude', 'latitude'
    coord_meta['wrap'] = 360, None
    coord_meta['unit'] = u.deg, u.deg
    coord_meta['format_unit'] = u.hour, u.deg

    fig = plt.figure(figsize=(10.4, 10))
    ax = WCSAxes(
        fig,
        [0.1, 0.07, 0.8, 0.9],
        aspect='equal',
        transform=transform_position_angle.inverted() + transform_target,
        coord_meta=coord_meta,
    )

    fig.add_axes(ax)
    ax.grid(color="#333333")
    ax.set_axisbelow(True)
    ax.set_facecolor('#111111')

    # star halo
    ax.scatter(
        ra,
        dec,
        c=colour,
        s=halo,
        alpha=0.4,
        marker='o',
        edgecolors="none",
        cmap=plt.cm.RdYlBu_r,
        vmin=-1.5,
        vmax=1.5,
        transform=transform_position_angle + ax.transData,
    )
    # star centers
    ax.scatter(
        ra,
        dec,
        c=colour,
        s=brightness,
        alpha=0.9,
        marker='D',
        # marker="$\u25b2$",
        edgecolors="none",
        cmap=plt.cm.RdYlBu_r,
        vmin=-1.5,
        vmax=1.5,
        label="Guide Stars",
        transform=transform_position_angle + ax.transData,
    )

    text_offset = 4 * 10 ** -3
    # the colour reflects the star's suitability
    for r, d, g, m in zip(ra, dec, g_mag, merit):
        if m > -1:
            ax.annotate(
                f"{g:.2f}",
                (r, d + text_offset),
                color=merit_colours[m],
                ha='center',
                xycoords=transform_position_angle + ax.transData,
            )

    # add fiducials

    # transform to equatorial equivalent coordinates
    one_arcmin = 1 / 60

    # add direction fiducials
    origin_radius = 5 / 60 * one_arcmin  # 5 arcseconds
    # North
    points = [
        (0, origin_radius),
        (0, 0.5 * one_arcmin),
    ]
    ax.add_artist(
        Line2D(
            *np.transpose(points),
            lw=0.5,
            color='cyan',
            transform=transform_position_angle + ax.transData,
        )
    )
    # East
    points = [
        (origin_radius, 0),
        (0.25 * one_arcmin, 0),
    ]
    ax.add_artist(
        Line2D(
            *np.transpose(points),
            lw=0.5,
            color='cyan',
            transform=transform_position_angle + ax.transData,
        )
    )
    # Origin
    ax.add_artist(Circle((0, 0), origin_radius, lw=0.5, color='cyan', fill=False,))

    # Draw telescope fiducials
    if instr.telescope is not None:
        for artist in instr.telescope.get_fiducials(ax.transData):
            ax.add_artist(artist).set_zorder(0.4)

    # Draw instrument fiducials
    for artist in instr.get_fiducials(ax.transData):
        ax.add_artist(artist).set_zorder(0.5)

    # Guide Stars
    text_offset = 4 * 10 ** -3
    for i, (r, d) in [
        (i, equitorial(instr.origin, s))
        for i, s in enumerate(best_stars)
        if s is not None
    ]:
        ax.add_artist(
            Circle(
                (r, d),
                10 / 60 * one_arcmin,
                color='cyan',
                fill=False,
                transform=transform_position_angle + ax.transData,
            )
        )
        probe = ['A', 'B']
        ax.annotate(
            f"Guide Star {probe[i]}",
            (r + text_offset, d),
            color='cyan',
            ha='right',
            xycoords=transform_position_angle + ax.transData,
        )

    # set axis limits
    ax.set_xlim(5.25 * one_arcmin, -5.25 * one_arcmin)
    ax.set_ylim(-5.25 * one_arcmin, 5.25 * one_arcmin)
    # set ticks
    ra_ticks = [
        Longitude(
            icrs(instr.origin, SkyCoord(t * u.deg, 0 * u.deg))[0], u.deg
        ).to_string(unit=u.hour, precision=0)
        for t in ax.get_xticks()
    ]
    ax.set_xticks(
        ax.get_yticks().tolist()
    )  # REMOVE IN THE FUTURE - PLACED TO AVOID WARNING - IT IS A BUG FROM MATPLOTLIB 3.3.1
    ax.set_xticklabels(ra_ticks)
    dec_ticks = [
        Latitude(
            icrs(instr.origin, SkyCoord(0 * u.deg, t * u.deg))[1], u.deg
        ).to_string(unit=u.deg, precision=0)
        for t in ax.get_yticks()
    ]
    ax.set_yticks(
        ax.get_yticks().tolist()
    )  # REMOVE IN THE FUTURE - PLACED TO AVOID WARNING - IT IS A BUG FROM MATPLOTLIB 3.3.1
    ax.set_yticklabels(dec_ticks)
    # label axes
    ax.set_xlabel(r'$RA$', fontsize=12)
    ax.set_ylabel(r'$Dec$', fontsize=12)
    ax.set_title("Guider Chart")

    # add legend
    legend_elements = [
        Patch(color=merit_colours[k], label=merit_names[k])
        for k in merit_colours.keys()
    ]
    ax.legend(
        handles=legend_elements[1:],  # skip 'Not processed'
        loc='upper center',
        bbox_to_anchor=(0.5, -0.05),
        ncol=len(legend_elements),
    )

    # output figure
    return plt
