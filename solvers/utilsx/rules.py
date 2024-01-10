"""Utility for general clingo rules."""


def display() -> str:
    """Generates a rule for displaying the black cells."""
    return "#show black/2."


def ranged(lower: int, upper: int, name: str = "range") -> str:
    """Generates a rule for getting a range of numbers."""
    return f"{name}({lower}..{upper})."


def grid(rows: int, cols: int) -> str:
    """Generates a rule for generating a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def shade(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid rule should be defined first."""
    return f"{{{color}(R, C)}} :- grid(R, C)."


def shade_without_num(name: str = "range", color: str = "black") -> str:
    """Generates a rule that enforces a {color} cell or a with cell with ranged numbers."""
    return f"{{number(R, C, N) : {name}(N) ; {color}(R, C)}} = 1 :- grid(R, C)."


def orth_adjacent() -> str:
    """
    Generates a rule for getting the orthogonal neighbors.

    A grid rule should be defined first.
    """
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."


def diag_adjacent() -> str:
    """
    Generates a rule for getting the diagonal neighbors.

    A grid rule should be defined first.
    """
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."


def avoid_adjacent(color: str = "black") -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj(R, C, R1, C1)."


def row_num_unique(color: str = "black") -> str:
    """
    Generates a constraint for unique {colo} numbered cell in every row.

    A number rule should be defined first.
    """
    return f":- number(_, C, N), 2 {{ {color}(R, C) : number(R, C, N) }}."


def col_num_unique(color: str = "black") -> str:
    """
    Generates a constraint for unique {color} numbered cell in every column.

    A number rule should be defined first.
    """
    return f":- number(R, _, N), 2 {{ {color}(R, C) : number(R, C, N) }}."


def connected(color: str = "black") -> str:
    """
    Generate a rule and a constraint to check the connectivity of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    reachable = f"reachable_{color_escape}(R, C) :- (R, C) = #min{{(R1, C1) : {color}(R1, C1), grid(R1, C1)}}."
    reachable_propagation = (
        f"reachable_{color_escape}(R, C) :- reachable_{color_escape}(R1, C1), adj(R, C, R1, C1), {color}(R, C)."
    )
    connectivity = f":- grid(R, C), {color}(R, C), not reachable_{color_escape}(R, C)."
    return "\n".join([reachable, reachable_propagation, connectivity])
