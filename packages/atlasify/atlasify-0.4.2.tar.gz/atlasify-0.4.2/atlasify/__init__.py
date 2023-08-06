"""
The atlasify package provides the method atlasify() which applies ATLAS style
to matplotlib plots.

Copyright (C) 2019-2020 Frank Sauerburger

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import os.path
from packaging import version

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.transforms import ScaledTranslation, IdentityTransform
import matplotlib.font_manager as font_manager

__version__ = '0.4.2'

def _setup_mpl():
    """
    Set sensible default values for matplotlib mainly concerning fonts.
    """
    # Add internal font directory
    font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts")
    font_files = font_manager.findSystemFonts(fontpaths=[font_dir])

    new_fonts = []
    try:
        # For mpl 3.2 and higher
        for font_file in font_files:
            # Resemble add_font
            font = mpl.ft2font.FT2Font(font_file)
            prop = font_manager.ttfFontProperty(font)
            new_fonts.append(prop)
    except AttributeError:
        # Legacy
        new_fonts = font_manager.createFontList(font_files)

    # Give precedence to fonts shipped in this package
    font_manager.fontManager.ttflist = new_fonts \
                                       + font_manager.fontManager.ttflist

    # Change font
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = ['Helvetica', 'Nimbus Sans',
                                       'Nimbus Sans L', 'Arial']

    # Disable Unicode minus signs for incompatible mpl versions
    if version.parse(mpl.__version__) < version.parse("3.3"):
        mpl.rcParams['axes.unicode_minus'] = False

_setup_mpl()

ATLAS = "ATLAS"
FONT_SIZE = 16
LABEL_FONT_SIZE = 16
SUB_FONT_SIZE = 12
LINE_SPACING = 1.2
PT = 1 / 72  # 1 point in inches

def enlarge_yaxis(axes, factor=1):
    """
    Enlarges the y-axis by the given factor. A factor of 1 has no effect. The
    lower boundary of the y-axis is not affected.
    """
    ylim = axes.get_ylim()
    y_upper = ylim[0] + (ylim[1] - ylim[0]) * factor
    axes.set_ylim((ylim[0], y_upper))


def _indent(outside):
    """
    Return the base point indent of the ATLAS badge.
    """
    return (2 if outside else 10) * PT

def _offset(outside, subtext):
    """
    Return the vertical offset of the base point of the ATLAS badge.
    """
    offset = -(5 + FONT_SIZE)  # Inside

    if outside:
        offset = 5  # Outside
        if isinstance(subtext, str):
            offset += LINE_SPACING * SUB_FONT_SIZE * (subtext.count("\n") + 1)

    return offset * PT

def atlasify_legend(axes):
    """
    Removes the frame from existing legend and enables legend if there are
    more then two handles. The location of a pre-exisitng legend is not
    changed.
    """
    handles, _ = axes.get_legend_handles_labels()
    legend = axes.get_legend()

    if legend is not None:
        # Remove frame from pre-existing legend
        legend.set_frame_on(False)
    elif len(handles) >= 2:
        # Automatically enable legend if there are more the two handles
        axes.legend(frameon=False, loc=1)

_ORIG_SET_XLABEL = mpl.axes.Axes.set_xlabel
def set_xlabel(axes, label, *args, **kwargs):
    """
    Set an x-label on a plot, and align it to the right. All arguments are
    forwarded.
    """
    kwargs_ = dict(x=1.0, ha="right")
    kwargs_.update(kwargs)
    _ORIG_SET_XLABEL(axes, label, *args, **kwargs_)

_ORIG_SET_YLABEL = mpl.axes.Axes.set_ylabel
def set_ylabel(axes, label, *args, **kwargs):
    """
    Set an y-label on a plot, and align it to the top. All arguments are
    forwarded.
    """
    kwargs_ = dict(y=1.0, ha="right")
    kwargs_.update(kwargs)
    _ORIG_SET_YLABEL(axes, label, *args, **kwargs_)

def monkeypatch_axis_labels():
    """
    Monkeypatch the `matplotlib.axes.Axes.set_(xy)labels` methods to have
    default alignment top and right.
    """
    mpl.axes.Axes.set_xlabel = set_xlabel
    mpl.axes.Axes.set_ylabel = set_ylabel

def atlasify(atlas=True, subtext=None, enlarge=None, axes=None, outside=False):
    """
    Applies the atlas style to the plot. If the atlas argument evaluates to
    True, the ATLAS badge is added. If the atlas argument is a non-empty
    string, the string is appended after the badge.

    If the subtext argument is given, this argument is added on the line
    below. Multiple lines are printed separately.

    The enlarge factor defines how fare the y-axis should be extended
    to accommodate for the badge.

    If the axes argument is None, the currently active axes is used.

    If the outside argument is True, the label will be placed above the plot.
    """
    if enlarge is None:
        enlarge = 1 + 0.3 * (not outside)

    if axes is None:
        axes = plt.gca()

    enlarge_yaxis(axes, enlarge)
    atlasify_legend(axes)

    axes.tick_params("both", which="both", direction="in")
    axes.tick_params("both", which="major", length=6)
    axes.tick_params("both", which="minor", length=3)
    axes.tick_params("x", which="both", top=True)
    axes.tick_params("y", which="both", right=True)
    axes.xaxis.set_minor_locator(AutoMinorLocator())
    axes.yaxis.set_minor_locator(AutoMinorLocator())


    trans_indent = ScaledTranslation(_indent(outside), 0,
                                     axes.figure.dpi_scale_trans)
    trans_top = ScaledTranslation(0, _offset(outside, subtext),
                                  axes.figure.dpi_scale_trans)

    trans_sub = IdentityTransform()

    if atlas:
        badge = axes.text(0, 1, ATLAS,
                          transform=axes.transAxes + trans_indent + trans_top,
                          fontdict={"size": FONT_SIZE,
                                    "style": "italic",
                                    "weight": "bold", })

        if isinstance(atlas, str):
            # Convert label with to dpi independent unit (pre-render)
            renderer = axes.figure.canvas.get_renderer()
            box = badge.get_window_extent(renderer)  # in display units
            box = axes.figure.dpi_scale_trans.inverted() \
                      .transform(box)  # in points
            badge_width = box[1][0] - box[0][0]

            trans_info = ScaledTranslation(0.23 * FONT_SIZE * PT + badge_width,
                                           0, axes.figure.dpi_scale_trans)
            axes.text(0, 1, atlas,
                      transform=axes.transAxes + trans_indent + trans_top +
                      trans_info, fontdict={"size": LABEL_FONT_SIZE, })

    if isinstance(subtext, str):
        trans_sub += ScaledTranslation(0, -LINE_SPACING * SUB_FONT_SIZE * PT,
                                       axes.figure.dpi_scale_trans)
        for line in subtext.split("\n"):
            axes.text(0, 1, line,
                      transform=axes.transAxes + trans_indent + trans_top +
                      trans_sub, fontdict={"size": SUB_FONT_SIZE, })
            trans_sub += ScaledTranslation(0, -LINE_SPACING * SUB_FONT_SIZE * PT,
                                           axes.figure.dpi_scale_trans)
