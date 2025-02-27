"""Utility for loops."""

from typing import Tuple


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
    constraint += ':- grid(R, C), grid_direction(R, C, "d"), not grid_direction(R + 1, C, "u").'
    return constraint


def intersect_loop(color: str = "white", path: bool = False) -> str:
    """
    Generate a loop (which can intersect itself) constraint with loop signs.

    A grid fact and a grid_direction rule should be defined first.
    """
    rule = "pass_by_loop(R, C) :- grid(R, C), #count { D: grid_direction(R, C, D) } = 2.\n"
    rule += "intersection(R, C) :- grid(R, C), #count { D: grid_direction(R, C, D) } = 4.\n"
    rule += "pass_by_loop(R, C) :- intersection(R, C).\n"

    visit_constraints = ["not pass_by_loop(R, C)"]
    if path:  # pragma: no cover
        visit_constraints.append("not dead_end(R, C)")
        rule += ":- dead_end(R, C), grid(R, C), #count { D: grid_direction(R, C, D) } != 1.\n"

    rule += f":- grid(R, C), {color}(R, C), {', '.join(visit_constraints)}.\n"
    rule += ':- grid(R, C), grid_direction(R, C, "l"), not grid_direction(R, C - 1, "r").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "u"), not grid_direction(R - 1, C, "d").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "r"), not grid_direction(R, C + 1, "l").\n'
    rule += ':- grid(R, C), grid_direction(R, C, "d"), not grid_direction(R + 1, C, "u").'
    return rule


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
    return constraint.strip()


def count_area_pass(target: int, _id: int) -> str:
    """
    Generate a rule that counts the times that a loop passes through an area.

    An area_border fact should be defined first.
    """
    return f":- #count {{ R, C, D: area_border({_id}, R, C, D), grid_direction(R, C, D) }} != {2 * target}."


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


def loop_sign(color: str = "white") -> str:
    """
    Generate a constraint to generate general loop signs.

    A grid fact and a grid_direction rule should be defined first.
    """
    rule = ""
    for d1, d2 in ("lu", "ld", "ru", "rd", "lr", "ud"):
        rule += f'loop_sign(R, C, "{d1}{d2}") :- grid(R, C), {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'

    return rule.strip()


def loop_segment(src_cell: Tuple[int, int]) -> str:
    """
    Generate a rule for a loop segment.

    A grid fact and a loop_sign rule should be defined first.
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

    return rule.strip()


def loop_straight(color: str = "white") -> str:
    """
    Generate a rule for straight passing through a cell.

    A grid fact and a grid_direction rule should be defined first.
    """
    rule = ""
    for d1, d2 in ("lr", "ud"):
        rule += f'straight(R, C) :- grid(R, C), {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'
    return rule.strip()


def loop_turning(color: str = "white") -> str:
    """
    Generate a rule for turning through a cell.

    A grid fact and a grid_direction rule should be defined first.
    """
    rule = ""
    for d1, d2 in ("lu", "ld", "ru", "rd"):
        rule += f'turning(R, C) :- grid(R, C), {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'
    return rule.strip()


def convert_direction_to_edge(directed: bool = False, diagonal: bool = False) -> str:
    """Convert grid direction fact to edge fact."""
    dir_dict = {"diag_down": "dr", "diag_up": "ur"} if diagonal else {"top": "r", "left": "d"}

    rule = ""
    for d, pos in dir_dict.items():
        new_row = "R + 1" if d == "diag_up" else "R"
        if directed:
            rule += f'edge_{d}(R, C) :- grid_in({new_row}, C, "{pos}").\n'
            rule += f'edge_{d}(R, C) :- grid_out({new_row}, C, "{pos}").\n'
        else:
            rule += f'edge_{d}(R, C) :- grid_direction({new_row}, C, "{pos}").\n'

    return rule.strip()
