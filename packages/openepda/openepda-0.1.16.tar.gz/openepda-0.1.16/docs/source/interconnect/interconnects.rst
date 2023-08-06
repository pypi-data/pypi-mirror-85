.. _openepda_interconnects:

======================
openEPDA interconnects
======================

Introduction
============
In addition to standard building blocks (see :ref:`pdk_components`), an
electronic-photonic circuit typically contains interconnects, which are
arbitrary-shape connectors between the pins of standard building blocks.
A simple example of an interconnect is straight or bended optical waveguide.

The interconnects are mostly defined for optical and electrical waveguides, but
also can refer to other connections, such as DC metal connections.

This specification defines the standard openEPDA interconnect conventions.
Each interconnect type (i.e. line, arc, ...) is specified independently of the
cross-section. When using an interconnect, a designer should specify the
cross-section in which the interconnect has to be drawn.

If not all interconnects make sense for all cross-sections, there could be a
list of permitted cross sections for each interconnect type. However, it is not
expected that this will be a problem.

Interconnect types
==================

line
----

The line interconnect has two parameters: the **length** and the **width**. For the
width, the specification is the logical width. That means that the actual width
of the interconnect will be also defined by the type of cross section. For
example a different etch type could demand a different trench width for the
same logical width of the interconnect.


arc
---

The arc interconnect has four parameters: the **width**, **radius**, **angle** and **offset**.
The radius refers to the center of the waveguide. The offset parameter defines
a lateral shift when connecting a waveguide interconnect. This is needed for
a low-loss and a low mode-conversion coupling between e.g. a straight and
curved waveguide. The image shows how this is done. It means that the input and
output pins of the arc (a0 and b0) are *not* in the center, but rather are
shifted outward by an amount equal to the offset.

.. image:: arc.svg
   :width: 400
   :align: center

linear taper
------------

The linear taper connects two waveguides of different width with a linearly
tapering section. It has three parameters: the **length** and **two widths**.

parabolic taper
---------------

The parabolic taper connects two waveguides of different width with a parabolic
tapering section. It has three parameters: the **length** and **two widths**. The
larger taper angle is at the smaller width side and thus the wide waveguide
side tapers more slowly. The function describing the width from :math:`z=0` to
:math:`z=\ell`, where :math:`w_1 \le w_2`, is given by:

..  math::

    w(z) = \sqrt{\frac{z}{\ell}\cdot (w_2^2-w_1^2) + w_1^2}

.. image:: parabolic_taper.svg
   :width: 350
   :align: center

sine bend
---------

The sine bend is a kind of S-bend which has zero curvature at the start and end
of the structure. It takes three parameters, **width**, **distance** (:math:`d`) and
**shift** (:math:`s`). The transverse coordinate (:math:`x`) of the center line
versus the longitudinal coordinate (:math:`0\le z \le d`) is given by:

.. math::

   x(z) = \frac{sz}{d} - \frac{s}{2\pi}\sin\left(\frac{2\pi z}{d}\right)


.. image:: sine_bend.svg
   :width: 400
   :align: center

Interconnect specification
==========================
A draft of :download:`interconnect specification (version 0.2)<0.2/interconnect_specification.yaml>`
in YAML format.
