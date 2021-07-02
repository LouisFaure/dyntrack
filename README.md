[![PyPI](https://img.shields.io/pypi/v/dyntrack.svg)](https://pypi.python.org/pypi/dyntrack/)
[![Build & Test](https://github.com/LouisFaure/dyntrack/actions/workflows/test.yml/badge.svg)](https://github.com/LouisFaure/dyntrack/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/LouisFaure/dyntrack/branch/main/graph/badge.svg)](https://codecov.io/gh/LouisFaure/dyntrack)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/LouisFaure/dyntrack/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# DynTrack

Python package for the study of particle dynamics from 2D tracks

Installation
------------

```bash
pip install -U dyntrack
```

Usage
-----

```python
import dyntrack as dt

DT = dt.ut.load_data("tracks.csv","background.tiff","Position X","Position Y","Parent","Time")

dt.tl.vector_field(DT)
dt.pl.vector_field(DT)

dt.tl.FTLE(DT, 20000,5)
dt.pl.FTLE(DT)

dt.tl.fit_ppt(DT,seed=1)
dt.pl.fit_ppt(DT)
```

Workflow
--------

![worflow](./docs/workflow.png)


Citations and used works
------------------------

The function `tl.vector_field` uses [vfkm](https://github.com/nivan/vfkm/) to generate vector fields (see [license](https://github.com/LouisFaure/dyntrack/blob/main/vfkm/LICENSE)), please cite the related study if you use it:

```
Ferreira, N., Klosowski, J. T., Scheidegger, C. & Silva, C. Vector Field k-Means: Clustering Trajectories by Fitting Multiple Vector Fields. Comput. Graph. Forum 32, 201–210 (2012).
```

Code from `tl.FTLE` have been adapted and optimized from [Richard Galvez's notebook](https://github.com/richardagalvez/Vortices-Python/blob/master/Vortex-FTLE.ipynb)
