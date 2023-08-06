=======
History
=======


0.x.x (coming soon)
--------------------

New features:
*

Bugfixes:
*


0.15.3 (2020-11-12)
--------------------

New features:
* Separated CI Jobs for optionally testing AC of EnMAP and/or Sentinel-2 data.

Bugfixes:
* Fixed Qhull error caused by scipy griddata function in except clause of ac_interpolation.
* Fixed error in getting ECMWF data.
* Modified input points and values for scipy RegularGridInterpolator to avoid NaN in interpolated variable.


0.15.2 (2020-10-22)
--------------------

New features:
* New handling of Sentinel-2 and Landsat-8 options files.

Bugfixes:
* Improved multispectral AC tables download during runtime by implementing an automatic check for table availability.


0.15.1 (2020-10-16)
--------------------

New features:
* Re-enabled and updated CI job for testing AC of Sentinel-2 data.

Bugfixes:
* Fixed scipy QHull error in interpolation function within Sentinel-2 AC.
* Updated package requirements.


0.15.0 (2020-10-12)
--------------------

New features:
* SICOR is now available as conda package on conda-forge.


0.14.6 (2020-10-05)
-------------------

New features:
* All needed AC tables both for hyper- and multispectral mode are now downloaded during runtime
* 'deploy_pypi' CI job is finally working after fixing some bugs.

Bugfixes:
* Fixed documentation links.
* Fixed pip install error caused by basemap library.


0.14.5 (2020-09-23)
-------------------

New features:
* Additional tables for multispectral mode are now downloaded during pip install.

Bugfixes:
* Moved imports of scikit-image from module level to function level to avoid
  'ImportError: dlopen: cannot load any more object with static TLS'.
* Fixed DeprecationWarnings h), i), and j) from issue #53.


0.14.4 (2020-09-07)
-------------------

New features:
* AC LUT is now downloaded during setup.py.

Bugfixes:
* Fixed issue #62 (ecmwf-api-client ImportError after following the installation instructions for the hyperspectral
  part of SICOR).


0.14.3 (2020-09-02)
-------------------
New features:
* The package is now available on the Python Package Index.
* Added 'deploy_pypi' CI job.


0.14.2 (2020-05-14)
-------------------
New features:
* Segmentation of input radiance data cubes to enhance processing speed.
* Empirical line solution for extrapolating reflectance spectra based on segment averages.


0.14.1 (2019-02-18)
-------------------
New features:
* Optimal estimation for atmospheric and surface parameters.
* Calculation of retrieval uncertainties.


0.14.0 (2019-02-11)
-------------------
New features:
* New EnMAP atmospheric correction.
* 3 phases of water retrieval for hyperspectral data.


0.13.0 (2018-12-18)
-------------------

* Development by Niklas Bohn started.
