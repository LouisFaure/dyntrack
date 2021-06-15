import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


def FTLE(X,
         Y,
         u,
         v,
         ftle,
         img,
         cmap = "jet",
         density=2, 
         linewidth=.75,
         arrowsize=1, 
         arrowstyle='->', 
         color="white",
         figsize=(7,4),
         ax=None,
         show=True):
    
    if ax is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        fig.set_tight_layout(True)
        
    ax.set_aspect('equal')
    contf = ax.contourf(X, Y, ftle, extend='both',cmap=cmap)
    ax.streamplot(X, Y, u, v, density=2, linewidth=.75, 
                   arrowsize=.75, arrowstyle='->', color=color)
    #ax.scatter(mouthpos["Position X"],mouthpos["Position Y"],zorder=3,c="white")
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.xaxis.set_major_formatter(plt.NullFormatter())
    ax.axis("off")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)
    cbar = plt.colorbar(contf,cax=cax)
    cbar.set_label('$FTLE$', fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])
    
    
    if show==False:
        return ax
    else:
        plt.show()
