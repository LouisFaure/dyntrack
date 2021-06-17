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

tdata, img = dt.ut.load_data("tracks.csv","background.tiff","Position X","Position Y","Parent","Time")

X, Y, u, v = dt.tl.vector_field(tdata)
dt.pl.vector_field(X, Y, u, v,img)

ftle=dt.tl.FTLE(X, Y, u, v, 20000,5)
dt.pl.FTLE(X,Y,u,v,ftle,img)

ppts=dt.tl.fit_ppt(tdata,seed=1)
dt.pl.fit_ppt(img,ppts,tdata)
```


If the function `tl.vector_field` is used, please cite the study that introduced the method for vector field generation:

```
Ferreira, N., Klosowski, J. T., Scheidegger, C. & Silva, C. Vector Field k-Means: Clustering Trajectories by Fitting Multiple Vector Fields. Comput. Graph. Forum 32, 201–210 (2012).
```

The license for the [redistributed code](https://github.com/nivan/vfkm/) can be found [here](https://github.com/LouisFaure/dyntrack/blob/main/vfkm/LICENSE)

Code from `tl.FTLE` have been adapted and optimized from [Richard Galvez's notebook](https://github.com/richardagalvez/Vortices-Python/blob/master/Vortex-FTLE.ipynb)
