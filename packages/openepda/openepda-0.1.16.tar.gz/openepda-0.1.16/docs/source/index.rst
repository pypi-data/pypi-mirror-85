.. openepda documentation master file, created by
   sphinx-quickstart on Sun Nov  4 02:02:22 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
openEPDA Overview
=================

About openEPDA
==============

openEPDA™ is a collection of open standards to be used in electronic-photonic
design automation. These include definition of data interchange formats to
facilitate Foundry PDK distribution and
easier simulation and measurement data exchange between the parties involved
in the PIC design chain.

openEPDA structure
------------------
openEPDA standards aim to cover the following parts of the EPDA:

1. Foundry PDK:

   a. Foundry technology including mask layers, cross-sections (*under development*);
   b. Foundry building blocks (:ref:`pdk_components`);
   c. Standard interconnects (:ref:`openepda_interconnects`);

2. Data (numeric / analytic, covers both raw measurement and analysis data):

   e. openEPDA data format (:ref:`openepda_data_format`);

3. Circuit design description (for measurements/ simulations):

   f. Chip description (:ref:`openepda_cdf_format`);
   g. Netlist format (*under development*);

4. Measurement / simulations definitions:

   h. Equipment API for python (*under development*);
   i. Measurement description (:ref:`openepda_mdf_format`);

5. General

   j. Analytic expression format to be used in other files (:ref:`analytic_expressions`)

In addition, there is a `openepda <https://pypi.org/project/openepda/>`_
python package, which includes validators for the above formats, as well as
file readers / writers.


Authors
=======

.. _authors:

openEPDA is a trademark of TU/e and PITC. openEPDA is maintained by TU/e and
PITC. The full list of contributors is listed on the :ref:`about` page.
Authors and copyright for specific standards are provided on the
corresponding pages.

.. toctree::
   :hidden:
   :caption: Overview

   about
   licensing_policy
   contributing

.. toctree::
   :caption: Standards
   :maxdepth: 2

   updk/pdk_components
   interconnect/interconnects
   data/openepda_data_format
   cdf/openepda_cdf_format
   mdf/openepda_mdf_format
   analytic_expressions

.. toctree::
   :hidden:
   :caption: Python package
   :maxdepth: 2

   pypi_package/api
   pypi_package/history_of_changes

.. toctree::
   :hidden:
   :caption: Other resources

   openEPDA Validation <https://validate.openepda.org>