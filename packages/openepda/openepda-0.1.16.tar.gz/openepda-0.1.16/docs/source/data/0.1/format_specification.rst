.. _openepda_data_format_v0_1:

===========
Version 0.1
===========

A file conforming to the openEPDA data format has the following structure.
The first line is a format identifier, ``# openEPDA DATA FORMAT v0.1``. After
this, the data part follows, which contains two sections. The first section
adheres to the `YAML format <http://yaml.org/spec/1.2/spec.html>`_, and
contains all scalar (numeric and textual) data in the name: value form.
This format is applicable for storing all previously mentioned types of
the data. The second section is a CSV-formatted (`RFC 4180 CSV Files
<https://tools.ietf.org/html/rfc4180>`_.) part to store the tabular
measurement data.

An example of a file recorded in the openEPDA data format is shown below.
Line 1 specifies the file format and its version. Lines 2 to 16 contain
metadata in YAML-format. Here, only string and float data types are used,
however arrays and maps can also be included. Line 17 contains a standard
document-end marker. Lines 18 to the end of the document contain the
CSV-formatted tabular data with a single header line.

Attributes
==========

Reserved
--------
The following keys have a special meaning:

* ``_timestamp``: time the data was created in ISO format.

Example data file
=================

+-------------+----------------------------------------------------+
| Line number | File contents                                      |
+=============+====================================================+
|           1 | # openEPDA DATA FORMAT v.0.1                       |
+-------------+----------------------------------------------------+
|           2 | _timestamp: '2018-09-12T09:59:19.310182'           |
+-------------+----------------------------------------------------+
|           3 | project: OpenPICs                                  |
+-------------+----------------------------------------------------+
|           4 | setup: RF setup                                    |
+-------------+----------------------------------------------------+
|           5 | operator: Xaveer                                   |
+-------------+----------------------------------------------------+
|           6 | wafer: 36386X                                      |
+-------------+----------------------------------------------------+
|           7 | sample: 13L8                                       |
+-------------+----------------------------------------------------+
|           8 | cell: SP35-1-3                                     |
+-------------+----------------------------------------------------+
|           9 | circuit: MSSOA1-6                                  |
+-------------+----------------------------------------------------+
|          10 | "current_density, kA/cm**2": 1                     |
+-------------+----------------------------------------------------+
|          11 | "reverse_bias, V": -2                              |
+-------------+----------------------------------------------------+
|          12 | configuration: 1                                   |
+-------------+----------------------------------------------------+
|          13 | polarization: TE                                   |
+-------------+----------------------------------------------------+
|          14 | port: "ioE132"                                     |
+-------------+----------------------------------------------------+
|          15 | "chip_temperature, degC": 18                       |
+-------------+----------------------------------------------------+
|          16 | "water_temperature, degC": 14                      |
+-------------+----------------------------------------------------+
|          17 | ...                                                |
+-------------+----------------------------------------------------+
|          18 | "wavelength, nm","transmitted power, dBm"          |
+-------------+----------------------------------------------------+
|          19 | 1550.00000000000000e+00,-21.000000000000000000e+00 |
+-------------+----------------------------------------------------+
|          20 | 1551.00000000000000e+00,-22.000000000000000000e+00 |
+-------------+----------------------------------------------------+
