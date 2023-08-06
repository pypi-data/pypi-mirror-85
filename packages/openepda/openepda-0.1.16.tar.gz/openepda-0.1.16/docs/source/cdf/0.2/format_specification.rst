.. _openepda_cdf_format_specification_v0_2:

Version 0.2
-----------
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA CDF``. After
this, the data section follows, which adheres to the YAML format [1],
and contains all settings (numeric and textual) data in the form of an
associative array.

An example of a file recorded in the openEPDA CDF format is shown below.

Reserved keys
^^^^^^^^^^^^^
The following keys are required to be present in the CDF:

* ``_openEPDA``: an object defining the format and its version.
* ``cdf``: a string with a unique identifier of the CDF
* ``cell``: a string with an identifier of the PIC design to be measured
* ``unit``: a string defining a unit for the coordinates in the file
* ``bbox``: a list with the coordinates of two bounding box corners,
  (south-west and north-east).
* ``io``: An object with IOs located on the chip.

The following keys are optional to be present in the CDF:

* ``fiducial``: an object with fiducial markers on the chip.


Example CDF file
^^^^^^^^^^^^^^^^

.. include:: example.rst

References
==========
1. "YAML Ain't Markup Language (YAML™) Version 1.2."
`<http://yaml.org/spec/1.2/spec.html>`_.