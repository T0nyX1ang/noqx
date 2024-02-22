"""Generating facts and meta-facts for the solver."""

from typing import List, Tuple


def display(item: str = "black", size: int = 2) -> str:
    """Generates a rule for displaying specific items with a certain size."""
    return f"#show {item}/{size}."


def grid(rows: int, cols: int) -> str:
    """Generates facts for a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def area(_id: int, src_cells: List[Tuple[int, int]]) -> str:
    """Generates facts for areas."""
    return "\n".join(f"area({_id}, {r}, {c})." for r, c in src_cells)


def edge(rows: int, cols: int) -> str:
    """
    Generates facts for grid edges.
    Note grid borders are set outside.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += "{ vertical_line(R, C) } :- vertical_range(R, C).\n"
    fact += "{ horizontal_line(R, C) } :- horizontal_range(R, C).\n"
    fact += f"vertical_line(0..{rows - 1}, 0).\n"
    fact += f"vertical_line(0..{rows - 1}, {cols}).\n"
    fact += f"horizontal_line(0, 0..{cols - 1}).\n"
    fact += f"horizontal_line({rows}, 0..{cols - 1})."
    return fact


def direction(directions: str) -> str:
    """Generates facts for directions."""
    format_d = map(lambda x: f'"{x}"', tuple(directions))
    return f"direction({';'.join(format_d)})."
