from typing import Union
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from ..DynTrack import DynTrack
from matplotlib.axes import Axes


def FTLE(
    DT: DynTrack,
    cmap="jet",
    density: float = 2,
    linewidth: float = 0.75,
    arrowsize: float = 1,
    arrowstyle: str = "->",
    color="white",
    figsize=(7, 4),
    show: bool = True,
    kwargs_for_countourf={},
    kwargs_for_streamplot={},
):
    """\
    Plotting counterpart of `tl.FTLE`.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    cmap
        Colormap used by :func:`matplotlib.pyplot.countourf`.
    density
        Density of arrows used by :func:`matplotlib.pyplot.streamplot`.
    linewidth
        Arrow line width used by :func:`matplotlib.pyplot.streamplot`.
    arrowsize
        Arrow size used by :func:`matplotlib.pyplot.streamplot`.
    arrowstyle
        Arrow style used by :func:`matplotlib.pyplot.streamplot`.
    color
        Arrow color used by :func:`matplotlib.pyplot.streamplot`.
    figsize
        Figure size.
    show
        Show the plot, do not return axis.
    **kwargs_for_contourf
        Arguments passed to :func:`matplotlib.pyplot.contourf`.
    **kwargs_for_streamplot
        Arguments passed to :func:`matplotlib.pyplot.streamplot`.

    Returns
    -------
    :class:`matplotlib.axes.Axes` if `show=True`

    """

    fig, (ax, cax) = plt.subplots(
        1, 2, gridspec_kw={"width_ratios": [96, 4], "wspace": 0}
    )
    ax.set_aspect("equal")

    contf = ax.contourf(
        DT.X, DT.Y, DT.ftle, extend="both", cmap=cmap, **kwargs_for_countourf
    )
    ax.streamplot(
        DT.X,
        DT.Y,
        DT.u,
        DT.v,
        density=2,
        linewidth=0.75,
        arrowsize=0.75,
        arrowstyle="->",
        color=color,
        **kwargs_for_streamplot
    )
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.axis("off")

    cbar = plt.colorbar(contf, ax=cax, pad=0, fraction=1)
    cbar.set_label("$FTLE$", fontsize=12)
    cax.axis("off")

    if show == False:
        return (ax, cax)
    else:
        plt.show()
