from glob import glob
import sys
import os

import subprocess
import tempfile

import pandas as pd
import numpy as np

from .. import settings
from .. import logging as logg
from ..DynTrack import DynTrack


def vector_field(
    DT: DynTrack, gridRes: int = 30, smooth: float = 0.5, copy: float = False
):
    """\
    Generate a grid vector field from track data.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    gridRes
        grid resolution in both horizontal and vertical axis.
    smooth
        Smooth parameter of the vfkm algorithm.
    copy
        Return a copy instead of writing to DT.

    Returns
    -------
    DT : :class:`dyntrack.DynTrack`
        if `copy=True` it returns or else add fields to `DT`:

        `.X`
            x coordinates of the grid.
        `.Y`
            y coordinates of the grid.
        `.u`
            x component of the vectors.
        `.v`
            y component of the vectors.

    """

    DT = DT.copy() if copy else DT

    tdata = DT.track_data

    allparents = np.unique(tdata["Parent"])
    allparents = allparents[~np.isnan(allparents)]
    ldata = list(
        map(
            lambda x: tdata[["Position X", "Position Y", "Time"]].loc[
                tdata.index[
                    tdata["Parent"].isin(
                        [x],
                    )
                ]
            ],
            [par for par in allparents],
        )
    )

    vfkm = settings.vfkm

    logg.info(
        f"Generating grid vector field with a {gridRes}x{gridRes} grid and a smoothing constrain of {smooth}",
        reset=True,
    )
    with tempfile.TemporaryDirectory() as tmp:
        # logg.hint("    Data temporary saved in "+tmp)
        init = [
            min(tdata["Position X"]),
            max(tdata["Position X"]),
            min(tdata["Position Y"]),
            max(tdata["Position Y"]),
            1,
            max(tdata["Time"]),
        ]
        with open(tmp + "/tracks", "w") as f:
            f.writelines(["%s " % item for item in init])
        for ld in ldata:
            ld.to_csv(tmp + "/tracks", mode="a", header=False, sep=" ", index=False)
            pd.DataFrame([0, 0, 0]).transpose().to_csv(
                tmp + "/tracks", header=False, sep=" ", mode="a", index=False
            )

        proc = subprocess.Popen(
            vfkm
            + " "
            + tmp
            + "/tracks "
            + str(gridRes)
            + " 1 "
            + str(smooth)
            + " "
            + tmp,
            stdout=subprocess.PIPE,
            shell=True,
        )
        (out, err) = proc.communicate()

        files_c = [f for f in glob(tmp + "/*curves_r_*", recursive=True)]
        files_v = [f for f in glob(tmp + "/*vf_r_*", recursive=True)]
        curves = pd.read_table(files_c[0], header=None, sep=" ")
        vect = pd.read_table(files_v[0], header=None, sep=" ", skiprows=1)

    gs = int(np.sqrt(vect.shape[0]))

    a = np.linspace(
        min(pd.concat(ldata)["Position X"]), max(pd.concat(ldata)["Position X"]), gs
    )
    b = np.linspace(
        min(pd.concat(ldata)["Position Y"]), max(pd.concat(ldata)["Position Y"]), gs
    )
    out = np.stack([each.ravel(order="C") for each in np.meshgrid(a, b)])

    u = vect[0].values.reshape(gs, gs)
    v = vect[1].values.reshape(gs, gs)
    X, Y = np.meshgrid(a, b)

    DT.X, DT.Y, DT.u, DT.v = X, Y, u, v

    logg.info("    finished", time=True, end=" " if settings.verbosity > 2 else "\n")
    logg.hint(
        "added \n"
        "    .X, x coordinates of the grid\n"
        "    .Y, y coordinates of the grid\n"
        "    .u, x component of the vectors\n"
        "    .v, y component of the vectors"
    )

    return DT if copy else None
