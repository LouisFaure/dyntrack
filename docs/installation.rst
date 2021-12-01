Installation
============

PyPi (MacOS/Linux/Windows)
--------------------------

A pre-compiled version is available on pypi

.. code:: bash

    pip install -U dyntrack


Building from source
--------------------

.. code:: bash

    git clone https://github.com/LouisFaure/dyntrack
    pip install .

Windows issues
--------------

If missing DLL errors occurs while running :func:`dyntrack.tl.vector_field`, or gcc is not available while building from source please install MinGW-w64:

.. code:: powershell

    choco install mingw
