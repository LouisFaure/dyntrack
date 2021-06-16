import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import warnings

from .utils import set_colorbar


def vector_field(
    X,
    Y,
    u,
    v,
    img,
    density=2,
    linewidth=1,
    arrowsize=1,
    arrowstyle="->",
    cmap="gnuplot",
    figsize=(7, 4),
    ax=None,
    show=True,
):

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            fig.set_tight_layout(True)

        ax.set_aspect("equal")
        ax.imshow(img, origin="lower")
        speed = np.sqrt(u ** 2 + v ** 2)
        h = ax.streamplot(
            X,
            Y,
            u,
            v,
            color=speed,
            density=density,
            linewidth=linewidth,
            arrowsize=arrowsize,
            arrowstyle=arrowstyle,
            cmap=cmap,
        )
        ax.axis("off")
        # ax.scatter(mouthpos["Position X"],mouthpos["Position Y"],zorder=3,c="white")

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
