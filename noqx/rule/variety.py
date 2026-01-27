"""Generate miscellaneous rules which are not catagorized in other files.

Warning:
    This module is for rules that do not fit into other categories. If you find that a rule can be categorized into an existing module, please consider moving it there. Moreover, the rules in this category may be constantly changing, please take with great care.
"""

from typing import Tuple, Union

from noqx.puzzle import Direction


def nori_adjacent(color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to ensure only `1 x 2` shaded rectangles are formed.

    * This is usually used as a constraint for nori-like puzzles, such as `norinori` and `norinuri`.

    Args:
        color: The color of the shaded cells.
        adj_type: The type of adjacency.
    """
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} != 1."


def yaji_count(
    target: int, src_cell: Tuple[int, int], arrow_direction: str, color: str = "black", unshade_src: bool = True
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
    op = "<" if arrow_direction in (Direction.TOP, Direction.LEFT) else ">"

    shade_clue = "" if unshade_src else f" not {color}({src_r}, {src_c}),"
    if arrow_direction in (Direction.LEFT, Direction.RIGHT):  # left, right
        return f":-{shade_clue} #count {{ C1 : {color}({src_r}, C1), C1 {op} {src_c} }} != {target}."

    if arrow_direction in (Direction.TOP, Direction.BOTTOM):  # top, bottom
        return f":-{shade_clue} #count {{ R1 : {color}(R1, {src_c}), R1 {op} {src_r} }} != {target}."

    raise ValueError("Invalid direction.")


def straight_at_ice(color: str = "white") -> str:
    """A rule to ensure a route goes straight at ice cells.

    * This is usually used as a constraint for puzzles involving some cells needed to be passed straightly, such as `pipelink returns` and `barns`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.
    """
    rule = ""
    for d1, d2 in ((Direction.TOP, Direction.BOTTOM), (Direction.LEFT, Direction.RIGHT)):
        rule += f':- ice(R, C), {color}(R, C), line_io(R, C, "{d1}"), not line_io(R, C, "{d2}").\n'
        rule += f':- ice(R, C), {color}(R, C), line_io(R, C, "{d2}"), not line_io(R, C, "{d1}").\n'

    return rule
