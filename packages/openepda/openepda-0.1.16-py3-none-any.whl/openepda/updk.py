# -*- coding: utf-8 -*-
"""openepda.updk.py

This file contains tools to work with uPDK files.

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import lru_cache
from io import StringIO
from numbers import Real
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

from .expr import TNestedRealList, evaluate_expression
from .geometry import isclose
from .geometry import process_polygon_vertices
from .geometry import TPtList

from .imports import HAS_NAZCA_DESIGN, dump_long, dump_short, safe_load
from .validators import (
    _check_building_block,
    _check_parameter,
    _check_pin,
    is_updk_sbb_valid,
)

if HAS_NAZCA_DESIGN:
    from .imports import nd

DEFAULT_BB_OUTLINE_LAYER = 1020
DEFAULT_BB_INFO_LAYER = 1025
DEFAULT_BB_PARAMS_LAYER = 1026
DEFAULT_PIN_LAYER = 1004
DEFAULT_PIN_INFO_LAYER = 1006
DEFAULT_BBOX_LAYER = 1021
DEFAULT_BB_METAL_OUTLINE_LAYER = 1027


def _check_or_add_xsection(xs_name, layer=DEFAULT_PIN_LAYER):
    if not HAS_NAZCA_DESIGN:
        print("This function requires nazca package.")
        return None

    try:
        nd.get_xsection(xs_name)
    except Exception:
        nd.add_layer(name=xs_name, layer=layer, accuracy=0.05)
        nd.add_xsection(name=xs_name)
        nd.add_layer2xsection(xsection=xs_name, layer=xs_name, accuracy=0.05)


def _get_or_add_layer(layer_name, layer=DEFAULT_BB_OUTLINE_LAYER):
    if not HAS_NAZCA_DESIGN:
        print("This function requires nazca package.")
        return None

    if layer_name in nd.get_layers().index:
        res = layer_name
    else:
        res = nd.add_layer(name=layer_name, layer=layer, accuracy=0.05)

    assert res == layer_name
    return res


class ParametrizedEntity(ABC):
    """Interface for classes with parameters.
    """

    @abstractmethod
    def get_parameter_values(self) -> Optional[Dict[str, Real]]:
        raise NotImplementedError


class ParametrizedChildEntity(ParametrizedEntity):
    """Mixin class implementing access to parent parameters

    """

    def __init__(self, parent: ParametrizedEntity = None):
        self._parent = parent

    def get_parameter_values(self):
        """Implementation of the interface method, using parent parameters.

        Returns
        -------

        """
        if not hasattr(self, "_parent"):
            self.__init__()
        elif self._parent:
            return self._parent.get_parameter_values()
        else:
            return {}


def ensure_num(
    func: Callable[[ParametrizedEntity], Any]
) -> Callable[[ParametrizedEntity], TNestedRealList]:
    """Decorator to ensure numeric type of the returned values.

    This decorator is used to ensure that the returned value has a numeric
    type. It passes the returned value through the evaluate_expression()
    function.

    This decorator is to be used on methods only, as it required the first
    argument of the decorated function to accept the class instance.

    If your would like to wrap a property, first apply this decorator, and
    then apply @property decorator:

    .. code-block:: python

        class A():

            @property
            @ensure_num
            def value(self):
                return 100

    Parameters
    ----------
    func : Callable[[ParametrizedEntity], Any]
        method to be wrapped

    Returns
    -------
    func : Callable[[ParametrizedEntity], TNestedRealList]
        wrapped method
    """

    def wrapper(inst):
        res = func(inst)
        if isinstance(res, Real):
            # This check is also performed in evaluate_expression(),
            # but we keep it here for no reason.
            pass
        else:
            param_values = inst.get_parameter_values()
            res = evaluate_expression(expr=res, param_values=param_values)
        return res

    return wrapper


class BBox(ParametrizedChildEntity):
    """Class to handle building block bounding boxes.

    Bounding box is a rectangle aligned with XY axis, and is characterized
    by its south-west and north-east corners.
    """

    def __init__(
        self,
        sw: Tuple[Real, Real],
        ne: Tuple[Real, Real],
        parent: Optional["BB"] = None,
    ):
        super().__init__(parent)
        assert sw[0] < ne[0]
        assert sw[1] < ne[1]
        self._sw = sw
        self._ne = ne

    @property
    def length(self) -> Real:
        """Bounding box size along X-axis

        Returns
        -------
        Real
        """
        length = self._ne[0] - self._sw[0]
        assert length >= 0
        return length

    @property
    def width(self) -> Real:
        """Bounding box size along Y-axis

        Returns
        -------
        Real
        """
        w = self._ne[1] - self._sw[1]
        assert w >= 0
        return w

    @property
    def sw(self) -> Tuple[Real, Real]:
        return self._sw

    @property
    def ne(self) -> Tuple[Real, Real]:
        return self._ne

    @property
    def nw(self) -> Tuple[Real, Real]:
        return self._sw[0], self._ne[1]

    @property
    def se(self) -> Tuple[Real, Real]:
        return self._ne[0], self._sw[1]

    @staticmethod
    def from_points(
        pts: Iterable[Tuple[Real, Real]], parent: ParametrizedEntity = None
    ):
        """Create a bounding box from a list of points.

        Points can describe any polygon.

        Parameters
        ----------
        pts: Iterable[Tuple[Real, Real]]
            List of (x, y) coordinates of the points.
        parent : Optional[ParametrizedEntity]
            Parent for the bounding box.

        Returns
        -------
        BBox
            Minimal bounding box which includes all points.
        """
        param_values = parent.get_parameter_values() if parent else {}
        x_coords = [
            evaluate_expression(p[0], param_values=param_values) for p in pts
        ]
        y_coords = [
            evaluate_expression(p[1], param_values=param_values) for p in pts
        ]

        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        return BBox(sw=(x_min, y_min), ne=(x_max, y_max), parent=parent)

    @property
    def center(self) -> Tuple[Real, Real]:
        return (
            (self._sw[0] + self._ne[0]) // 2,
            (self._sw[1] + self._ne[1]) // 2,
        )

    def __eq__(self, other: "BBox") -> bool:
        sw = isclose(self._sw, other._sw, abs_tol=1e-10, rel_tol=1e-10)
        ne = isclose(self._ne, other._ne, abs_tol=1e-10, rel_tol=1e-10)
        return sw and ne

    def __str__(self):
        return f"<BBox (sw={self.sw}, ne={self.ne})>"


class Polygon(ParametrizedChildEntity):
    def __init__(
        self,
        points: Iterable[Tuple[Real, Real]],
        parent: Optional["BB"] = None,
    ):
        super().__init__(parent)
        self._points = None
        self.points = points

    @property
    def points(self) -> TPtList:
        return self._points

    @staticmethod
    def from_points(
        points: Iterable[Tuple[Real, Real]], parent: ParametrizedEntity = None
    ):
        param_values = parent.get_parameter_values() if parent else {}
        points_num = [
            (
                evaluate_expression(p[0], param_values=param_values),
                evaluate_expression(p[1], param_values=param_values),
            )
            for p in points
        ]
        return Polygon(points=points_num, parent=parent)

    @points.setter
    def points(self, value):
        self._points = process_polygon_vertices(
            value,
            sort=True,
            orient=True,
            clockwise=True,
            make_valid=False,
            close=False,
        )

    @property
    def n_points(self) -> int:
        if self.points is None:
            return 0
        else:
            return len(self.points)

    def __str__(self):
        return f"<Polygon (no. points={self.n_points})>"

    def __eq__(self, other: "Polygon"):

        equal_length = self.n_points == other.n_points

        if equal_length:
            pts_equal = (
                isclose(p1[0], p2[0], abs_tol=1e-10, rel_tol=1e-10)
                and isclose(p1[1], p2[1], abs_tol=1e-10, rel_tol=1e-10)
                for (p1, p2) in zip(self.points, other.points)
            )
            return all(pts_equal)
        else:
            return False

    def __lt__(self, other):
        if self.points[0] < other.points[0]:
            return True
        elif self.points[0] > other.points[0]:
            return False
        elif self.points[1] < other.points[1]:
            return True
        else:
            return False


class BbMetalOutline(ParametrizedChildEntity):
    def __init__(
        self, outlines: Iterable[Polygon], parent: Optional["BB"] = None,
    ):
        super().__init__(parent)
        self._outlines = None
        self.outlines = outlines

    @property
    def outlines(self) -> List[Polygon]:
        return self._outlines

    @outlines.setter
    def outlines(self, value):
        assert len(value) >= 1
        type_correct = (isinstance(p, Polygon) for p in value)
        assert all(type_correct)
        self._outlines = sorted(value)

    @property
    def n_outlines(self) -> int:
        if self.outlines is None:
            return 0
        else:
            return len(self.outlines)

    @staticmethod
    def from_points(
        polygon_pts: Iterable[Iterable[Tuple[Real, Real]]],
        parent: ParametrizedEntity = None,
    ):
        param_values = parent.get_parameter_values() if parent else {}

        polygon_pts_num = [
            [
                (
                    evaluate_expression(p[0], param_values=param_values),
                    evaluate_expression(p[1], param_values=param_values),
                )
                for p in poly_points
            ]
            for poly_points in polygon_pts
        ]
        polygons = [
            Polygon(points=pts, parent=parent) for pts in polygon_pts_num
        ]
        return BbMetalOutline(outlines=polygons, parent=parent)

    def __str__(self):
        return f"<BbMetalOutline (no. outlines={self.n_outlines})>"

    def __eq__(self, other):
        equal_length = self.n_outlines == other.n_outlines

        if equal_length:
            polys_equal = (
                p1 == p2 for (p1, p2) in zip(self.outlines, other.outlines)
            )
            return all(polys_equal)
        else:
            return False


class Pin(ParametrizedChildEntity):
    DIR_SYMBOLS = defaultdict(
        lambda: "?",
        {"0.0": "->", "90.0": "/\\", "180.0": "<-", "270.0": r"\/"},
    )

    def __init__(
        self,
        name: str,
        pin_data: Dict,
        skip_checks: bool = False,
        parent: Optional["BB"] = None,
    ):
        super().__init__(parent)
        self.name = name
        self._is_valid = skip_checks

        self._data = None
        self.data = pin_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, pin_data):
        if self._data:
            raise UserWarning(
                "Can not change the existing Pin. Create a new one instead."
            )
        self._data = pin_data

        if not self._is_valid:
            try:
                if self._parent:
                    bb_name = self._parent.name
                    bb_params = list(self._parent.get_parameter_values().keys())
                else:
                    bb_name = "NOT DEFINED"
                    bb_params = []

                _check_pin(self.name, self._data, bb_name, bb_params)
            except Exception as e:
                self._data = None
                raise ValueError("Error validating the pin data: {}.".format(e))

    @property
    def xsection(self) -> str:
        return self._data["xsection"]

    @property
    @ensure_num
    def width(self) -> Real:
        width = self._data["width"]
        return width

    @property
    def doc(self) -> str:
        return self._data["doc"]

    def __str__(self):
        a_str = "{:.1f}".format(float(self.xya[2] % 360))
        direction = self.DIR_SYMBOLS[a_str]

        return "Pin {} {} (w={}, xs={})".format(
            self.name, direction, self.width, self.xsection
        )

    @property
    @ensure_num
    def xya(self) -> Tuple[Real, Real, Real]:
        return tuple(self._data["xya"])

    @property
    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "xsection": self.xsection,
            "width": self.width,
            "xya": self.xya,
        }


class Parameter(object):
    def __init__(
        self,
        name: str,
        parameter_data: Dict,
        skip_checks: bool = False,
        parent: Optional["BB"] = None,
    ):
        self._parent = parent
        self.name = name
        self._is_valid = skip_checks

        self._data = None
        self.data = parameter_data

        self._value = None
        self.value = self.default_value

    @property
    def typ(self) -> str:
        t = self.data["type"]
        assert t in ("float", "str", "bool", "int")
        return t

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, parameter_data):
        if self._data:
            raise UserWarning(
                "Can not change the existing Parameter. "
                "Create a new one instead."
            )
        self._data = parameter_data

        if not self._is_valid:
            try:
                if self._parent:
                    bb_name = self._parent.name
                else:
                    bb_name = "NOT DEFINED"
                _check_parameter(self.name, self._data, bb_name)
            except Exception as e:
                self._data = None
                raise ValueError(
                    "Error validating the parameter data: {}.".format(e)
                )

    @property
    def default_value(self) -> Real:
        return self._data["value"]

    @property
    def min_value(self) -> Optional[Real]:
        try:
            return self._data["min"]
        except KeyError:
            raise AttributeError(
                f"Parameter '{self.name}' is of '{self.typ}' type and "
                f"it does not have min value."
            )

    @property
    def max_value(self) -> Optional[Real]:
        try:
            return self._data["max"]
        except KeyError:
            raise AttributeError(
                f"Parameter '{self.name}' is of '{self.typ}' type and "
                f"it does not have max value."
            )

    @property
    def value(self) -> Real:
        if not self._value:
            self.value = self.default_value
        return self._value

    @value.setter
    def value(self, value):
        if self.typ in ("int", "float"):
            if self.min_value > value:
                raise ValueError(
                    f"Value {value} for parameter {self.name} is "
                    f"too small. Minimum value is {self.min_value}."
                )
            if value > self.max_value:
                raise ValueError(
                    f"Value {value} for parameter {self.name} is "
                    f"too large. Maximum value is {self.max_value}."
                )
            self._value = value
        elif self.typ in ("bool",):
            if not isinstance(value, bool):
                raise ValueError(
                    f"Value for parameter {self.name} should be boolean. "
                    f"{value} (type: {type(value)}) is given."
                )
            self._value = value
        elif self.typ in ("str",):
            if not isinstance(value, str):
                raise ValueError(
                    f"Value for parameter {self.name} should be string. "
                    f"{value} (type: {type(value)}) is given."
                )
            self._value = value


class BB(ParametrizedEntity):
    """Building block class to handle the uPDK block data.

    """

    CELL_TYPES = {0: "static", 1: "p-cell"}

    def __init__(self, name: str, bb_data: dict, skip_checks: bool = False):
        """Initialize new building block.

        Parameters
        ----------
        name : str
            name of the building block
        bb_data : dict
            building block data. A complex nested structure defined by
            the uPDK format.
        skip_checks : bool
            set to True if you have performed the validation and sure
            that the data is correct, expressions can be evaluated, etc.
        """
        self.name = name
        self._is_valid = skip_checks

        self._data = None
        self.data = bb_data
        self._cells: Dict[str, "nd.Cell"] = {}  # keeps {name: Cell} pairs

        # {pin_name: (pin_data, Pin)}: this structure is used to store
        # pin data and Pin instances together in a single dictionary. Pin
        # instances are not created before they are accessed by get_pin()
        # method.
        self._pins: Dict[str, Tuple[Dict, Optional[Pin]]] = {
            k: (v, None) for k, v in self.data["pins"].items()
        }

        # {parameter_name: (parameter_data, Parameter)}: This structure is
        # used to store parameter data and Parameter instances together in a
        # single dictionary. Parameter instances are not created before they are
        # accessed by get_parameter() method.
        if self.is_pcell:
            self._params: Dict[str, Tuple[Dict, Optional[Parameter]]] = {
                k: (v, None) for k, v in self.data["parameters"].items()
            }
        else:
            self._params = {}

    @property
    def full_name(self):
        """Return full name unique for a given set of parameters.

        Returns
        -------
        full_name : str
            full BB name. Takes into account current parameter values.
        """
        if self.is_pcell:
            values = self.get_parameter_values()
            if values:
                suffix = ", ".join(
                    "{}={}".format(p_name, v) for p_name, v in values.items()
                )
                full = f"{self.name}: {suffix}"
            else:
                full = self.name
        else:
            full = self.name
        return full

    @property
    def data(self) -> Dict:
        return self._data

    @data.setter
    def data(self, bb_data):
        if self._data:
            raise UserWarning(
                "Can not change the existing BB. Create a new one instead."
            )
        self._data = bb_data

        if not self._is_valid:
            try:
                _check_building_block(self.name, self._data)
            except Exception as e:
                self._data = None
                raise ValueError("Error validating the BB data: {}.".format(e))

    @property
    def is_pcell(self) -> bool:
        """Flag if the building block is parametric.

        Returns
        -------
        bool
            True if the building block is a p-cell, False if it is static.
        """
        return True if self._data["parameters"] else False

    @property
    def cell_type(self) -> str:
        return BB.CELL_TYPES[self.is_pcell]

    @property
    def current_cell(self) -> Optional["nd.Cell"]:
        return self.get_cell(self.full_name)

    @property
    def cell_names(self) -> Tuple[str]:
        """Return names of the existing cells
        """
        return tuple(sorted(self._cells.keys()))

    def get_cell(self, name) -> Optional["nd.Cell"]:
        """Get cell by the name.

        For p-cells, it provides access to previously generated cells with
        other parameters.

        Parameters
        ----------
        name : str
            The name of the generated cell.

        Returns
        -------
        cell : Optional[nazca.Cell]
        """
        if name in self.cell_names:
            return self._cells[name]
        else:
            return None

    @property
    def n_pins(self) -> int:
        return len(self._pins)

    @property
    @lru_cache(maxsize=1)
    def pin_names(self) -> Tuple[str]:
        return tuple(sorted(self._pins.keys()))

    def get_pin_data(self, name) -> Dict:
        if name not in self.pin_names:
            raise ValueError(
                f"Pin '{name}' is not defined in the {self.name} BB."
            )

        return self._pins[name][0]

    def get_pin(self, name) -> "Pin":
        """Get pin by name

        Parameters
        ----------
        name : str
            pin name

        Returns
        -------
        Pin : Pin
            Pin instance
        """
        if name not in self.pin_names:
            raise ValueError(
                f"Pin '{name}' is not defined in the {self.name} BB."
            )

        if self._pins[name][1]:
            pin = self._pins[name][1]
        else:
            data = self.get_pin_data(name)
            pin = Pin(name, data, parent=self)
            self._pins.update({name: (data, pin)})
        return pin

    @property
    @lru_cache(maxsize=1)
    def parameter_names(self) -> Union[Tuple[str], Tuple]:
        if self.is_pcell:
            return tuple(sorted(self._params.keys()))
        else:
            return ()

    def get_parameter_data(self, name) -> Dict:
        if name in self.parameter_names:
            return self._params[name][0]
        else:
            raise ValueError(
                f"Parameter '{name}' is not defined in the {self.name} BB."
            )

    def get_parameter(self, name) -> "Parameter":
        """Get parameter by name

        Parameters
        ----------
        name : str
            parameter name

        Returns
        -------
        parameter : Parameter
            parameter instance
        """
        if name not in self.parameter_names:
            raise ValueError(
                f"Parameter '{name}' is not defined in the {self.name} BB."
            )
        if self._params[name][1]:
            parameter = self._params[name][1]
        else:
            data = self.get_parameter_data(name)
            parameter = Parameter(name, data)
            self._params.update({name: (data, parameter)})
        return parameter

    def get_parameter_value(self, name) -> Real:
        return self.get_parameter(name).value

    def get_parameter_values(self) -> Dict[str, Real]:
        values = {
            name: self.get_parameter_value(name)
            for name in self.parameter_names
        }

        return values

    def __str__(self) -> str:
        return "<BB {} ({}, {} pins)>".format(
            self.name, self.cell_type, self.n_pins
        )

    @property
    @ensure_num
    def bb_outline(self) -> List[Tuple[Real, Real]]:
        return [(x, y) for x, y in self.data["bbox"]]

    @property
    def bbox(self) -> "BBox":
        return BBox.from_points(self.bb_outline, parent=self)

    @property
    def bb_metal_outline(self):
        if "bb_metal_outline" in self.data:
            return BbMetalOutline.from_points(
                self.data["bb_metal_outline"], parent=self
            )
        else:
            return None

    def get_or_make_cell(self) -> Optional["nd.Cell"]:
        """Create a cell for the building block.

        If the cell already exists, it will be returned.
        This method runs only if nazca package is installed.
        The cell is also added to private attribute _cells.

        Returns
        -------
        cell : Optional[nazca.Cell]
            None is returned in case if nazca is not installed,
            of if error occurs.
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return None
        # if self.is_pcell:
        #     print(f"Cannot create a cell for a p-cell ({self.name}).")
        #     return None
        cell = self.get_cell(self.full_name)
        if not cell:
            cell = self._make_cell()
        return cell

    def _make_cell(self, add_foundry_params=False):
        """Make a new cell.

        This is not a safe method: if the cell already exists, a new one with
        a different name will be created. Use get_or_make_cell() instead.
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return None

        try:
            # Create cross-sections
            for pin_name in self.pin_names:
                pin = self.get_pin(pin_name)
                _check_or_add_xsection(pin.xsection)

            with nd.Cell(self.full_name, hashme=False) as C:
                # C.default_pins(bb_data["pin_in"], bb_data["pin_out"])
                # C.autobbox = True
                # C.store_pins = True
                # C.version = version

                # Pins
                pin_names = []
                layer = _get_or_add_layer(
                    "pin_info_layer", DEFAULT_PIN_INFO_LAYER
                )
                for pin_name in self.pin_names:
                    pin = self.get_pin(pin_name)
                    nd.Pin(
                        name=str(pin),
                        xs=pin.xsection,
                        width=float(pin.width),
                        remark=pin.doc,
                    ).put(*pin.xya)

                    pin_info_str = StringIO()
                    dump_short(pin.info, pin_info_str)
                    pin_info_str = pin_info_str.getvalue()
                    nd.Annotation(layer=layer, text=pin_info_str).put(*pin.xya)

                    pin_names.append(str(pin))
                nd.put_stub(pin_names)

                # BB outline
                layer = _get_or_add_layer(
                    "bb_outline_layer", DEFAULT_BB_OUTLINE_LAYER
                )
                nd.Polygon(points=self.bb_outline, layer=layer).put(0)

                # BB metal outline
                layer = _get_or_add_layer(
                    "bb_metal_outline_layer", DEFAULT_BB_METAL_OUTLINE_LAYER
                )
                bb_metal_outline = self.bb_metal_outline
                if bb_metal_outline:
                    for p in bb_metal_outline.outlines:
                        nd.Polygon(points=p.points, layer=layer).put(0)

                # BB bounding box
                bbox = self.bbox
                nd.put_boundingbox(
                    "org",
                    length=float(bbox.length),
                    width=float(bbox.width),
                    raise_pins=False,
                    move=(bbox.sw[0], bbox.sw[1], 0),
                    align="lb",
                )

                # Parameter values
                pv = self.get_parameter_values()

                if pv:
                    pv_str = StringIO()
                    dump_long(pv, pv_str)
                    pv_str = pv_str.getvalue()
                    layer = _get_or_add_layer(
                        "bb_params_layer", DEFAULT_BB_PARAMS_LAYER
                    )
                    nd.Annotation(layer=layer, text=pv_str).put(
                        bbox.center[0], bbox.center[1], 0
                    )
                if add_foundry_params:
                    C.parameters = pv
                    nd.put_parameters(
                        pv, pin=(bbox.center[0], bbox.center[1], 0)
                    )

                # Cell info
                info = self.get_info()
                info_str = StringIO()
                dump_long(info, info_str)
                info_str = info_str.getvalue()
                layer = _get_or_add_layer(
                    "bb_info_layer", DEFAULT_BB_INFO_LAYER
                )
                nd.Annotation(layer=layer, text=info_str).put(0)

            # C._add_bbox()
            # if bb_text[bn]:
            #     nd.text(
            #         bb_text[bn], height=3, align="cc", layer="DeepLogic"
            #     ).put(C.pin["bc"].move(-3, 0, 90))

            self._cells.update({C.cell_name: C})
            return C
        except Exception as e:
            print(f"Error creating cell for BB '{self.full_name}': {e}.")
            return None

    @property
    def version(self) -> Optional[str]:
        try:
            return self._data["version"]
        except KeyError:
            return None

    def get_info(self):
        info = {
            "cell_name": self.name,
            "pdk_version": None,
            "bb_version": self.version,
            "bb_owner": None,
        }
        return info

    def set_parameters(self, **kwargs):
        for param_name, value in kwargs.items():
            self.set_parameter(param_name, value)

    def set_predefined_parameters(self, which="default"):
        for param_name in self.parameter_names:
            self.set_predefined_parameter(param_name, which=which)

    def set_predefined_parameter(self, name, which="default"):
        parameter = self.get_parameter(name)

        if which == "default":
            value = parameter.default_value
        elif which == "min":
            try:
                value = parameter.min_value
            except AttributeError:
                value = parameter.default_value
        elif which == "max":
            try:
                value = parameter.max_value
            except AttributeError:
                value = parameter.default_value
        else:
            raise ValueError(f"Unknown option for which: '{which}'.")

        self.set_parameter(name, value)

    def set_parameter(self, name, value):
        self.get_parameter(name).value = value
        # Reset caches here if needed
        # bbox, outline, pins


class UPDK(object):
    """Class to handle the uPDK file data.
    """

    def __init__(self, updk_data):
        self._data = None
        self.data = updk_data
        self._cells: Dict[str, "nd.Cell"] = {}

        # {bb_name: (bb_data, BB)}: This structure is used to store BB data and
        # BB instances together in a single dictionary. BB instances are not
        # created before they are accessed by get_building_block() method.
        self._bbs: Dict[str, Tuple[Dict, Optional[BB]]] = {
            k: (v, None) for k, v in self.data["blocks"].items()
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, updk_data):
        is_updk_sbb_valid(updk_data, raise_error=True)
        self._data = updk_data

    @staticmethod
    def from_file(filename):
        """Create a UPDK instance from a uPDK file.

        Parameters
        ----------
        filename
            str or a path-like object

        Returns
        -------
        updk : UPDK
        """
        with open(filename) as s:
            updk_data = safe_load(s)
        return UPDK(updk_data)

    @property
    @lru_cache(maxsize=1)
    def building_block_names(self) -> Tuple[str]:
        return tuple(sorted(self._bbs.keys()))

    def get_building_block_data(self, name) -> Dict:
        if name not in self.building_block_names:
            raise ValueError(
                f"Building block '{name}' is not defined in the uPDK."
            )

        return self._bbs[name][0]

    def get_building_block(self, name) -> BB:
        """Get building block by name

        Parameters
        ----------
        name : str
            building block name

        Returns
        -------
        bb : BB
            building block instance
        """
        if name not in self.building_block_names:
            raise ValueError(
                f"Building block '{name}' is not defined in the uPDK."
            )

        if self._bbs[name][1]:
            bb = self._bbs[name][1]
        else:
            data = self.get_building_block_data(name)
            bb = BB(name, data)
            self._bbs.update({name: (data, bb)})
        return bb

    def get_cells(self, bb_name) -> List["nd.Cell"]:
        """All generated cells for a given building block.
        """
        bb = self.get_building_block(bb_name)
        return [bb.get_cell(cell_name) for cell_name in bb.cell_names]

    @property
    def cells(self) -> List["nd.Cell"]:
        """All generated cells for all building blocks.
        """
        cells = []
        for bb_name in self.building_block_names:
            cells += self.get_cells(bb_name)

        return cells

    def make_cell(self, bb_name) -> Optional[str]:
        """Make a cell for a bb with currently set parameters.
        """
        bb = self.get_building_block(bb_name)
        return bb.get_or_make_cell()

    def make_cells(self) -> bool:
        """Create cells for the building blocks.

        This method runs only if nazca package is installed.
        Only static cells are processed now. The created cells are
        available via UPDK.cells property.

        Returns
        -------
        result : bool
            True if the cells were created successfully
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return False

        for bb_name in self.building_block_names:
            self.make_cell(bb_name)

        return True

    def export_cells(self, filename) -> bool:
        """Export building block cells to a GDSII file.

        This method runs only if nazca package is installed.
        The cells should be first created using UPDK.make_cells() method.

        Parameters
        ----------
        filename : str
            The target GDSII filename.

        Returns
        -------
        result : bool
            True if the cells were created successfully
        """
        if not HAS_NAZCA_DESIGN:
            print("This function requires nazca package.")
            return False

        if not self.cells:
            print(
                "No cells were created for this PDK. "
                "Run UPDK.make_sells() first."
            )
            return False

        nd.export_gds(self.cells, filename=filename)
        return True
