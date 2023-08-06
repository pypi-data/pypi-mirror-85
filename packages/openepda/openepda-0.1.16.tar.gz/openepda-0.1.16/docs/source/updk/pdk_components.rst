.. include:: <isonum.txt>

.. _pdk_components:

============================
openEPDA uPDK |trade| Blocks
============================

**uPDK** |trade| **license:** CC BY-SA 4.0

**CC-attribution:** openEPDA-uPDK-SBB-v0.3

|copy| Copyright 2017-2020, Ronald Broeke

Context
=======
A building block, or block in short, represents an electro-optical component
on a photonic integrated circuit (PIC), such as a power coupler, a phase shifter
or an amplifier. A block may be parameterized. A block may have different
"views" or representations, e.g. a layout view in gds or a circuit view for
circuit simulations. For design purposes it makes sense to group cells in
the layout view and circuit view in the same way, such that a layout cell
in gds also represents a logical circuit block. This description is part of
the uPDK |trade| or universal-process-design-kit, where you as designer have
access to interface definitions to solve design challenges in your project.


Purpose of uPDK blocks
======================

The purpose of the uPDK |trade| block description standard defined in this
text is to provide a representation of blocks that is

- open;
- scriptless;
- parameterizable;
- tool-independent.

The blocks in this description are called "standard black blocks" (SBB). This
description can be used by foundries to distribute block information to
software providers for building a PDK distribution or to designers directly.
Note that "open" here means that the description of the interface is open.
The content and data maybe bound by a non-disclosure agreement. The blocks
are not intended to contain the full manufacturing information when
distributed, which allows for IP protection and the simplified scriptless
based representation; Hence, the name "black block".

The standard black blocks for layout correspond to a (gds) layout cell each
and are replaced by the foundry in the mask compilation process with the
full information required for manufacturing of the design.  As stated, the
standard black blocks do not contain script code, however, a specific set
of mathematical equations is allowed to take care of parameterization. A
block must contain sufficient information to employ it in a gds layout as a
cell, and/or in a circuit schematic as described below.

Any building blocks that would need a script-based solution require an
extended description with flow control. Those blocks can be implemented
directly in the script environment of a layout tool. However, it remains to
be seen if these blocks are needed as part of the foundry PDK at all. Block
descriptions can either be made more elegant and fit the scriptless description
or instead can be considered as tool-specific extensions beyond the standard
foundry description. Technically, these blocks could be provided/distributed
as well as (compiled) libraries, which is beyond the scope of the SBB defined
here.


Minimum SBB requirement
=======================

For gds layout purposes a standard black block needs to contain at a minimum
the following items:

- a bounding box polygon
- a definition of all the pins to connect to, including their geometrical position
- design rules: e.g for placement with respect to the reticle/wafer orientation
  for compatibility with manufacturing


For circuit simulation purposes the block needs to contain at a minimum the
following items:

- a description of all the pins to connect to
- a circuit model of the functional connectivity between the pins in the block,
  e.g. a S-matrix.

Building block information is stored together with licensing information. The
Specification section explain how this information has to be described.

Specification
=============

.. toctree::
   :maxdepth: 1

   0.4/format_specification
   0.3/format_specification
   0.2/format_specification

Copying
=======

The uPDK superschemata and schemata can be freely used and distributed in their original form under the CC BY-SA 4.0 license, which means in short:

- CC: Creative Commons license
- BY-SA : This lets others reuse the work for any purpose, including
  commercially; the changes and adaptations on the specifications must be
  licensed under the identical terms, and credit must be provided to the
  original creation.
- 4.0: license version


Hence, the license does not allow others to modify **and** redistribute the
content as an openEPDA standard.
More on the license can be found at https://creativecommons.org/licenses/.

--------

**uPDK** |trade| **license:** CC BY-SA 4.0

**CC-attribution:** openEPDA-uPDK-SBB-v0.3

|copy| Copyright 2017-2020, Ronald Broeke

uPDK is a trade mark of Ronald Broeke.
