import matplotlib.pyplot as plt
import numpy as np
import simpleppt


def fit_ppt(DT, times=None, figsize=(7, 4), ax=None, show=True, **kwargs):

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
    ax.imshow(DT.img, origin="lower")
    ax.axis("off")

    if show == False:
        return ax
    else:
        plt.show()
