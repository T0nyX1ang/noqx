"""Utility for general clingo rules."""

from typing import List, Literal, Tuple, Union


def display(color: Union[str, List[str]] = "black") -> str:
    """Generates a rule for displaying the {color} cells."""
    if isinstance(color, str):
        return f"#show {color}/2."

    return "\n".join(f"#show {c}/2." for c in color)

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


def adjacent(_type: int = 4) -> str:
    """
    Generates a rule for getting the adjacent neighbors.
    If _type = 4, then only orthogonal neighbors are considered.
    If _type = 8, then both orthogonal and diagonal neighbors are considered.

    A grid rule should be defined first.
    """
    if _type == 4:
        return "adj_4(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."

    if _type == 8:
        res = "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1.\n"
        res += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return res

    raise ValueError("Invalid type, must be one of '4', '8'.")


def avoid_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def count_adjacent(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} != {target}."


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


def reachable(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the reachability of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    tag = f"reachable_{color_escape}"
    reachable_source = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1), grid(R1, C1) }}."
    reachable_propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {color}(R, C)."
    return reachable_source + "\n" + reachable_propagation


def connected(color: str = "black") -> str:
    """
    Generate a constraint to check the connectivity of {color} cells.

    A grid rule and a reachable rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    return f":- grid(R, C), {color}(R, C), not reachable_{color_escape}(R, C)."


def region(
    src_cell: Tuple[int, int], exclude_cells: List[Tuple[int, int]] = None, color: str = "black", adj_type: int = 4
) -> str:
    """
    Generate a rule to construct a region of {color} cells from a source cell.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    tag = f"region_{src_r}_{src_c}_{color_escape}"

    excludes = ""
    if isinstance(exclude_cells, list):
        for exclude_r, exclude_c in exclude_cells:
            excludes += f"not {tag}({exclude_r}, {exclude_c}).\n"

    source_cell = f"{tag}({src_r}, {src_c})."
    reachable_propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {color}(R, C)."
    return source_cell + "\n" + excludes + reachable_propagation


def count_region(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    """
    Generate a constraint to count the size of {color} region connected to a source cell.

    A region rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    return f":- {{ region_{src_r}_{src_c}_{color_escape}(R, C) }} != {target}."


def avoid_unknown_region(known_src_cells: Tuple[int, int], color: str = "black") -> str:
    """
    Generate a constraint to avoid regions that does not derive from a source cell.

    A grid rule and a region rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    included = ""
    for src_r, src_c in known_src_cells:
        included += f"not region_{src_r}_{src_c}_{color_escape}(R, C), "

    return f":- grid(R, C), {included.strip()} {color}(R, C)."


def lit_up(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    tag = f"lit_{src_r}_{src_c}_{color_escape}"
    source_cell = f"{tag}({src_r}, {src_c})."
    lit_propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {color}(R, C), (R - {src_r}) * (C - {src_c}) == 0."  # pylint: disable=line-too-long
    return source_cell + "\n" + lit_propagation


def count_lit_up(target: int, src_cell: Tuple[int, int], color: str = "black") -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit-up rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    return f":- {{ lit_{src_r}_{src_c}_{color_escape}(R, C) }} != {target}."


def avoid_rect(rect_r: int, rect_c: int, color: str = "black") -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid rule should be defined first.
    """
    rect_pattern = [f"grid(R + {r}, C + {c}), {color}(R + {r}, C + {c})" for r in range(rect_r) for c in range(rect_c)]
    return f":- {', '.join(rect_pattern)}."
