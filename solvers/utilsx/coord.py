"""Utility for borders."""

from enum import Enum
from typing import Tuple, Union

Direction = Enum("Direction", "LEFT TOP")


def rcd_to_elt(r: int, c: int, d: Direction = None) -> str:
    """Convert row, column and direction (if has) to compatible elt ID."""
    if d is None:
        return f"{r * 2 + 1},{c * 2 + 1}"

    data = {
        Direction.TOP: f"{r * 2},{c * 2 + 1}",
        Direction.LEFT: f"{r * 2 + 1},{c * 2}",
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
