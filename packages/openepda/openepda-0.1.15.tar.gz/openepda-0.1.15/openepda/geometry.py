# -*- coding: utf-8 -*-
"""openepda.geometry.py

This file contains routines to work with geometrical objects: points and
lines.

Author: Dima Pustakhod
Copyright: 2020, TU/e - PITC and authors

Changelog
---------
2020.04.29
    Initial commit
"""
from numbers import Real
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union as U

import numpy as np

TPt = Tuple[Real, Real]
TPts = Sequence[TPt]
TPtList = List[TPt]


import numbers
import math


def isclose(a, b, *, rel_tol=None, abs_tol=None) -> bool:
    """Perform safe comparison of a and b

    If a and b are numbers.Number, math.isclose function is used.
    If a and b are sets, they are sorted and compared element-wise recursively.
    If a and b are dicts, keys and corresponding items are compared recursively.
    if a and b are iterables, they are compared recursively element-wise.
    For all other types of a and b, the function uses standard `==` operator.

    Examples
    --------
    >>> isclose(1.0, 1.001, abs_tol=1e-3)
    True
    >>> isclose(1.0, 1.01, abs_tol=1e-3)
    False
    >>> isclose('a', 'a', abs_tol=1e-3)
    True
    >>> isclose('a', 'b', abs_tol=1e-3)
    False
    """
    if isinstance(a, numbers.Real) and isinstance(b, numbers.Real):
        kwargs = {}
        if rel_tol is not None:
            kwargs.update({"rel_tol": rel_tol})
        if abs_tol is not None:
            kwargs.update({"abs_tol": abs_tol})
        res = math.isclose(a, b, **kwargs)
    elif isinstance(a, str) and isinstance(b, str):
        res = bool(a == b)
    elif isinstance(a, set) and isinstance(b, set):
        res = all((isclose(ai, bi) for ai, bi in zip(a, b)))
    elif isinstance(a, dict) and isinstance(b, dict):
        try:
            res = bool(len(a) == len(b))
            if res:
                res = isclose(sorted(set(a.keys())), sorted(set(b.keys())))
            if res:
                res = all((isclose(a[k], b[k]) for k in a.keys()))
        except Exception:
            res = False
    else:
        try:
            res = bool(len(a) == len(b))
            if res:
                res = all((isclose(ai, bi) for ai, bi in zip(a, b)))
        except Exception:
            res = bool(a == b)
    return res


def _are_points_equal(p1: TPt, p2: TPt) -> bool:
    """Check if the points are close to each other. Not type safe!
    """
    return math.isclose(p1[0], p2[0]) and math.isclose(p1[1], p2[1])


def _is_first_point_smaller(p1: TPt, p2: TPt) -> True:
    """ Check if first point is smaller than the second

    Smaller means located a) more to the left, and b) more to the bottom.
    b) is checked only if a) is inconclusive.

    Parameters
    ----------
    p1: tuple
        contains two coordinates of the point
    p2: tuple
        contains two coordinates of the point
    """
    if math.isclose(p1[0], p2[0]):
        return p1[1] < p2[1]
    else:
        return p1[0] < p2[0]


def count_edges(points: TPts) -> int:
    """Count number of edges in the line.

    Returns
    -------
    int
        -1 if no points are given, 0 if a single point is given.
    """
    return len(points) - 1


def count_vertices(points: TPts) -> int:
    """Count points in the line
    """
    return len(points)


def ensure_line_valid(points: TPts, min_point_count=2) -> TPtList:
    """ Return a point list representing a valid line.

    Parameters
    ----------
    points : list of tuples
        each tuple contains two coordinates of a point
    min_point_count : int
        1 or 2. number of points

    """
    if min_point_count not in (1, 2):
        raise ValueError(
            "min_point_count must have a value of 1 or 2."
            "{} is given".format(min_point_count)
        )

    n_lines = count_edges(points)
    if n_lines < 0:
        return [(0, 0)] * min_point_count
    elif n_lines == 0:
        # single point. return it several times
        return list(points) * min_point_count
    else:
        return list(points)


def is_line_string_closed(points: TPts, raise_error=True) -> bool:
    """ Determine if the line is closed.

    The line given by a sequence of points is closed, if the first and
    the last point are the same. A pen drawing them returns to the same
    location or doesn't move at all.

    Parameters
    ----------
    points : list of points
        a point can be a Point, or a tuple / list of two coordinates
    raise_error : bool
        if True, raise error if points is an empty list. If False, return False.
    """
    n_lines = count_edges(points)
    if n_lines < 0:
        # empty array
        if raise_error:
            raise ValueError("List of points must contain at least one point.")
        else:
            return False
    if n_lines == 0:
        # single point, always closed
        return True
    else:
        return _is_line_string_closed([points[0], points[-1]])


def _is_line_string_closed(points: TPts) -> bool:
    """Determine if the line is closed. Not type safe!

    The line given by a sequence of points is closed, if the first and
    the last point are the same.

    Parameters
    ----------
    points : TPts
        each tuple contains two coordinates of a point
    """
    return _are_points_equal(points[0], points[-1])


def ensure_line_is_closed(
    points: TPts, raise_error=True, min_point_count=2
) -> List[TPt]:
    """ Return a closed line.

    Check if line is closed and add the starting point to the end if it is not.

    Parameters
    ----------
    points : TPts
        each tuple contains two coordinates of a point
    raise_error : bool

    min_point_count : int

    """
    n_lines = count_edges(points)
    if n_lines < 0:
        if raise_error:
            raise ValueError("List of points must contain at least 3 points.")
        else:
            return ensure_line_valid([(0, 0)], min_point_count)
    elif n_lines == 0:
        # single point, always closed. return it several times
        return ensure_line_valid(points, min_point_count)
    else:
        if is_line_string_closed(points):
            return list(points)
        else:
            return list(points) + [points[0]]


def calculate_area(points: TPts) -> U[int, float]:
    """ Calculate the area of simple polygon given by a list of tuples.

    Sign is positive if points are sorted counter clockwise.

    Parameters
    ----------
    points : list of tuples
        each tuple contains two coordinates of a point

    """
    points = np.array(ensure_line_is_closed(points, raise_error=False,))
    area = (
        sum(points[:-1, 0] * points[1:, 1] - points[1:, 0] * points[:-1, 1]) / 2
    )
    return int(area) if area.is_integer() else float(area)


def is_oriented_cw(points: TPts) -> bool:
    """ Calculate the line orientation.

    Parameters
    ----------
    points : list of tuples
        each tuple contains two coordinates of a point

    Return
    ------
    o : bool
        False if line if oriented counter clockwise,
        True if line is oriented clockwise.
    """
    a = calculate_area(points)

    if a < 0:
        return True
    elif a > 0:
        return False
    else:
        return None


def sort_polygon_vertices(points: TPts) -> TPtList:
    """ Sort polygon vertices list.

    Parameters
    ----------
    points : TPts
        each tuple contains two coordinates of a point

    """
    n_pts = count_vertices(points)
    if n_pts <= 1:
        return list(points)
    else:
        return _sort_polygon_vertices(points)


def _sort_polygon_vertices(points: TPts) -> TPtList:
    """Sort polygon vertices list.

    The first point will be the most SW point. The order of other points
    is preserved.

    Parameters
    ----------
    points : list of tuples
        each tuple contains two coordinates of a point

    """
    min_ind, min_p = 0, points[0]
    for i, pt in enumerate(points):
        if _is_first_point_smaller(pt, min_p):
            min_ind, min_p = i, pt

    pts_sorted = points[min_ind:] + points[0:min_ind]
    return pts_sorted


def orient_polygon_vertices(
    points: TPts, clockwise=True, keep_first=False
) -> List[TPt]:
    """Change orientation of the polygon vertices list.

    If orientation is different from required, the point order is inverted.
    No sorting is done.

    Parameters
    ----------
    points : TPts
        each tuple contains two coordinates of a point
    clockwise : bool
        Direction of the vertices orientation.
    keep_first : bool
        Flag to force keeping the first point the same

    """
    o = is_oriented_cw(points)  #

    if o is None or o == clockwise:
        # Orientation not defined or it is correct
        return list(points)
    elif o != clockwise:
        if keep_first:
            return [points[0]] + list(reversed(points[1:]))
        else:
            return list(reversed(points))
    else:
        assert False


def process_polygon_vertices(
    points: TPts,
    sort=True,
    orient=True,
    clockwise=True,
    make_valid=True,
    close=False,
) -> TPtList:
    """
    Parameters
    ----------
    points : TPts

    """
    if make_valid:
        points = ensure_line_valid(points, min_point_count=2)

    if orient:
        points = orient_polygon_vertices(points, clockwise, False)

    if sort:
        points = sort_polygon_vertices(points)

    if close:
        points = ensure_line_is_closed(
            points, raise_error=False, min_point_count=2
        )

    return points
