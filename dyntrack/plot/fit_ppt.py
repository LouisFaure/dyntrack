from typing import Union, Sequence
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import simpleppt
from ..DynTrack import DynTrack


def fit_ppt(
    DT: DynTrack,
    times: Union[Sequence, None] = None,
    figsize: tuple = (7, 4),
    ax: Union[Axes, None] = None,
    show: bool = True,
):
    """\
    Plotting counterpart of `tl.fit_ppt`.

    Display all principal trees to reveal structure in trajectories.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    times
        set of timepoints/frames to plot, by default uses all.
    figsize
        Figure size.
    ax
        A matplotlib axes object.
    show
        Show the plot, do not return axis.

    Returns
    -------
    :class:`matplotlib.axes.Axes` if `show=True`

    """

    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        fig.set_tight_layout(True)

    tdata = DT.track_data

    times = tdata.Time.unique() if times is None else times
    ax.set_aspect("equal")
    i = 0
    for t in times:
        toproject = tdata.loc[tdata.Time == t, ["Position X", "Position Y"]]
        simpleppt.project_ppt(
            DT.ppts[i],
            toproject,
            ax=ax,
            plot_datapoints=False,
            alpha_nodes=0,
            alpha_seg=0.05,
            show=False,
        )
        i = i + 1

    if DT.img is not None:
        ax.imshow(DT.img, origin="lower")
    ax.axis("off")

    if show == False:
        return ax
    else:
        plt.show()
