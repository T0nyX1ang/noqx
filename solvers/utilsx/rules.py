"""Utility for general clingo rules."""


def display() -> str:
    """Generates a rule for displaying the black cells."""
    return "#show black/2."


def ranged(lower: int, upper: int, name: str = "range") -> str:
    """Generates a rule for getting a range of numbers."""
    assert name.isalpha() is True
    return f"{name}({lower}..{upper})."


def grid(rows: int, cols: int) -> str:
    """Generates a rule for generating a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def shading(name: str = "range") -> str:
    """Generates a rule that enforces a black cell or a with cell with ranged numbers."""
    assert name.isalpha() is True
    return "1 {number(R, C, N) : range(N) ; black(R, C)} 1 :- grid(R, C)."


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
    assert color.isalpha() is True
    adj_rule = adjacent()
    avoid_rule = f":- {color}(R, C), {color}(R1, C1), adj(R, C, R1, C1)."
    return f"{adj_rule}\n{avoid_rule}"
