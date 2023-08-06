.. _openepda_cdf_format_specification_v0_3:

====================
Version 0.3 (latest)
====================
A file conforming to the openEPDA CDF format has the following structure.
The first line is the format identifier, ``# openEPDA CDF``. After
this, the data section follows, which adheres to the `YAML format
<http://yaml.org/spec/1.2/spec.html>`_, and contains all settings
(numeric and textual) data in the form of an associative array.

An example of a file recorded in the openEPDA CDF format is shown below.

JSON Schema
===========
In order to validate the CDF data, the following `JSON Schema <https://json-schema.org/>`_
can be used: :download:`cdf_schema_v0.3.yaml <../../../../openepda/schemas/cdf_schema_v0.3.yaml>`.
In case of documentation disagreements, JSON schema has priority.

Attributes
==========
In this section, a list and explanation of the attributes is given.
Additional attributes which are not listed below are not allowed.

Required
--------
The following attributes are required to be present in the CDF:

* ``_openEPDA``: a dictionary defining the format and its version.
  See the field in the example.
* ``cdf``: a string with a unique identifier of the CDF.
* ``cell``: a string with an identifier of the PIC design described by
  the CDF.
* ``unit``: a string defining the length unit for the coordinates in
  the file.
* ``bbox``: a list with the coordinates of two bounding box corners,
  (south-west and north-east).
* ``io``: A dictionary with IOs located on the chip.

Optional
--------
The following attributes are optional to be present in the CDF:

* ``fiducial``: a dictionary with fiducial markers on the chip.


Example CDF
===========

.. include:: example.rst
