import dyntrack as dt
import numpy as np


def test_all():
    DT = dt.ut.load_example()

    repr(DT)

    dt.pl.tracks(DT)

    dt.tl.vector_field(DT)
    dt.pl.vector_field(DT)
    dt.tl.FTLE(DT, 20000, 5)
    dt.pl.FTLE(DT)
    dt.tl.fit_ppt(DT, times=range(200, 220), seed=1)
    dt.pl.fit_ppt(DT, times=range(200, 220))

    assert np.allclose(
        DT.X[0, :5],
        [2.31421127, 25.57012909, 48.82604692, 72.08196474, 95.33788256],
        rtol=1e-2,
    )

    assert np.allclose(
        DT.Y[0, :5],
        [0.99373803, 0.99373803, 0.99373803, 0.99373803, 0.99373803],
        rtol=1e-2,
    )

    assert np.allclose(
        DT.u[0, :5],
        [-1.31697, -1.29131, -1.30477, -1.33974, -1.37175],
        rtol=1e-2,
    )

    assert np.allclose(
        DT.v[0, :5],
        [-0.388019, -0.384006, -0.379422, -0.381275, -0.398514],
        rtol=1e-2,
    )

    assert np.allclose(
        DT.ftle[0, :5],
        [0.00041502, 0.00041524, 0.00041525, 0.00041478, 0.00041478],
        rtol=1e-2,
    )

    assert np.allclose(
        DT.ppts[0].F[0, :5],
        [484.61573908, 231.13676703, 423.2637024, 597.67431024, 453.89848974],
        rtol=1e-2,
    )
