from typing import Union
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import warnings
from ..DynTrack import DynTrack
from matplotlib.axes import Axes


def vector_field(
    DT: DynTrack,
    density: float = 2,
    linewidth: float = 1,
    arrowsize: float = 1,
    arrowstyle="->",
    cmap="gnuplot",
    figsize: tuple = (7, 4),
    show: bool = True,
    **kwargs
):
    """\
    Plotting counterpart of `tl.vector_field`.

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
    save
        Save plot to file
    **kwargs
        Arguments passed to :func:`matplotlib.pyplot.streamplot`.

    Returns
    -------
    :class:`matplotlib.axes.Axes` if `show=True`

    """

    fig, (ax, cax) = plt.subplots(
        1, 2, gridspec_kw={"width_ratios": [96, 4], "wspace": 0}
    )
    ax.set_aspect("equal")

    if DT.img is not None:
        ax.imshow(DT.img, origin="lower")
    speed = np.sqrt(DT.u ** 2 + DT.v ** 2)
    h = ax.streamplot(
        DT.X,
        DT.Y,
        DT.u,
        DT.v,
        color=speed,
        density=density,
        linewidth=linewidth,
        arrowsize=arrowsize,
        arrowstyle=arrowstyle,
        cmap=cmap,
        **kwargs
    )
    ax.axis("off")

    cbar = plt.colorbar(
        h.lines, ax=cax, ticks=[speed.min(), speed.max()], pad=0, fraction=1
    )
    cbar.ax.set_yticklabels(["low", "high"])
    cbar.set_label("particle speed", fontsize=12)
    cax.axis("off")

    if show == False:
        return (ax, cax)
    else:
        plt.show()
