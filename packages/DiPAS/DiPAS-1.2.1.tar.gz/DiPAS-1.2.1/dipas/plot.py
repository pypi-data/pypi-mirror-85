import bisect
from collections import UserList
import itertools as it
from typing import Sequence, Tuple, Union

from matchable import match, Spec
from matchable.spec import LastSeenWins
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.collections import PatchCollection
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from . import compute
from .elements import (CompoundElement, Element, Monitor, Kicker, HKicker, VKicker, SBend, RBend, Quadrupole, Sextupole,
                       Segment, ThinElement)


def plot_twiss(lattice: Segment, *, data: pd.DataFrame = None, figsize: Tuple[float, float] = (16, 12),
               top: Union[Sequence[str], str] = ('bx', 'by'), bottom: Union[Sequence[str], str] = ('dx',),
               fontsize: float = 12, hover: bool = True, min_width: float = 0.01, guide_lw: float = 0):
    """Plot Twiss parameters and lattice elements.

    Parameters
    ----------
    lattice : :class:`Segment`
        The lattice which will be visualized on the plot.
    data : pd.DataFrame
        Lattice functions such as returned by ``compute.twiss(lattice)['lattice']``; if None this command is used to
        generate the data.
    figsize : (float, float)
        The figure size in inches.
    top, bottom : str or list of str
        Columns in `data` which should be plotted on the top and bottom axis respectively.
    fontsize : float
        Fontsize of axes labels.
    hover, min_width, guide_lw
        See :func:`plot_lattice`.

    Returns
    -------
    fig
        The matplotlib figure.
    axes : 3-tuple
        The three axes of the figure (lattice, top, bottom).
    """
    if data is None:
        lattice.apply_unique_labels()
        data = compute.twiss(lattice)['lattice']

    if isinstance(top, str):
        top = (top,)
    if isinstance(bottom, str):
        bottom = (bottom,)

    fig, (ax_lat, ax_top, ax_bot) = create_top_lattice_figure(2, figsize=figsize)

    ax_top.spines['top'].set_visible(False)
    ax_top.spines['bottom'].set_linestyle('dashed')
    ax_top.spines['bottom'].set_linewidth(1.0)
    ax_top.spines['right'].set_visible(False)
    ax_bot.spines['top'].set_visible(False)
    ax_bot.spines['right'].set_visible(False)

    ax_top.set_ylabel('$' + ', '.join(LABEL_MAP[k] for k in top) + '$', fontsize=fontsize)
    ax_bot.set_ylabel('$' + ', '.join(LABEL_MAP[k] for k in bottom) + '$', fontsize=fontsize)
    ax_bot.set_xlabel('s [m]', fontsize=fontsize)
    ax_top.yaxis.set_tick_params(labelsize=fontsize)
    ax_bot.xaxis.set_tick_params(labelsize=fontsize)
    ax_bot.yaxis.set_tick_params(labelsize=fontsize)

    plot_lattice(ax_lat, lattice, guide_ax=(ax_top, ax_bot), guide_lw=guide_lw, hover=hover, min_width=min_width)
    ax_lat.set_ylim([-1.5 * MAX_HEIGHT, MAX_HEIGHT])  # Add some distance to ax_top.

    s_pos = list(it.accumulate(e.l.item() for e in lattice))
    s_map = {e.label: s for e, s in zip(lattice, s_pos)}
    s_pos_plot = data.index.map(s_map)
    for ax, labels in zip((ax_top, ax_bot), (top, bottom)):
        for label in labels:
            ax.plot(s_pos_plot, data[label], '-', label=f'${LABEL_MAP[label]}$')
        ax.legend()

    return fig, (ax_lat, ax_top, ax_bot)


def plot_lattice(ax, lattice: Segment, *, min_width: float = 0.01, guide_lw: float = 0, guide_ax: Sequence = (),
                 hover: bool = True):
    """Plot a layout of the given lattice on the given axis.

    Parameters
    ----------
    ax : Axes
        The axis used to plot the lattice.
    lattice : :class:`Segment`
        The lattice which will be plotted.
    min_width : float
        Minimum width for zero length elements.
    guide_lw : float
        Line width for the guiding lines which indicate lattice elements. The default is 0 which means no guiding lines
        will be visible, only when hovering over an element.
    guide_ax : list of Axes
        Additional axes on which to plot guiding lines for lattice elements.
    hover : bool
        If true, an event listener will be connected which shows the element label when hovering over an element.
    """
    ax.get_yaxis().set_visible(False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    all_patches = Spec.from_patterns({
        match(Element): _ZOrderList(zorder=10),
        match(Kicker): _ZOrderList(zorder=12),
        match(SBend): _ZOrderList(zorder=11),
        match(Quadrupole): _ZOrderList(zorder=11),
        match(Quadrupole).k1 == 0: _ZOrderList(zorder=10),
        match(Sextupole): _ZOrderList(zorder=11),
    })
    s_lines = _SLines(lw_off=guide_lw)
    s_pos = []
    s = 0
    for element in lattice:
        if isinstance(element, ThinElement):
            element = element.base
        element = element.element  # Possibly wrapped by AlignmentError.
        length = max(element.l.item(), min_width)
        patch_func = MAKE_PATCH.match(element)
        patch_config = PATCH_CONFIG.match(element)
        all_patches.match(element).append(patch_func(element, s, length, config=patch_config))
        s_lines.append([])
        for ax_ in (ax, *guide_ax):
            s_lines[-1].append(ax_.axvline(s + length/2, color='gray', lw=guide_lw, zorder=-1))
        s += length
        s_pos.append(s)  # Lattice functions are computed at exit of elements.
    for patch_list in all_patches.options.values():
        patch_list = Spec.unwrap(patch_list)
        if patch_list:
            ax.add_collection(PatchCollection(patch_list, match_original=True, zorder=patch_list.zorder))
    ax.set_xlim([0, s])
    ax.set_ylim([-MAX_HEIGHT, MAX_HEIGHT])
    ax.axhline(0, lw=0.5, color='gray', zorder=-1)

    if hover:
        fig = ax.figure
        hover_label = ax.annotate('', xy=(0, 0), xytext=(0, 0), textcoords='offset points',
                                  bbox=dict(boxstyle='round', fc='white'), zorder=50)
        hover_label.set_visible(False)

        def hover_listener(event):
            if event.inaxes == ax:
                visible = hover_label.get_visible()
                if event.xdata is not None:
                    index = bisect.bisect_left(s_pos, event.xdata)
                    hover_label.xy = event.xdata, event.ydata
                    hover_label.set_text(lattice[index].label)
                    hover_label.set_visible(True)
                    s_lines.highlight(index)
                    fig.canvas.draw_idle()
                elif visible:
                    hover_label.set_visible(False)
                    s_lines.highlight(None)
                    fig.canvas.draw_idle()
            else:
                hover_label.set_visible(False)
                s_lines.highlight(None)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', hover_listener)


def create_top_lattice_figure(nrows: int = 2,
                              *, figsize: Tuple[float, float] = None, height_ratios: Tuple[float, ...] = None):
    """Create a figure with axes layout such that an additional axis at the top is reserved for a lattice plot.

    Parameters
    ----------
    nrows : int
        The number of axes *excluding* the additional lattice axis at the top. E.g. ``nrows=2`` will create a figure
        with 3 axes where the top axis is reserved for the lattice plot (and has decreased height ratio).
    figsize : float, float
        The figure size in inches.
    height_ratios : tuple of float
        The height ratios for each of the axes *including* the additional lattice axis; i.e. this tuple should have
        ``nrows + 1`` items.

    Returns
    -------
    fig : Figure
        The created figure.
    axes : tuple of Axes
        The corresponding axes where ``axes[0]`` is the lattice axis.
    """
    if figsize is None:
        figsize = (16, 1.5 + nrows * 5.25)
    if height_ratios is None:
        height_ratios = (2.,) + nrows * (14 / nrows,)
    fig = plt.figure(figsize=figsize)
    spec = gridspec.GridSpec(nrows=nrows+1, ncols=1, height_ratios=height_ratios)
    ax_lat = fig.add_subplot(spec[0])
    axes = [ax_lat]
    for i in range(nrows):
        axes.append(fig.add_subplot(spec[i+1], sharex=ax_lat))
    fig.subplots_adjust(hspace=0)
    return fig, tuple(axes)


def _make_patch_default(e: Monitor, s: float, length: float, *, config: dict):
    return patches.Rectangle((s, -MAX_HEIGHT/2), length, MAX_HEIGHT, **config)


def _make_patch_kicker(e: Kicker, s: float, length: float, *, config: dict):
    s += length/2
    return patches.FancyArrowPatch((s, -MAX_HEIGHT/2), (s, MAX_HEIGHT/2), **config)


def _make_patch_quadrupole(e: Quadrupole, s: float, length: float, *, config: dict):
    return patches.Rectangle((s, 0), length, np.sign(e.k1.item())*MAX_HEIGHT, **config)


class _SLines(UserList):
    def __init__(self, other=None, *, lw_on=0.8, lw_off=0.1):
        super().__init__(other)
        self.last_highlighted = None
        self.lw_on = lw_on
        self.lw_off = lw_off

    def highlight(self, index):
        if index == self.last_highlighted:
            return
        if self.last_highlighted is not None:
            for line in self[self.last_highlighted]:
                line.set_linewidth(self.lw_off)
        if index is not None:
            for line in self[index]:
                line.set_linewidth(self.lw_on)
        self.last_highlighted = index


class _ZOrderList(UserList):
    def __init__(self, other=None, *, zorder=0):
        super().__init__(other)
        self.zorder = zorder


MAX_HEIGHT = 1.0
MAKE_PATCH = Spec.from_patterns({
    match(Element): _make_patch_default,
    match(CompoundElement): _make_patch_default,
    match(Kicker): _make_patch_kicker,
    match(HKicker): _make_patch_default,
    match(VKicker): _make_patch_default,
    match(Quadrupole): _make_patch_quadrupole,
    match(Quadrupole).k1 == 0: _make_patch_default,
})
PATCH_CONFIG = Spec.from_patterns({
    match(Element): dict(fc='none'),
    match(Monitor): dict(fc='darkgray'),
    match(Kicker): dict(arrowstyle='<->', mutation_scale=20),
    match(HKicker): LastSeenWins(dict(ec='dimgray', fc='white', lw=1)),
    match(VKicker): LastSeenWins(dict(ec='dimgray', fc='white', lw=1)),
    match(SBend): dict(fc='gold'),
    match(RBend): dict(fc='gold'),
    match(Quadrupole).k1 > 0: dict(fc='blue'),
    match(Quadrupole).k1 == 0: dict(fc='tab:gray', alpha=0.5),
    match(Quadrupole).k1 < 0: dict(fc='tab:red'),
    match(Sextupole): dict(fc='tab:green'),
})
LABEL_MAP = {
    'bx': r'\beta_x [m]',
    'by': r'\beta_y [m]',
    'ax': r'\alpha_x',
    'ay': r'\alpha_y',
    'dx': 'D_x [m]',
    'dy': 'D_y [m]',
    'dpx': 'D_{p_x}',
    'dpy': 'D_{p_y}',
    'mx': r'\mu_x [2\pi]',
    'my': r'\mu_y [2\pi]',
}
