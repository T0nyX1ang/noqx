"""Rules and constraints to detect certain shapes."""

from .helper import tag_encode

def all_rectangles(color: str = "black") -> str:
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


def valid_omino(num: int = 4, color: str = "black", _type: str = "grid") -> str:
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """
    common = f"omino_{num}(T, V, DR, DC), R = AR + DR, C = AC + DC"
    tag = tag_encode("valid_omino", num, color)

    if _type == "grid":
        count_valid = f"#count {{ R, C : grid(R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}(T, AR, AC) :- grid(AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    if _type == "area":
        count_valid = f"#count {{ R, C : area(A, R, C), {color}(R, C), {common} }} = {num}"
        return f"{tag}(A, T, AR, AC) :- area(A, AR, AC), omino_{num}(T, V, _, _), {count_valid}."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")
