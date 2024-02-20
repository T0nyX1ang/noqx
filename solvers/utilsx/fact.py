"""Generating facts and meta-facts for the solver."""

from typing import List, Tuple

from .helper import get_variants

OMINOES = {
    4: {
        "T": ((0, 0), (1, 0), (1, 1), (2, 0)),
        "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (2, 1)),
        "S": ((0, 0), (0, 1), (1, 1), (1, 2)),
    },
    5: {
        "F": ((0, 0), (0, 1), (1, -1), (1, 0), (2, 0)),
        "I": ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
        "L": ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)),
        "N": ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3)),
        "P": ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0)),
        "T": ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1)),
        "U": ((0, 0), (0, 2), (1, 0), (1, 1), (1, 2)),
        "V": ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
        "W": ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)),
        "X": ((0, 0), (1, -1), (1, 0), (1, 1), (2, 0)),
        "Y": ((0, 0), (1, -1), (1, 0), (1, 1), (1, 2)),
        "Z": ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)),
    },
}


def display(item: str = "black", size: int = 2) -> str:
    """Generates a rule for displaying specific items with a certain size."""
    return f"#show {item}/{size}."


def grid(rows: int, cols: int) -> str:
    """Generates facts for a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def area(_id: int, src_cells: List[Tuple[int, int]]) -> str:
    """Generates facts for areas."""
    return "\n".join(f"area({_id}, {r}, {c})." for r, c in src_cells)


def omino(num: int = 4, _types: List[str] = None) -> str:
    """Generates facts for omino types."""
    if _types is None:
        _types = list(OMINOES[num].keys())

    data = []

    for omino_type in _types:
        omino_shape = OMINOES[num][omino_type]
        omino_variants = get_variants(omino_shape, allow_rotations=True, allow_reflections=True)

        for i, variant in enumerate(omino_variants):
            for dr, dc in variant:
                data.append(f'omino_{num}("{omino_type}", {i}, {dr}, {dc}).')

    return "\n".join(data)


def edge(rows: int, cols: int) -> str:
    """
    Generates facts for grid edges.
    Note grid borders are set outside.
    """
    fact = f"vertical_range(0..{rows - 1}, 0..{cols}).\n"
    fact += f"horizontal_range(0..{rows}, 0..{cols - 1}).\n"
    fact += "{ vertical_line(R, C) } :- vertical_range(R, C).\n"
    fact += "{ horizontal_line(R, C) } :- horizontal_range(R, C)."
    return fact


def direction(directions: str) -> str:
    """Generates facts for directions."""
    format_d = map(lambda x: f'"{x}"', tuple(directions))
    return f"direction({';'.join(format_d)})."
