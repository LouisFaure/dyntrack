import numpy as np
from .. import logging as logg
from .. import settings
from ..utils.FTLE import *
from ..DynTrack import DynTrack


def get_traj(X, Y, u, v, integration_time, dt, verbose=True):
    """Returns the FTLE particle trajectory, faster approach

    Arguments
    ---------
    x, y -- mesh grid coordinates
    dt -- integral time step
    """

    N = np.shape(X[:, 1])[0]
    x = X[0, :]
    y = Y[:, 0]

    xy = np.array(np.meshgrid(x, y)).T.reshape(-1, 2).tolist()
    xy = list(map(np.array, xy))

    # res=np.zeros(xy.shape)
    res = np.apply_along_axis(integrate, 1, xy, integration_time, dt, X, Y, u, v)
    # res=np.array(p_map(integrate, xy,disable=False))

    return res[:, 0].reshape(N, N).T, res[:, 1].T.reshape(N, N).T


def get_ftle(traj_x, traj_y, X, Y, integration_time):
    """Returns the FTLE scalar field

    Mostly adapted from Steven's FTLE code (GitHub user stevenliuyi)

    Arguments
    ---------
    traj_x, traj_y -- The trajectories of the FTLE particles
    X, Y -- Meshgrid
    integration_time -- the duration of the integration time

    """

    N = np.shape(X[:, 0])[0]
    ftle = np.zeros((N, N))

    for i in range(0, N):
        for j in range(0, N):
            # index 0:left, 1:right, 2:down, 3:up
            xt = np.zeros(4)
            yt = np.zeros(4)
            xo = np.zeros(2)
            yo = np.zeros(2)

            if i == 0:
                xt[0] = traj_x[j][i]
                xt[1] = traj_x[j][i + 1]
                yt[0] = traj_y[j][i]
                yt[1] = traj_y[j][i + 1]
                xo[0] = X[j][i]
                xo[1] = X[j][i + 1]
            elif i == N - 1:
                xt[0] = traj_x[j][i - 1]
                xt[1] = traj_x[j][i]
                yt[0] = traj_y[j][i - 1]
                yt[1] = traj_y[j][i]
                xo[0] = X[j][i - 1]
                xo[1] = X[j][i]
            else:
                xt[0] = traj_x[j][i - 1]
                xt[1] = traj_x[j][i + 1]
                yt[0] = traj_y[j][i - 1]
                yt[1] = traj_y[j][i + 1]
                xo[0] = X[j][i - 1]
                xo[1] = X[j][i + 1]

            if j == 0:
                xt[2] = traj_x[j][i]
                xt[3] = traj_x[j + 1][i]
                yt[2] = traj_y[j][i]
                yt[3] = traj_y[j + 1][i]
                yo[0] = Y[j][i]
                yo[1] = Y[j + 1][i]
            elif j == N - 1:
                xt[2] = traj_x[j - 1][i]
                xt[3] = traj_x[j][i]
                yt[2] = traj_y[j - 1][i]
                yt[3] = traj_y[j][i]
                yo[0] = Y[j - 1][i]
                yo[1] = Y[j][i]
            else:
                xt[2] = traj_x[j - 1][i]
                xt[3] = traj_x[j + 1][i]
                yt[2] = traj_y[j - 1][i]
                yt[3] = traj_y[j + 1][i]
                yo[0] = Y[j - 1][i]
                yo[1] = Y[j + 1][i]

            lambdas = eigs(xt, yt, xo, yo)
            if np.isnan(lambdas).all():
                ftle[j][i] = float("nan")
            else:
                ftle[j][i] = 0.5 * np.log(max(lambdas)) / (integration_time)

    return ftle


def FTLE(DT: DynTrack, integration_time: float, delta_t: float, copy: bool = False):
    """\
    Generate a scalar FTLE field from vector data.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    integration_time
        Overall integration time for sampling the vector field.
    delta_t
        Delta t used during the integration.
    copy
        Return a copy instead of writing to DT.

    Returns
    -------
    DT : :class:`dyntrack.DynTrack`
        if `copy=True` it returns or else add fields to `DT`:

        `.ftle`
            FTLE scalar values of the vector field.

    """

    DT = DT.copy() if copy else DT
    logg.info("Obtaining FTLE scalar field", reset=True)
    logg.info(f"    integration time: {integration_time}, delta_t: {delta_t}")
    logg.info("    Generating FTLE particle trajectories", end="... ")
    traj_x, traj_y = get_traj(DT.X, DT.Y, DT.u, DT.v, integration_time, delta_t)
    logg.info("done")
    ftle = get_ftle(traj_x, traj_y, DT.X, DT.Y, integration_time)

    DT.ftle = ftle

    logg.info("    finished", time=True, end=" " if settings.verbosity > 2 else "\n")
    logg.hint("added \n" "    .ftle, FTLE scalar values of the vector field.")

    return DT if copy else None
