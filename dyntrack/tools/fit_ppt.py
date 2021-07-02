from typing import Sequence, Union
from tqdm import tqdm
import warnings
import sys
import simpleppt
from .. import logging as logg
from .. import settings
from ..DynTrack import DynTrack

simpleppt.settings.verbosity = 0


def fit_ppt(
    DT: DynTrack,
    times: Union[Sequence, None] = None,
    lam: float = 10,
    sigma: float = 10,
    copy: bool = False,
    **kwargs,
):

    """\
    Compute a principal tree from partical position at each frame.

    Parameters
    ----------
    DT
        A :class:`dyntrack.DynTrack` object.
    times
        set of timepoints/frames to use for the fitting, by default uses all.
    lam
        Lambda parameter from SimplePPT algorithm.
    sigma
        Sigma parameter from SimplePPT algorithm.
    copy
        Return a copy instead of writing to DT.
    **kwargs
        Additional parameters to be passed to :func:`simpleppt.ppt`

    Returns
    -------
    DT : :class:`dyntrack.DynTrack`
        if `copy=True` it returns or else add fields to `DT`:

        `.ppts`
            List of principal trees calculated per frame.

    """

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
