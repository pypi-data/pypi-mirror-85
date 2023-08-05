.. _analytic_expressions:

==========================
Analytic Expression Format
==========================

Introduction
============

In many cases, the coordinates, the sizes, locations and other numeric
values can be represented as real numbers. However, often an analytic
expression which is evaluated at runtime is needed. Example use cases are
parametric building blocks and compact models describing bulding block
performance. Therefore, openEPDA defines a standardized analytic expression
format, which can be used anywhere where a numeric value is expected.

Grammar
=======

Informal summary
----------------
The expression grammar was chosen to cover a minimum yet  set of expressions.
It supports standard mathematical operations, basic mathematical
functions and variables defined at runtime.

Expressions can include the following items:

- basic binary arithmetic operations (addition `+`, subtraction `-`,
  multiplication `*`, division `/`, exponentiation `^`, and modulus `%`);
- unary negation `-`;
- mathematical functions (1 argument): `abs`, `acos`, `asin`, `ceil`,
  `cos`, `cosh`, `exp`, `fac`, `floor`, `log`, `log10`, `sin`, `sinh`,
  `sqrt`, `tan`, `tanh`;
- mathematical functions (2 arguments): `atan2`, `pow`;
- constants: `e`, `pi`;
- numbers (as defined in `RFC 7159 - The JSON Data Interchange Format,
  Section 6. Numbers <https://tools.ietf.org/html/rfc7159.html#section-6>`_);
- arbitrary variable identifiers, starting with a letter, and containing
  small and capital letters `[a-zA-Z]`, digits `[0-9]`, and an
  underscore `_`;
- combinations of the above enclosed in the parentheses `(` and `)`.

Notes:

- `log` function stands for natural logarithm.
- variable identifiers can not be reserved python keywords. See the list
  `here <https://docs.python.org/3.8/reference/lexical_analysis.html#keywords>`_.

Formal description
------------------
To be added after the specification and reference implementation is complete.

Evaluation
==========
A result of expression evaluation should be a numeric value. This means
that the information required for expression evaluation (such as variable
values) should be available prior to evaluation.

A valid expression can be evaluated using the standard python's `eval`
function. Also, a valid openEPDA expression is possible to evaluate using
`tinyexpr C parser <https://github.com/codeplea/tinyexpr>`_.

A parser (e.g. to check expression validity) and an evaluator are available
in the `openepda <https://pypi.org/project/openepda/>`_ python package.
