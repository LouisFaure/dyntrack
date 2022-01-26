from typing import Union
from glob import glob
import sys
import os

import subprocess
import tempfile

import pandas as pd
import numpy as np
import sys
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

    vfkm = settings.vfkm
    if not os.path.exists(vfkm):
        raise Exception(
            "vfkm binary not detected, check dyntrack installation!\n" "path: %s" % vfkm
        )

    DT = DT.copy() if copy else DT

    tdata = DT.track_data

    allparents = np.unique(tdata["Parent"])
    allparents = allparents[~np.isnan(allparents)]
    ldata = [group.iloc[:, [0, 1, 3]] for _, group in tdata.groupby("Parent")]

    logg.info(
        f"Generating grid vector field with a {gridRes}x{gridRes} grid and a smoothing constrain of {smooth}",
        reset=True,
    )
    with tempfile.TemporaryDirectory() as tmp:
        # logg.hint("    Data temporary saved in "+tmp)
        init = [
            np.floor(tdata["Position X"].min()),
            np.ceil(tdata["Position X"].max()),
            np.floor(tdata["Position Y"].min()),
            np.ceil(tdata["Position Y"].max()),
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

        command = [vfkm, tmp + "/tracks", str(gridRes), "1", str(smooth), tmp]

        result = subprocess.run(
            command, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print(result.stdout.decode("utf-8"), file=sys.stdout, end="")
            print(result.stderr.decode("utf-8"), file=sys.stderr, end="")
            raise subprocess.CalledProcessError(1, cmd=command, stderr=result.stderr)

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
    DT_B: Union[None, DynTrack] = None,
    alternative: Union[str, None] = None,
    return_stats: bool = False,
    return_data: bool = False,
    seed: Union[bool, int] = None,
):

    """\
    Perform a coordination test on the data.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    DT_B
        Another :class:`dyntrack.DynTrack` object to compare with.
        If not specified, the comparison will be done with a random vector field.
    alternative
        if None, will set to `greater` if comparing to randomized vectors, to `two-sided` if not.
    return_stats
        Return statistics.
    return_data
        Return data use for the statistics.
    copy
        Return a copy instead of writing to DT.

    Returns
    -------
    tuple of results and/or data depedning on parameters: `return_stats` & `return_data`

    """
    if alternative is None:
        alternative = "greater" if DT_B is None else "two-sided"
    logg.info("Testing coordination of the vector field (%s)" % alternative, reset=True)

    n_vals = len(DT.u.ravel())
    angles_A = np.array(
        [compute_angle([DT.u.ravel()[i], DT.v.ravel()[i]]) for i in range(n_vals)]
    ).reshape(DT.X.shape)

    logg.info("    Local variance on observed angles", end="... ")
    var_A = local_var(angles_A)
    logg.info("done")

    if DT_B is None:
        logg.info("    Local variance on randomly generated angles", end="... ")
        if seed is not None:
            np.random.seed(seed)
        u = np.random.normal(scale=np.std(DT.u.ravel()), size=n_vals)
        v = np.random.normal(scale=np.std(DT.v.ravel()), size=n_vals)
    else:
        logg.info("    Local variance on second observations angles", end="... ")
        u, v = DT_B.u, DT_B.v

    angles_B = np.array(
        [compute_angle([u.ravel()[i], v.ravel()[i]]) for i in range(n_vals)]
    ).reshape(DT.X.shape)

    var_B = local_var(angles_B)
    logg.info("done")

    var_A[0, :] = np.nan
    var_A[:, 0] = np.nan
    var_A[var_A.shape[0] - 1, :] = np.nan
    var_A[:, var_A.shape[1] - 1] = np.nan

    var_B[0, :] = np.nan
    var_B[:, 0] = np.nan
    var_B[var_B.shape[0] - 1, :] = np.nan
    var_B[:, var_B.shape[1] - 1] = np.nan

    stat, pval = ranksums(var_B.ravel(), var_A.ravel(), alternative)

    logg.info("    finished", time=True, end=" " if settings.verbosity > 2 else "\n")
    logg.info(f"Wilcoxon rank sum test results:\n    stat: {stat}\n    pval: {pval}")

    ret = ()
    if return_stats:
        ret = (*ret, stat, pval)
    if return_data:
        ret = (
            *ret,
            angles_A,
            angles_B,
            var_A,
            var_B,
            u.reshape(DT.u.shape),
            v.reshape(DT.v.shape),
        )

    if len(ret) > 0:
        return ret
