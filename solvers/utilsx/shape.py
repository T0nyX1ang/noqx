"""Rules and constraints to detect certain shapes."""

from typing import Tuple

from .helper import tag_encode


def all_rect(color: str = "black") -> str:
    """
    Generate a constraint to force rectangles.

    A grid rule should be defined first.
    """

    not_color = "not_color(R, C) :- grid(R + 1, C), not grid(R, C).\n"
    not_color += "not_color(R, C) :- grid(R, C + 1), not grid(R, C).\n"
    not_color += f"not_color(R, C) :- grid(R, C), not {color}(R, C)."

    upleft = f"upleft(R, C) :- grid(R, C), {color}(R, C), not_color(R - 1, C), not_color(R, C - 1)."
    left = f"left(R, C) :- grid(R, C), {color}(R, C), upleft(R - 1, C), {color}(R - 1, C), not_color(R, C - 1).\n"
    left += f"left(R, C) :- grid(R, C), {color}(R, C), left(R - 1, C), {color}(R - 1, C), not_color(R, C - 1)."
    up = f"up(R, C) :- grid(R, C), {color}(R, C), upleft(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    up += f"up(R, C) :- grid(R, C), {color}(R, C), up(R, C - 1), {color}(R, C - 1), not_color(R - 1, C).\n"
    remain = "remain(R, C) :- grid(R, C), left(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), left(R, C - 1), remain(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), up(R - 1, C).\n"
    remain += "remain(R, C) :- grid(R, C), remain(R, C - 1), remain(R - 1, C)."

    constraint = f":- grid(R, C), {color}(R, C), not upleft(R, C), not left(R, C), not up(R, C), not remain(R, C)."
    constraint += f":- grid(R, C), remain(R, C), not {color}(R, C)."
    return not_color + "\n" + upleft + "\n" + left + "\n" + up + "\n" + remain + "\n" + constraint


def avoid_rect(rect_r: int, rect_c: int, corner: Tuple[int, int] = (None, None), color: str = "black") -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid fact should be defined first.
    """
    corner_r, corner_c = corner
    corner_r = corner_r if corner_r is not None else "R"
    corner_c = corner_c if corner_c is not None else "C"

    if corner_r != "R" and corner_c != "C":
        rect_pattern = [f"{color}({corner_r + r}, {corner_c + c})" for r in range(rect_r) for c in range(rect_c)]
    else:
        rect_pattern = [f"{color}({corner_r} + {r}, {corner_c} + {c})" for r in range(rect_r) for c in range(rect_c)]
        rect_pattern.append(f"grid({corner_r}, {corner_c})")
        rect_pattern.append(f"grid({corner_r} + {rect_r - 1}, {corner_c} + {rect_c - 1})")

    return f":- {', '.join(rect_pattern)}."


def valid_omino(num: int = 4, color: str = "black", _type: str = "grid", distinct_variant: bool = False) -> str:
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """
    common = f"omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC"
    tag = tag_encode("valid_omino", num, color)
    param = "T, V" if distinct_variant else "T"

    if _type == "grid":
        count_valid = f"#count {{ R, C : grid(R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}({param}, AR, AC) :- grid(AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    if _type == "area":
        count_valid = f"#count {{ R, C : area(A, R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}(A, {param}, AR, AC) :- area(A, AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    if _type == "edge":
        constraint = f"{{ {tag}({param}, R, C) : omino_{num}(T, V, _, _)}} 1 :- grid(R, C).\n"
        count_omino = f"#count {{ DR, DC : reachable_edge(AR, AC, R, C), {color}(R, C), {common} }}"
        constraint += (
            f":- {tag}({param}, AR, AC), grid(AR, AC), {color}(R, C), not reachable_edge(AR, AC, R, C), {common}."
        )
        constraint += f":- not {tag}({param}, AR, AC), grid(AR, AC), omino_{num}(T, V, _, _), {count_omino} = {num}."
        return constraint

    raise ValueError("Invalid type, must be one of 'grid', 'area', 'edge'.")
