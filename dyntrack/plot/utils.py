import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def set_colorbar(elem, ax, orientation="vertical", labelsize=None):
    cax = inset_axes(ax, width="2%", height="30%", loc=4, borderpad=0)
    cb = plt.colorbar(elem, orientation=orientation, cax=cax)
    cb.set_alpha(1)
    cb.ax.tick_params(labelsize=labelsize)
    cb.draw_all()
    cb.locator = MaxNLocator(nbins=3, integer=True)
    cb.update_ticks()
