"""Helper functions for generation solvers and rules."""

import random
from typing import Any, Dict, FrozenSet, Optional, Set, Tuple, Union

from .penpa import Direction


def mark_and_extract_clues(
    original_clues: Dict[Tuple[int, int], Any],
    shaded_color: str = "black",
    safe_color: str = "green",
) -> Tuple[Dict[Tuple[int, int], int], str]:
    """
    Mark clues to the solver and extract the clues that are not color-relevant.

    Recommended to use it before performing a bfs on a grid. (deprecation warning)
    """
    clues = {}  # remove color-relevant clues here
    rule = ""
    for (r, c), clue in original_clues.items():
        if isinstance(clue, list):
            if clue[1] == shaded_color:
                rule += f"{shaded_color}({r}, {c}).\n"
            elif clue[1] == safe_color:
                rule += f"not {shaded_color}({r}, {c}).\n"
            clues[(r, c)] = int(clue[0])
        elif clue == shaded_color:
            rule += f"{shaded_color}({r}, {c}).\n"
        elif clue == safe_color:
            rule += f"not {shaded_color}({r}, {c}).\n"
        else:
            clues[(r, c)] = int(clue)
    return clues, rule.strip()


def extract_two_symbols(symbol_set: Set[str]) -> Tuple[str, str]:
    """Extract two symbols from a set."""
    if len(symbol_set) == 2:
        symbol_1 = list(symbol_set)[0]
        symbol_2 = list(symbol_set)[1]
    elif len(symbol_set) == 1:
        symbol_1 = list(symbol_set)[0]
        symbol_2 = "circle_M__1" if symbol_1 == "circle_M__2" else "circle_M__2"
    elif len(symbol_set) == 0:
        symbol_1 = "circle_M__1"
        symbol_2 = "circle_M__2"
    else:
        raise ValueError("At most two symbols are allowed.")
    return symbol_1, symbol_2


def extract_initial_edges(edges: Set[Tuple[int, int, Direction]]) -> str:
    """Extract the initial edges to the solver."""
    rule = ""
    for r, c, d in edges:
        if d == Direction.LEFT:
            rule += f"vertical_line({r}, {c}).\n"
        elif d == Direction.TOP:
            rule += f"horizontal_line({r}, {c}).\n"
    return rule.strip()


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


def full_bfs(
    rows: int, cols: int, borders: Set[Tuple[int, int, Direction]], clues: Optional[Dict[Tuple[int, int], Any]] = None
) -> Dict[FrozenSet[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """
    Given puzzle dimensions (rows, cols), a list of border coordinates,
    and (optionally) a dictionary mapping clue cells to values,

    Returns:
            a dictionary mapping a frozenset of the (r, c) coordinates of the room
            to the clue cell in that room (if a room has no clue cells, it gets ignored).
    """
    # initially, all cells are unexplored
    unexplored_cells = {(r, c) for c in range(cols) for r in range(rows)}

    # build a set of rooms
    # (if there are clues, we need this for stranded-edge checks)
    clue_to_room: Dict[FrozenSet[Tuple[int, int]], Optional[Tuple[int, int]]] = {}

    # --- HELPER METHOD FOR full_bfs---
    def bfs(start_cell: Tuple[int, int]) -> Tuple[Union[Tuple[int, int], None], FrozenSet[Tuple[int, int]]]:
        # find the clue cell in this room
        clue_cell = None
        # keep track of which cells are in this grid_color_connected component
        connected_component = {start_cell}

        # the start cell has now been explored
        unexplored_cells.remove(start_cell)

        # bfs!
        frontier = {start_cell}
        while frontier:
            new_frontier = set()
            for r, c in frontier:
                # build a set of coordinates that are not divided by borders
                neighbors = set()
                if (r, c, Direction.LEFT) not in borders:
                    neighbors.add((r, c - 1))

                if (r, c + 1, Direction.LEFT) not in borders:
                    neighbors.add((r, c + 1))

                if (r, c, Direction.TOP) not in borders:
                    neighbors.add((r - 1, c))

                if (r + 1, c, Direction.TOP) not in borders:
                    neighbors.add((r + 1, c))

                # for each neighbor that is a valid grid cell and not in this grid_color_connected component
                for neighbor in neighbors:
                    if neighbor in unexplored_cells:
                        connected_component.add(neighbor)
                        unexplored_cells.remove(neighbor)
                        new_frontier.add(neighbor)

                # find the clue cell
                if clues and (r, c) in clues:
                    clue_cell = (r, c)

            frontier = new_frontier
        return clue_cell, frozenset(connected_component)

    while len(unexplored_cells) != 0:
        # get a random start cell
        start_cell = random.choice(tuple(unexplored_cells))
        # run bfs on that grid_color_connected component
        clue, room = bfs(start_cell)
        clue_to_room[room] = clue

    def get_room(r: int, c: int) -> FrozenSet[Tuple[int, int]]:
        """Given a cell, return the room that it belongs to."""
        for room in clue_to_room:
            if (r, c) in room:
                return room

        raise ValueError("Cell not found in any room.")

    # check that there are no stranded edges
    for r, c, d in borders:
        if d == Direction.LEFT and c < cols:
            room = get_room(r, c)
            if (r, c - 1) in room:
                raise ValueError("There is a dead-end edge.")
        elif d == Direction.TOP and r < rows:
            room = get_room(r, c)
            if (r - 1, c) in room:
                raise ValueError("There is a dead-end edge.")

    return clue_to_room
