from tqdm import tqdm
import warnings
import sys
import simpleppt
from .. import logging as logg
from .. import settings

simpleppt.settings.verbosity = 0


def fit_ppt(DT, times=None, lam=10, sigma=10, seed=0, copy=False, **kwargs):

    logg.info(
        f"Generating principal tree per timepoints (lambda: {lam}, sigma: {sigma})",
        reset=True,
    )
    DT = DT.copy() if copy else DT

    tdata = DT.track_data

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
                    **kwargs,
                )
            ]

    DT.ppts = ppts

    logg.info("    finished", time=True, end=" " if settings.verbosity > 2 else "\n")
    logg.hint("added \n" "    .ppts, list of SimplePPT objects.")

    return DT if copy else None
