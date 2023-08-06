=====
About
=====

.. image:: https://enmap.gitext-pages.gfz-potsdam.de/sicor/doc/_images/sicor_logo_lr.png
   :width: 150px
   :alt: SICOR Logo

Sensor Independent Atmospheric Correction of optical Earth Observation (EO) data from both multispectral and
hyperspectral instruments. Currently, SICOR can be applied to Sentinel-2 and EnMAP data but the implementation of
additional space- and airborne sensors is under development. As a unique feature for the processing of hyperspectral
data, SICOR_ incorporates a three phases of water retrieval based on Optimal Estimation (OE) including the calculation
of retrieval uncertainties. The atmospheric modeling in case of hyperspectral data is based on the MODTRAN radiative
transfer code whereas the atmospheric correction of multispectral data relies on the MOMO code.

This project was funded by GFZ's EnMAP_ and GeoMultiSens_ activities, AgriCircle trough cooperation with Adama,
and ESA. The MODTRAN trademark is being used with the express permission of the owner, Spectral Sciences, Inc. The
package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

Feature overview
----------------

* Sentinel-2 L1C to L2A processing
* EnMAP L1B to L2A processing
* generic atmospheric correction for hyperspectral airborne and spaceborne data
* retrieval of the three phases of water from hyperspectral data
* calculation of various retrieval uncertainties
  (including a posteriori errors, averaging kernels, gain matrices, degrees of freedom, information content)
* atmospheric correction for Landsat-8: work in progress
* CH4 retrieval from hyperspectral data: work in progress



.. _SICOR: https://gitext.gfz-potsdam.de/EnMAP/sicor/
.. _GeoMultiSens: http://www.geomultisens.de/
.. _EnMAP: http://www.enmap.org/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
