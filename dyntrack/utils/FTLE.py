import numpy as np
import math
from matplotlib import pyplot
import time
import sys
import numba


@numba.jit
def bilinear_interpolation(X, Y, f, x, y):
    """Returns the approximate value of f(x,y) using bilinear interpolation.

    Arguments
    ---------
    X, Y -- mesh grid.
    f -- the function f that should be an NxN matrix.
    x, y -- coordinates where to compute f(x,y)

    """

    N = np.shape(X[:, 0])[0]

    dx, dy = X[0, 1] - X[0, 0], Y[1, 0] - Y[0, 0]
    x_start, y_start = X[0, 0], Y[0, 0]

    i1, i2 = int((x - x_start) / dx), int((x - x_start) / dx) + 1
    j1, j2 = int((y - y_start) / dy), int((y - y_start) / dy) + 1

    # Take care of boundaries

    # 1. Right boundary

    if i1 >= N - 1 and j1 <= N - 1 and j1 >= 0:
        return f[j1, N - 1]
    if i1 >= N - 1 and j1 <= 0:
        return f[0, N - 1]
    if i1 >= N - 1 and j1 >= N - 1:
        return f[N - 1, N - 1]

    # 2. Left boundary

    if i1 <= 0 and j1 <= N - 1 and j1 >= 0:
        return f[j1, 0]
    if i1 <= 0 and j1 <= 0:
        return f[0, 0]
    if i1 <= 0 and j1 >= N - 1:
        return f[N - 1, 0]

    # 3. Top boundary

    if j1 >= N - 1 and i1 <= N - 1 and i1 >= 0:
        return f[N - 1, i1]
    if j1 >= N - 1 and i1 <= 0:
        return f[N - 1, 0]

    # 3. Bottom boundary

    if j1 <= 0 and i1 <= N - 1 and i1 >= 0:
        return f[0, i1]
    if j1 <= 0 and i1 >= N - 1:
        return f[N - 1, 0]

    x1, x2 = X[j1, i1], X[j2, i2]
    y1, y2 = Y[j1, i1], Y[j2, i2]

    f_interpolated = (
        1
        / (x2 - x1)
        * 1
        / (y2 - y1)
        * (
            f[j1, i1] * (x2 - x) * (y2 - y)
            + f[j1, i2] * (x - x1) * (y2 - y)
            + f[j2, i1] * (x2 - x) * (y - y1)
            + f[j2, i2] * (x - x1) * (y - y1)
        )
    )

    return f_interpolated


@numba.jit
def rk4(X, Y, x, y, f, h, dim):
    """Returns the approximate value of f(x,y) using bilinear interpolation.

    Arguments
    ---------
    X, Y -- mesh grid.
    x, y -- coordinates where to begin the evolution.
    f -- the function f that will be evolved.
    h -- the time step (usually referred to this as dt.)
    dim -- 0 for x and 1 for y.

    """

    k1 = h * bilinear_interpolation(X, Y, f, x, y)
    k2 = h * bilinear_interpolation(X, Y, f, x + 0.5 * h, y + 0.5 * k1)
    k3 = h * bilinear_interpolation(X, Y, f, x + 0.5 * h, y + 0.5 * k2)
    k4 = h * bilinear_interpolation(X, Y, f, x + h, y + k3)

    if dim == 0:
        return x + 1.0 / 6 * k1 + 1.0 / 3 * k2 + 1.0 / 3 * k3 + 1.0 / 6 * k4
    elif dim == 1:
        return y + 1.0 / 6 * k1 + 1.0 / 3 * k2 + 1.0 / 3 * k3 + 1.0 / 6 * k4
    else:
        print("invalid dimension parameter passed to rk4, exiting")
        # sys.exit()


@numba.jit
def integrate(x_y, integration_time, dt, X, Y, u, v):
    xs = x_y[0]
    ys = x_y[1]
    tr_x = xs
    tr_y = ys
    for k in range(0, int(integration_time / dt)):
        xs, ys = rk4(X, Y, xs, ys, u, dt, 0), rk4(X, Y, xs, ys, v, dt, 1)
        tr_x += xs
        tr_y += ys
    return [tr_x, tr_y]


def eigs(xt, yt, xo, yo):
    ftlemat = np.zeros((2, 2))
    ftlemat[0][0] = (xt[1] - xt[0]) / (xo[1] - xo[0])
    ftlemat[1][0] = (yt[1] - yt[0]) / (xo[1] - xo[0])
    ftlemat[0][1] = (xt[3] - xt[2]) / (yo[1] - yo[0])
    ftlemat[1][1] = (yt[3] - yt[2]) / (yo[1] - yo[0])

    if True in np.isnan(ftlemat):
        return "nan"

    ftlemat = np.dot(ftlemat.transpose(), ftlemat)
    w, v = np.linalg.eig(ftlemat)

    return w
