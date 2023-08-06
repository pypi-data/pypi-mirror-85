.. _openepda_cdf_format:

===================
openEPDA CDF format
===================

Summary
=======
This document contains draft description of the Chip Description File
(CDF), which is used as a reference for electrical pads and optical
ports positions for the measurements to be performed on Photonic
Integrated Circuits (PIC). The latest version is 0.3.

Introduction
============
CDF is a configuration file that contains data with design coordinates
of the chip inputs and outputs (IO) (both electrical and optical). Therefore
it is linked to a specific design (cell), meaning that for
every new die design, also the applicable CDF needs to be composed.

The format of the file is meant to be human readable and intuitive in its
structure. It provides all necessary information starting from cell design
identification data, which is to be crosschecked with other configuration
files (e.g. MDF), up to the IO coordinates themselves.

Relation to netlist and MDF
---------------------------
There are multiple standards used to describe a simulation on an
electronic circuit. Let's have a look how one of the most popular such
formats -- SPICE -- is organized. It usually consists of two sections,
the netlist and the analyses section. The former one describes the circuit,
its elements, parameters, and connections. The latter -- Analyses part --
tells the simulator what kind of simulation is to be run on the circuit.

With introducing CDF and MDF, openEPDA makes the same distinction
between the circuit itself and measurements/simulations to be performed
on this circuit.

Now, the circuit can be described in different ways. For *fabrication*,
a representation in the form of a mask set is required (GDSII or OASIS
format). For *circuit simulation*, or from a designer's perspective,
a circuit is a set of interconnected BBs representing a netlist. For the
*measurements*, a black box description of the circuit is sufficient:
only the names and location of the inputs/outputs of the circuit are
needed. CDF is the format which describes this last representation.

License
=======
openEPDA CDF format is available under CC BY-SA 4.0 license.

This is Creative Commons Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0). See full license text here:
`CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/legalcode>`_.

More details on openEPDA view on standards licensing are available on
:ref:`Licensing policy <licensing_policy>` page.

Specification
=============
The standard specifies the *contents* of the file, which means which
*attributes* have to be defined in the file. Some attributes are *required*
and some are *optional*. There are also *reserved* attributes which
start with an underscore.

Besides the contents, the standard also defines the actual representation
of the data, which is YAML format. More information regarding the YAML
syntax can be found here: https://yaml.org/spec/1.2/spec.html.

.. toctree::
   :maxdepth: 1

   0.3/format_specification
   0.2/format_specification

Validation
==========
openEPDA provides online validators for the Chip Description Files, go to
`this page <https://validate.openepda.org/v/cdf>`_.