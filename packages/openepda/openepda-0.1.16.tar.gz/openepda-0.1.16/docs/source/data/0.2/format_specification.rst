.. _openepda_data_format_v0_2:

====================
Version 0.2 (latest)
====================
A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA DATA FORMAT``. After
this, the data part follows, which contains two sections. The first section
adheres to the `YAML format <http://yaml.org/spec/1.2/spec.html>`_, and
contains all scalar (numeric and textual) data in the name: value form.
This format is applicable for storing all previously mentioned types of
the data. The second section is a CSV-formatted (`RFC 4180 CSV Files
<https://tools.ietf.org/html/rfc4180>`_) part to store the tabular
measurement data.

An example of a file recorded in the openEPDA data format is shown below.
Line 1 specifies the file format. Lines 2 to 16 contain
metadata in YAML-format, including the values for two reserved keys.
Here, only string and float data types are used, however arrays and maps can
also be included. Line 18 contains a standard document-end marker.
Lines 19 to the end of the document contain the CSV-formatted tabular data
with a single header line.

Attributes
==========

Reserved
--------
The following keys have a special meaning:

* ``_timestamp``: time the data was created in ISO format.
* ``_openEPDA_version``: string defining the format version, e.g. ``'0.2'``

Example data file
=================

+-------------+----------------------------------------------------+
| Line number | File contents                                      |
+=============+====================================================+
|           1 | ``# openEPDA DATA FORMAT``                         |
+-------------+----------------------------------------------------+
|           2 | ``_timestamp: '2018-09-12T09:59:19.310182'``       |
+-------------+----------------------------------------------------+
|           3 | ``_openEPDA_version: '0.2'``                       |
+-------------+----------------------------------------------------+
|           4 | ``project: OpenPICs``                              |
+-------------+----------------------------------------------------+
|           5 | ``setup: RF setup``                                |
+-------------+----------------------------------------------------+
|           6 | ``operator: Xaveer``                               |
+-------------+----------------------------------------------------+
|           7 | ``wafer: 36386X``                                  |
+-------------+----------------------------------------------------+
|           8 | ``sample: 13L8``                                   |
+-------------+----------------------------------------------------+
|           9 | ``cell: SP35-1-3``                                 |
+-------------+----------------------------------------------------+
|          10 | ``circuit: MSSOA1-6``                              |
+-------------+----------------------------------------------------+
|          11 | ``'current_density, kA/cm**2': 1``                 |
+-------------+----------------------------------------------------+
|          12 | ``'reverse_bias, V': -2``                          |
+-------------+----------------------------------------------------+
|          13 | ``configuration: 1``                               |
+-------------+----------------------------------------------------+
|          14 | ``polarization: TE``                               |
+-------------+----------------------------------------------------+
|          15 | ``port: 'ioE132'``                                 |
+-------------+----------------------------------------------------+
|          16 | ``'chip_temperature, degC': 18``                   |
+-------------+----------------------------------------------------+
|          17 | ``'water_temperature, degC': 14``                  |
+-------------+----------------------------------------------------+
|          18 | ``...``                                            |
+-------------+----------------------------------------------------+
|          19 | ``"wavelength, nm","transmitted power, dBm"``      |
+-------------+----------------------------------------------------+
|          20 | ``1550.0000000000000e+00,-21.000000000000000e+00`` |
+-------------+----------------------------------------------------+
|          21 | ``1551.0000000000000e+00,-22.000000000000000e+00`` |
+-------------+----------------------------------------------------+
