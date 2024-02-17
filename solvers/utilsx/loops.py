"""Utility for loops."""

# --- ISOLATED CELL PATTERNS ---
ISOLATED = ["."]

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
NON_DIRECTED = ["J", "7", "L", "r", "-", "1"]

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
DIRECTED = ["J^", "J<", "7v", "7<", "L^", "L>", "r>", "rv", "->", "-<", "1^", "1v"]
DIRECTED_BENDS = ["J^", "J<", "7v", "7<", "L^", "L>", "r>", "rv"]
DIRECTED_STRAIGHTS = ["->", "-<", "1^", "1v"]

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
