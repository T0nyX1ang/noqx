"""Utility for general clingo rules."""


def get_ranged_number_rule(lower: int, upper: int, name: str = "range") -> str:
    """Generates a rule for getting a range of numbers."""
    assert name.isalpha() is True
    return f"{name}({lower}..{upper})."


def get_grid_rule(rows: int, cols: int) -> str:
    """Generates a rule for generating a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def get_hv_neighbors_rule() -> str:
    """Generates a rule for getting the horizontal/vertical neighbors."""
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."


def get_diag_neighbors_rule() -> str:
    """Generates a rule for getting the diagonal neighbors."""
    return "adj(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."


def get_surroundings_rule() -> str:
    """Generates a rule for getting the surroundings neighbors."""
    hv_rule = get_hv_neighbors_rule()
    diag_rule = get_diag_neighbors_rule()
    return f"{hv_rule}\n{diag_rule}"
