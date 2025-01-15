"""Helper functions for generation solvers and rules."""

import random
from collections import deque
from typing import Dict, Iterable, Iterator, Optional, Tuple, Union

from noqx.puzzle import Direction, Point


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


def validate_type(_type: Optional[Union[int, str]], target_type: Union[int, str, Iterable[Union[int, str]]]):
    """Validate any matching type."""
    if _type is None:
        raise ValueError("Type cannot be 'None'.")

    if isinstance(target_type, (int, str)) and _type != target_type:
        raise ValueError(f"Invalid type '{_type}'.")

    if not isinstance(target_type, (int, str)) and _type not in target_type:
        raise ValueError(f"Invalid type '{_type}'.")


def validate_direction(r: int, c: int, d: Optional[Direction], target: Direction = Direction.CENTER):
    """Validate the direction of any element."""
    if d != target:
        raise ValueError(f"The element in ({r}, {c}) should be placed in the {target.value}.")


def fail_false(express: bool, msg: str):
    """Raise error if the expression is false. Works like an assertion in the background."""
    if express is False:
        raise ValueError(msg)


def full_bfs(
    rows: int,
    cols: int,
    edges: Dict[Point, bool],
    clues: Optional[Dict[Point, Union[int, str]]] = None,
) -> Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]]:
    """Generate a dict of rooms with their unique clue."""
    unexplored_cells = {(r, c) for c in range(cols) for r in range(rows)}
    clue_to_room: Dict[Tuple[Tuple[int, int], ...], Optional[Tuple[int, int]]] = {}
    rc_set = {(r, c) for (r, c, _, _) in clues} if clues else set()

    def get_neighbors(r: int, c: int) -> Iterator[Tuple[int, int]]:
        """Get the neighbors of a cell."""
        if edges.get(Point(r, c, Direction.LEFT)) is not True:
            yield (r, c - 1)

        if edges.get(Point(r, c + 1, Direction.LEFT)) is not True:
            yield (r, c + 1)

        if edges.get(Point(r, c, Direction.TOP)) is not True:
            yield (r - 1, c)

        if edges.get(Point(r + 1, c, Direction.TOP)) is not True:
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

            if clues and (r, c) in rc_set:
                clue_cell = (r, c)

        return clue_cell, tuple(connected_component)

    while len(unexplored_cells) != 0:
        start_cell = random.choice(tuple(unexplored_cells))  # get a random start cell
        clue, room = single_bfs(start_cell)
        clue_to_room[room] = clue

    return clue_to_room
