"""Utility for general clingo rules."""

from typing import List, Tuple

from .helper import tag_encode

rev_op_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}


def shade_c(color: str = "black") -> str:
    """
    Generate a rule that a cell is either {color} or not {color}.

    A grid fact should be defined first.
    """
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


def avoid_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid adjacent {color} cells based on adjacent definition.

    An adjacent rule should be defined first.
    """
    return f":- {color}(R, C), {color}(R1, C1), adj_{adj_type}(R, C, R1, C1)."


def area_adjacent(adj_type: int = 4, color: str = None) -> str:
    """
    Generate a rule for getting the adjacent areas.

    An adjacent rule should be defined first.
    """
    area_adj = f"area(A, R, C), area(A1, R1, C1), adj_{adj_type}(R, C, R1, C1), A < A1"
    if color is not None:
        area_adj += f", {color}(R, C), {color}(R1, C1)"
        return f"{tag_encode('area_adj', adj_type, color)}(A, A1) :- {area_adj}."
    return f"area_adj_{adj_type}(A, A1) :- {area_adj}."


def avoid_area_adjacent(color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint to avoid same {color} cells on the both sides of an area.

    An adjacent rule and an area fact should be defined first.
    """
    area_adj = area_adjacent(adj_type, color)
    return area_adj[area_adj.find(":-") :]


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


def connected(color: str = "black", adj_type: int = 4, _type: str = "grid") -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    tag = tag_encode("reachable", adj_type, color)

    if _type == "grid":
        initial = f"{tag}(R, C) :- (R, C) = #min{{ (R1, C1) : {color}(R1, C1), grid(R1, C1) }}."
        propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), grid(R, C), {color}(R, C)."
        constraint = f":- grid(R, C), {color}(R, C), not {tag}(R, C)."
    elif _type == "area":
        initial = f"{tag}(A, R, C) :- area(A, _, _), (R, C) = #min{{ (R1, C1) : area(A, R1, C1), {color}(R1, C1) }}."
        propagation = f"{tag}(A, R, C) :- {tag}(A, R1, C1), adj_{adj_type}(R, C, R1, C1), area(A, R, C), {color}(R, C)."
        constraint = f":- area(A, R, C), {color}(R, C), not {tag}(A, R, C)."
    else:
        raise ValueError("Invalid type, must be one of 'grid', 'area'.")

    return initial + "\n" + propagation + "\n" + constraint


def connected_parts(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to get all the connected components of {color} cells.
    Please note that 'reachable/4' is much slower than the 'reachable/2' which only searches for one component.

    An adjacent rule and a grid fact should be defined first.
    """
    tag = tag_encode("reachable", adj_type, color)
    initial = f"{tag}(R0, C0, R, C) :- grid(R0, C0), {color}(R0, C0), R = R0, C = C0."
    propagation = (
        f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), adj_{adj_type}(R, C, R1, C1), grid(R, C), {color}(R, C)."
    )
    return initial + "\n" + propagation


def count_connected_parts(target: int, color: str = "black", adj_type: int = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the number of connected components of {color} cells.

    A reachable rule should be defined first.
    """
    op = rev_op_dict[op]
    tag = tag_encode("reachable", adj_type, color)
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {tag}(R, C, R1, C1) }} {op} {target}."


def region(
    src_cell: Tuple[int, int], exclude_cells: List[Tuple[int, int]] = None, color: str = "black", adj_type: int = 4
) -> str:
    """
    Generate a rule to construct a region of {color} cells from a source cell.

    An adjacent rule and a grid fact should be defined first.
    """
    src_r, src_c = src_cell
    tag = tag_encode("region", adj_type, src_r, src_c, color)

    excludes = ""
    if isinstance(exclude_cells, list):
        for exclude_r, exclude_c in exclude_cells:
            excludes += f"not {tag}({exclude_r}, {exclude_c}).\n"

    source_cell = f"{tag}({src_r}, {src_c})."
    reachable_propagation = f"{tag}(R, C) :- {tag}(R1, C1), adj_{adj_type}(R, C, R1, C1), {color}(R, C)."
    return source_cell + "\n" + excludes + reachable_propagation


def count_region(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to count the size of {color} region connected to a source cell.

    A region rule should be defined first.
    """
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('region', adj_type, src_r, src_c, color)}(R, C) }} != {target}."


def lit(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    tag = tag_encode("lit", adj_type, src_r, src_c, color)
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


def count_lit(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit rule should be defined first.
    """
    op = rev_op_dict[op]
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('lit', adj_type, src_r, src_c, color)}(R, C) }} {op} {target}."


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


def count_valid_omino(target: int, omino_type: str, num: int = 4, op: str = "eq", color: str = "black") -> str:
    """
    Generates a rule for a valid omino.

    A grid rule or an area rule should be defined first.
    """
    op = rev_op_dict[op]
    tag = tag_encode("valid_omino", num, color)
    return f":- #count {{ R, C: {tag}({omino_type}, R, C) }} {op} {target}."
