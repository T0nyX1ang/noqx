"""Utility for loops."""

# --- ISOLATED CELL PATTERNS ---
ISOLATED = [".", ""]

# --- NON-DIRECTIONAL PATTERNS ---
# Each cell has 0 or 2 edges in.
# The possible connectivity patterns are:
# - left and up, 'J'
# - left and down, '7'
# - right and up, 'L'
# - right and down, 'r'
# - left and right, '-'
# - up and down, '1'
LEFT_CONNECTING = ["J", "7", "-"]
RIGHT_CONNECTING = ["L", "r", "-"]
UP_CONNECTING = ["J", "L", "1"]
DOWN_CONNECTING = ["7", "r", "1"]
NON_DIRECTED_BENDS = ["J", "7", "L", "r"]
NON_DIRECTED_STRAIGHTS = ["-", "1"]
NON_DIRECTED = ["J", "7", "L", "r", "-", "1", ""]

# --- DIRECTIONAL CELL PATTERNS ---
# These are similar to the directionless edges, but there is
# an arrow-like character for each one that shows its direction.
LEFT_IN = ["J^", "7v", "->"]
RIGHT_IN = ["L^", "rv", "-<"]
TOP_IN = ["J<", "L>", "1v"]
BOTTOM_IN = ["7<", "r>", "1^"]
LEFT_OUT = ["J<", "7<", "-<"]
RIGHT_OUT = ["L>", "r>", "->"]
TOP_OUT = ["J^", "L^", "1^"]
BOTTOM_OUT = ["7v", "rv", "1v"]
DIRECTED = ["J^", "J<", "7v", "7<", "L^", "L>", "r>", "rv", "->", "-<", "1^", "1v", ""]
DIRECTED_BENDS = ["J^", "J<", "7v", "7<", "L^", "L>", "r>", "rv"]
DIRECTED_STRAIGHTS = ["->", "-<", "1^", "1v", ""]

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


def connected_loop(color: str = "white") -> str:
    """
    Generate a loop rule to constrain connectivity.

    A grid fact and a loop/path fact should be defined first.
    """
    initial = f"reachable_loop(R, C) :- (R, C) = #min{{ (R1, C1) : grid(R1, C1), {color}(R1, C1) }}.\n"
    propagation = f"reachable_loop(R, C) :- {color}(R, C), reachable_loop(R1, C1), adj_loop(R1, C1, R, C).\n"
    constraint = f":- grid(R, C), {color}(R, C), not reachable_loop(R, C)."
    return initial + propagation + constraint


def single_loop(color: str = "white", visit_all: bool = False):
    """
    Generate a single loop constraint.
    For a hamilton loop, set `visit_all=True`. Otherwise set `visit_all=False`.
    This will also generate a rule for loop signs.

    A grid fact and a grid_direction rule should be defined first.
    """
    constraint = "pass_by_loop(R, C) :- grid(R, C), #count{ D: grid_direction(R, C, D) } = 2.\n"
    if visit_all:
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C).\n"
    else:
        constraint += "not_pass_by_loop(R, C) :- grid(R, C), #count{ D: grid_direction(R, C, D) } = 0.\n"
        constraint += f":- grid(R, C), {color}(R, C), not pass_by_loop(R, C), not not_pass_by_loop(R, C).\n"
    constraint += f':- {color}(R, C), grid_direction(R, C, "l"), not grid_direction(R, C - 1, "r").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "u"), not grid_direction(R - 1, C, "d").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "r"), not grid_direction(R, C + 1, "l").\n'
    constraint += f':- {color}(R, C), grid_direction(R, C, "d"), not grid_direction(R + 1, C, "u").\n'

    dirs = ["lu", "ld", "ru", "rd", "lr", "ud"]
    rule = ""
    for sign, (d1, d2) in zip(NON_DIRECTED[:6], dirs):
        rule += f'loop_sign(R, C, "{sign}") :- grid(R, C), {color}(R, C), grid_direction(R, C, "{d1}"), grid_direction(R, C, "{d2}").\n'
    if not visit_all:
        rule += f'loop_sign(R, C, "") :- grid(R, C), not_pass_by_loop(R, C).'
    return constraint + rule.strip()
