"""Utility for regions."""

from .border import Direction, get_edge_id


def is_valid_coord(rows, cols, r, c):
    """
    Given puzzle dimensions (rows, cols), and a specific (r, c) coordinate,

    Returns True iff (r, c) is a valid grid coordinate.
    """
    return 0 <= r < rows and 0 <= c < cols


def full_bfs(rows, cols, borders, clues=None):
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
    room_set = set()
    if clues:
        # build a mapping of (clue cell coordinate): {the entire room}
        clue_to_room = {}

    # --- HELPER METHOD FOR full_bfs---
    def bfs(start_cell):
        # find the clue cell in this room
        clue_cell = None
        # keep track of which cells are in this connected component
        connected_component = {start_cell}

        # the start cell has now been explored
        unexplored_cells.remove(start_cell)

        # bfs!
        frontier = {start_cell}
        while frontier:
            new_frontier = set()
            for r, c in frontier:
                # build a set of coordinates that are not divided by borders
                # (they don't have to be part of the grid;
                # we'll check for membership / validity later)
                neighbors = set()
                if (r, c, Direction.LEFT) not in borders:
                    neighbors.add((r, c - 1))
                if get_edge_id(rows, cols, r, c, Direction.RIGHT) not in borders:
                    neighbors.add((r, c + 1))
                if (r, c, Direction.TOP) not in borders:
                    neighbors.add((r - 1, c))
                if get_edge_id(rows, cols, r, c, Direction.BOTTOM) not in borders:
                    neighbors.add((r + 1, c))
                # find the clue cell
                if clues and (r, c) in clues:
                    clue_cell = (r, c)
                # for each neighbor that is a valid grid cell and not in this
                # connected component:
                for neighbor in neighbors:
                    if neighbor in unexplored_cells:
                        connected_component.add(neighbor)
                        unexplored_cells.remove(neighbor)
                        new_frontier.add(neighbor)
            frontier = new_frontier
        return clue_cell, frozenset(connected_component)

    while len(unexplored_cells) != 0:
        # get a random start cell
        iterator = iter(unexplored_cells)
        start_cell = next(iterator)
        # run bfs on that connected component
        clue, room = bfs(start_cell)
        # add the room to the room-set
        room_set.add(room)
        if clue:
            clue_to_room[clue] = room

    # --- HELPER METHOD FOR FINDING WHICH ROOM A CELL BELONGS TO ---
    def get_room(r, c):
        for room in room_set:
            if (r, c) in room:
                return room

    # check that there are no stranded edges
    for r, c, d in borders:
        if d == Direction.LEFT:
            # if there is a left neighbor
            if is_valid_coord(rows, cols, r, c - 1):
                room = get_room(r, c)
                # make sure it's not in the same room
                if (r, c - 1) in room:
                    raise ValueError("There is a dead-end edge.")
        elif d == Direction.TOP:
            if is_valid_coord(rows, cols, r - 1, c):
                room = get_room(r, c)
                if (r - 1, c) in room:
                    raise ValueError("There is a dead-end edge.")
        elif d == Direction.RIGHT:
            if is_valid_coord(rows, cols, r, c + 1):
                room = get_room(r, c)
                if (r, c + 1) in room:
                    raise ValueError("There is a dead-end edge.")
        elif d == Direction.BOTTOM:
            if is_valid_coord(rows, cols, r + 1, c):
                room = get_room(r, c)
                if (r + 1, c) in room:
                    raise ValueError("There is a dead-end edge.")

    if clues:
        return clue_to_room
    return room_set
