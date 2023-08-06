.. _openepda_data_format:

====================
openEPDA data format
====================

About openEPDA data format
==========================

Summary
-------
With the development of fab-less approach to integrated photonics, there is
an increasing demand on infrastructure for handling measurement, analysis
and simulation data. In order to facilitate data exchange between parties we
fill the gap in the data file formats and describe an open standard for
file format, which is human readable and at the same time allows convenient
storage and manipulation of heterogeneous measurement data.

Motivation
----------
In integrated electronics and photonics various data in different
formats is generated on multiple stages of the fabrication chain:
design, simulations, fabrication, testing, and device characterization.
For example, testing is performed on different stages of the fabrication:
from on-wafer testing during and after the fabrication to module-level
testing of the packaged devices. The data generated during these measurements is
heterogeneous, and is used for different purposes: pass-fail procedure,
process control, device models development and calibration. This involves
various parties, such as foundry, measurement labs, designers, and software
companies which use different tools to generate and process the test data.

Data types
==========
The generated data comes from different sources and is heterogeneous.
The main data is obtained from the measurement equipment directly when
the observation is performed. This data is usually numeric (scalar or arrays).
The identifiers of the wafer, die and circuit under test represent metadata
for the given observation. Metadata also may include the equipment used,
the equipment settings, date of calibration, ambient conditions, etc.
The metadata can be of various simple (numeric, textual) and structured
types (arrays, maps). The overview of the data types is presented in the
table below.

+-----------+-----------------------------+---------------------------------+------------------------------+
| Data type | Description                 | Examples                        | Remarks                      |
+===========+=============================+=================================+==============================+
| Number    | Any numeric value           | 1                               | Representation is same       |
|           |                             | 2.3                             | as in section 10.2.1.4       |
|           |                             | .inf                            | of [1]                       |
|           |                             | 1.9e-3                          |                              |
+-----------+-----------------------------+---------------------------------+------------------------------+
|           | A list of characters        | 'spectrum analyzer'             |                              |
| String    |                             | 'SPM18-3'                       |                              |
+-----------+-----------------------------+---------------------------------+------------------------------+
| Array     | A sorted list of numeric    | [1, 2, 3, 4]                    | Values may have mixed types, |
|           | or string values            | ['voltage', 'current', 'power'] | which is discouraged         |
+-----------+-----------------------------+---------------------------------+------------------------------+
| Map       | Mapping of a set of values  |  {'wafer': 'SPM18-3',           | Also called a named array,   |
|           | to another set of values    |  'die': '38X23',                | a look-up table, or a        |
|           | in the ``key: value`` form  |  'design': 'SP00-38'}           | dictionary                   |
+-----------+-----------------------------+---------------------------------+------------------------------+

To facilitate exchange of the data between these parties, we have developed
a standard file data format, which can store the measurement data and metadata
in a human-readable way. The format is sufficiently flexible to include any
arbitrary structured data, including arrays and maps. The generated files are
straightforward to be imported by any software or analysis tool, for example
MatLab, python, and Excel.

License
=======
openEPDA data formats are available under CC BY-SA 4.0 license.

This is Creative Commons Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0). See full license text here:
`CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/legalcode>`_.

More details on openEPDA view on standards licensing are available on
:ref:`Licensing policy <licensing_policy>` page.

Specification
=============
The data format defines how to write the information into a file. Besides
this, YAML section contains reserved keys which start with the underscore
symbol. The list of reserved keys is given for a particular format version.

.. toctree::
   :maxdepth: 1

   0.2/format_specification
   0.1/format_specification
