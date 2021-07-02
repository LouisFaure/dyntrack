import matplotlib.image as mpimg
import pandas as pd
from ..DynTrack import DynTrack
from .. import __path__
import os


def load_data(csv_path, img_path, x_col, y_col, parent_col, time_col):
    """\
    Load data required for dynamical tracks analysis.

    Parameters
    ----------
    csv_path
        Path of the csv file.
    img_path
        Path of the img file.
    x_col
        Name of the x coordinate column.
    x_col
        Name of the y coordinate column.
    parent_col
        Name of the track ID column.
    time_col
        Name of the time/frame ID column.

    Returns
    -------
    :class:`dyntrack.DynTrack`
        A DynTrack object
    """

    tdata = pd.read_csv(csv_path)
    tdata = tdata[[x_col, y_col, parent_col, time_col]]
    tdata.columns = ["Position X", "Position Y", "Parent", "Time"]
    img = mpimg.imread(img_path) if img_path is not None else None

    return DynTrack(tdata, img)


def load_example():
    csv = os.path.join(__path__[0], "data", "tracks.csv")
    img = os.path.join(__path__[0], "data", "background.tiff")
    return load_data(csv, img, "Position X", "Position Y", "Parent", "Time")
