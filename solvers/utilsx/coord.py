"""Utility for borders."""

from enum import Enum
from typing import Tuple, Union


Direction = Enum("Direction", "LEFT TOP RIGHT BOTTOM")
DEFAULT_DIRECTIONS = {Direction.LEFT, Direction.TOP}


def rcd_to_elt(r: int, c: int, d: Direction = None) -> str:
    """Convert row, column and direction (if has) to compatible elt ID."""
    if d is None:
        return f"{r * 2 + 1},{c * 2 + 1}"

    data = {
        Direction.TOP: f"{r * 2},{c * 2 + 1}",
        Direction.LEFT: f"{r * 2 + 1},{c * 2}",
        Direction.BOTTOM: f"{r * 2 + 2},{c * 2 + 1}",
        Direction.RIGHT: f"{r * 2 + 1},{c * 2 + 2}",
    }
    return data[d]


def grid_to_rc(coord: str, rows: int, cols: int) -> Tuple[Union[int, str], int]:
    """Convert grid coordinates to row and column."""
    gr, gc = map(int, coord.split(","))

    if gr == -1:
        return "top", gc // 2

    if gr == 2 * rows + 1:
        return "bottom", gc // 2

    if gc == -1:
        return "left", gr // 2

    if gc == 2 * cols + 1:
        return "right", gr // 2

    return gr // 2, gc // 2


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
