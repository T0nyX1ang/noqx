"""Helper functions for generation solvers and rules."""

import random
from collections import deque
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, Optional, Set, Tuple, Union


class Direction(Enum):
    """Enumeration for directions."""

    LEFT = "left"
    TOP = "top"
    DIAG_UP = "diag_up"
    DIAG_DOWN = "diag_down"


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


def validate_type(_type: Union[int, str], target_type: Iterable[Union[int, str]]) -> None:
    """Validate any matching type."""
    assert _type in target_type, f"Invalid type '{_type}'."


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
