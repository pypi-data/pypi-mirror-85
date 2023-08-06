.. include:: <isonum.txt>

.. _openepda_updk_format_v0_3:

===================================================
openEPDA uPDK |trade| Blocks - Version 0.3 (stable)
===================================================

This page contains specification for the uPDK |trade| block description
standard. For general information about uPDK including the licensing terms, see
:ref:`pdk_components`.

General format info
===================
The standard building block schema is defined in a JSON/YAML-compatible style
as these are:

- very commonly used/standard formats
- open and accessible to everybody
- human readable
- hierarchical
- label based

Any logical yaml features like linking are omitted to keep the schemas as
generic and format independent as possible. We omit the brackets of a json
style format for readability.
Note that it is straightforward to read this schema as yaml and convert it
between yaml, json and/or xml as you see a need for it. Here we convert it
to html tables as well for documentation purposes.

SBB schema example
==================

Before discussing a more formal SBB definition, we first show an example of
two blocks in the SBB schema, i.e. a MMI power coupler *mmi* and an optical
amplifier *soa*. They are grouped under the *blocks* label. Licensing and
background information is organized under the *header* label.

.. include:: sbb_example.rst


SBB schema description
======================

The standard building block schema description in table form is printed
below. Alternatively, download the SBB schema description below in
:download:`csv <openEPDA_uPDK_SBB_v0.3.yaml.csv>` format. More information
on the label <...> notation is found below the table. The columns have the
following meaning:

- **label**:  shows the label hierarchy by indentation (or by number in csv).
- **type**: the datatype of each label. A datatype is *int*, *float*, *str*,
  *object*, or *subschema*. See the SSB metadata schema for more detail.
- **required**: A bullet value indicates that a label must be present in the
  SBB to have a minimum set of data to describe the block. If not present
  the default value must be assumed. If there is no default the schema is
  incomplete.
- **documentation**: describes the purpose of the label
- **default**: default value where applicable. If a value is missing the
  default must be assumed.
- **allowed_values**: list of allowed values, if applicable
- **example**: example data


Defined top labels are

- **header**: license and background information on the schema
- **blocks**: standard black blocks (SBB)
- **subschemas**: subschemas that may be called from other parts of the
  schema. Note that a subschema may contain another subschema as long as
  there are no circular references.


.. include:: openEPDA_uPDK_SBB_v0.3.yaml.rst


<label>
--------
Labels expressed with the syntax <label> denote that the text <label> has
to be replaced with one or more explicit label name(s), e.g. pin1, myblock5.
It also denotes that there can be more than one label at the same hierarchy level.

Using subschemas
-----------------
Labels with type *subschema* point to a label under the top-level label
"subschema". The subschema structure is to be inserted at the label of type
*subschema*: This allows for reuse of hierarchical data structures and/or
indicate that different structures are possible depending on the context.
For example

.. code-block:: yaml

  # label with a subschema reference to "ruleset":
  rules:
    ruleset

  # subschema:
  ruleset:
    label1: data1
    label2: data2

  # expansion in SBB schema:
  rules:
    label1: data1
    label2: data2

Special values
--------------

- true: logical true
- false: logical false
- null: null, void, None


Coordinates
-----------
Geometrical coordinates are described in the Cartesian coordinate system.



SBB superschema
===============

.. _sbb-superschema:


The SBB schema is defined by a SBB superschema, which is defined in the same
json/yaml format as the SBB schema. It can be downloaded in
:download:`yaml <openEPDA_uPDK_SBB_v0.3.yaml>`.
The superschema describes the labels and structure of the SBB schema along
with its metadata.
Metadata can be identified by the superschema labels that start with an _
character. Labels without a _ as first character represent labels of the
SBB schema as discussed in the previous sections.



Metadata labels
---------------

The following metadata labels are defined:

Labels that are always present under a SBB label:

- **_type:** datatype of the label:

  - **str:** a string: "I am a string"
  - **list:** a list of elements, e.g. values, strings or other lists: [1.0, 10.0, 100.0]
  - **object:** hierarchically nested data, i.e. more levels exist under this label
  - **subschema:** a label reference to a subschema object stored directly
    under the top-label 'subschema'.
- **_required:** true, if the label is mandatory, false otherwise. Note
  the _required label is only relevant  specific cases where the parent in
  the hierarchy SBB exists.
- **_doc:** description of the purpose of the label

Situational labels:

- **_properties:** start the description of a new hierarchy level, i.e. a
  new level of labels
- **_example:** example of the data content of a label
- **_default:** default data value
- **_allowed_values:** list of allowed data values of the label, e.g. [um, nm, pm]

Below an example of the metadata labels in a superschema. Note that the
metadata labels reside at the odd hierarchy level 1, 3, 5, ..., where as the
normal labels occupy the even levels 0, 2, 6, ...

.. include:: sbb_superschema_example.rst


Release notes
=============

The following changes are included in the uPDK format v.0.3 as compared to v.0.2:

- License is now CC BY-SA 4.0 instead of CC BY-ND 4.0.
