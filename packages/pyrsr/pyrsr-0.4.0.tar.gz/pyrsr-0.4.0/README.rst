=====
pyrsr
=====

A package providing relative spectral response functions for remote sensing instruments.

* Free software: GNU General Public License v3 or later (GPLv3+)
* Documentation: https://geomultisens.gitext-pages.gfz-potsdam.de/pyrsr/doc/
* Submit feedback by filing an issue `here <https://gitext.gfz-potsdam.de/geomultisens/pyrsr/issues>`__.


Status
------

.. image:: https://gitext.gfz-potsdam.de/geomultisens/pyrsr/badges/master/pipeline.svg
        :target: https://gitext.gfz-potsdam.de/geomultisens/pyrsr/commits/master
.. image:: https://gitext.gfz-potsdam.de/geomultisens/pyrsr/badges/master/coverage.svg
        :target: https://geomultisens.gitext-pages.gfz-potsdam.de/pyrsr/coverage/
.. image:: https://img.shields.io/pypi/v/pyrsr.svg
        :target: https://pypi.python.org/pypi/pyrsr
.. image:: https://img.shields.io/pypi/l/pyrsr.svg
        :target: https://gitext.gfz-potsdam.de/geomultisens/pyrsr/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/pyrsr.svg
        :target: https://img.shields.io/pypi/pyversions/pyrsr.svg
.. image:: https://img.shields.io/pypi/dm/pyrsr.svg
        :target: https://pypi.python.org/pypi/pyrsr
.. .. image:: https://img.shields.io/travis/danschef/pyrsr.svg
        :target: https://travis-ci.org/danschef/pyrsr
.. .. image:: https://readthedocs.org/projects/pyrsr/badge/?version=latest
        :target: https://pyrsr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. .. image:: https://pyup.io/repos/github/danschef/pyrsr/shield.svg
     :target: https://pyup.io/repos/github/danschef/pyrsr/
     :alt: Updates

See also the latest coverage_ report and the nosetests_ HTML report.


Features
--------

Quick usage example for getting the spectral response functions of Sentinel-2A:

.. code-block::

    >>> from pyrsr import RelativeSpectralResponse
    >>> RSR = RelativeSpectralResponse(satellite='Sentinel-2A', sensor='MSI')
    >>> RSR.plot_rsrs()

.. image:: https://gitext.gfz-potsdam.de/geomultisens/pyrsr/raw/master/docs/images/S2A_RSRs.png

.. code-block::

    >>> RSR.rsrs

    {'1': array([ 0.0001003 ,  0.00023005,  0.00020481, ...,  0.        ,
                  0.        ,  0.        ]),
     '2': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '3': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '4': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '5': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '6': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '7': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '8': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '8A': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '9': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '10': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '11': array([ 0.,  0.,  0., ...,  0.,  0.,  0.]),
     '12': array([ 0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
                   4.06617574e-05,   2.94133865e-05,   1.28975620e-05])}


List of supported sensors:

* Terra ASTER
* Landsat-4 TM
* Landsat-5 TM
* Landsat-7 ETM+
* Landsat-8 OLI_TIRS
* Aqua MODIS
* Terra MODIS
* RapidEye-5 MSI
* Sentinel-2A MSI
* Sentinel-2B MSI
* SPOT-1 HRV1
* SPOT-1 HRV2
* SPOT-2 HRV1
* SPOT-2 HRV2
* SPOT-3 HRV1
* SPOT-3 HRV2
* SPOT-4 HRVIR1
* SPOT-4 HRVIR2
* SPOT-5 HRG1
* SPOT-5 HRG2


Credits
-------

The pyrsr package was developed within the context of the GeoMultiSens project funded
by the German Federal Ministry of Education and Research (project grant code: 01 IS 14 010 A-C).

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _coverage: https://geomultisens.gitext-pages.gfz-potsdam.de/pyrsr/coverage/
.. _nosetests: https://geomultisens.gitext-pages.gfz-potsdam.de/pyrsr/nosetests_reports/nosetests.html
