# -*- coding: utf-8 -*-
"""openepda.expr.py

This file contains a parser of analytic expressions.

The parser can be used to parse the analytic expressions and thus
check their correctness in a safe way, and also to evaluate the
expressions.

The grammar is intended to be very similar to the tinyexpr library
grammar (https://github.com/codeplea/tinyexpr).

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
import re
from collections import Counter
from functools import lru_cache, partial
from importlib import import_module
from itertools import chain
from keyword import kwlist
from numbers import Real
from operator import contains
from typing import (
    Any,
    ByteString,
    Dict,
    Iterable,
    List,
    MutableSequence,
    Sequence,
    Union,
)

import tatsu
from more_itertools import collapse
from tatsu.exceptions import FailedParse

# grammar symbols
OPERATORS = tuple("+-*/^%")
BRACKETS = tuple("()")
LIST_SEPARATOR = tuple(",")
LETTERS_LOWER = tuple("abcdefghijklmnopqrstuvwxyz")
LETTERS_UPPER = tuple(l.upper() for l in LETTERS_LOWER)
LETTERS_ALL = LETTERS_LOWER + LETTERS_UPPER
DIGITS = tuple("0123465789")
UNDERSCORE = tuple("_")
VARIABLE_NAME = LETTERS_ALL + UNDERSCORE + DIGITS
SPACE = tuple(" ")

ALLOWED_SYMBOLS = (
    LETTERS_ALL
    + DIGITS
    + BRACKETS
    + LIST_SEPARATOR
    + UNDERSCORE
    + SPACE
    + OPERATORS
)

# template includes placeholders for optional items. In the comments are
# examples of what should be in the placeholder.
GRAMMAR_TEMPLATE = r"""
    @@grammar :: openepda_expr
    @@whitespace :: / +/

    start = list $ ;
    list = expr ',' list | expr ;
    expr = expr {{('+' | '-') term}} | term ;
    term = term '%' factor | term '*' factor | term '/' factor | factor ;
    factor = factor "{power_op}" power | power ;  # association right or left
    power = '+' power | '-' power | base ;
    base = number
           {func2_base}  # | func2 '(' expr ',' expr ')'
           {func1_base}  # | func1 '(' expr ')'
           {allow_skip_parenth}  # | func1 power  # optional
           {allow_parenth_after_const}  # | const '(' ')'  # optional
           {const_base}  # | const  # optional
           | var
           | "(" list ")" ;

    number = /\d*\.\d+[eE][+-]?\d+/
             | /\d+\.?[eE][+-]?\d+/
             | /\d*\.\d+/
             | /\d+\.?/ ;

    {const_list}  # const = 'e' | 'pi' ;

    {func1_list}  # func1 = 'abs' | 'acos' | 'asin' | 'atan' | 'ceil' | 'cos'
                  # | 'cosh' |'exp' | 'fac' | 'floor' | 'ln' | 'log' | 'log10'
                  # | 'sin' |'sinh' | 'sqrt' | 'tan' | 'tanh' ;

    {func2_list}  # func2 = 'atan2' | 'pow' | 'npr' | 'ncr' ;

    # var = /[a-zA-Z][a-zA-Z0-9_]*/ ;
    var = {exclude} var:/[a-zA-Z][a-zA-Z0-9_]*/;
"""

CHOICES_TEMPLATE = "{name} = {choices_str} ;"
EXCLUDE_TEMPLATE = "! ( {choices_str} )"

# Predefined identifiers
CONSTANTS_MAP = {"pi": ("math", "pi"), "e": ("math", "e")}
CONSTANTS = tuple(CONSTANTS_MAP.keys())

# Mapping of functions available in the expressions, 1 and 2 parameters
STANDARD_FCNS_1_ARG_MAP = {
    "abs": ("math", "fabs"),
    "acos": ("math", "acos"),
    "asin": ("math", "asin"),
    "atan": ("math", "atan"),
    "ceil": ("math", "ceil"),
    "cos": ("math", "cos"),
    "cosh": ("math", "cosh"),
    "exp": ("math", "exp"),
    "fac": ("math", "factorial"),
    "floor": ("math", "floor"),
    "ln": ("math", "log"),
    # "log": ("math", "log"),  # option to use log10
    "log10": ("math", "log10"),
    "sin": ("math", "sin"),
    "sinh": ("math", "sinh"),
    "sqrt": ("math", "sqrt"),
    "tan": ("math", "tan"),
    "tanh": ("math", "tanh"),
}
STANDARD_FCNS_1_ARG = tuple(STANDARD_FCNS_1_ARG_MAP.keys())

STANDARD_FCNS_2_ARG_MAP = {
    "atan2": ("math", "atan2"),
    "pow": ("math", "pow"),
    "ncr": ("scipy.special", "comb"),
    "npr": ("scipy.special", "perm"),
}
STANDARD_FCNS_2_ARG = tuple(STANDARD_FCNS_2_ARG_MAP.keys())


class OpenEpdaError(Exception):
    pass


class OpenEpdaExpressionError(Exception):
    pass


class _BaseParser(object):
    KW_SUFFIX = "_KW"

    def __init__(
        self,
        allow_skip_parenth=False,
        use_nat_log=False,
        power_from_right=True,
        use_caret_for_power=True,
        constants=None,
        functions_1=None,
        functions_2=None,
        allow_parenth_after_const=False,
        parameters=(),
        exclude=(),
    ):
        """Create a parser.

        `constants`, `functions_1`, `functions_2` are dictionaries in the
        form: {'expression_name': ('module_name', 'module_attribute')}.
        `parameters` are just an iterable with variable identifiers.
        Their values are submitted to the eval method.

        Parameters
        ----------
        allow_skip_parenth : bool
            if True, in expressions with function of one argument
            (e.g. 'sin 0.5') parentheses can be omitted. If False,
            parentheses are required. Note, that if this option is True,
            parsing of the expression is possible, but evaluation is not
            currently supported.
        use_nat_log : bool
            if True, `log` evaluates to the natural logarithm. Otherwise,
            it is log10.
        power_from_right : bool
            if True, the following association rules are used for
            exponentiation: `a^b^c == a^(b^c)` and `-a^b == -(a^b)`. This is
            default Python behavior. If False, the following rules are used:
            `a^b^c == (a^b)^c` and `-a^b == (-a)^b`. Note, that if this
            option is True, parsing of the expression is possible, but
            evaluation is not currently supported.
        use_caret_for_power : bool
            if True, caret symbol '^' will be used for power operation.
            Otherwise, a standard python operator '**' is used.
        constants : dict
            constants to be allowed in the expression.
        functions_1 : dict
            list of functions of 1 argument to be allowed in the expression.
        functions_2 : dict
            list of functions of 2 arguments to be allowed in the expression.
        parameters : list
            list of parameter identifiers to be allowed in the expression.
        exclude : iterable of str
            identifiers to be excluded from the final list
        """
        # parsing options
        self._allow_parenth_after_const = allow_parenth_after_const
        self._use_caret_for_power = use_caret_for_power

        self._allow_skip_parenth = allow_skip_parenth  # not used
        self._power_from_right = power_from_right  # not used

        # evaluation option
        self._use_nat_log = use_nat_log

        self._exclude = exclude

        constants = constants or {}
        functions_1 = functions_1 or {}
        functions_2 = functions_2 or {}

        # member variables
        self._parser = None
        self._imported_symbols = {}

        # import and add symbols
        self._check_symbols(constants.keys())
        added_symbols = self._add_symbols(constants, exclude=self._exclude)
        self._constants = added_symbols

        self._check_symbols(functions_1.keys())
        added_symbols = self._add_symbols(functions_1, exclude=self._exclude)
        self._f1 = added_symbols

        self._check_symbols(functions_2.keys())
        added_symbols = self._add_symbols(functions_2, exclude=self._exclude)
        self._f2 = added_symbols

        self._check_symbols(parameters)
        self._vars = parameters

        # create parser
        self.compile_parser()

    def _check_symbols(self, symbols):
        """Check if the symbols are allowed in the expression

        The check will not pass if:
            - there are repetitions inside symbols
            - any symbol was already defined before in this parser

        Parameters
        ----------
        symbols : iterable of str

        Returns
        -------
        True

        Raises
        ------
        ValueError:
            if the check fails.
        """
        if len(symbols) == 0:
            return True

        # check there is no repeated symbols
        repeated_symb, no_repetitions = Counter(symbols).most_common()[0]
        if no_repetitions > 1:
            raise OpenEpdaExpressionError(
                'Symbol "{}" is defined more than once ({} times).'.format(
                    repeated_symb, no_repetitions
                )
            )

        # Check each symbol
        for s in symbols:
            if s in self._imported_symbols.keys():
                # already defined symbols
                raise OpenEpdaExpressionError(
                    'Symbol "{}" is already defined.'.format(s)
                )
        return True

    def _clean_keywords(self, expr, param_values):
        param_values = param_values.copy()
        for kw in kwlist:
            expr, n_repl = re.subn(
                r"\b{}\b".format(kw), "{}{}".format(kw, self.KW_SUFFIX), expr
            )
            if n_repl:
                v = param_values.pop(kw)
                param_values.update({"{}{}".format(kw, self.KW_SUFFIX): v})

        return expr, param_values

    @property
    def reserved_identifiers(self):
        return tuple(self._imported_symbols)

    def _add_symbols(self, symbols, exclude=()):
        """

        Parameters
        ----------
        symbols : dict

        exclude : iterable of str

        Returns
        -------
        tuple of str
            list of imported symbols
        """
        res = make_symbol_mapping(symbols, exclude=exclude)
        self._imported_symbols.update(res)
        return tuple(res.keys())

    def compile_parser(self):
        """Create a parser.

        This is an expensive action, so preferably has to be done only
        once. Parsing itself is much faster.
        """
        # Create data to fill grammar template
        # lists of symbols
        const_list = make_grammar_choice_item("const", self._constants)
        func1_list = make_grammar_choice_item("func1", self._f1)
        func2_list = make_grammar_choice_item("func2", self._f2)

        const_base = r"| const" if const_list else ""
        func1_base = r"| func1 '(' expr ')'" if func1_list else ""
        func2_base = r"| func2 '(' expr ',' expr ')'" if func2_list else ""

        exclude = make_grammar_exclude_item(
            kwlist, self._constants, self._f1, self._f2
        )

        # optional items
        if self._allow_skip_parenth and func1_list:
            allow_skip_parenth = "| func1 power"
        else:
            allow_skip_parenth = ""

        if self._allow_parenth_after_const and const_list:
            allow_parenth_after_const = "| const '(' ')'"
        else:
            allow_parenth_after_const = ""

        power_op = "^" if self._use_caret_for_power else "**"

        grammar = GRAMMAR_TEMPLATE.format(
            power_op=power_op,
            const_base=const_base,
            const_list=const_list,
            func1_base=func1_base,
            func1_list=func1_list,
            func2_base=func2_base,
            func2_list=func2_list,
            allow_skip_parenth=allow_skip_parenth,
            allow_parenth_after_const=allow_parenth_after_const,
            exclude=exclude,
        )

        # print(grammar)
        self._parser = tatsu.compile(grammar)

    @lru_cache(maxsize=1000)
    def parse(self, expr):
        """Parse the expression.

        Parameters
        ----------
        expr : str
            expression to be parsed

        Returns
        -------
        tatsu.contexts.closure
            AST for the expression
        """
        if not self._parser:
            raise OpenEpdaExpressionError("Parser has not been created yet.")

        if expr == "":
            raise OpenEpdaExpressionError("Cannot parse empty expression")

        try:
            ast = self._parser.parse(expr)
        except FailedParse as e:
            raise OpenEpdaExpressionError(
                "error parsing expression '{}': {}.".format(expr, e)
            )
        return ast

    def get_parameter_names(self, expr: str):
        """Parse expression and get the names of parameters used in it.

        Parameters
        ----------
        expr : str
            expression to the parsed

        Returns
        -------
        set of str
            set of parameter names present in the expression
        """
        # Replace all numeric values by 666. This is done to make
        # better use of parser cache: for the task of checking
        # parameter names it does not matter which numeric values are
        # there.
        # several digits followed by optional decimal part
        pattern = r"\b\d+\.?\d*\b"
        repl = "666"
        expr = re.sub(pattern, repl, expr)

        # Clean the keywords
        # expr = self._clean_keywords(expr)

        ast = self.parse(expr)
        flat_ast = collapse(ast, base_type=dict)
        param_names = {
            item["var"] for item in flat_ast if isinstance(item, dict)
        }
        return param_names

    def eval(self, expr, param_values: Dict[str, Any] = None):
        """

        Parameters
        ----------
        expr : str
            expression to be evaluated
        param_values : Dict[str, Any]
            {'parameter_name': parameter_value}

        Returns
        -------
        Any
            evaluation result
        """
        if not self._power_from_right:
            raise NotImplementedError(
                "Evaluations of expressions with left association of "
                "exponentiation is not implemented."
            )

        if self._allow_skip_parenth:
            raise NotImplementedError(
                "Evaluations of expressions with missing parentheses "
                "for a function of one argument is not implemented."
            )

        param_values = param_values or {}
        self.check_missing_params(expr, frozenset(param_values.keys()))

        if self._allow_parenth_after_const:
            for c in self._constants:
                expr = re.sub(r"{}\( *\)".format(c), "{}".format(c), expr)

        if self._use_caret_for_power:
            expr = expr.replace("^", "**")

        expr, param_values = self._clean_keywords(expr, param_values)

        res = eval(expr, self._imported_symbols, param_values)
        return res

    def check_missing_params(self, expr, params: Iterable[str]):
        """Verify that all params that are present in the expr are present.

        Parameters
        ----------
        expr : str

        params : Iterable of str
            allowed parameters

        """
        actual_param_names = self.get_parameter_names(expr)
        missing_params = actual_param_names - set(params)
        if missing_params:
            raise OpenEpdaExpressionError(
                "expression '{}' contains undefined params: {}.".format(
                    expr, missing_params
                )
            )
        else:
            return True


def make_choice_list(*choices, exclude=()):
    """Combine choices into a single list with unique items.

    Some of the choices can be excluded.

    Parameters
    ----------
    choices : iterable of str
        each iterable contains a list of functions to be included into
        the symbols.
    exclude: iterable of str
        list of symbols to be excluded.
    Returns
    -------
    list of str
        sorted list of symbols, where all choices are united, and
        strings from exclude parameter are removed.
    """
    choices_clean = sorted(set(chain.from_iterable(choices)))

    ch = list(c for c in choices_clean if c not in exclude)
    return ch


def make_symbol_mapping(mapping, exclude=()):
    """Import all symbols from the mapping using their name

    Parameters
    ----------
    mapping : Dict[str, Tuple(str, str)]
        keys are symbol names, values are 2-tuples. value[0] is a
        module name, value[1] is attribute name to be imported from this
        module and to be used under symbol name.
    exclude : iterable of str
        identifiers to be excluded from the final list

    Returns
    -------
    Dict[str, Any]
        keys are imported symbol names, values are imported entities,
        e.g. function, parameters, etc.
    """
    res = {}

    for symbol_name, (module_name, attr) in mapping.items():
        if symbol_name in exclude:
            continue
        m = import_module(module_name)
        try:
            symbol = getattr(m, attr)
        except AttributeError as e:
            raise ValueError(
                "Incorrect data for symbol '{}', cannot import it: {}.".format(
                    symbol_name, e
                )
            )
        res.update({symbol_name: symbol})
    return res


def make_choice_str(choices=None):
    """

    Parameters
    ----------
    choices : iterable of str

    Returns
    -------
    str
    """
    if choices:
        choices_str = "' | '".join(choices)
        if choices_str != "":
            choices_str = "'{}'".format(choices_str)
    else:
        choices_str = ""

    return choices_str


def make_grammar_choice_item(name="", choices=None):
    choices_str = make_choice_str(choices)

    if choices_str != "":
        res = CHOICES_TEMPLATE.format(name=name, choices_str=choices_str)
    else:
        res = ""
    return res


def make_grammar_exclude_item(*choices):
    choices_flat = chain.from_iterable(choices)
    choices_str = make_choice_str(choices_flat)

    if choices_str != "":
        res = EXCLUDE_TEMPLATE.format(choices_str=choices_str)
    else:
        res = ""
    return res


def check_parameter_name(name, reserved=()):
    """Check if name can be used as identifier in the expression.

    - Contains letters, underscores, or digits
    - Starts with a letter
    - Is not one of the reserved identifiers

    Parameters
    ----------
    name : str
        identifier to be checked
    reserved : iterable of str
        identifiers which are reserved and are therefore illegal,
        e.g. for other functions.

    Returns
    -------
    bool
        True if name is a correct identifier
    """
    if not (name[0] in LETTERS_LOWER or name[0] in LETTERS_UPPER):
        # First symbol
        raise OpenEpdaExpressionError(
            'First symbol of the parameter name "{}" is not one of allowed'
            " symbols.".format(name)
        )
    elif set(name) - set(VARIABLE_NAME):
        # Other symbols
        raise OpenEpdaExpressionError(
            'Parameter name "{}" contains symbol(s) which is (are) not '
            "letters or an underscore.".format(name)
        )
    elif name in reserved:
        raise OpenEpdaExpressionError(
            'Parameter name "{}" is a reserved identifier.'.format(name)
        )
    else:
        return True


def check_expr(expr):
    if not isinstance(expr, str):
        raise TypeError(
            "Expression is not a str type. It is {}.".format(type(expr))
        )

    expr = expr.replace(" ", "")  # remove whitespaces

    if not all(map(partial(contains, ALLOWED_SYMBOLS), expr)):
        raise OpenEpdaExpressionError("Expression contains illegal symbols.")
    else:
        return True


openepda_parser = _BaseParser(
    functions_1=STANDARD_FCNS_1_ARG_MAP,
    functions_2=STANDARD_FCNS_2_ARG_MAP,
    constants=CONSTANTS_MAP,
    # exclude="ln",
)

TNestedSequence = Union[str, Real, Sequence["TNestedSequence"]]
TNestedRealSequence = Union[Real, Sequence["TNestedRealSequence"]]
TNestedRealList = Union[Real, List["TNestedRealList"]]


def evaluate_expression(
    expr: TNestedSequence, param_values: Dict[str, Any] = None
) -> Union[Real, TNestedRealList]:
    """Evaluate expression if necessary and return a numeric value.

    Parameters
    ----------
    expr : TNestedSequence
        expression to be checked and evaluated if needed. Can be a sequence
        of expressions, or a sequence of sequences...
    param_values : Optional[Dict[str, Any]]
        Parameter values to be used during expression evaluation.
        We do not restrict parameter values to the Real type, however,
        this could make sense. It depends on whether the functions used in the
        expression are able to produce numeric output for non-numeric inputs.

    Returns
    -------
    res : Union[Real, TNestedRealList]
        the input expression if it is a number, or the expression evaluation
         result if it is a number.

    Raises
    ------
    TypeError
        In cases when the expression cannot be evaluated, or when it returned
        a non-numeric result.
    """
    if isinstance(expr, Real):
        res = expr
    elif isinstance(expr, str):
        res = openepda_parser.eval(expr, param_values=param_values)
        if not isinstance(res, Real):
            raise TypeError(
                "Expression '{}' was evaluated, and a non-numeric type {} "
                "was returned. Evaluation result: {}.".format(
                    expr, type(res), res
                )
            )
    elif isinstance(expr, (MutableSequence, list)):
        res = [evaluate_expression(e, param_values=param_values) for e in expr]
    elif isinstance(expr, tuple):
        res = tuple(
            evaluate_expression(e, param_values=param_values) for e in expr
        )
    elif isinstance(expr, Sequence) and not isinstance(ByteString):
        res = tuple(
            evaluate_expression(e, param_values=param_values) for e in expr
        )
    else:
        raise TypeError(
            "Provided input '{}' has type {}. It is not a string or a number, "
            "and therefore cannot be evaluated as a numeric value. ".format(
                expr, type(expr)
            )
        )
    return res
