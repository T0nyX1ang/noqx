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


def shading(name: str = "range") -> str:
    """Generates a rule that enforces a black cell or a with cell with ranged numbers."""
    return f"1 {{number(R, C, N) : {name}(N) ; black(R, C)}} 1 :- grid(R, C)."


def hv_adjacent() -> str:
    """Generates a rule for getting the horizontal/vertical neighbors."""
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."


def diag_adjacent() -> str:
    """Generates a rule for getting the diagonal neighbors."""
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."


def adjacent() -> str:
    """Generates a rule for getting the surroundings neighbors."""
    hv_rule = hv_adjacent()
    diag_rule = diag_adjacent()
    return f"{hv_rule}\n{diag_rule}"


def no_adjacent(color: str = "black") -> str:
    """Generates a rule for no adjacent {color: default = black} cells."""
    adj_rule = adjacent()
    avoid_rule = f":- {color}(R, C), {color}(R1, C1), adj(R, C, R1, C1)."
    return f"{adj_rule}\n{avoid_rule}"


def r_unique(color: str = "-black") -> str:
    """Generates a rule for unique {color: default = not black} cell in every row."""
    return f":- number(_, C, N), 2 {{ {color}(R, C) : number(R, C, N) }}."


def c_unique(color: str = "-black") -> str:
    """Generates a rule for unique {color: default = not black} cell in every row."""
    return f":- number(R, _, N), 2 {{ {color}(R, C) : number(R, C, N) }}."


def rc_unique(color: str = "-black") -> str:
    """Generates a rule for unique {color: default = not black} cell in every row and column."""
    r_uni_rule = r_unique(color)
    c_uni_rule = c_unique(color)
    return f"{r_uni_rule}\n{c_uni_rule}"
