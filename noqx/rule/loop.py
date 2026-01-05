"""Generate loop- and path-relevant rules for the solver."""

from typing import Tuple, Union

from noqx.puzzle import Direction
from noqx.rule.helper import target_encode


def single_loop(color: str = "white", path: bool = False) -> str:
    """A rule to ensure the route is a valid undirected loop or path.

    * A *loop* is that every cell has two lines connected to it, and there are no dead ends.

    * A *path* is that there are two endpoints having only one line connected to them, and other cells have two lines connected to them. The endpoints are marked as `dead_end`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.common.fill_line` rule.
        path: Whether the route is a path.
    """
    constraint = "pass_by_loop(R, C) :- grid(R, C), #count { D: line_io(R, C, D) } = 2.\n"

    if path:
        constraint += ":- dead_end(R, C), grid(R, C), #count { D: line_io(R, C, D) } != 1.\n"
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C), not dead_end(R, C).\n"
    else:
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C).\n"

    constraint += ':- grid(R, C), line_io(R, C, "l"), not line_io(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), line_io(R, C, "u"), not line_io(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), line_io(R, C, "r"), not line_io(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), line_io(R, C, "d"), not line_io(R + 1, C, "u").'
    return constraint


def directed_loop(color: str = "white", path: bool = False) -> str:
    """A rule to ensure the route is a valid undirected loop or path.

    * The definitions are the same as `single_loop`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.common.fill_line` rule.
        path: Whether the route is a path.
    """
    constraint = f"pass_by_loop(R, C) :- grid(R, C), {color}(R, C), #count {{ D: line_in(R, C, D) }} = 1, #count {{ D: line_out(R, C, D) }} = 1, line_in(R, C, D0), not line_out(R, C, D0).\n"

    if path:
        constraint += ":- path_start(R, C), grid(R, C), #count { D: line_out(R, C, D) } != 1.\n"
        constraint += ":- path_start(R, C), grid(R, C), #count { D: line_in(R, C, D) } != 0.\n"
        constraint += ":- path_end(R, C), grid(R, C), #count { D: line_in(R, C, D) } != 1.\n"
        constraint += ":- path_end(R, C), grid(R, C), #count { D: line_out(R, C, D) } != 0.\n"
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C), not path_start(R, C), not path_end(R, C).\n"
    else:
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C).\n"

    constraint += ':- grid(R, C), line_in(R, C, "l"), not line_out(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), line_in(R, C, "u"), not line_out(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), line_in(R, C, "r"), not line_out(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), line_in(R, C, "d"), not line_out(R + 1, C, "u").\n'
    constraint += ':- grid(R, C), line_out(R, C, "l"), not line_in(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), line_out(R, C, "u"), not line_in(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), line_out(R, C, "r"), not line_in(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), line_out(R, C, "d"), not line_in(R + 1, C, "u").\n'
    return constraint


def count_area_pass(target: Union[int, Tuple[str, int]], _id: int) -> str:
    """A rule that compares the times that a loop passes through an area to a specified target.

    * This rule should be used with the `noqx.neighbor.area_border`.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        _id: The ID of the area.
    """
    rop, num = target_encode(target)
    return f":- #count {{ R, C, D: area_border({_id}, R, C, D), line_io(R, C, D) }} {rop} {2 * num}."


def separate_item_from_loop(inside_item: str, outside_item: str) -> str:
    """A rule to separate two items from inside and outside of a loop.

    Args:
        inside_item: The item that should be inside of the loop.
        outside_item: The item that should be outside of the loop.
    """
    rule = "outside_loop(-1, C) :- grid(_, C).\n"
    rule += 'outside_loop(R, C) :- grid(R, C), outside_loop(R - 1, C), not line_io(R, C, "r").\n'
    rule += 'outside_loop(R, C) :- grid(R, C), not outside_loop(R - 1, C), line_io(R, C, "r").\n'

    constraint = ""
    if len(inside_item) > 0:
        constraint = f":- {inside_item}(R, C), outside_loop(R, C).\n"

    if len(outside_item) > 0:
        constraint += f":- {outside_item}(R, C), not outside_loop(R, C).\n"

    return rule + constraint


def loop_sign(color: str = "white") -> str:
    """A rule to define valid loop signs.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.common.fill_line` rule.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d1, d2 in ("lu", "ld", "ru", "rd", "lr", "ud"):
        rule += f'loop_sign(R, C, "{d1}{d2}") :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), line_io(R, C, "{d2}").\n'

    return rule


def loop_segment(src_cell: Tuple[int, int]) -> str:
    """A rule to define valid loop segments from a source cell.

    * The loop segment from the source cell is similar to the line of sight of a bulb.

    * This rule requires the `loop_sign` rule first.

    Args:
        src_cell: The source cell in (`row`, `col`).

    Warning:
        This rule only supports undirected routes.
    """
    r, c = src_cell

    max_u = f'#max {{ R0: grid(R0 + 1, {c}), not loop_sign(R0, {c}, "ud"), R0 < {r} }}'
    min_d = f'#min {{ R0: grid(R0 - 1, {c}), not loop_sign(R0, {c}, "ud"), R0 > {r} }}'
    max_l = f'#max {{ C0: grid({r}, C0 + 1), not loop_sign({r}, C0, "lr"), C0 < {c} }}'
    min_r = f'#min {{ C0: grid({r}, C0 - 1), not loop_sign({r}, C0, "lr"), C0 > {c} }}'

    rule = f'segment({r}, {c}, N1, N2, "T") :- loop_sign({r}, {c}, "lu"), N1 = {max_u}, N2 = {max_l}.\n'
    rule += f'segment({r}, {c}, N1, N2, "T") :- loop_sign({r}, {c}, "ld"), N1 = {min_d}, N2 = {max_l}.\n'
    rule += f'segment({r}, {c}, N1, N2, "T") :- loop_sign({r}, {c}, "ru"), N1 = {max_u}, N2 = {min_r}.\n'
    rule += f'segment({r}, {c}, N1, N2, "T") :- loop_sign({r}, {c}, "rd"), N1 = {min_d}, N2 = {min_r}.\n'
    rule += f'segment({r}, {c}, N1, N2, "V") :- loop_sign({r}, {c}, "ud"), N1 = {max_u}, N2 = {min_d}.\n'
    rule += f'segment({r}, {c}, N1, N2, "H") :- loop_sign({r}, {c}, "lr"), N1 = {max_l}, N2 = {min_r}.\n'

    return rule


def loop_straight(color: str = "white") -> str:
    """A rule to define all the cells that the route goes straight at.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.common.fill_line` rule.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d1, d2 in ("lr", "ud"):
        rule += f'straight(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), line_io(R, C, "{d2}").\n'
    return rule


def loop_turning(color: str = "white") -> str:
    """A rule to define all the cells that the route make turns at.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.common.fill_line` rule.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d1, d2 in ("lu", "ld", "ru", "rd"):
        rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), line_io(R, C, "{d2}").\n'
    return rule


def convert_line_to_edge(directed: bool = False, diagonal: bool = False) -> str:
    """A rule to convert the line definitions to edge definitions.

    * In some logic puzzles like `firefly` and `slitherlink`, the path is drawn on the edge although they are loop/path puzzles. This rule helps to do the compatibility conversions.

    Args:
        directed: Whether the route is directed.
        diagonal: Whether the route is diagonal.
    """
    if diagonal:
        dir_convert_dict = {Direction.DIAG_DOWN: "dr", Direction.DIAG_UP: "ur"}
    else:
        dir_convert_dict = {Direction.TOP: "r", Direction.LEFT: "d"}

    rule = ""
    for d, label in dir_convert_dict.items():
        new_row = "R + 1" if d == Direction.DIAG_UP else "R"
        if directed:
            rule += f'edge(R, C, "{d}") :- line_in({new_row}, C, "{label}").\n'
            rule += f'edge(R, C, "{d}") :- line_out({new_row}, C, "{label}").\n'
        else:
            rule += f'edge(R, C, "{d}") :- line_io({new_row}, C, "{label}").\n'

    return rule
