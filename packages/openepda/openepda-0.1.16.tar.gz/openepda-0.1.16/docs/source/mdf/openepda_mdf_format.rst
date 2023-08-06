.. _openepda_mdf_format:

===================
openEPDA MDF format
===================

Summary
=======
This document contains draft description of the Measurement Description File
(MDF), which is used for hardware- and setup-independent configuring of the
measurements to be performed on Photonic Integrated Circuits (PIC).

Introduction
============
MDF is configuration file that contains data
regarding the measurement sequences that are to be performed on a specific
die. Therefore it is linked to a specific design (cell), meaning that for
every new die design, also the applicable MDF needs to be composed. A new
MDF needs also to be composed if a different measurement sequence has to
be performed on the same die.

Being a YAML file, its content is human readable and intuitive in its structure.
It provides all necessary information starting from cell identification data, which is to be
crosschecked with other configuration files, up to the very essence of
the file which is the definition of the measurements themselves. More
details regarding YAML syntax can be found here:
https://yaml.org/spec/1.2/spec.html.

License
=======
openEPDA MDF format is available under CC BY-SA 4.0 license.

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

   0.2/format_specification
