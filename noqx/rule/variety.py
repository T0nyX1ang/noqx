"""Generate miscellaneous rules which are not catagorized in other files.

Warning:
    This module is for rules that do not fit into other categories. If you find that a rule can be categorized into an existing module, please consider moving it there. Moreover, the rules in this category may be constantly changing, please take with great care.
"""

from typing import Iterable, List, Tuple, Union

from noqx.puzzle import Direction
from noqx.rule.helper import tag_encode, target_encode


def nori_adjacent(target: Union[int, Tuple[str, int]] = 1, color: str = "black", adj_type: Union[int, str] = 4) -> str:
    """A rule to ensure there are certain amount of adjacent shaded cells around a shaded cell.

    * This is usually used as a constraint for nori-like puzzles, such as `norinori` and `norinuri`.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        color: The color of the shaded cells.
        adj_type: The type of adjacency.
    """
    rop, num = target_encode(target)
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }} {rop} {num}."


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


def straight_at_ice(color: str = "white", directed: bool = False) -> str:
    """A rule to ensure a route goes straight at ice cells.

    * This is usually used as a constraint for puzzles involving some cells needed to be passed straightly, such as `pipelink returns` and `barns`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.
        directed: Whether the route is directed.
    """
    rule = ""
    for d1, d2 in ((Direction.TOP, Direction.BOTTOM), (Direction.LEFT, Direction.RIGHT)):
        if directed:
            rule += f':- ice(R, C), not crossing(R, C), {color}(R, C), line_in(R, C, "{d1}"), not line_out(R, C, "{d2}").\n'
            rule += f':- ice(R, C), not crossing(R, C), {color}(R, C), line_in(R, C, "{d2}"), not line_out(R, C, "{d1}").\n'
        else:
            rule += f':- ice(R, C), not crossing(R, C), {color}(R, C), line_io(R, C, "{d1}"), not line_io(R, C, "{d2}").\n'
            rule += f':- ice(R, C), not crossing(R, C), {color}(R, C), line_io(R, C, "{d2}"), not line_io(R, C, "{d1}").\n'
    return rule.strip()


def classify_area(classifiers: Iterable[Tuple[str, str]]) -> str:
    """A rule to classify the area by the classifiers.

    * All the areas must be classified by one of the classifiers.

    * If the color matches with one target classifier on a cell, the color should be drawn on every target classifier in this area.

    * If the color does not match with the target classifier, the color should not be drawn on every target classifier in this area.

    Args:
        classifiers: A list of tuples of (`predicate`, `color`), where `predicate` is the name of the predicate to classify the area, and `color` is the color of the area.
    """
    rule = ""
    all_tags: List[str] = []
    all_predicates = [predicate for (predicate, _) in classifiers]

    for predicate, color in classifiers:
        tag = tag_encode(predicate, "area")
        all_tags.append(tag)

        rule += f"{tag}(A) :- area(A, R, C), {predicate}(R, C), {color}(R, C).\n"
        rule += f":- {tag}(A), area(A, R, C), {predicate}(R, C), not {color}(R, C).\n"

        for other_predicate in all_predicates:
            if other_predicate != predicate:
                rule += f":- {tag}(A), area(A, R, C), {other_predicate}(R, C), {color}(R, C).\n"

    spawn_tags = ", ".join(f"not {tag}(A)" for tag in all_tags)
    rule += f":- area(A, _, _), {spawn_tags}."
    return rule
