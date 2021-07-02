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
    ax: Union[Axes, None] = None,
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
    ax
        A matplotlib axes object.
    show
        Show the plot, do not return axis.
    **kwargs
        Arguments passed to :func:`matplotlib.pyplot.streamplot`.

    Returns
    -------
    :class:`matplotlib.axes.Axes` if `show=True`

    """

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            fig.set_tight_layout(True)

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

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="2%", pad=1)
        cbar = plt.colorbar(h.lines, ax=cax, ticks=[speed.min(), speed.max()])
        cbar.ax.set_yticklabels(["low", "high"])
        cbar.set_label("particle speed", fontsize=12)
        cax.axis("off")

        if show == False:
            return ax
        else:
            plt.show()
