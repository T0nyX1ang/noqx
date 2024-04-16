"""Utility for loops."""

from typing import List, Tuple


NON_DIRECTED = ["J", "7", "L", "r", "-", "1", ""]
DIRECTED = ["J^", "J<", "7v", "7<", "L^", "L>", "r>", "rv", "->", "-<", "1^", "1v", ""]
DIRECTIONAL_PAIR_TO_UNICODE = {
    "J^": "⬏",
    "J<": "↲",
    "7v": "↴",
    "7<": "↰",
    "L^": "⬑",
    "L>": "↳",
    "r>": "↱",
    "rv": "⬐",
    "->": "→",
    "-<": "←",
    "1^": "↑",
    "1v": "↓",
}


def single_loop(color: str = "white", path: bool = False) -> str:
    """
    Generate a single loop constraint with loop signs.

    A grid fact and a grid_direction rule should be defined first.
    """
    constraint = "pass_by_loop(R, C) :- grid(R, C), #count { D: grid_direction(R, C, D) } = 2.\n"

    visit_constraints = ["not pass_by_loop(R, C)"]
    if path:
        visit_constraints.append("not dead_end(R, C)")
        constraint += ":- dead_end(R, C), grid(R, C), #count { D: grid_direction(R, C, D) } != 1.\n"

    constraint += f":- grid(R, C), {color}(R, C), {', '.join(visit_constraints)}.\n"
    constraint += ':- grid(R, C), grid_direction(R, C, "l"), not grid_direction(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), grid_direction(R, C, "u"), not grid_direction(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), grid_direction(R, C, "r"), not grid_direction(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), grid_direction(R, C, "d"), not grid_direction(R + 1, C, "u").\n'

    dirs = ["lu", "ld", "ru", "rd", "lr", "ud"]
    rule = ""
    for sign, (d1, d2) in zip(NON_DIRECTED[:6], dirs):
        rule += f'loop_sign(R, C, "{sign}") :- grid(R, C), {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'
    return constraint + rule.strip()


def directed_loop(color: str = "white", path: bool = False) -> str:
    """
    Generate a directed loop constraint with loop signs.

    A grid fact and a grid_direction rule should be defined first.
    """
    constraint = f"pass_by_loop(R, C) :- grid(R, C), {color}(R, C), #count {{ D: grid_in(R, C, D) }} = 1, #count {{ D: grid_out(R, C, D) }} = 1, grid_in(R, C, D0), not grid_out(R, C, D0).\n"

    visit_constraints = ["not pass_by_loop(R, C)"]
    if path:
        visit_constraints.append("not path_start(R, C)")
        visit_constraints.append("not path_end(R, C)")
        constraint += ":- path_start(R, C), grid(R, C), #count { D: grid_out(R, C, D) } != 1.\n"
        constraint += ":- path_start(R, C), grid(R, C), #count { D: grid_in(R, C, D) } != 0.\n"
        constraint += ":- path_end(R, C), grid(R, C), #count { D: grid_in(R, C, D) } != 1.\n"
        constraint += ":- path_end(R, C), grid(R, C), #count { D: grid_out(R, C, D) } != 0.\n"

    constraint += f":- grid(R, C), {color}(R, C), {', '.join(visit_constraints)}.\n"
    constraint += ':- grid(R, C), grid_in(R, C, "l"), not grid_out(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), grid_in(R, C, "u"), not grid_out(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), grid_in(R, C, "r"), not grid_out(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), grid_in(R, C, "d"), not grid_out(R + 1, C, "u").\n'
    constraint += ':- grid(R, C), grid_out(R, C, "l"), not grid_in(R, C - 1, "r").\n'
    constraint += ':- grid(R, C), grid_out(R, C, "u"), not grid_in(R - 1, C, "d").\n'
    constraint += ':- grid(R, C), grid_out(R, C, "r"), not grid_in(R, C + 1, "l").\n'
    constraint += ':- grid(R, C), grid_out(R, C, "d"), not grid_in(R + 1, C, "u").\n'

    dirs = ["lu", "ul", "ld", "dl", "ru", "ur", "dr", "rd", "lr", "rl", "du", "ud"]
    rule = ""
    for sign, (d1, d2) in zip(DIRECTED[:12], dirs):
        sign = DIRECTIONAL_PAIR_TO_UNICODE[sign]
        rule += f'loop_sign(R, C, "{sign}") :- grid(R, C), {color}(R, C), grid_in(R, C, "{d1}"), grid_out(R, C, "{d2}").\n'
    return constraint + rule.strip()


def pass_area_once(ar: List[Tuple[int, int]]) -> str:
    """
    Generate a rule that a loop passes through an area exactly once.

    A direction fact should be defined first.
    """
    edges = []
    for r, c in ar:
        for dr, dc, direc in ((0, -1, "l"), (-1, 0, "u"), (0, 1, "r"), (1, 0, "d")):
            r1, c1 = r + dr, c + dc
            if (r1, c1) not in ar:
                edges.append(f'grid_direction({r}, {c}, "{direc}")')
    edges = "; ".join(edges)
    return f":- {{ {edges} }} != 2."


def separate_item_from_loop(inside_item: str, outside_item: str) -> str:
    """
    Generate a constraint to make outside_items outside of the loop, and make inside_items inside of loop.

    A grid_direction fact should be defined first.
    """
    rule = "outside_loop(-1, C) :- grid(_, C).\n"
    rule += 'outside_loop(R, C) :- grid(R, C), outside_loop(R - 1, C), not grid_direction(R, C, "r").\n'
    rule += 'outside_loop(R, C) :- grid(R, C), not outside_loop(R - 1, C), grid_direction(R, C, "r").\n'

    constraint = ""
    if len(inside_item) > 0:
        constraint = f":- {inside_item}(R, C), outside_loop(R, C).\n"

    if len(outside_item) > 0:
        constraint += f":- {outside_item}(R, C), not outside_loop(R, C).\n"

    return (rule + constraint).strip()
