Citations and used works
***********************

Vector field building
--------------------

The function :func:`dyntrack.tl.vector_field` uses
`vfkm <https://github.com/nivan/vfkm/>`__ to generate vector fields (see
`license <https://github.com/LouisFaure/dyntrack/blob/main/vfkm/LICENSE>`__),
please cite the related study if you use it:

::

    Ferreira, N., Klosowski, J. T., Scheidegger, C. & Silva, C.
    Vector Field k-Means: Clustering Trajectories by Fitting Multiple Vector Fields.
    Comput. Graph. Forum 32, 201–210 (2012).


FTLE scalar field generation
---------------------------

Code from :func:`dyntrack.tl.FTLE` have been adapted and optimized from `Richard
Galvez's
notebook <https://github.com/richardagalvez/Vortices-Python/blob/master/Vortex-FTLE.ipynb>`__


Principal tree fitting with SimplePPT
------------------------------------

Code from :func:`dyntrack.tl.fit_ppt` uses SimplePPT algorithm to fit principal trees on each frames.
SimplePPT has been described in the following paper::

    Mao et al. (2015), SimplePPT: A simple principal tree algorithm
    SIAM International Conference on Data Mining.
