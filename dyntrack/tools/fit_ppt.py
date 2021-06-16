from tqdm import tqdm
import warnings
import sys

import simpleppt

simpleppt.settings.verbosity = 0


def fit_ppt(tdata, times=None, lam=10, sigma=10, seed=0, **kwargs):
    times = tdata.Time.unique() if times is None else times
    ppts = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for t in tqdm(times, file=sys.stdout, desc="    fitting"):
            tofit = tdata.loc[tdata.Time == t, ["Position X", "Position Y"]]
            ppts = ppts + [
                simpleppt.ppt(
                    tofit,
                    tofit.shape[0],
                    seed=seed,
                    lam=lam,
                    sigma=sigma,
                    progress=False,
                    **kwargs
                )
            ]

    return ppts
