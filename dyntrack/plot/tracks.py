from typing import Union
import matplotlib.pyplot as plt
import numpy as np
from ..DynTrack import DynTrack
from matplotlib.axes import Axes


def tracks(
    DT: DynTrack,
    figsize: tuple = (7, 4),
    ax: Union[Axes, None] = None,
    show: bool = True,
    **kwargs
):
    """\
    Plotting all single tracks.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    figsize
        Figure size.
    ax
        A matplotlib axes object.
    show
        Show the plot, do not return axis.
    **kwargs
        Arguments passed to :func:`matplotlib.pyplot.plot`.

    Returns
    -------
    :class:`matplotlib.axes.Axes` if `show=True`

    """

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        fig.set_tight_layout(True)

    ax.set_aspect("equal")
    if DT.img is not None:
        ax.imshow(DT.img, origin="lower")

    for t in DT.track_data.Parent.unique():
        ax.plot(
            DT.track_data.loc[DT.track_data.Parent == t, "Position X"],
            DT.track_data.loc[DT.track_data.Parent == t, "Position Y"],
            **kwargs
        )

    ax.axis("off")

    if show == False:
        return ax
    else:
        plt.show()
