"""Utility for borders."""

from enum import Enum

Direction = Enum("Direction", "LEFT TOP RIGHT BOTTOM")
DEFAULT_DIRECTIONS = {Direction.LEFT, Direction.TOP}


def rc_to_grid(r: int, c: int) -> str:
    """Convert row and column to compatible grid coordinates."""
    return f"{r * 2 + 1},{c * 2 + 1}"


def rcd_to_edge(r: int, c: int, d: Direction) -> str:
    """Convert row, column and direction to compatible edge coordinates."""
    data = {
        Direction.TOP: f"{r * 2},{c * 2 + 1}",
        Direction.LEFT: f"{r * 2 + 1},{c * 2}",
        Direction.BOTTOM: f"{r * 2 + 2},{c * 2 + 1}",
        Direction.RIGHT: f"{r * 2 + 1},{c * 2 + 2}",
    }
    return data[d]


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
