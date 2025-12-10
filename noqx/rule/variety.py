"""Generate miscellaneous rules which are not catagorized in other files.

Warning:
    This module is for rules that do not fit into other categories. If you find that a rule can be
    categorized into an existing module, please consider moving it there. Moreover, the rules in
    this category may be constantly changing, please take with great care.
"""

from typing import Tuple


def nori_adjacent(color: str = "gray", adj_type: int = 4) -> str:
    """A rule to ensure only `1 x 2` shaded rectangles are formed.

    * This is usually used as a constraint for nori-like puzzles, such as `norinori` and `norinuri`.

    Args:
        color: The color of the shaded cells.
        adj_type: The type of adjacency.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def yaji_count(
    target: int, src_cell: Tuple[int, int], arrow_direction: int, color: str = "black", unshade_src: bool = True
) -> str:
    """A rule to compare the number of shaded cells from a certain direction starting from a source cell.

    * This is usually used as a constraint for yaji-like puzzles, such as `yajilin` and `yajikazu`.

    Args:
        target: The target number for comparison.
        src_cell: The source cell (row, column) from which the counting starts.
        arrow_direction: The direction of the arrow indicating the counting direction.
        color: The color of the shaded cells.
        unshade_src: Whether the source cell should be unshaded.
    """
    src_r, src_c = src_cell
    op = "<" if arrow_direction in [0, 1] else ">"

    shade_clue = "" if unshade_src else f" not {color}({src_r}, {src_c}),"
    if arrow_direction in [1, 2]:  # left, right
        return f":-{shade_clue} #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in [0, 3]:  # top, bottom
        return f":-{shade_clue} #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise ValueError("Invalid direction.")
