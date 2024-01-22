"""Utility for general clingo rules."""

import itertools
from typing import List, Tuple, Union

rev_op_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}


def display(color: Union[str, List[str]] = "black") -> str:
    """Generates a rule for displaying the {color} cells."""
    if isinstance(color, str):
        return f"#show {color}/2."

    return "\n".join(f"#show {c}/2." for c in color)


def grid(rows: int, cols: int) -> str:
    """Generates a rule for generating a grid."""
    return f"grid(0..{rows - 1}, 0..{cols - 1})."


def area(_id: int, src_cells: List[Tuple[int, int]]) -> str:
    """Generates a rule for defining an area."""
    return "\n".join(f"area_{_id}({r}, {c})." for r, c in src_cells)


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


def count(target: int, op: str = "eq", color: str = "black", _type: str = "grid", _id: int = None) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a grid / row / column / area.

    A grid rule should be defined first.
    """
    op = rev_op_dict[op]

    if _id is None:
        _id = "R" if _type == "row" else "C" if _type == "col" else None

    if _type == "grid":
        return f":- #count {{ grid(R, C) : {color}(R, C) }} {op} {target}."

    if _type == "row":
        return f":- grid({_id}, _), #count {{ C : {color}({_id}, C) }} {op} {target}."

    if _type == "col":
        return f":- grid(_, {_id}), #count {{ R : {color}(R, {_id}) }} {op} {target}."

    if _type == "area":
        return f":- #count {{ R, C : area_{_id}(R, C), {color}(R, C) }} {op} {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'row', 'col', 'area'.")


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

    raise ValueError("Invalid adjacent type, must be one of '4', '8'.")


def avoid_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def count_adjacent(
    target: int, src_cell: Tuple[int, int], op: str = "eq", color: str = "black", adj_type: int = 4
) -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    op = rev_op_dict[op]
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {op} {target}."


def identical_adjacent_map(known_cells: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate n * (n - 1) / 2 constraints and n rules to enfroce identical adjacent cell maps.

    A grid rule and an adjacent rule should be defined first. n is the number of known source cells.
    """

    rules = "\n".join(
        f"{{ map_{r}_{c}(R, C): adj_{adj_type}(R, C, {r}, {c}), {color}(R, C) }} = 1 :- grid({r}, {c})."
        for r, c in known_cells
    )  # n rules are generated
    constraints = "\n".join(
        f":- map_{r1}_{c1}(R, C), map_{r2}_{c2}(R, C). "
        for (r1, c1), (r2, c2) in itertools.combinations(known_cells, 2)
    )  # n * (n - 1) / 2 constraints are generated
    return rules + "\n" + constraints


def unique_num(color: str = "black", _type: str = "row") -> str:
    """
    Generates a constraint for unique {color} numbered cells in a row / column.

    A number rule should be defined first.
    """
    if _type == "row":
        return f":- number(_, C, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "col":
        return f":- number(R, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    raise ValueError("Invalid line type, must be one of 'row', 'col'.")


def connected(color: str = "black", adj_type: int = 4, area_id: int = None) -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    tag = f"reachable_{color_escape}" + f"_area_{area_id}" * (area_id is not None)
    _type = f"area_{area_id}" if area_id is not None else "grid"

    initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1), {_type}(R1, C1) }}."
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {_type}(R, C), {color}(R, C)."
    constraint = f":- {_type}(R, C), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


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


def avoid_unknown_region(known_cells: Tuple[int, int], color: str = "black") -> str:
    """
    Generate a constraint to avoid regions that does not derive from a source cell.

    A grid rule and a region rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    included = ""
    for src_r, src_c in known_cells:
        included += f"not region_{src_r}_{src_c}_{color_escape}(R, C), "

    return f":- grid(R, C), {included.strip()} {color}(R, C)."


def lit(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    tag = f"lit_{src_r}_{src_c}_{color_escape}"
    source_cell = f"{tag}({src_r}, {src_c})."

    if adj_type == 4:
        lit_constraint = f"(R - {src_r}) * (C - {src_c}) == 0"
    elif adj_type == 8:
        lit_constraint = (
            f"(R - {src_r}) * (C - {src_c}) * (R - {src_r} - C + {src_c}) * (R - {src_r} + C - {src_c}) == 0"
        )
    else:
        raise ValueError("Invalid adjacent type, must be one of '4', '8'.")

    lit_propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {color}(R, C), {lit_constraint}."
    return source_cell + "\n" + lit_propagation


def count_lit(target: int, src_cell: Tuple[int, int], op: str = "eq", color: str = "black") -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit rule should be defined first.
    """

    color_escape = color.replace("-", "_").replace(" ", "_")  # make a valid predicate name
    src_r, src_c = src_cell
    op = rev_op_dict[op]
    return f":- {{ lit_{src_r}_{src_c}_{color_escape}(R, C) }} {op} {target}."


def avoid_rect(rect_r: int, rect_c: int, corner: Tuple[int, int] = (None, None), color: str = "black") -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid rule should be defined first.
    """
    corner_r, corner_c = corner
    corner_r = corner_r if corner_r is not None else "R"
    corner_c = corner_c if corner_c is not None else "C"

    if corner_r != "R" and corner_c != "C":
        rect_pattern = [f"{color}({corner_r + r}, {corner_c + c})" for r in range(rect_r) for c in range(rect_c)]
    else:
        rect_pattern = [
            f"grid({corner_r} + {r}, {corner_c} + {c}), {color}({corner_r} + {r}, {corner_c} + {c})"
            for r in range(rect_r)
            for c in range(rect_c)
        ]

    return f":- {', '.join(rect_pattern)}."
