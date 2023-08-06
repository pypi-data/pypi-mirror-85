============
Installation
============

Using Anaconda or Miniconda (recommended)
-----------------------------------------

Using conda_, SICOR is installed as follows:

1. Create virtual environment for SICOR (optional but recommended):

   .. code-block:: bash

    $ conda create -c conda-forge --name sicor python=3
    $ source activate sicor

2. Then install SICOR itself:

   .. code-block:: bash

    $ conda install -c conda-forge sicor

This is the preferred method to install SICOR, as it will always install the most recent stable release and
automatically resolve all the dependencies.


Using pip (not recommended)
---------------------------

There is also a `pip`_ installer for SICOR. However, please note that SICOR depends on some
open source packages that may cause problems when installed with pip. Therefore, we strongly recommend
to resolve the following dependencies before the pip installer is run:

    * arosics
    * gdal
    * h5py
    * matplotlib
    * numba
    * numpy
    * pyproj
    * pytables
    * scikit-image
    * scikit-learn<=0.24.0

Then, the pip installer can be run by:

   .. code-block:: bash

    $ pip install sicor

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.


Using git (not recommended)
---------------------------

Alternatively you can install SICOR by cloning the following repository:

 .. code-block:: bash

    git clone https://gitext.gfz-potsdam.de/EnMAP/sicor.git
    cd sicor
    python setup.py install


.. _conda: https://conda.io/docs/
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
