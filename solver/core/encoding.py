"""Utility for encoding and decoding puzzle inputs and outputs."""

import json
import urllib.parse
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

Direction = Enum("Direction", "LEFT TOP")


def rcd_to_elt(r: int, c: int, d: Optional[Direction] = None) -> str:
    """Convert row, column and direction (if has) to compatible elt ID."""
    if d is None:
        return f"{r * 2 + 1},{c * 2 + 1}"

    data = {
        Direction.TOP: f"{r * 2},{c * 2 + 1}",
        Direction.LEFT: f"{r * 2 + 1},{c * 2}",
    }
    return data[d]


def elt_to_rcd(coord: str) -> Tuple[int, int, Union[None, Direction]]:
    """Convert grid coordinates to row and column."""
    gr, gc = map(int, coord.split(","))
    r, c = gr // 2, gc // 2

    if gr % 2 == 1 and gc % 2 == 1:  # coordinate case
        return r, c, None

    if gr % 2 == 0 and gc % 2 == 1:  # horizontal border case
        return r, c, Direction.TOP  # bottom border will be ignored

    if gr % 2 == 1 and gc % 2 == 0:  # vertical border case
        return r, c, Direction.LEFT  # right border will be ignored

    raise ValueError("Invalid coordinate!")


def tag_encode(name: str, *data: Union[str, int, None]) -> str:
    """Encode a valid tag predicate without spaces or hyphens."""
    tag_data = [name]
    for d in data:  # recommended data sequence: *_type, src_r, src_c, color
        if d is not None:
            tag_data.append(str(d).replace("-", "_").replace(" ", "_"))

    return "_".join(tag_data)


def reverse_op(op: str) -> str:
    """Return the reverse of the given operator."""
    op_rev_dict = {"eq": "!=", "ge": "<", "gt": "<=", "le": ">", "lt": ">=", "ne": "="}
    return op_rev_dict[op]


def target_encode(target: Union[int, Tuple[str, int]]) -> Tuple[str, int]:
    """Encode a target number for comparison."""
    if isinstance(target, int):
        return ("!=", target)

    return (reverse_op(target[0]), target[1])


class Encoding:
    """Encoding of a puzzle."""

    def __init__(
        self,
        rows: int,
        cols: int,
        clue_cells: Dict[Tuple[int, int], Any],
        params: Optional[Dict[str, Any]] = None,
        edge_ids: Optional[Set[Tuple[int, int, Direction]]] = None,
        top_clues: Optional[Dict[int, Any]] = None,
        right_clues: Optional[Dict[int, Any]] = None,
        bottom_clues: Optional[Dict[int, Any]] = None,
        left_clues: Optional[Dict[int, Any]] = None,
    ):
        """Initialize the encoding of the puzzle."""
        self.R = rows
        self.C = cols
        self.clues = clue_cells
        self.params = params if params else {}
        self.edges = edge_ids if edge_ids else set()
        self.top = top_clues if top_clues else {}
        self.right = right_clues if right_clues else {}
        self.bottom = bottom_clues if bottom_clues else {}
        self.left = left_clues if left_clues else {}


def unquote_plus(value: Union[str, List, Any]) -> Union[str, List, Any]:
    """Unquote a string or a list of strings."""
    if isinstance(value, list):
        return [unquote_plus(x) for x in value]
    elif isinstance(value, str):
        return urllib.parse.unquote_plus(value)
    else:
        return value


def clue_encoder(data: Union[str, List, Any]) -> Union[str, List, Any]:
    """
    If 'data' is a number, return its int value.
    If 'data' is '?' or '' or a color name or a single letter, return data.
    Otherwise, raise an error.
    """
    data = unquote_plus(data)

    if isinstance(data, list):  # list
        return data
    if data.isnumeric():  # numbers
        return int(data)
    if data in ["?", "", "+", "-", "|"]:  # valid clue symbol
        return data
    if data in ["black", "gray", "blue", "green", "yellow", "red"]:  # valid color name
        return data
    if data.isalpha() and len(data) == 1:  # single letter
        return data
    if data[0] == "s" and data[1:].isnumeric():  # signpost clue
        return data

    raise RuntimeError("Invalid input")


def encode(string: str) -> Encoding:
    """Parse a JSON object and encode a puzzle."""
    json_obj: Dict[str, Any] = json.loads(string)

    # default values
    edge_ids, top_clues, right_clues, bottom_clues, left_clues = set(), {}, {}, {}, {}

    json_grid: Dict[str, Any] = json_obj["grid"]
    json_params: Dict[str, Any] = json_obj["param_values"]
    json_properties: Dict[str, Any] = json_obj["properties"]

    # encode grid dimensions
    if "r" in json_params and "c" in json_params:
        rows, cols = int(json_params["r"]), int(json_params["c"])
    elif "n" in json_params:
        rows, cols = int(json_params["n"]), int(json_params["n"])
    else:  # sudoku (8/10/2020)
        rows, cols = 9, 9

    # add outside borders manually, just in case
    if json_properties["border"]:
        for r in range(rows):
            edge_ids.add((r, 0, Direction.LEFT))
            edge_ids.add((r, cols, Direction.LEFT))
        for c in range(cols):
            edge_ids.add((0, c, Direction.TOP))
            edge_ids.add((rows, c, Direction.TOP))

    # encode every clue cells and edge ids from the input
    clue_cells = {}
    for coord_str in json_grid.keys():
        r, c, d = elt_to_rcd(coord_str)
        if d is None:
            if r < 0:
                top_clues[c] = clue_encoder(json_grid[coord_str])
            elif r >= rows:
                bottom_clues[c] = clue_encoder(json_grid[coord_str])
            elif c < 0:
                left_clues[r] = clue_encoder(json_grid[coord_str])
            elif c >= cols:
                right_clues[r] = clue_encoder(json_grid[coord_str])
            else:
                clue_cells[(r, c)] = clue_encoder(json_grid[coord_str])
        else:
            if 0 <= r < rows and 0 <= c < cols:
                edge_ids.add((r, c, d))  # ignore borders outside the grid

    return Encoding(rows, cols, clue_cells, json_params, edge_ids, top_clues, right_clues, bottom_clues, left_clues)


def decode(solutions: List[Dict[str, str]]) -> str:
    """
    Given a list of solutions,
    Return a string of the format:
        {
            (solution #): (solution),
            'num_solutions': (# of solutions),
        }.
    """
    solution_str = "{"
    for i, solution in enumerate(solutions):
        solution_str += f'"{i+1}":{json.dumps(solution)},'
    solution_str += f'"num_solutions":{len(solutions)}'
    solution_str += "}"
    return solution_str
