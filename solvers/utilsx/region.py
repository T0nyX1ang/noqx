"""Utility for regions."""

import random
from typing import Any, Dict, FrozenSet, Set, Tuple, Union

from .coord import Direction


def full_bfs(
    rows: int, cols: int, borders: Set[Tuple[int, int, Direction]], clues: Dict[Tuple[int, int], Any] = None
) -> Union[Dict[Tuple[int, int], FrozenSet[Tuple[int, int]]], Set[FrozenSet[Tuple[int, int]]]]:
    """
    Given puzzle dimensions (rows, cols), a list of border coordinates,
    and (optionally) a dictionary mapping clue cells to values,

    Returns:
        if clues were provided:
            a dictionary mapping each clue cell to a frozenset of
                the (r, c) coordinates of the room that the clue is in
            (if a room has no clue cells, it gets ignored)
        else:
            a set of frozensets, where each frozenset contains the (r, c)
                coordinates of an entire room
    """
    # initially, all cells are unexplored
    unexplored_cells = {(r, c) for c in range(cols) for r in range(rows)}

    # build a set of rooms
    # (if there are clues, we need this for stranded-edge checks)
    room_set: Set[FrozenSet[Tuple[int, int]]] = set()
    clue_to_room: Dict[Tuple[int, int], FrozenSet[Tuple[int, int]]] = {}

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
        # add the room to the room-set
        room_set.add(room)
        if clue:
            clue_to_room[clue] = room

    def get_room(r: int, c: int) -> FrozenSet[Tuple[int, int]]:
        """Given a cell, return the room that it belongs to."""
        for room in room_set:
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

    return clue_to_room if clues else room_set
