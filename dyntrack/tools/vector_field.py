from typing import Union
from glob import glob
import sys
import os

import subprocess
import tempfile

import pandas as pd
import numpy as np

import math
from scipy.stats import ranksums

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


import numba


@numba.stencil
def _local_var(x):
    mean = (
        x[-1, -1]
        + x[-1, 0]
        + x[-1, 1]
        + x[0, -1]
        + x[0, 0]
        + x[0, 1]
        + x[1, -1]
        + x[1, 0]
        + x[1, 1]
    ) // 9
    return np.sqrt(
        (
            (x[-1, -1] - mean) ** 2
            + (x[-1, 0] - mean) ** 2
            + (x[-1, 1] - mean) ** 2
            + (x[0, -1] - mean) ** 2
            + (x[0, 0] - mean) ** 2
            + (x[0, 1] - mean) ** 2
            + (x[1, -1] - mean) ** 2
            + (x[1, 0] - mean) ** 2
            + (x[1, 1] - mean) ** 2
        )
        // 9
    )


@numba.njit
def local_var(x):
    return _local_var(x)


def compute_angle(uv):
    base = [0, 1]
    unit_vector_1 = base / np.linalg.norm(base)
    unit_vector_2 = uv / np.linalg.norm(uv)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return math.degrees(angle)


def coordination_test(
    DT: DynTrack,
    return_stats: bool = False,
    return_data: bool = False,
    seed: Union[bool, int] = None,
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

    logg.info("Testing coordination of the vector field", reset=True)

    n_vals = len(DT.u.ravel())
    angles_obs = np.array(
        [compute_angle([DT.u.ravel()[i], DT.v.ravel()[i]]) for i in range(n_vals)]
    ).reshape(DT.X.shape)

    logg.info("    Local variance on observed angles", end="... ")
    var_obs = local_var(angles_obs)
    logg.info("done")

    if seed is not None:
        np.random.seed(seed)
    u = np.random.normal(scale=np.std(DT.u.ravel()), size=n_vals)
    v = np.random.normal(scale=np.std(DT.v.ravel()), size=n_vals)

    angles_rand = np.array(
        [compute_angle([u.ravel()[i], v.ravel()[i]]) for i in range(n_vals)]
    ).reshape(DT.X.shape)

    logg.info("    Local variance on randomly generated angles", end="... ")
    var_rand = local_var(angles_rand)
    logg.info("done")

    ret = ()

    stat, pval = ranksums(var_rand.ravel(), var_obs.ravel(), "greater")

    logg.info("    finished", time=True, end=" " if settings.verbosity > 2 else "\n")
    logg.info(f"Wilcoxon rank sum test results:\n    stat: {stat}\n    pval: {pval}")

    if return_stats:
        ret = (*ret, stat, pval)
    if return_data:
        ret = (*ret, angle_obs, angles_rand, var_obs, var_rand)

    if len(ret) > 0:
        return ret
