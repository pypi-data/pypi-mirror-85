=======
History
=======

0.4.0 (2020-11-10)
------------------

* Replaced deprecated 'source activate' by 'conda activate'.
* Added Terra and Aqua MODIS spectral response functions (bands 1-16 only).


0.3.8 (2020-10-12)
------------------

* Use SPDX license identifier and set all files to GLP3+ to be consistent with license headers in the source files.
* Exclude tests from being installed via 'pip install'.


0.3.7 (2019-09-29)
-------------------

* Updated S2B band 1 RSR.


0.3.6 (2020-09-25)
------------------

* Moved matplotlib import to function level to avoid static TLS ImportError.


0.3.5 (2020-09-24)
------------------

* Moved scipy import to function level to avoid static TLS ImportError.


0.3.4 (2020-09-15)
------------------

* Updated deprecated HTTP links.


0.3.3 (2020-03-31)
------------------

* Added quick usage example to README.rst.
* Improved list of compatible sensors.
* Updated development status.


0.3.2 (2020-03-31)
------------------

* Fixed title underscore too short.


0.3.1 (2020-03-31)
------------------

* Fixed issue #9 (ValueError: No sensor specifications for combination 'Sentinel-2B' 'MSI' 'S2B20' found).
* Updated HISTORY.rst


0.3.0 (2020-03-27)
------------------

* Revised RSR_reader.
* RSR_reader now accepts a logger and may ignore missing files.
* Added list of supported sensors to README.rst.
* Fixed pipeline badge.
* Updated HISTORY.rst


0.2.10 (2019-09-24)
-------------------

* Updated S2A band 1 RSR.


0.2.9 (2019-08-23)
------------------

* Fixed missing LayerBandsAssignment and wrong bandnames.


0.2.8 (2019-08-23)
------------------

* Fixed missing LayerBandsAssignment and wrong bandnames.


0.2.7 (2019-08-22)
------------------

* Fixed FileNotFoundError in case the requested satellite is 'RapidEye-5'.


0.2.6 (2019-08-22)
------------------

* Cleaned up and added some comments.


0.2.5 (2019-08-22)
------------------

* Added setuptools-git to setup requirements.


0.2.4 (2019-08-22)
------------------

* Fixed missing package data.


0.2.3 (2019-08-22)
------------------

* Fixed missing data.


0.2.2 (2019-08-22)
------------------

* Fixed missing data.


0.2.1 (2019-08-22)
------------------

* Moved references.


0.2.0 (2019-08-22)
------------------

New features:

* First working version.
* Made RelativeSpectralResponse importable on the top level of the package.
* Added 'RSR' as alias for RelativeSpectralResponse.
* Implemented sensor specifications and possibility to ignore pan and thermal bands.
* Added possibility to ignore bands removed by AC.
* Added copyright and license notes.
* Added CI setup files. Added rules to Makefile. Added test requirements.
* Added .gitlab-ci.yml
* Updated README.rst.
* Added Sentinel-2 reference.
* Added references.

Bug fixes and enhancements:

* Refactored the term 'srf' to 'rsr'.
* Fix LayerBandsAssignment not properly passed through.
* Fixed CI setup.
* Fixed wrong links.
* Updated Sentinel-2A and -2B RSRs. (fixes issue #1).


0.1.0 (2019-08-19)
------------------

* First release on PyPI.
