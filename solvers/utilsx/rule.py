"""Utility for general clingo rules."""

from typing import Any, Iterable, List, Tuple

from .helper import ConnectivityHelper, tag_encode

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


def fill_num(_range: Iterable[int], _type: str = "grid", _id: int = "A", color: str = None) -> str:
    """
    Generate a rule that a cell numbered within {_range}.
    {_range} should have the format "low..high", or "x;y;z" for a list of numbers.

    A grid fact or an area fact should be defined first.
    """
    color_part = "" if color is None else f"; {color}(R, C)"

    _range = sorted(set(_range))  # canonicize the range
    i, range_seq = 0, []

    while i < len(_range):
        start = i
        while i < len(_range) - 1 and _range[i + 1] - _range[i] == 1:
            i += 1
        end = i
        if start < end:
            range_seq.append(f"{_range[start]}..{_range[end]}")
        else:
            range_seq.append(str(_range[start]))
        i += 1

    range_str = f"{';'.join(range_seq)}"

    if _type == "grid":
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- grid(R, C)."

    if _type == "area":
        return f"{{ number(R, C, ({range_str})){color_part} }} = 1 :- area({_id}, R, C)."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")


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


def adjacent(_type: Any = 4) -> str:
    """
    Generates a rule for getting the adjacent neighbors.
    If _type = 4, then only orthogonal neighbors are considered.
    If _type = 8, then both orthogonal and diagonal neighbors are considered.

    A grid fact should be defined first.
    """
    if _type == 4:
        return "adj_4(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1."

    if _type == "x":
        return "adj_x(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."

    if _type == 8:
        res = "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| + |C - C1| == 1.\n"
        res += "adj_8(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| == 1, |C - C1| == 1."
        return res

    if _type == "edge":
        adj = "adj_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), not vertical_line(R, C + 1).\n"
        adj += "adj_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), not horizontal_line(R + 1, C).\n"
        adj += "adj_edge(R, C, R1, C1) :- adj_edge(R1, C1, R, C)."
        return adj

    if _type == "loop":
        adj = 'adj_loop(R0, C0, R, C) :- R = R0, C = C0 + 1, grid(R, C), grid(R0, C0), grid_direction(R, C, "l").\n'
        adj += 'adj_loop(R0, C0, R, C) :- R = R0 + 1, C = C0, grid(R, C), grid(R0, C0), grid_direction(R, C, "u").\n'
        adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
        return adj

    if _type == "loop_directed":
        adj = 'adj_loop(R0, C0, R, C) :- R = R0, C = C0+1, grid(R, C), grid(R0, C0), grid_in(R, C, "l").\n'
        adj += 'adj_loop(R0, C0, R, C) :- R = R0+1, C = C0, grid(R, C), grid(R0, C0), grid_in(R, C, "u").\n'
        adj += 'adj_loop(R0, C0, R, C) :- R = R0, C = C0+1, grid(R, C), grid(R0, C0), grid_out(R, C, "l").\n'
        adj += 'adj_loop(R0, C0, R, C) :- R = R0+1, C = C0, grid(R, C), grid(R0, C0), grid_out(R, C, "u").\n'
        adj += "adj_loop(R0, C0, R, C) :- adj_loop(R, C, R0, C0)."
        return adj

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


def count_adjacent(target: int, src_cell: Tuple[int, int], op: str = "eq", color: str = "black", adj_type: int = 4) -> str:
    """
    Generates a constraint for counting the number of {color} cells adjacent to a cell.

    An adjacent rule should be defined first.
    """
    src_r, src_c = src_cell
    op = rev_op_dict[op]
    return f":- #count {{ R, C: {color}(R, C), adj_{adj_type}(R, C, {src_r}, {src_c}) }} {op} {target}."


def count_adjacent_lines(target: int, src_cell: Tuple[int, int], op: str = "eq") -> str:
    """
    Return a rule that counts the adjacent lines around a cell.

    An edge rule should be defined first.
    """
    src_r, src_c = src_cell
    op = rev_op_dict[op]
    v_1 = f"vertical_line({src_r}, {src_c})"
    v_2 = f"vertical_line({src_r}, {src_c + 1})"
    h_1 = f"horizontal_line({src_r}, {src_c})"
    h_2 = f"horizontal_line({src_r + 1}, {src_c})"
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} != {target}."


def unique_num(color: str = "black", _type: str = "row") -> str:
    """
    Generates a constraint for unique {color} numbered cells in a(an) row / column / area.
    {color} can be set to "grid" for wildcard colors.

    A number rule should be defined first.
    """
    if _type == "row":
        return f":- grid(_, C), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "col":
        return f":- grid(R, _), number(_, _, N), {{ {color}(R, C) : number(R, C, N) }} > 1."

    if _type == "area":
        return f":- area(A, _, _), number(_, _, N), {{ {color}(R, C) : area(A, R, C), number(R, C, N) }} > 1."

    raise ValueError("Invalid line type, must be one of 'row', 'col', 'area'.")


def connected(color: str = "black", adj_type: int = 4, _type: str = "grid") -> str:
    """
    Generate a constraint to check the reachability of {color} cells.

    An adjacent rule and a grid fact should be defined first.
    """
    helper = ConnectivityHelper("reachable", _type, color, adj_type)
    initial = helper.initial()
    propagation = helper.propagation()
    constraint = helper.constraint()
    return initial + "\n" + propagation + "\n" + constraint


def connected_edge(row: int, col: int, color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a constraint to check the reachability of {color} cells from the edge.

    An adjacent rule and a grid fact should be defined first.
    """
    borders = [(r, c) for r in range(row) for c in range(col) if r in [0, row - 1] or c in [0, col - 1]]
    helper = ConnectivityHelper("reachable_edge", "grid", color, adj_type)
    initial = helper.initial(borders, enforce_color=True)
    propagation = helper.propagation()
    constraint = helper.constraint()
    return initial + "\n" + propagation + "\n" + constraint


def connected_parts(color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to get all the connected components of {color} cells.
    Please note that 'reachable/4' is much slower than the 'reachable/2' which only searches for one component.

    An adjacent rule and a grid fact should be defined first.
    """
    helper = ConnectivityHelper("reachable", "grid", color, adj_type)
    initial = helper.initial(full_search=True)
    propagation = helper.propagation(full_search=True)
    return initial + "\n" + propagation


def count_connected_parts(target: int, color: str = "black", adj_type: int = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the number of connected components of {color} cells.

    A reachable rule should be defined first.
    """
    op = rev_op_dict[op]
    tag = tag_encode("reachable", "adj", adj_type, color)
    return f":- grid(R, C), {color}(R, C), #count {{ R1, C1: {tag}(R, C, R1, C1) }} {op} {target}."


def region(
    src_cell: Tuple[int, int],
    exclude_cells: List[Tuple[int, int]] = None,
    color: str = "black",
    adj_type: int = 4,
    avoid_unknown: bool = False,
) -> str:
    """
    Generate a rule to construct a region of {color} cells from a source cell.

    An adjacent rule and a grid fact should be defined first.
    """
    if exclude_cells is None:
        exclude_cells = []
    helper = ConnectivityHelper("region", "grid", color, adj_type)
    initial = helper.initial([src_cell], exclude_cells, full_search=True)
    propagation = helper.propagation(full_search=True)
    constraint = "\n" + helper.constraint(full_search=True) if avoid_unknown else ""
    return initial + "\n" + propagation + constraint


def count_region(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the size of {color} region connected to a source cell.

    A region rule should be defined first.
    """
    op = rev_op_dict[op]
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('region', 'adj', adj_type, color)}({src_r}, {src_c}, R, C) }} {op} {target}."


def lit(src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate a rule to check the cells can be lit up with a source {color} cell.

    An adjacent rule should be defined first.
    """
    r, c = src_cell
    if adj_type == 4:
        lit_constraint = f"(R - {r}) * (C - {c}) == 0"
    elif adj_type == 8:
        lit_constraint = f"(R - {r}) * (C - {c}) * (R - {r} - C + {c}) * (R - {r} + C - {c}) == 0"
    else:
        raise ValueError("Invalid adjacent type, must be one of '4', '8'.")

    helper = ConnectivityHelper("lit", "grid", color, adj_type)
    initial = helper.initial([src_cell], [], full_search=True)
    propagation = helper.propagation([src_cell], full_search=True, extra_constraint=lit_constraint)
    return initial + "\n" + propagation


def count_lit(target: int, src_cell: Tuple[int, int], color: str = "black", adj_type: int = 4, op: str = "eq") -> str:
    """
    Generate a constraint to count the number of {color} cells lit up by a source cell.

    A lit rule should be defined first.
    """
    op = rev_op_dict[op]
    src_r, src_c = src_cell
    return f":- {{ {tag_encode('lit', 'adj', adj_type, color)}({src_r}, {src_c}, R, C) }} {op} {target}."


def reachable_edge() -> str:
    """
    Define edges as numbers on its adjacent grids are different.

    A grid fact and an adjacent edge rule should be defined first.
    """
    initial = "reachable_edge(R, C, R, C) :- grid(R, C).\n"
    propagation = "reachable_edge(R0, C0, R, C) :- grid(R, C), reachable_edge(R0, C0, R1, C1), adj_edge(R, C, R1, C1).\n"
    # edge between two reachable grids is forbidden.
    constraint = ":- reachable_edge(R, C, R, C + 1), vertical_line(R, C + 1).\n"
    constraint += ":- reachable_edge(R, C, R + 1, C), horizontal_line(R + 1, C).\n"
    constraint += ":- reachable_edge(R, C + 1, R, C), vertical_line(R, C + 1).\n"
    constraint += ":- reachable_edge(R + 1, C, R, C), horizontal_line(R + 1, C)."
    return initial + propagation + constraint


def reachable_source_edge(
    src_cell: Tuple[int, int],
    exclude_cells: List[Tuple[int, int]] = None,
) -> str:
    """
    Define edges as numbers on its adjacent grids are different.

    A grid fact and an adjacent edge rule should be defined first.
    """
    r, c = src_cell
    helper = ConnectivityHelper("reachable", "grid", None, "edge")
    tag = helper.get_tag()
    initial = helper.initial([src_cell], exclude_cells, full_search=True)
    propagation = f"{tag}({r}, {c}, R, C) :- grid(R, C), {tag}({r}, {c}, R1, C1), adj_edge(R, C, R1, C1)."

    # edge between two reachable grids is forbidden.
    constraint = f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R, C + 1), vertical_line(R, C + 1).\n"
    constraint += f":- {tag}({r}, {c}, R, C), {tag}({r}, {c}, R + 1, C), horizontal_line(R + 1, C).\n"

    return initial + "\n" + propagation + "\n" + constraint


def split_by_edge() -> str:
    """
    A description of two adjacent cells split by edge.
    """
    constraint = "split_by_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), horizontal_line(R + 1, C).\n"
    constraint += "split_by_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), vertical_line(R, C + 1).\n"
    constraint += "split_by_edge(R, C, R1, C1) :- split_by_edge(R1, C1, R, C)."
    return constraint


def count_reachable_edge(target: int, op: str = "eq", color: str = None) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule should be defined first.
    """
    op = rev_op_dict[op]
    if not color:
        return f":- grid(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."

    return f":- grid(R0, C0), {color}(R0, C0), #count {{ R, C: reachable_edge(R0, C0, R, C) }} {op} {target}."


def count_shape(target: int, name: str, _id: int = None, color: str = "black", _type: str = "grid", op: str = "eq") -> str:
    """
    Generates a constraint to count the number of a shape.

    A grid rule and a shape rule should be defined first.
    """
    tag = tag_encode("shape", name, color)
    op = rev_op_dict[op]
    _id = "_" if _id is None else _id

    if _type == "grid":
        return f":- {{ {tag}(R, C, {_id}, _) }} {op} {target}."

    if _type == "area":
        return f":- area(A, _, _), {{ {tag}(A, R, C, _, {_id}) }} {op} {target}."

    raise ValueError("Invalid type, must be one of 'grid', 'area'.")
