# -*- coding: utf-8 -*-
"""openepda.validators.py

This file contains validators for the data formats defined by
the openEPDA.

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
import os
from itertools import chain
from numbers import Real

from .expr import OpenEpdaExpressionError
from .expr import check_parameter_name
from .expr import openepda_parser

try:
    from ruamel.yaml import YAML

    yaml = YAML(typ="safe")
    safe_load = yaml.load
except ImportError:
    from yaml import safe_load


module_fpath = os.path.abspath(os.path.join(__file__, ".."))

CDF_VERSIONS = ["0.1", "0.2", "0.3"]
CDF_SCHEMA_NAME_TEMPLATE = "/schemas/cdf_schema_v{version}.yaml"

UPDK_SBB_VERSIONS = ["0.3", "0.2"]
UPDK_SBB_SCHEMA_NAME_TEMPLATE = "/schemas/updk_sbb_schema_v{version}.yaml"


def is_cdf_valid(data, version="latest", raise_error=False, full_output=False):
    """Check if the data is a correct CDF of a given version.

    JSON Schema is used for validation. See http://json-schema.org

    Parameters
    ----------
    data : any
        data structure to be validated
    version : str
        CDF format version, 'X.Y' or 'latest'
    raise_error : bool
        If True, a jsonschema.ValidationError is raised in case of wrong
        format. If False, a boolean result will be returned (with
        optional message).
    full_output : bool
        If False, only resulting boolean value is returned. Otherwise,
        additional string with a validation message is returned.

    Returns
    -------
    bool
        validation result
    str
        validation message (optional)

    Examples
    --------
    >>> with open('tests/_test_data/cdf_correct_v0.3.cdf') as s:
    ...     data = safe_load(s)
    >>> is_cdf_valid(data, raise_error=False)
    True

    >>> is_cdf_valid(data, version='0.3', raise_error=False)
    True

    """
    from jsonschema import validate, ValidationError

    allowed_versions = ["latest"] + CDF_VERSIONS
    if version not in allowed_versions:
        raise ValueError(
            "Unknown version of the CDF specified: {version}. "
            "Allowed versions: {allowed_versions}.".format(
                version=version, allowed_versions=allowed_versions
            )
        )
    if version == "latest":
        version = CDF_VERSIONS[-1]

    cdf_schema_file_name = module_fpath + CDF_SCHEMA_NAME_TEMPLATE.format(
        version=version
    )

    with open(cdf_schema_file_name) as s:
        schema = safe_load(s)

    # default reply
    result, msg = True, "Data is valid CDF v.{version}.".format(version=version)

    # Validate against the schema
    if raise_error:
        validate(instance=data, schema=schema)
    else:
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            result = False
            msg = str(e)

    if full_output:
        return result, msg
    else:
        return result


def is_updk_sbb_valid(
    data, version="latest", raise_error=False, full_output=False
):
    """Check if the data structure is a correct uPDK SBB.

    JSON Schema is used for validation. See http://json-schema.org .
    Validation runs against a specification with a given version.

    Parameters
    ----------
    data : Dict
        data structure to be validated
    version : str
        format version, 'X.Y' or 'latest'
    raise_error : bool
        If True, a jsonschema.ValidationError is raised in case of wrong
        format. If False, an boolean result will be returned (with
        optional message).
    full_output : bool
        If False, only resulting boolean value is returned. Otherwise,
        additional string with a validation message is returned.

    Returns
    -------
    bool
        validation result
    str
        validation message (optional)

    Examples
    --------
    >>> with open('tests/_test_data/sbb_correct_v0.2.yaml') as s:
    ...     data = safe_load(s)
    >>> is_updk_sbb_valid(data, raise_error=True)
    True

    """
    from jsonschema import validate, ValidationError

    allowed_versions = ["latest"] + UPDK_SBB_VERSIONS
    if version not in allowed_versions:
        raise ValueError(
            "Unknown version of the uPDK specified: {version}. "
            "Allowed versions: {allowed_versions}.".format(
                version=version, allowed_versions=allowed_versions
            )
        )
    if version == "latest":
        version = UPDK_SBB_VERSIONS[-1]

    updk_schema_file_name = module_fpath + UPDK_SBB_SCHEMA_NAME_TEMPLATE.format(
        version=version
    )

    with open(updk_schema_file_name) as s:
        schema = safe_load(s)

    # default reply
    result, msg = True, "Data is valid uPDK SBB v.{}.".format(version)

    # validate against the schema
    if raise_error:
        validate(instance=data, schema=schema)
    else:
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            result = False
            msg = str(e)

    # validate bb parameter names
    if result:
        if raise_error:
            _check_building_blocks(data["blocks"])
        else:
            try:
                _check_building_blocks(data["blocks"])
            except ValueError as e:
                result = False
                msg = str(e)

    if full_output:
        return result, msg
    else:
        return result


def _check_building_blocks(building_blocks):
    """Check building blocks' params and expressions.

    Parameters
    ----------
    building_blocks : dict

    Returns
    -------
    bool
        True if all BBs are correct

    Raises
    ------
    ValueError
        if check fails
    """
    for bb_name, bb in building_blocks.items():
        _check_building_block(bb_name, bb)


def _check_building_block(bb_name, bb):
    """Check building blocks' params and expressions.

    Currently checking:
        - BB parameter names
        - BB width, length expressions
        - BB bounding box coordinates
        - BB pins width and xya

    Parameters
    ----------
    bb_name : str
        name of the building block.
    bb : dict
        Building block item from the uPDK.

    Returns
    -------
    bool
        True if all BBs are correct

    Raises
    ------
    ValueError
        if check fails
    """
    # Check parameters
    has_params = bool(bb["parameters"])

    if has_params:
        for name, param in bb["parameters"].items():
            _check_parameter(name, param, bb_name)
        bb_params = list(bb["parameters"].keys())
    else:
        bb_params = []

    if "bb_width" in bb:
        _check_bb_num_value(bb["bb_width"], bb_name, params=bb_params)

    if "bb_length" in bb:
        _check_bb_num_value(bb["bb_length"], bb_name, params=bb_params)

    # check bbox
    _check_bbox(bb["bbox"], bb_name, bb_params)

    # check pins
    for pin_name, pin in bb["pins"].items():
        _check_pin(pin_name, pin, bb_name, bb_params)

    for p in ("pin_in", "pin_out"):
        if p in bb:
            if not bb[p] in bb["pins"].keys():
                raise ValueError(
                    "{} '{}' is not present in the list of pins "
                    "for in BB {}.".format(p, bb["pin_in"], bb_name)
                )

    return True


def _check_parameter(name, data, bb_name):
    check_parameter_name(name, reserved=openepda_parser.reserved_identifiers)


def _check_bbox(bbox_data, bb_name, bb_params):
    # check bbox
    for bbox_coord_expr in chain(*bbox_data):
        _check_bb_num_value(bbox_coord_expr, bb_name, params=bb_params)


def _check_bb_num_value(v, bb_name, params=(), parser=openepda_parser):
    """Wrapper around _check_num_value() for BB params.
    """
    try:
        _check_num_value(v, params=params, parser=parser)
    except OpenEpdaExpressionError as e:
        raise ValueError(
            "error in numeric value in BB {}: {}".format(bb_name, e)
        )
    return True


def _check_pin(pin_name, pin_data, bb_name, bb_params):
    _check_pin_num_value(pin_data["width"], pin_name, bb_name, params=bb_params)
    for i in range(3):
        _check_pin_num_value(
            pin_data["xya"][i], pin_name, bb_name, params=bb_params
        )


def _check_pin_num_value(
    v, pin_name, bb_name, params=(), parser=openepda_parser
):
    """Wrapper around _check_num_value() for BB pin params.
    """
    try:
        _check_num_value(v, params=params, parser=parser)
    except OpenEpdaExpressionError as e:
        raise ValueError(
            "error in numeric value in pin {} of BB {}: {}".format(
                pin_name, bb_name, e
            )
        )
    return True


def _check_num_value(v, params=(), parser=openepda_parser):
    """Check if the value is a proper number or expression

    Check is successful if the expression is a number, or if:
        - expression can be parsed using parser
        - it contains only params which are explicitly listed in params

    Parameters
    ----------
    v : num or str
        Expression to be checked.
    params : iterable of str
        list of allowed variable names
    parser : _BaseParser
        parser to be used for the expression parsing

    Returns
    -------
    bool
        True if expr is correct

    Raises
    ------
    ValueError
        if the check is not successful
    """
    if isinstance(v, Real):
        return True
    else:
        return parser.check_missing_params(v, params)


def main():
    import doctest

    os.chdir("{}/..".format(module_fpath))
    doctest.testmod(verbose=False)


if __name__ == "__main__":
    main()
