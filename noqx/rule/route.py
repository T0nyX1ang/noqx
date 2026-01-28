"""Generate loop- and path-relevant rules for the solver."""

from typing import List, Tuple, Union

from noqx.puzzle import Direction
from noqx.rule.helper import tag_encode, target_encode


def single_route(color: str = "white", path: bool = False, crossing: bool = False) -> str:
    """A rule to ensure the route is a valid undirected loop or path.

    * A *loop* is that every cell has two lines connected to it, and there are no dead ends.

    * A *path* is that there are two endpoints having only one line connected to them, and other cells have two lines connected to them. The endpoints are marked as `dead_end`.

    * A *crossing* is that a cell can have four lines connected to it, forming a crossing. The route on the crossing cell should go straight in both directions. The crossing cells are marked as `crossing`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.
        path: Whether the route is a path.
        crossing: Whether the route contains crossing cells.

    Success:
        This rule will generate a predicate named `pass_by_route(R, C)`.

    Warning:
        This rule conflicts with `directed_route`.
    """
    rule = "pass_by_route(R, C) :- grid(R, C), #count { D: line_io(R, C, D) } = 2.\n"
    available: List[str] = ["pass_by_route"]

    if crossing:
        rule += ":- crossing(R, C), grid(R, C), #count { D: line_io(R, C, D) } != 4.\n"
        available.append("crossing")

    if path:
        rule += ":- dead_end(R, C), grid(R, C), #count { D: line_io(R, C, D) } != 1.\n"
        available.append("dead_end")

    rule += f":- grid(R, C), {color}(R, C), {', '.join(f'not {predicate}(R, C)' for predicate in available)}.\n"
    rule += f':- grid(R, C), line_io(R, C, "{Direction.LEFT}"), not line_io(R, C - 1, "{Direction.RIGHT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.TOP}"), not line_io(R - 1, C, "{Direction.BOTTOM}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.RIGHT}"), not line_io(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), line_io(R, C, "{Direction.BOTTOM}"), not line_io(R + 1, C, "{Direction.TOP}").'
    return rule


def directed_route(color: str = "white", path: bool = False, crossing: bool = False) -> str:
    """A rule to ensure the route is a valid directed loop or path.

    * The definitions are the same as `single_route`.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.
        path: Whether the route is a path.
        crossing: Whether the route contains crossing cells.

    Success:
        This rule will generate a predicate named `pass_by_route(R, C)`.

    Warning:
        This rule conflicts with `single_route`.
    """
    rule = f"pass_by_route(R, C) :- grid(R, C), {color}(R, C), #count {{ D: line_in(R, C, D) }} = 1, #count {{ D: line_out(R, C, D) }} = 1, line_in(R, C, D0), not line_out(R, C, D0).\n"
    available: List[str] = ["pass_by_route"]

    if path:
        rule += ":- path_start(R, C), grid(R, C), #count { D: line_out(R, C, D) } != 1.\n"
        rule += ":- path_start(R, C), grid(R, C), #count { D: line_in(R, C, D) } != 0.\n"
        rule += ":- path_end(R, C), grid(R, C), #count { D: line_in(R, C, D) } != 1.\n"
        rule += ":- path_end(R, C), grid(R, C), #count { D: line_out(R, C, D) } != 0.\n"
        available.append("path_start")
        available.append("path_end")

    if crossing:
        rule += ":- crossing(R, C), grid(R, C), #count { D: line_in(R, C, D) } != 2.\n"
        rule += ":- crossing(R, C), grid(R, C), #count { D: line_out(R, C, D) } != 2.\n"
        rule += f':- crossing(R, C), line_in(R, C, "{Direction.TOP}"), not line_out(R, C, "{Direction.BOTTOM}").\n'
        rule += f':- crossing(R, C), line_in(R, C, "{Direction.BOTTOM}"), not line_out(R, C, "{Direction.TOP}").\n'
        rule += f':- crossing(R, C), line_in(R, C, "{Direction.LEFT}"), not line_out(R, C, "{Direction.RIGHT}").\n'
        rule += f':- crossing(R, C), line_in(R, C, "{Direction.RIGHT}"), not line_out(R, C, "{Direction.LEFT}").\n'
        available.append("crossing")

    rule += f":- grid(R, C), {color}(R, C), {', '.join(f'not {predicate}(R, C)' for predicate in available)}.\n"
    rule += f':- grid(R, C), line_in(R, C, "{Direction.LEFT}"), not line_out(R, C - 1, "{Direction.RIGHT}").\n'
    rule += f':- grid(R, C), line_in(R, C, "{Direction.TOP}"), not line_out(R - 1, C, "{Direction.BOTTOM}").\n'
    rule += f':- grid(R, C), line_in(R, C, "{Direction.RIGHT}"), not line_out(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), line_in(R, C, "{Direction.BOTTOM}"), not line_out(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), line_out(R, C, "{Direction.LEFT}"), not line_in(R, C - 1, "{Direction.RIGHT}").\n'
    rule += f':- grid(R, C), line_out(R, C, "{Direction.TOP}"), not line_in(R - 1, C, "{Direction.BOTTOM}").\n'
    rule += f':- grid(R, C), line_out(R, C, "{Direction.RIGHT}"), not line_in(R, C + 1, "{Direction.LEFT}").\n'
    rule += f':- grid(R, C), line_out(R, C, "{Direction.BOTTOM}"), not line_in(R + 1, C, "{Direction.TOP}").\n'
    return rule


def crossing_route_connected(color: str = "white", directed: bool = False) -> str:
    """A rule to ensure a crossing route is connected in a grid.

    * This rule is similar to the `noqx.rule.reachable.grid_color_connected` rule. Since crossing routes can go straight in both directions, two reachability tags are generated for horizontal and vertical directions. Moreover, it is impossible to combine these reachability tags into one, this rule is specifically moved into the `route` module.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.
        directed: Whether the route is directed.

    Success:
        This rule will generate a predicate named `reachable_grid_adj_{line|line_directed}_crossing_{color}(R, C)`.
    """
    adj_type = "line" if not directed else "line_directed"
    tag = tag_encode("reachable", "grid", "adj", adj_type, "crossing", color)

    rule = f'{tag}(R, C, "H") :- (R, C) = #min {{ (R1, C1): grid(R1, C1), {color}(R1, C1) }}.\n'
    rule += f'{tag}(R, C, "H") :- {tag}(R, C1, "H"), adj_{adj_type}(R, C, R, C1).\n'
    rule += f'{tag}(R, C, "V") :- {tag}(R1, C, "V"), adj_{adj_type}(R, C, R1, C).\n'
    rule += f'{tag}(R, C, "V") :- {tag}(R, C, "H"), grid(R, C), not crossing(R, C).\n'
    rule += f'{tag}(R, C, "H") :- {tag}(R, C, "V"), grid(R, C), not crossing(R, C).\n'
    rule += f':- grid(R, C), {color}(R, C), not {tag}(R, C, "H").\n'
    rule += f':- grid(R, C), {color}(R, C), not {tag}(R, C, "V").\n'

    return rule.strip()


def count_area_pass(target: Union[int, Tuple[str, int]], _id: int, directed: bool = False) -> str:
    """A rule that compares the times that a undirected route passes through an area to a specified target.

    * This rule should be used with the `noqx.rule.neighbor.area_border`.

    Args:
        target: The target number or a tuple of (`operator`, `number`) for comparison.
        _id: The ID of the area.
        directed: Whether the route is directed.
    """
    rop, num = target_encode(target)

    if directed:
        return f":- #count {{ R, C, D: area_border({_id}, R, C, D), line_in(R, C, D) }} {rop} {num}."

    return f":- #count {{ R, C, D: area_border({_id}, R, C, D), line_io(R, C, D) }} {rop} {2 * num}."


def separate_item_from_route(inside_item: str, outside_item: str) -> str:
    """A rule to separate two items from inside and outside of route.

    Args:
        inside_item: The item that should be inside of the route.
        outside_item: The item that should be outside of the route.

    Warning:
        This rule only supports undirected routes.
    """
    rule = "outside_route(-1, C) :- grid(_, C).\n"
    rule += f'outside_route(R, C) :- grid(R, C), outside_route(R - 1, C), not line_io(R, C, "{Direction.RIGHT}").\n'
    rule += f'outside_route(R, C) :- grid(R, C), not outside_route(R - 1, C), line_io(R, C, "{Direction.RIGHT}").\n'
    rule += f":- {inside_item}(R, C), outside_route(R, C).\n"
    rule += f":- {outside_item}(R, C), not outside_route(R, C).\n"

    return rule


def route_sign(color: str = "white") -> str:
    """A rule to define valid route signs.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d, d1, d2 in (
        (Direction.TOP_LEFT, Direction.TOP, Direction.LEFT),
        (Direction.TOP_RIGHT, Direction.TOP, Direction.RIGHT),
        (Direction.BOTTOM_LEFT, Direction.BOTTOM, Direction.LEFT),
        (Direction.BOTTOM_RIGHT, Direction.BOTTOM, Direction.RIGHT),
        (Direction.TOP_BOTTOM, Direction.TOP, Direction.BOTTOM),
        (Direction.LEFT_RIGHT, Direction.LEFT, Direction.RIGHT),
    ):
        rule += f'route_sign(R, C, "{d}") :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), line_io(R, C, "{d2}").\n'

    return rule


def route_segment(src_cell: Tuple[int, int]) -> str:
    """A rule to define valid route segments from a source cell.

    * The route segment from the source cell is similar to the line of sight of a bulb.

    Args:
        src_cell: The source cell in (`row`, `col`).

    Success:
        This rule will generate a predicate named `segment(R0, C0, R, C, S)`.

    Warning:
        This rule only supports undirected routes.
    """
    r, c = src_cell

    max_u = f'#max {{ R0: grid(R0 + 1, {c}), not route_sign(R0, {c}, "{Direction.TOP_BOTTOM}"), R0 < {r} }}'
    min_d = f'#min {{ R0: grid(R0 - 1, {c}), not route_sign(R0, {c}, "{Direction.TOP_BOTTOM}"), R0 > {r} }}'
    max_l = f'#max {{ C0: grid({r}, C0 + 1), not route_sign({r}, C0, "{Direction.LEFT_RIGHT}"), C0 < {c} }}'
    min_r = f'#min {{ C0: grid({r}, C0 - 1), not route_sign({r}, C0, "{Direction.LEFT_RIGHT}"), C0 > {c} }}'

    rule = f'segment({r}, {c}, N1, N2, "T") :- route_sign({r}, {c}, "{Direction.TOP_LEFT}"), N1 = {max_u}, N2 = {max_l}.\n'
    rule += f'segment({r}, {c}, N1, N2, "T") :- route_sign({r}, {c}, "{Direction.BOTTOM_LEFT}"), N1 = {min_d}, N2 = {max_l}.\n'
    rule += f'segment({r}, {c}, N1, N2, "T") :- route_sign({r}, {c}, "{Direction.TOP_RIGHT}"), N1 = {max_u}, N2 = {min_r}.\n'
    rule += (
        f'segment({r}, {c}, N1, N2, "T") :- route_sign({r}, {c}, "{Direction.BOTTOM_RIGHT}"), N1 = {min_d}, N2 = {min_r}.\n'
    )
    rule += f'segment({r}, {c}, N1, N2, "V") :- route_sign({r}, {c}, "{Direction.TOP_BOTTOM}"), N1 = {max_u}, N2 = {min_d}.\n'
    rule += f'segment({r}, {c}, N1, N2, "H") :- route_sign({r}, {c}, "{Direction.LEFT_RIGHT}"), N1 = {max_l}, N2 = {min_r}.\n'

    return rule


def route_straight(color: str = "white") -> str:
    """A rule to define all the cells that the route goes straight at.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.

    Success:
        This rule will generate a predicate named `straight(R, C)`.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d1, d2 in ((Direction.TOP, Direction.BOTTOM), (Direction.LEFT, Direction.RIGHT)):
        rule += f'straight(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), line_io(R, C, "{d2}").\n'
    return rule.strip()


def route_turning(color: str = "white", directed: bool = False) -> str:
    """A rule to define all the cells that the route make turns at.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.

    Success:
        This rule will generate a predicate named `turning(R, C)`.

    Warning:
        This rule only supports undirected routes.
    """
    rule = ""
    for d1, d2 in ((Direction.TOP, Direction.BOTTOM), (Direction.LEFT, Direction.RIGHT)):
        if directed:
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_in(R, C, "{d1}"), not line_out(R, C, "{d2}").\n'
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_in(R, C, "{d2}"), not line_out(R, C, "{d1}").\n'
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_out(R, C, "{d1}"), not line_in(R, C, "{d2}").\n'
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_out(R, C, "{d2}"), not line_in(R, C, "{d1}").\n'
        else:
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{d1}"), not line_io(R, C, "{d2}").\n'
            rule += f'turning(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{d2}"), not line_io(R, C, "{d1}").\n'
    return rule.strip()


def route_crossing(color: str = "white") -> str:
    """A rule to define all the cells that the route crosses at.

    Args:
        color: The color of the route. Should be aligned with the color defined in `noqx.rule.common.fill_line` rule.

    Success:
        This rule will generate a predicate named `crossing(R, C)`.

    Warning:
        This rule only supports undirected routes.
    """
    rule = f'crossing(R, C) :- grid(R, C), {color}(R, C), line_io(R, C, "{Direction.TOP}"), line_io(R, C, "{Direction.BOTTOM}"), line_io(R, C, "{Direction.LEFT}"), line_io(R, C, "{Direction.RIGHT}").'
    return rule


def convert_line_to_edge(directed: bool = False, diagonal: bool = False) -> str:
    """A rule to convert the line definitions to edge definitions.

    * In some logic puzzles like `haisu` and `slitherlink`, the path is drawn on the edge although they are loop/path puzzles. This rule helps to do the compatibility conversions.

    Args:
        directed: Whether the route is directed.
        diagonal: Whether the route is diagonal.
    """
    if diagonal:
        dir_convert_dict = {Direction.TOP_LEFT: Direction.BOTTOM_RIGHT, Direction.TOP_RIGHT: Direction.TOP_RIGHT}
    else:
        dir_convert_dict = {Direction.TOP: Direction.RIGHT, Direction.LEFT: Direction.BOTTOM}

    rule = ""
    for d, label in dir_convert_dict.items():
        new_row = "R + 1" if d == Direction.TOP_RIGHT else "R"
        if directed:
            rule += f'edge(R, C, "{d}") :- line_in({new_row}, C, "{label}").\n'
            rule += f'edge(R, C, "{d}") :- line_out({new_row}, C, "{label}").\n'
        else:
            rule += f'edge(R, C, "{d}") :- line_io({new_row}, C, "{label}").\n'

    return rule
