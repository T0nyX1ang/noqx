"""Utility for general clingo rules."""

import itertools
from typing import List, Tuple, Union

from .shapes import OMINOES, get_variants

rev_op_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}


def tag_encode(_type: str, src_cell: Tuple[int, int] = (None, None), color: str = "black") -> str:
    """Encode a valid tag predicate without spaces or hyphens."""
    tag_data = [_type]

    src_r, src_c = src_cell
    if src_r is not None and src_c is not None:
        tag_data.append(str(src_r))
        tag_data.append(str(src_c))

    if color is not None:
        tag_data.append(color.replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def display(color: Union[str, List[str]] = "black") -> str:
    """Generates a rule for displaying the {color} cells."""
    if isinstance(color, str):
        return f"#show {color}/2."

    return "\n".join(f"#show {c}/2." for c in color)


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


def shade_c(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid fact should be defined first."""
    return f"{{ {color}(R, C) }} :- grid(R, C)."


def shade_cc(colors: List[str]) -> str:
    """
    Generates a rule that enforces several different {color} cells.

    A grid fact should be defined first.
    """
    return f"{{ {'; '.join(str(c) + '(R, C)' for c in colors)} }} = 1 :- grid(R, C)."


def count(target: int, op: str = "eq", color: str = "black", _type: str = "grid", _id: int = None) -> str:
    """
    Generates a constraint for counting the number of {color} cells in a grid / row / column / area.

    A grid fact should be defined first.
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
        return f":- #count {{ R, C : area({_id}, R, C), {color}(R, C) }} {op} {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'row', 'col', 'area'.")


def adjacent(_type: int = 4) -> str:
    """
    Generates a rule for getting the adjacent neighbors.
    If _type = 4, then only orthogonal neighbors are considered.
    If _type = 8, then both orthogonal and diagonal neighbors are considered.

    A grid fact should be defined first.
    """
    if _type == 4:
        return "adj_4(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."

    if _type == 8:
        res = "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1.\n"
        res += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return res

    raise ValueError("Invalid adjacent type, must be one of '4', '8'.")


def area_adjacent(adj_type: int = 4, color: str = None) -> str:
    """
    Generate a rule for getting the adjacent areas.

    An adjacent rule should be defined first.
    """
    if color is not None:
        return f"{tag_encode(f'area_adj_{adj_type}', color=color)}(A, A1) {avoid_area_adjacent(color, adj_type)}"
    return f"area_adj_{adj_type}(A, A1) :- area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1."


def avoid_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def avoid_area_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid same {color} cells on the both sides of an area.

    An adjacent rule and an area fact should be defined first.
    """
    return f":- area(A, R, C), {color}(R, C), area(A1, R1, C1), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1."


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

    A grid fact and an adjacent rule should be defined first. n is the number of known source cells.
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


def connected(color: str = "black", adj_type: int = 4, _in: str = "grid") -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    tag = tag_encode(f"reachable_{_in}", color=color)

    if _in == "grid":
        initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1), grid(R1, C1) }}."
        propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), grid(R, C), {color}(R, C)."
        constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    elif _in == "area":
        initial = f"{tag}(A, R, C) :- area(A, _, _), (R, C) = #min{{ (R1, C1) : area(A, R1, C1), {color}(R1, C1) }}."
        propagation = f"{tag}(A, R, C) :- {tag}(A, R1, C1), adj_{adj_type}(R, C, R1, C1), area(A, R, C), {color}(R, C)."
        constraint = f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C)."
    else:
        raise ValueError("Invalid type, must be one of 'grid', 'area'.")

    return initial + "\n" + propagation + "\n" + constraint


def region(
    src_cell: Tuple[int, int], exclude_cells: List[Tuple[int, int]] = None, color: str = "black", adj_type: int = 4
) -> str:
    """
    Generate a rule to construct a region of {color} cells from a source cell.

    An adjacent rule and a grid fact should be defined first.
    """
    src_r, src_c = src_cell
    tag = tag_encode("region", src_cell, color)

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
    return f":- {{ {tag_encode('region', src_cell, color)}(R, C) }} != {target}."


def avoid_unknown_region(known_cells: Tuple[int, int], color: str = "black") -> str:
    """
    Generate a constraint to avoid regions that does not derive from a source cell.

    A grid fact and a region rule should be defined first.
    """
    included = ""
    for src_cell in known_cells:
        included += f"not {tag_encode('region', src_cell, color)}(R, C), "
    return f":- grid(R, C), {included.strip()} {color}(R, C)."


def lit(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """
    tag = tag_encode("lit", src_cell, color)
    src_r, src_c = src_cell
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
    op = rev_op_dict[op]
    return f":- {{ {tag_encode('lit', src_cell, color)}(R, C) }} {op} {target}."


def avoid_rect(rect_r: int, rect_c: int, corner: Tuple[int, int] = (None, None), color: str = "black") -> str:
    """
    Generates a constraint to avoid rectangular patterned {color} cells.

    A grid fact should be defined first.
    """
    corner_r, corner_c = corner
    corner_r = corner_r if corner_r is not None else "R"
    corner_c = corner_c if corner_c is not None else "C"

    if corner_r != "R" and corner_c != "C":
        rect_pattern = [f"{color}({corner_r + r}, {corner_c + c})" for r in range(rect_r) for c in range(rect_c)]
    else:
        rect_pattern = [f"{color}({corner_r} + {r}, {corner_c} + {c})" for r in range(rect_r) for c in range(rect_c)]
        rect_pattern.append(f"grid({corner_r}, {corner_c})")
        rect_pattern.append(f"grid({corner_r} + {rect_r - 1}, {corner_c} + {rect_c - 1})")

    return f":- {', '.join(rect_pattern)}."
