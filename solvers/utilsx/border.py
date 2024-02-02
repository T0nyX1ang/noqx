"""Utility for borders."""

from enum import Enum

Direction = Enum("Direction", "LEFT TOP RIGHT BOTTOM")
DEFAULT_DIRECTIONS = {Direction.LEFT, Direction.TOP}


def get_edge_id_from_border_coord(rows, cols, i, j):
    """
    Given the dimensions (rows and cols) of a puzzle grid,
    and a border coordinate (i, j),

    Returns the canonical edge id of the edge.
    """
    if j % 2 == 0:
        if j // 2 == cols:
            return (i // 2, j // 2, Direction.RIGHT)
        else:
            return (i // 2, j // 2, Direction.LEFT)
    else:
        if i // 2 == rows:
            return (i // 2, j // 2, Direction.BOTTOM)
        else:
            return (i // 2, j // 2, Direction.TOP)


def get_border_coord_from_edge_id(r, c, d):
    """
    Given an edge id,

    Returns the border coordinate of the edge.
    """
    if d == Direction.TOP:
        return "{},{}".format(r * 2, c * 2 + 1)
    elif d == Direction.LEFT:
        return "{},{}".format(r * 2 + 1, c * 2)
    elif d == Direction.BOTTOM:
        return "{},{}".format((r + 1) * 2, c * 2 + 1)
    elif d == Direction.RIGHT:
        return "{},{}".format(r * 2 + 1, (c + 1) * 2)


def get_edge_id(rows, cols, r, c, d):
    """
    Given row and column coordinates and a direction,
    returns the edge id (the canonical tuple representation).

    e.g. (0, 0, bottom) -> (1, 0, top)
    """
    if d in DEFAULT_DIRECTIONS:
        return (r, c, d)
    elif d == Direction.RIGHT:
        if c == cols - 1:
            return (r, c, Direction.RIGHT)
        else:
            return (r, c + 1, Direction.LEFT)
    elif d == Direction.BOTTOM:
        if r == rows - 1:
            return (r, c, Direction.BOTTOM)
        else:
            return (r + 1, c, Direction.TOP)
    else:
        raise RuntimeError("Expected 'd' to be a valid Direction enum value")
