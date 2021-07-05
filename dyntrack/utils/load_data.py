from typing import Union, Optional
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
from ..DynTrack import DynTrack
from .. import __path__
import os


def load_data(
    df: Union[pd.DataFrame, str],
    x_col: str,
    y_col: str,
    parent_col: str,
    time_col: str,
    img: Optional[Union[np.ndarray, str]] = None,
):
    """\
    Load data required for dynamical tracks analysis.

    Parameters
    ----------
    df
        Path of a csv file, or a :class:`pandas.DataFrame` object.
    x_col
        Name of the x coordinate column.
    x_col
        Name of the y coordinate column.
    parent_col
        Name of the track ID column.
    time_col
        Name of the time/frame ID column.
    img
        Path of an img file, or a :class:`numpy.ndarray`.

    Returns
    -------
    :class:`dyntrack.DynTrack`
        A DynTrack object
    """

    tdata = pd.read_csv(df) if type(df) is str else df
    tdata = tdata[[x_col, y_col, parent_col, time_col]]
    tdata.columns = ["Position X", "Position Y", "Parent", "Time"]
    img = mpimg.imread(img) if type(img) is str else img

    return DynTrack(tdata, img)


def load_example():
    csv = os.path.join(__path__[0], "data", "tracks.csv")
    img = os.path.join(__path__[0], "data", "background.tiff")
    return load_data(csv, "Position X", "Position Y", "Parent", "Time", img)
