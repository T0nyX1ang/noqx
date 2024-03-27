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


def elt_to_rcd(coord: str) -> Tuple[int, int, Union[None, Direction]]:
    """Convert grid coordinates to row and column."""
    gr, gc = map(int, coord.split(","))
    r, c = gr // 2, gc // 2

    if gr % 2 == 1 and gc % 2 == 1:  # coordinate case
        return r, c, None

    if gr % 2 == 0 and gc % 2 == 1:  # horizontal border case
        return r, c, Direction.TOP  # bottom border will be ignored

    if gr % 2 == 1 and gc % 2 == 0:  # vertical border case
        return r, c, Direction.LEFT  # right border will be ignored

    raise ValueError("Invalid coordinate!")


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
