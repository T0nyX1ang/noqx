"""Utility for encoding and decoding puzzle inputs and outputs."""

import json
import urllib.parse
from typing import Any, Dict, List, Set, Tuple, Union

from .border import Direction, get_edge_id_from_border_coord


class Encoding:
    """Encoding of a puzzle."""

    def __init__(
        self,
        rows: int = None,
        cols: int = None,
        clue_cells: Dict[Tuple[int, int], Any] = None,
        params: Dict[str, Any] = None,
        edge_ids: Set[Tuple[int, int, Direction]] = None,
        top_clues: Dict[int, Any] = None,
        right_clues: Dict[int, Any] = None,
        bottom_clues: Dict[int, Any] = None,
        left_clues: Dict[int, Any] = None,
    ):
        """Initialize the encoding of the puzzle."""
        self.R = rows
        self.C = cols
        self.clues = clue_cells
        self.params = params
        self.edges = edge_ids
        self.top = top_clues
        self.right = right_clues
        self.bottom = bottom_clues
        self.left = left_clues


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
    if isinstance(data, str) and data[0] == "s" and data[1:].isnumeric():  # signpost clue
        return data

    raise RuntimeError("Invalid input")


def grid_to_rc(i: int, j: int) -> Tuple[int, int]:
    return i // 2, j // 2


def encode(string: str, has_borders=False) -> Encoding:
    """
    Given a JSON object representing a puzzle,
     - has_params = True iff the puzzle has parameters
     - has_borders = True iff the puzzle has borders / regions
     as part of its input
     - outside_clues = a binary string which specifies the presence
     of outside clues in the perimeter, in a top, right, bottom, left
     ordering, where a 0 represents no border in that location
    """
    json_obj: Dict[str, Any] = json.loads(string)

    # default values
    params, edge_ids, top_clues, right_clues, bottom_clues, left_clues = [None] * 6

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

    # encode extra parameters
    if json_params:
        params = json_params.copy()
        if "r" in params:
            del params["r"]
        if "c" in params:
            del params["c"]
        if "n" in params:
            del params["n"]

    # add outside borders manually, just in case
    if has_borders:
        edge_ids = set()
        for r in range(rows):
            edge_ids.add((r, 0, Direction.LEFT))
            edge_ids.add((r, cols - 1, Direction.RIGHT))
        for c in range(cols):
            edge_ids.add((0, c, Direction.TOP))
            edge_ids.add((rows - 1, c, Direction.BOTTOM))

    # encode clue cells and inner edge ids
    clue_cells = {}
    for i in range(2 * (rows + 1)):
        for j in range(2 * (cols + 1)):
            coord_str = f"{i},{j}"
            if coord_str in json_grid:
                if (i % 2, j % 2) == (1, 1):  # cell coords
                    if i < 2 * rows and j < 2 * cols:
                        clue_cells[grid_to_rc(i, j)] = clue_encoder(json_grid[coord_str])
                else:  # border coords
                    edge_ids.add(get_edge_id_from_border_coord(rows, cols, i, j))

    # encode outside clues
    outside_clue_string = json_properties["outside"]
    if outside_clue_string[0] == "1":
        top_clues = {}
        for j in range(2 * (cols + 1)):
            input_coord_string = f"{-1},{j}"
            if input_coord_string in json_grid:
                top_clues[j // 2] = clue_encoder(json_grid[input_coord_string])

    if outside_clue_string[1] == "1":
        right_clues = {}
        for i in range(2 * (rows + 1)):
            input_coord_string = f"{i},{2 * cols + 1}"
            if input_coord_string in json_grid:
                right_clues[i // 2] = clue_encoder(json_grid[input_coord_string])

    if outside_clue_string[2] == "1":
        bottom_clues = {}
        for j in range(2 * (cols + 1)):
            input_coord_string = f"{2 * rows + 1},{j}"
            if input_coord_string in json_grid:
                bottom_clues[j // 2] = clue_encoder(json_grid[input_coord_string])

    if outside_clue_string[3] == "1":
        left_clues = {}
        for i in range(2 * (rows + 1)):
            input_coord_string = f"{i},{-1}"
            if input_coord_string in json_grid:
                left_clues[i // 2] = clue_encoder(json_grid[input_coord_string])

    return Encoding(rows, cols, clue_cells, params, edge_ids, top_clues, right_clues, bottom_clues, left_clues)


def decode(solutions):
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
