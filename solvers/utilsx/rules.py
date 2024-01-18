"""Utility for general clingo rules."""

from typing import List, Literal


def display(color: str = "black") -> str:
    """Generates a rule for displaying the {color} cells."""
    return f"#show {color}/2."


def grid(rows: int, cols: int) -> str:
    """Generates a rule for generating a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def shade_c(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid rule should be defined first."""
    return f"{{ {color}(R, C) }} :- grid(R, C)."


def shade_cc(colors: List[str]) -> str:
    """
    Generates a rule that enforces several different {color} cells.

    A grid rule should be defined first.
    """
    return f"{{ {'; '.join(str(c) + '(R, C)' for c in colors)} }} = 1 :- grid(R, C)."


def count(target: int, color: str = "black", _type: str = Literal["grid", "row", "col"]) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a grid / row / column.

    A grid rule should be defined first.
    """

    if _type == "grid":
        return f":- #count {{ grid(R, C) : {color}(R, C) }} != {target}."

    if _type == "row":
        return f":- grid(R, _), #count {{ C : {color}(R, C) }} != {target}."

    if _type == "col":
        return f":- grid(_, C), #count {{ R : {color}(R, C) }} != {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'row', 'col'.")


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


def count_adjacent(target: int, src_r: int, src_c: int, color: str = "black") -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    return f":- #count {{ R, C: {color}(R, C), adj(R, C, {src_r}, {src_c}) }} != {target}."


def unique_num(color: str = "black", _type: Literal["row", "col"] = "row") -> str:
    """
    Generates a constraint for unique {color} numbered cells in a row / column.

    A number rule should be defined first.
    """
    if _type == "row":
        return f":- number(_, C, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "col":
        return f":- number(R, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    raise ValueError("Invalid type, must be one of 'row', 'col'.")


def unique_linecolor(colors: List[str], _type: Literal["row", "col"] = "row") -> str:
    """
    Generates a constraint for unique row / column in a grid.
    At least one pair of cells in the same row / column should have different colors.

    A grid rule should be defined first.
    """
    if _type == "row":
        colors_row = ", ".join(
            f"#count {{ C : grid(R1, C), grid(R2, C), {color}(R1, C), not {color}(R2, C) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(R1, _), grid(R2, _), R1 < R2, {colors_row}."

    if _type == "col":
        colors_col = ", ".join(
            f"#count {{ R : grid(R, C1), grid(R, C2), {color}(R, C1), not {color}(R, C2) }} = 0" for color in colors
        ).replace("not not ", "")
        return f":- grid(_, C1), grid(_, C2), C1 < C2, {colors_col}."

    raise ValueError("Invalid type, must be one of 'row', 'col'.")


def reachable(color: str = "black") -> str:
    """
    Generate a rule to check the reachability of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    reachable_source = f"reachable_{color_escape}(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1), grid(R1, C1) }}."
    reachable_propagation = (
        f"reachable_{color_escape}(R, C) :- reachable_{color_escape}(R1, C1), adj(R, C, R1, C1), {color}(R, C)."
    )
    return reachable_source + "\n" + reachable_propagation


def connected(color: str = "black") -> str:
    """
    Generate a constraint to check the connectivity of {color} cells.

    A grid rule and a reachable rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    return f":- grid(R, C), {color}(R, C), not reachable_{color_escape}(R, C)."


def lit_up(src_r: int, src_c: int, color: str = "black") -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    tag = f"lit_{src_r}_{src_c}_{color_escape}"
    source_cell = f"{tag}({src_r}, {src_c})."
    lit_propagation = (
        f"{tag}(R, C) :- {tag}(R1, C1), adj(R, C, R1, C1), {color}(R, C), (R - {src_r}) * (C - {src_c}) == 0."
    )
    return source_cell + "\n" + lit_propagation


def count_lit_up(target: int, src_r: int, src_c: int, color: str = "black") -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit-up rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    tag = f"lit_{src_r}_{src_c}_{color_escape}"
    return f":- {{ {tag}(R, C) }} != {target}."


def avoid_rect(rect_r: int, rect_c: int, color: str = "black") -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid rule should be defined first. (This is indirectly required by the shade rule.)
    """
    rect_pattern = [f"grid(R + {r}, C + {c}), {color}(R + {r}, C + {c})" for r in range(rect_r) for c in range(rect_c)]
    return f":- {', '.join(rect_pattern)}."
