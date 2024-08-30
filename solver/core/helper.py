"""Helper functions for generation solvers and rules."""

import random
from collections import deque
from typing import Any, Dict, Optional, Set, Tuple, Union, Iterator

from .penpa import Direction


def extract_two_symbols(symbol_set: Set[str]) -> Tuple[str, str]:
    """Extract two symbols from a set."""
    if len(symbol_set) == 2:
        symbol_1 = list(symbol_set)[0]
        symbol_2 = list(symbol_set)[1]
    elif len(symbol_set) == 1:
        symbol_1 = list(symbol_set)[0]
        symbol_2 = "circle_M__1__0" if symbol_1 == "circle_M__2__0" else "circle_M__2__0"
    elif len(symbol_set) == 0:
        symbol_1 = "circle_M__1__0"
        symbol_2 = "circle_M__2__0"
    else:
        raise AssertionError("At most two symbols are allowed.")
    return symbol_1, symbol_2


def extract_initial_edges(edges: Set[Tuple[int, int, Direction]], helper_x: Set[Tuple[int, int, Direction]]) -> str:
    """Extract the initial edges to the solver."""
    rule = ""
    for r, c, d in edges:
        if d == Direction.LEFT:
            rule += f"edge_left({r}, {c}).\n"
        elif d == Direction.TOP:
            rule += f"edge_top({r}, {c}).\n"
        elif d == Direction.DIAG_UP:
            rule += f"edge_diag_up({r}, {c}).\n"
        elif d == Direction.DIAG_DOWN:
            rule += f"edge_diag_down({r}, {c}).\n"

    for r, c, d in helper_x:
        if d == Direction.LEFT:
            rule += f"not edge_left({r}, {c}).\n"
        elif d == Direction.TOP:
            rule += f"not edge_top({r}, {c}).\n"

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
    rows: int, cols: int, edges: Set[Tuple[int, int, Direction]], clues: Optional[Dict[Tuple[int, int], Any]] = None
) -> Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]]:
    """Generate a dict of rooms with their unique clue."""
    unexplored_cells = {(r, c) for c in range(cols) for r in range(rows)}
    clue_to_room: Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]] = {}

    def get_neighbors(r: int, c: int) -> Iterator[Tuple[int, int]]:
        """Get the neighbors of a cell."""
        if (r, c, Direction.LEFT) not in edges:
            yield (r, c - 1)

        if (r, c + 1, Direction.LEFT) not in edges:
            yield (r, c + 1)

        if (r, c, Direction.TOP) not in edges:
            yield (r - 1, c)

        if (r + 1, c, Direction.TOP) not in edges:
            yield (r + 1, c)

    def single_bfs(start_cell: Tuple[int, int]) -> Tuple[Union[Tuple[int, int], None], Tuple[Tuple[int, int], ...]]:
        clue_cell = None
        connected_component = {start_cell}
        unexplored_cells.remove(start_cell)

        queue = deque([start_cell])  # make a deque for BFS
        while queue:
            r, c = queue.popleft()
            for neighbor in get_neighbors(r, c):
                if neighbor in unexplored_cells:
                    connected_component.add(neighbor)
                    unexplored_cells.remove(neighbor)
                    queue.append(neighbor)

            if clues and (r, c) in clues:
                clue_cell = (r, c)

        return clue_cell, tuple(connected_component)

    while len(unexplored_cells) != 0:
        start_cell = random.choice(tuple(unexplored_cells))  # get a random start cell
        clue, room = single_bfs(start_cell)
        clue_to_room[room] = clue

    return clue_to_room
