from typing import Any, Union, Optional  # Meta
from typing import Mapping
import pandas as pd
import numpy as np


class DynTrack:
    def __init__(
        self,
        track_data: pd.DataFrame,
        img: np.ndarray,
        X: Optional[Union[np.ndarray, None]] = None,
        Y: Optional[Union[np.ndarray, None]] = None,
        u: Optional[Union[np.ndarray, None]] = None,
        v: Optional[Union[np.ndarray, None]] = None,
        ftle: Optional[Union[np.ndarray, None]] = None,
        ppts: Optional[Mapping[str, Any]] = None,
    ):

        self.track_data = track_data
        self.img = img
        self.X = X
        self.Y = Y
        self.u = u
        self.v = v
        self.ftle = ftle
        self.ppts = ppts

    def __repr__(self):
        dp = self.track_data.shape[0]
        tr = len(self.track_data.Parent.unique())

        descr = f"DynTrack object with the following data:"
        descr += f"\n    track_data ({tr} tracks, {dp} datapoints)"
        for attr in ["img", "X", "Y", "u", "v", "ftle", "ppts"]:
            dt = getattr(self, attr)
            if (dt is not None) & (attr != "ppts"):
                descr += f"\n    {attr} {dt.shape}"
            if (dt is not None) & (attr == "ppts"):
                descr += f"\n    {attr} ({len(dt)} ppt)"

        return descr
