.. _openepda_mdf_format_v0_2:

====================
Version 0.2 (draft)
====================
A file conforming to the openEPDA MDF format has the following structure.
The first line is a format identifier, ``# openEPDA MDF``. After
this, the data section follows, which adheres to the `YAML format
<http://yaml.org/spec/1.2/spec.html>`_,
and contains all settings (numeric and textual) data in the form of an
associative array.

An example of a file recorded in the openEPDA MDF format is shown below.

Attributes
==========
In this section, a list and explanation of the attributes is given.
Additional attributes which are not listed below are not allowed.

Required
--------
The following keys are required to be present in the MDF:

* ``_openEPDA``: an object defining the format and its version.
* ``mdf``: a string with a unique identifier of the MDF
* ``cell``: a string with an identifier of the PIC design to be measured
* ``die_rotation``: an angle for die position on the setup. It
  determines the orientation of the die, e.g. west-to-left or west-to-right.
* ``measurements``: Definition of the measurements used in the file. A
  measurement includes the measurement module and its settings.
  Key is the name of the measurement, value is a dictionary with
  measurement module name and settings (see Note 4).
* ``reference``: A list of reference circuits. Each list element is a
  dictionary: key is a reference port label, value is a dictionary
  `{side: port}`.
* ``measurement_sequence``: Each list element is a measurement group.
  A measurement group is a list of dictionaries, each describing a set of
  individual observation on a single circuit.

Notes
-----
1. All the above attributes are obligatory to be present in an MDF in order
   to be used. Otherwise MDF reader should return an error of incorrect MDF
   format.
2. There must be two reference circuits defined, each containing one east
   and west port.
3. For each circuit to be measured, two ports maximum can be used at the
   same time, and they must be on the opposite sides of the chip (this comes
   from a hardware restrictions of the current setup). The ports for a circuit
   are grouped by the side, and their combinations are generated based on
   settings in measurements key.
4. The measurements key contains a dictionary of the measurements that are
   intended to be used in the MDF. The names for these can be arbitrary
   (``mmi_perm`` in the example) and they are referenced later on in the
   `measurement_sequence` part. The value contains a dictionary with required
   keys `measurement_module` and `measurement_module_settings`.
5. Measurement module name is a valid class which describes the algorithm
   performing the measurements. A measurement module can be standard or a
   user-defined. See the list of standard modules with their parameters in the
   next section.
6. The measurement_sequence tag contains a list of measurement groups. Each
   measurement group is identified by its label (top_mmi in the example) and
   contains a list of observations sets. In the example, the group top_mmi
   contains two measurement sets, each set determined by the mmi_perm
   measurement name.
7. Each dictionary describing an observation set must contain the following keys:

   * measurement
   * west_ports
   * east_ports

   The in_ports and out_ports keys can be either single port or lists of ports.
   The combinations of these to be actually used in the measurement are
   determined by in the measurements section.
8. Comments are standard YAML comments, they start with a hashtag
   symbol and can be placed at the end of any line. E.g., # This is a comment.

Example MDF file
================

.. include:: example.rst