# -*- coding: utf-8 -*-
"""openepda.black_box.py

This file contains a black box interface and .

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors
"""
from abc import ABC
from abc import abstractmethod
from numbers import Real
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union as U
from pathlib import Path

from jsonschema import validate, ValidationError

from .geometry import process_polygon_vertices, isclose
from .imports import HAS_KLAYOUT
from .imports import safe_load
from .updk import BB
from .updk import DEFAULT_BB_INFO_LAYER
from .updk import DEFAULT_BB_OUTLINE_LAYER
from .updk import DEFAULT_BB_PARAMS_LAYER
from .updk import DEFAULT_BBOX_LAYER
from .updk import DEFAULT_PIN_INFO_LAYER
from .updk import UPDK
from .updk import BBox

if HAS_KLAYOUT:
    from .imports import Cell, Layout

MAPPING = {
    "bbox": [DEFAULT_BBOX_LAYER, 0],
    "bb_outline": [DEFAULT_BB_OUTLINE_LAYER, 0],
    # 'pin_location': [1004, 0],
    # 'pin_stub': [1001, 0],
    "pin_info": [DEFAULT_PIN_INFO_LAYER, 0],
    # 'pin_name': [1002, 0],
    "bb_parameters": [DEFAULT_BB_PARAMS_LAYER, 0],
    "bb_info": [DEFAULT_BB_INFO_LAYER, 0],
}

TParamValue = U[str, bool, int, Real]
TParamValues = Dict[str, TParamValue]
TPinInfoValue = U[str, float, Tuple[float, float, float]]
TPinInfo = Dict[str, TPinInfoValue]

MODULE_PATH = Path(__file__).resolve().parent


def is_gds_mapping_valid(mapping, raise_error=False, full_output=False):
    version = "0.1"
    mapping_schema_fname = (
        MODULE_PATH / "schemas" / f"gds_mapping_v{version}.yaml"
    )

    with open(mapping_schema_fname) as s:
        schema = safe_load(s)

    # default reply
    result, msg = True, f"Mapping is valid v.{version}."

    # Validate against the schema
    if raise_error:
        validate(instance=mapping, schema=schema)
    else:
        try:
            validate(instance=mapping, schema=schema)
        except ValidationError as e:
            result = False
            msg = str(e)

    if full_output:
        return result, msg
    else:
        return result


def is_pin_info_valid(pin_info, raise_error=False, full_output=False):
    version = "0.1"
    mapping_schema_fname = MODULE_PATH / "schemas" / f"pin_info_v{version}.yaml"

    with open(mapping_schema_fname) as s:
        schema = safe_load(s)

    # default reply
    result, msg = True, f"Pin info is valid v.{version}."

    # Validate against the schema
    if raise_error:
        validate(instance=pin_info, schema=schema)
    else:
        try:
            validate(instance=pin_info, schema=schema)
        except ValidationError as e:
            result = False
            msg = str(e)

    if full_output:
        return result, msg
    else:
        return result


class _BlackBox(ABC):
    """Interface to store black boxes.
    """

    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("")

    @property
    @abstractmethod
    def version(self):
        raise NotImplementedError("")

    @property
    def info(self):
        info = {
            "cell_name": self.name,
            "bb_version": self.version,
        }
        return info

    @property
    @abstractmethod
    def bb_outline(self) -> List[Tuple[Real, Real]]:
        raise NotImplementedError("")

    @property
    @abstractmethod
    def bbox(self) -> "BBox":
        raise NotImplementedError("")

    @property
    @abstractmethod
    def pin_names(self) -> Tuple[str]:
        raise NotImplementedError("")

    def get_pin_info(self, pin_name) -> Dict[str, Any]:
        """Returns pin specs

        Returns
        -------
        dict
            Must contain name (str), width (float), xsection_name (str) and
            xya (3-tuple of float)
        """
        pin_infos = self.get_pin_infos()
        assert pin_name in pin_infos
        return pin_infos[pin_name]

    @abstractmethod
    def get_pin_infos(self) -> Dict[str, TPinInfo]:
        raise NotImplementedError("")

    @property
    @abstractmethod
    def parameter_names(self) -> Tuple[str]:
        raise NotImplementedError("")

    def get_parameter_value(self, name) -> TParamValue:
        param_values = self.get_parameter_values()
        assert name in param_values
        return param_values[name]

    @abstractmethod
    def get_parameter_values(self) -> TParamValues:
        raise NotImplementedError("")

    def __eq__(self, other: "_BlackBox") -> bool:
        n = self.name == other.name
        v = self.version == other.version
        outline = isclose(
            self.bb_outline, other.bb_outline, abs_tol=1e-10, rel_tol=1e-10
        )
        bbox = self.bbox == other.bbox

        param_names = set(self.parameter_names) == set(other.parameter_names)
        param_vals = isclose(
            self.get_parameter_values(),
            other.get_parameter_values(),
            abs_tol=1e-10,
            rel_tol=1e-10,
        )

        pin_names = set(self.pin_names) == set(other.pin_names)
        pin_infos = isclose(
            self.get_pin_infos(),
            other.get_pin_infos(),
            abs_tol=1e-10,
            rel_tol=1e-10,
        )

        result = (
            n
            and v
            and outline
            and bbox
            and param_names
            and param_vals
            and pin_names
            and pin_infos
        )
        return result

    @property
    def full_info(self):
        s = (
            f"{self.__class__.__name__}\n"
            f"  Info: {self.info}\n"
            f"  BBox: {self.bbox}\n"
            f"  BB outline: {self.bb_outline}\n"
            f"  Parameters: {self.get_parameter_values()}\n"
            f"  Pins: {self.get_pin_infos()}"
        )
        return s


class uPDKBlackBox(_BlackBox):
    def __init__(self, bb: BB, parameter_values=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bb = bb

        self._bbox = None
        self._bb_outline = None
        self._parameter_values = None
        self._pin_infos = {}

        self.parameter_values = parameter_values

    @property
    def name(self):
        return self._bb.name

    @property
    def version(self):
        return self._bb.version

    @property
    def bb_outline(self) -> List[Tuple[Real, Real]]:
        # set parameters, generate the outline
        if not self._bb_outline:
            self._bb.set_parameters(**self.parameter_values)
            self._bb_outline = process_polygon_vertices(
                self._bb.bb_outline,
                sort=True,
                orient=True,
                clockwise=True,
                make_valid=False,
                close=False,
            )
        return self._bb_outline

    @property
    def bbox(self) -> BBox:
        if not self._bbox:
            self._bb.set_parameters(**self.parameter_values)
            self._bbox = self._bb.bbox
        return self._bbox

    @property
    def pin_names(self) -> Tuple[str]:
        return self._bb.pin_names

    def get_pin_infos(self) -> Dict[str, TPinInfo]:
        if self._pin_infos == {}:
            self._bb.set_parameters(**self.parameter_values)
            for pin_name in self.pin_names:
                pin = self._bb.get_pin(pin_name)
                info = {
                    "name": pin.name,
                    "width": pin.width,
                    "xsection": pin.xsection,
                    "xya": pin.xya,
                }
                self._pin_infos.update({pin_name: info})

        return self._pin_infos

    @property
    def parameter_names(self) -> Tuple[str]:
        return self._bb.parameter_names

    @property
    def parameter_values(self) -> TParamValues:
        return self._parameter_values

    @parameter_values.setter
    def parameter_values(self, values: Optional[Dict[str, TParamValue]]):
        if values is None:
            if self.parameter_names != ():
                raise ValueError(
                    "The parameter values for parameters {} must be "
                    "specified.".format(self.parameter_names)
                )
            self._parameter_values = {}
        else:
            if set(values.keys()) != set(self.parameter_names):
                raise ValueError(
                    "List of provided parameters ({}) does not match the BB "
                    "parameters {}.".format(
                        list(values.keys()), self.parameter_names
                    )
                )
            self._parameter_values = values

    def get_parameter_values(self) -> TParamValues:
        return self.parameter_values


class GdsBlackBox(_BlackBox):
    REQUIRED_MAPPING_KEYS = {
        "bbox",
        "bb_outline",
        "pin_info",
        "bb_parameters",
        "bb_info",
    }
    REQUIRED_PIN_INFO_KEYS = {"name", "xsection", "xya", "width"}

    def __init__(self, cell: "Cell", mapping=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cell = None
        self._name = None
        self._bbox = None
        self._bb_outline = None
        self._parameter_values = None
        self._pin_infos: Dict[str, TPinInfo] = {}

        self._mapping = None
        self._bb_info = None
        self._bb_parameters = None

        mapping = mapping or MAPPING
        self.mapping = mapping

        self.cell = cell
        # self.parameter_values = parameter_values

    @property
    def cell(self) -> Optional["Cell"]:
        return self._cell

    @cell.setter
    def cell(self, c):
        if not isinstance(c, Cell):
            raise TypeError(
                f"cell must be a klayout Cell object. {c} ({type(c)}) is "
                f"given."
            )
        self._cell = c

    @property
    def _layout(self) -> "Layout":
        return self.cell.layout()

    @property
    def _dbu(self):
        return self._layout.dbu

    def _to_um(self, v):
        return v * self._dbu

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, m):
        GdsBlackBox.validate_mapping(m)
        self._mapping = m

    @classmethod
    def validate_mapping(cls, m):
        assert isinstance(cls.REQUIRED_MAPPING_KEYS, set)
        is_valid, msg = is_gds_mapping_valid(
            m, raise_error=False, full_output=True
        )
        if not is_valid:
            if isinstance(m, dict):
                missing_keys = cls.REQUIRED_MAPPING_KEYS - set(m.keys())
                if missing_keys:
                    raise ValueError(
                        f"The layer mapping has the following layers missing: "
                        f"{missing_keys}."
                    )
                else:
                    raise ValueError(
                        f"Incorrect format of the layer mapping. The following "
                        f"error was returned by the validator: {msg}"
                    )
            else:
                raise ValueError(
                    f"Layer mapping must be a dictionary. {m} "
                    f"({type(m)}) is given."
                )
        return True

    @property
    def bb_parameters(self) -> TParamValues:
        if self._bb_parameters is None:
            i = self._layout.find_layer(*self.mapping["bb_parameters"])
            if i is None:
                raise ValueError(
                    "BB parameters layer is not found in the layout."
                )
            shapes = self._cell.shapes(i)
            n_data = shapes.size()
            if n_data == 0:
                print(f"No parameters found for the BB {self.name}")
                bb_params = {}
            elif n_data > 1:
                raise ValueError(
                    f"More that a single list of parameters is found "
                    f"({n_data})."
                )
            else:
                shape = list(shapes.each())[0]
                if shape.is_text():
                    text = shape.text_string
                else:
                    raise ValueError(
                        "BB parameters layer contains non-text objects."
                    )

                try:
                    bb_params = safe_load(text)
                except Exception as e:
                    raise ValueError(
                        f"Failure loading the BB parameters text. Make sure "
                        f"the text block is a valid YAML. The following "
                        f"error occurred: {e}"
                    )
                if not isinstance(bb_params, dict):
                    raise ValueError(
                        f"BB parameters must be a dictionary "
                        f"{{parameter_name: value, ...}}. {bb_params} "
                        f"({type(bb_params)}) is given."
                    )
                for n, v in bb_params.items():
                    if not isinstance(v, (int, float, bool, str)):
                        raise ValueError(
                            f"Value for BB parameter '{n}' must be a number, "
                            f"a boolean, or a dictionary. {v} ({type(v)}) is "
                            f"given."
                        )
            self._bb_parameters = bb_params or {}

        return self._bb_parameters

    @property
    def bb_info(self):
        if self._bb_info is None:
            i = self._layout.find_layer(*self.mapping["bb_info"])
            if i is None:
                raise ValueError("BB info layer is not found in the GDS file.")
            shapes = self._cell.shapes(i)
            n_data = shapes.size()
            if n_data == 0:
                raise ValueError(
                    "No BB info items are found in the bb_info layer."
                )
            elif n_data > 1:
                raise ValueError(
                    f"More than one BB info items ({n_data}) are found  in "
                    f"the bb_info layer."
                )
            shape = list(shapes.each())[0]
            if not shape.is_text():
                raise ValueError("BB info layer contains non-text objects.")

            text = shape.text_string
            try:
                bb_info = safe_load(text)
            except Exception as e:
                raise ValueError(
                    f"Failure loading the BB info text. Make sure the text "
                    f"block is a valid YAML. The following error occurred: {e}"
                )
            if not isinstance(bb_info, dict):
                raise ValueError(
                    f"BB info must be a dictionary. {bb_info} ({type(bb_info)})"
                    f" is given."
                )
            self._bb_info = bb_info
        return self._bb_info

    @property
    def name(self):
        if "cell_name" not in self.bb_info:
            raise ValueError(
                f"Unable to retrieve cell name from the BB info. The "
                f"'cell_name' attribute is missing."
            )
        n = self.bb_info["cell_name"]
        return n

    @property
    def version(self):
        if "bb_version" not in self.bb_info:
            raise ValueError(
                f"Unable to retrieve BB version from the BB info. The "
                f"'bb_version' attribute is missing."
            )
        v = self.bb_info["bb_version"]
        return v

    @property
    def bb_outline(self) -> List[Tuple[Real, Real]]:
        # set parameters, generate the outline
        if not self._bb_outline:
            i = self._layout.find_layer(*self.mapping["bb_outline"])
            if i is None:
                raise ValueError("BB outline layer is not found in the layout.")
            shapes = self._cell.shapes(i)
            n_shapes = shapes.size()
            if n_shapes != 1:
                raise ValueError(
                    f"No. of BB outlines must be 1. {n_shapes} is found."
                )
            shape = list(shapes.each())[0]
            if shape.is_box():
                # width = shape.box_width
                # height = shape.box_height
                sw = (self._to_um(shape.box_p1.x), self._to_um(shape.box_p1.y))
                ne = (self._to_um(shape.box_p2.x), self._to_um(shape.box_p2.y))
                pts = [sw, (sw[0], ne[1]), ne, (ne[0], sw[1])]
                # n_pts = len(pts)
            elif shape.is_simple_polygon():
                pts = [
                    (self._to_um(p.x), self._to_um(p.y))
                    for p in shape.simple_polygon.each_point()
                ]
                pts = process_polygon_vertices(
                    pts,
                    sort=True,
                    orient=True,
                    clockwise=True,
                    make_valid=False,
                    close=False,
                )
                # width = shape.bbox().width()
                # height = shape.bbox().height()
                # sw = (shape.bbox().p1.x, shape.bbox().p1.y)
                # ne = (shape.bbox().p2.x, shape.bbox().p2.y)
                # n_pts = len(pts)
            else:
                raise ValueError("BBox is not a box or a simple poly.")

            self._bb_outline = pts

        return self._bb_outline

    @property
    def bbox(self) -> BBox:
        if not self._bbox:
            i = self._layout.find_layer(*self.mapping["bbox"])
            if i is None:
                raise ValueError("Bbox layer is not found in the layout.")
            shapes = self._cell.shapes(i)
            n_shapes = shapes.size()
            if n_shapes != 1:
                raise ValueError(
                    f"No. of bboxes must be 1. {n_shapes} is found."
                )
            shape = list(shapes.each())[0]
            if shape.is_box():
                # width = shape.box_width
                # height = shape.box_height
                sw = (self._to_um(shape.box_p1.x), self._to_um(shape.box_p1.y))
                ne = (self._to_um(shape.box_p2.x), self._to_um(shape.box_p2.y))
                self._bbox = BBox(sw, ne)
            elif shape.is_simple_polygon():
                raise NotImplementedError(
                    "BBox as a simple poly is not implemented yet."
                )
            else:
                raise ValueError("BBox is not a box or a simple poly.")
        return self._bbox

    @property
    def pin_names(self) -> Tuple[str]:
        return tuple(sorted(self.get_pin_infos().keys()))

    def get_pin_infos(self) -> Dict[str, TPinInfo]:
        if self._pin_infos == {}:
            i = self._layout.find_layer(*self.mapping["pin_info"])
            if i is None:
                raise ValueError("Pin info layer is not found in the layout.")
            shapes = self._cell.shapes(i)
            n_data = shapes.size()
            if n_data == 0:
                raise ValueError(f"No pins are found in the pin_info layer.")

            for shape in shapes.each():
                if not shape.is_text():
                    raise ValueError(
                        "Pin info layer contains a non-text object."
                    )
                v = shape.text_trans.disp
                xt, yt = self._to_um(v.x), self._to_um(v.y)
                text = shape.text_string

                try:
                    pin_info = safe_load(text)
                except Exception as e:
                    raise ValueError(
                        f"Failure loading the pin info text. Make sure the "
                        f"text block is a valid YAML. The following error "
                        f"occurred: {e}"
                    )

                GdsBlackBox.validate_pin_info(pin_info)

                pin_name = pin_info["name"]
                x, y, a = pin_info["xya"]
                if not (
                    isclose(xt, x, abs_tol=1e-10, rel_tol=1e-10)
                    and isclose(yt, y, abs_tol=1e-10, rel_tol=1e-10)
                ):
                    raise ValueError(
                        "The pin xya {} for pin '{}' does not match the "
                        "actual text position ({}, {}).".format(
                            pin_info["xya"], pin_name, xt, yt
                        )
                    )
                pin_info["xya"] = tuple(pin_info["xya"])
                self._pin_infos.update({pin_name: pin_info})

        return self._pin_infos

    @classmethod
    def validate_pin_info(cls, pin_info):
        is_valid, msg = is_pin_info_valid(
            pin_info, raise_error=False, full_output=True
        )
        if not is_valid:
            if isinstance(pin_info, dict):
                missing_keys = cls.REQUIRED_PIN_INFO_KEYS - set(pin_info.keys())
                if missing_keys:
                    raise ValueError(
                        f"The pin info has the following attributes missing: "
                        f"{missing_keys}."
                    )
                else:
                    raise ValueError(
                        f"Incorrect format of the pin info. The following error "
                        f"was returned by the validator: {msg}"
                    )
            else:
                raise ValueError(
                    f"Pin info must be a dictionary. {pin_info} "
                    f"({type(pin_info)}) is given."
                )
        return True

    @property
    def parameter_names(self) -> Tuple[str]:
        return tuple(sorted(self.bb_parameters.keys()))

    def get_parameter_values(self) -> TParamValues:
        return self.bb_parameters


class GdsFile(object):
    REQUIRED_MAPPING_KEYS = GdsBlackBox.REQUIRED_MAPPING_KEYS

    def __init__(self, file_name: str, mapping=None):
        if not HAS_KLAYOUT:
            raise RuntimeWarning("The GdsFile class requires klayout package.")

        self._fn: Optional[Path] = None
        self._top_cell_names = None
        self._cell_names = None
        self._mapping = None
        self._layout = Layout()
        self._layer_map = None

        mapping = mapping or MAPPING
        self.mapping = mapping

        self.filename = file_name
        # {cell_name: (Cell, GdsBlackBox)}: For each cell_name, it contains
        # a klayout cell, and a GdsBlackBox. GdsBlackBox are not created
        # before they are accessed by get_gds_black_box() method.
        self._black_boxes: Dict[str, Tuple["Cell", Optional[GdsBlackBox]]] = {
            n: (self._layout.cell(n), None) for n in self.cell_names
        }

    @property
    def filename(self) -> Optional[Path]:
        return self._fn

    @filename.setter
    def filename(self, fn):
        fn = Path(fn)
        if not fn.is_file():
            raise ValueError(
                f"Incorrect gds file name {fn}. It is either not a file, "
                f"or it does not exist, or the path is incorrect."
            )
        else:
            try:
                self._layer_map = self._layout.read(fn.as_posix())
            except Exception as e:
                raise ValueError(
                    f"Error while reading GDS file '{fn}'. Check the file "
                    f"format.The following error was returned by the reader: "
                    f"{e}"
                )
        self._fn = fn

    @property
    def mapping(self):
        return self._mapping

    @mapping.setter
    def mapping(self, m):
        GdsBlackBox.validate_mapping(m)
        self._mapping = m

    @property
    def top_cell_names(self) -> Tuple[str]:
        if self._top_cell_names is None:
            self._top_cell_names = tuple(
                sorted(str(c.name) for c in self._layout.top_cells())
            )
        return self._top_cell_names

    @property
    def cell_names(self) -> Tuple[str]:
        if self._cell_names is None:
            self._cell_names = tuple(
                sorted(str(c.name) for c in self._layout.each_cell())
            )
        return self._cell_names

    def get_cell(self, name) -> "Cell":
        if name not in self.cell_names:
            raise ValueError(f"Cell '{name}' is not found in the GDS file.")

        return self._black_boxes[name][0]

    def get_gds_black_box(self, name: str) -> GdsBlackBox:
        """

        Parameters
        ----------
        name : str
            cell name

        Returns
        -------
        GdsBlackBox
        """
        if name not in self.cell_names:
            raise ValueError(f"Cell '{name}' is not found in the GDS file.")

        if self._black_boxes[name][1]:
            black_box = self._black_boxes[name][1]
        else:
            cell = self.get_cell(name)
            black_box = GdsBlackBox(cell, self.mapping)
            self._black_boxes.update({name: (cell, black_box)})

        return black_box


class BbValidator(object):
    def __init__(self, updk: UPDK, gds_file: GdsFile):
        self._updk = updk
        self._gds_file = gds_file

        self._name_map = None
        self._matched_cell_names = None
        self._updk_black_box_map = None

        assert isinstance(self.matched_cell_names, list)
        assert isinstance(self.unmatched_cell_names, list)

    @staticmethod
    def from_files(updk_name: str, gds_name: str, mapping=None):
        updk = UPDK.from_file(updk_name)
        gds_file = GdsFile(gds_name, mapping=mapping)

        return BbValidator(updk, gds_file)

    @property
    def gds_cell_names(self):
        return self._gds_file.cell_names

    def _find_bb_name_by_cell_name(
        self, cell_name
    ) -> Tuple[List[str], int, str]:
        black_box = self._gds_file.get_gds_black_box(cell_name)
        try:
            black_box_name = black_box.name
        except ValueError as e:
            msg = (
                f"Error getting black box name for cell '{cell_name}':" f" {e}"
            )
            return [], 0, msg

        matching_names = self._find_bb_name_for_black_box_name(black_box_name)

        n = len(matching_names)
        if n == 0:
            msg = (
                f"No matching uPDK block name found for cell '{cell_name}', "
                f"GDS black box name: '{black_box_name}'."
            )
        elif n > 1:
            msg = (
                f"Multiple matching uPDK block names found for cell name "
                f"'{black_box_name}', GDS black box name '{black_box_name}': "
                f"{matching_names}."
            )
        else:
            msg = "Found single matching BB name."

        return matching_names, n, msg

    def _find_bb_name_for_black_box_name(self, black_box_name) -> List[str]:
        bb_names = self._updk.building_block_names

        matching_names = []
        for bb_name in bb_names:
            if self._check_bb_name_match(black_box_name, bb_name):
                matching_names.append(bb_name)

        return matching_names

    @staticmethod
    def _check_bb_name_match(gds_box_name, updk_block_name) -> bool:
        if updk_block_name == gds_box_name:
            return True
        # elif bb_name.startswith(black_box_name):
        #     if not bb_name[len(black_box_name)].isalnum():
        #         matching_names.append(bb_name)

    @property
    def cell_name_map(self) -> Dict[str, Tuple[List[str], int, str]]:
        if self._name_map is None:
            name_map = {}
            for cell_name in self._gds_file.cell_names:
                matching_names, n, msg = self._find_bb_name_by_cell_name(
                    cell_name
                )
                name_map.update({cell_name: (matching_names, n, msg)})
            self._name_map = name_map

        return self._name_map

    @property
    def matched_cell_names(self) -> List[str]:
        if self._matched_cell_names is None:
            matched = []
            for cell_name, match in self.cell_name_map.items():
                if match[1] == 1:
                    matched.append(cell_name)
            self._matched_cell_names = matched

        return self._matched_cell_names

    @property
    def matched_name_map(self) -> Dict[str, str]:
        matched_map = {}
        for cell_name in self.matched_cell_names:
            matched_map.update({cell_name: self.cell_name_map[cell_name][0][0]})
        return matched_map

    @property
    def unmatched_cell_names(self) -> List[str]:
        unmatched = []
        for cell_name, match in self.cell_name_map.items():
            if match[1] != 1:
                unmatched.append(cell_name)
        return unmatched

    def get_unmatched_cells_report(
        self,
    ) -> Tuple[bool, Dict[str, Dict[str, U[int, str, List]]]]:
        report = {}
        passed = True
        for cell_name in self.unmatched_cell_names:
            try:
                names, n, msg = self.cell_name_map[cell_name]
                report.update(
                    {
                        cell_name: {
                            "n_matches": n,
                            "matching_blocks": names,
                            "message": msg,
                        }
                    }
                )
            except Exception as e:
                msg = f"Error fetching match report for cell '{cell_name}': {e}"
                report.update(
                    {
                        cell_name: {
                            "n_matches": None,
                            "matching_blocks": [],
                            "message": msg,
                        }
                    }
                )
                passed = passed and False
        return passed, report

    def get_matching_block_name(self, cell_name) -> str:
        if cell_name not in self.matched_cell_names:
            raise ValueError(
                f"Cell '{cell_name}' does not have a matching uPDK block. Use "
                f"BbValidator.get_unmatched_cells_report() for more details."
            )
        return self.matched_name_map[cell_name]

    def get_gds_black_box(self, cell_name) -> GdsBlackBox:
        return self._gds_file.get_gds_black_box(cell_name)

    def get_parameter_values(self, cell_name) -> Dict:
        black_box = self.get_gds_black_box(cell_name)
        p_values = black_box.get_parameter_values()
        return p_values

    def get_matching_updk_block(self, cell_name) -> BB:
        if cell_name not in self.gds_cell_names:
            raise ValueError(
                f"Cell '{cell_name}' is not present in the GDS file."
            )
        block_name = self.get_matching_block_name(cell_name)
        updk_block = self._updk.get_building_block(block_name)
        return updk_block

    def get_matching_updk_black_box(self, cell_name) -> uPDKBlackBox:
        updk_block = self.get_matching_updk_block(cell_name)
        param_values = self.get_parameter_values(cell_name)
        updk_black_box = uPDKBlackBox(updk_block, param_values)
        return updk_black_box

    def get_matched_cells_report(self) -> Tuple[bool, Dict]:
        report = {}
        passed = True
        for cell_name in self.matched_cell_names:
            try:
                black_gds = self.get_gds_black_box(cell_name)
            except Exception as e:
                msg = (
                    f"Error while obtaining GDS black box for cell "
                    f"'{cell_name}': {e}"
                )
                report.update({cell_name: {"matches": False, "message": msg}})
                passed = passed and False
                continue

            try:
                black_updk = self.get_matching_updk_black_box(cell_name)
            except Exception as e:
                msg = (
                    f"Error while obtaining matching uPDK block for cell "
                    f"'{cell_name}': {e}"
                )
                report.update({cell_name: {"matches": False, "message": msg}})
                passed = passed and False
                continue

            try:
                equal = bool(black_updk == black_gds)

            except Exception as e:
                msg = (
                    f"Error comparing GDS cell '{cell_name}' with the uPDK "
                    f"block '{black_updk.name}': {e}"
                )
                report.update({cell_name: {"matches": False, "message": msg}})
                continue

            params = black_gds.get_parameter_values()
            if equal:
                msg = (
                    f"GDS cell '{cell_name}' matches the uPDK block "
                    f"'{black_updk.name}' with parameters {params}."
                )
                report.update({cell_name: {"matches": True, "message": msg}})
            else:
                msg = (
                    f"GDS cell '{cell_name}' does not match the uPDK block "
                    f"'{black_updk.name}' with parameters {params}."
                )
                report.update(
                    {
                        cell_name: {
                            "matches": False,
                            "message": msg,
                            "gds_block_info": black_gds.full_info,
                            "updk_block_info": black_updk.full_info,
                        }
                    }
                )
                passed = passed and False
        return passed, report
