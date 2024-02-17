"""
A script to tranform vars(E) to data.
Usage: add
    print(vars(E))
to a certain solver (i.e., akari.py),
then paste the printed things to `exec_str` and run this script.
Finally, paste the output to a certain data grid in static/noq/data.js.
"""

from enum import Enum

Direction = Enum("Direction", "LEFT TOP RIGHT BOTTOM")


def rcd_to_edge(r, c, d):
    """Given an edge id, returns the border coordinate of the edge."""
    data = {
        Direction.TOP: f"{r*2},{c*2+1}",
        Direction.LEFT: f"{r*2+1},{c*2}",
        Direction.BOTTOM: f"{r*2+2},{c*2+1}",
        Direction.RIGHT: f"{r*2+1},{c*2+2}",
    }
    return data[d]


E = None
exec_str = "E = {'rows': 5, 'r': 5, 'R': 5, 'cols': 6, 'c': 6, 'C': 6, 'clues': {}, 'clue_cells': {}, 'params': {}, 'edge_ids': {(0, 1, <Direction.LEFT: 1>), (4, 5, <Direction.LEFT: 1>), (3, 0, <Direction.TOP: 2>), (0, 5, <Direction.TOP: 2>), (0, 3, <Direction.LEFT: 1>), (1, 3, <Direction.LEFT: 1>), (4, 5, <Direction.RIGHT: 3>), (4, 2, <Direction.TOP: 2>), (2, 5, <Direction.TOP: 2>), (1, 1, <Direction.LEFT: 1>), (3, 2, <Direction.TOP: 2>), (3, 0, <Direction.LEFT: 1>), (0, 5, <Direction.LEFT: 1>), (3, 4, <Direction.TOP: 2>), (0, 5, <Direction.RIGHT: 3>), (1, 5, <Direction.LEFT: 1>), (4, 0, <Direction.LEFT: 1>), (0, 0, <Direction.TOP: 2>), (4, 1, <Direction.BOTTOM: 4>), (4, 2, <Direction.LEFT: 1>), (0, 4, <Direction.TOP: 2>), (0, 2, <Direction.TOP: 2>), (4, 3, <Direction.BOTTOM: 4>), (4, 4, <Direction.LEFT: 1>), (1, 5, <Direction.RIGHT: 3>), (2, 0, <Direction.TOP: 2>), (3, 2, <Direction.LEFT: 1>), (2, 5, <Direction.RIGHT: 3>), (2, 2, <Direction.TOP: 2>), (3, 4, <Direction.LEFT: 1>), (0, 0, <Direction.LEFT: 1>), (4, 5, <Direction.BOTTOM: 4>), (0, 2, <Direction.LEFT: 1>), (1, 0, <Direction.LEFT: 1>), (3, 1, <Direction.TOP: 2>), (1, 4, <Direction.TOP: 2>), (3, 3, <Direction.TOP: 2>), (2, 4, <Direction.TOP: 2>), (4, 3, <Direction.TOP: 2>), (2, 0, <Direction.LEFT: 1>), (2, 2, <Direction.LEFT: 1>), (1, 2, <Direction.LEFT: 1>), (3, 1, <Direction.LEFT: 1>), (3, 5, <Direction.TOP: 2>), (2, 1, <Direction.TOP: 2>), (4, 0, <Direction.BOTTOM: 4>), (4, 1, <Direction.LEFT: 1>), (4, 2, <Direction.BOTTOM: 4>), (0, 1, <Direction.TOP: 2>), (0, 3, <Direction.TOP: 2>), (2, 4, <Direction.LEFT: 1>), (4, 4, <Direction.BOTTOM: 4>), (1, 3, <Direction.TOP: 2>), (2, 3, <Direction.TOP: 2>), (3, 5, <Direction.LEFT: 1>), (3, 5, <Direction.RIGHT: 3>)}, 'edges': {(0, 1, <Direction.LEFT: 1>), (4, 5, <Direction.LEFT: 1>), (3, 0, <Direction.TOP: 2>), (0, 5, <Direction.TOP: 2>), (0, 3, <Direction.LEFT: 1>), (1, 3, <Direction.LEFT: 1>), (4, 5, <Direction.RIGHT: 3>), (4, 2, <Direction.TOP: 2>), (2, 5, <Direction.TOP: 2>), (1, 1, <Direction.LEFT: 1>), (3, 2, <Direction.TOP: 2>), (3, 0, <Direction.LEFT: 1>), (0, 5, <Direction.LEFT: 1>), (3, 4, <Direction.TOP: 2>), (0, 5, <Direction.RIGHT: 3>), (1, 5, <Direction.LEFT: 1>), (4, 0, <Direction.LEFT: 1>), (0, 0, <Direction.TOP: 2>), (4, 1, <Direction.BOTTOM: 4>), (4, 2, <Direction.LEFT: 1>), (0, 4, <Direction.TOP: 2>), (0, 2, <Direction.TOP: 2>), (4, 3, <Direction.BOTTOM: 4>), (4, 4, <Direction.LEFT: 1>), (1, 5, <Direction.RIGHT: 3>), (2, 0, <Direction.TOP: 2>), (3, 2, <Direction.LEFT: 1>), (2, 5, <Direction.RIGHT: 3>), (2, 2, <Direction.TOP: 2>), (3, 4, <Direction.LEFT: 1>), (0, 0, <Direction.LEFT: 1>), (4, 5, <Direction.BOTTOM: 4>), (0, 2, <Direction.LEFT: 1>), (1, 0, <Direction.LEFT: 1>), (3, 1, <Direction.TOP: 2>), (1, 4, <Direction.TOP: 2>), (3, 3, <Direction.TOP: 2>), (2, 4, <Direction.TOP: 2>), (4, 3, <Direction.TOP: 2>), (2, 0, <Direction.LEFT: 1>), (2, 2, <Direction.LEFT: 1>), (1, 2, <Direction.LEFT: 1>), (3, 1, <Direction.LEFT: 1>), (3, 5, <Direction.TOP: 2>), (2, 1, <Direction.TOP: 2>), (4, 0, <Direction.BOTTOM: 4>), (4, 1, <Direction.LEFT: 1>), (4, 2, <Direction.BOTTOM: 4>), (0, 1, <Direction.TOP: 2>), (0, 3, <Direction.TOP: 2>), (2, 4, <Direction.LEFT: 1>), (4, 4, <Direction.BOTTOM: 4>), (1, 3, <Direction.TOP: 2>), (2, 3, <Direction.TOP: 2>), (3, 5, <Direction.LEFT: 1>), (3, 5, <Direction.RIGHT: 3>)}, 'top_clues': {0: 2}, 'top': {0: 2}, 'right_clues': {1: 1, 3: 3}, 'right': {1: 1, 3: 3}, 'bottom_clues': {0: 3, 1: 1, 2: 0}, 'bottom': {0: 3, 1: 1, 2: 0}, 'left_clues': {0: 1, 1: 3, 3: 3}, 'left': {0: 1, 1: 3, 3: 3}}"
for dir, num in zip(["LEFT", "TOP", "RIGHT", "BOTTOM"], [1, 2, 3, 4]):
    exec_str = exec_str.replace(f"<Direction.{dir}: {num}>", f"Direction.{dir}")
exec(exec_str)

# E = {'rows': 5, 'r': 5, 'R': 5, 'cols': 6, 'c': 6, 'C': 6, 'clues': {}, 'clue_cells': {}, 'params': {}, 'edge_ids': {(0, 1, <Direction.LEFT: 1>), (4, 5, <Direction.LEFT: 1>), (3, 0, <Direction.TOP: 2>), (0, 5, <Direction.TOP: 2>), (0, 3, <Direction.LEFT: 1>), (1, 3, <Direction.LEFT: 1>), (4, 5, <Direction.RIGHT: 3>), (4, 2, <Direction.TOP: 2>), (2, 5, <Direction.TOP: 2>), (1, 1, <Direction.LEFT: 1>), (3, 2, <Direction.TOP: 2>), (3, 0, <Direction.LEFT: 1>), (0, 5, <Direction.LEFT: 1>), (3, 4, <Direction.TOP: 2>), (0, 5, <Direction.RIGHT: 3>), (1, 5, <Direction.LEFT: 1>), (4, 0, <Direction.LEFT: 1>), (0, 0, <Direction.TOP: 2>), (4, 1, <Direction.BOTTOM: 4>), (4, 2, <Direction.LEFT: 1>), (0, 4, <Direction.TOP: 2>), (0, 2, <Direction.TOP: 2>), (4, 3, <Direction.BOTTOM: 4>), (4, 4, <Direction.LEFT: 1>), (1, 5, <Direction.RIGHT: 3>), (2, 0, <Direction.TOP: 2>), (3, 2, <Direction.LEFT: 1>), (2, 5, <Direction.RIGHT: 3>), (2, 2, <Direction.TOP: 2>), (3, 4, <Direction.LEFT: 1>), (0, 0, <Direction.LEFT: 1>), (4, 5, <Direction.BOTTOM: 4>), (0, 2, <Direction.LEFT: 1>), (1, 0, <Direction.LEFT: 1>), (3, 1, <Direction.TOP: 2>), (1, 4, <Direction.TOP: 2>), (3, 3, <Direction.TOP: 2>), (2, 4, <Direction.TOP: 2>), (4, 3, <Direction.TOP: 2>), (2, 0, <Direction.LEFT: 1>), (2, 2, <Direction.LEFT: 1>), (1, 2, <Direction.LEFT: 1>), (3, 1, <Direction.LEFT: 1>), (3, 5, <Direction.TOP: 2>), (2, 1, <Direction.TOP: 2>), (4, 0, <Direction.BOTTOM: 4>), (4, 1, <Direction.LEFT: 1>), (4, 2, <Direction.BOTTOM: 4>), (0, 1, <Direction.TOP: 2>), (0, 3, <Direction.TOP: 2>), (2, 4, <Direction.LEFT: 1>), (4, 4, <Direction.BOTTOM: 4>), (1, 3, <Direction.TOP: 2>), (2, 3, <Direction.TOP: 2>), (3, 5, <Direction.LEFT: 1>), (3, 5, <Direction.RIGHT: 3>)}, 'edges': {(0, 1, <Direction.LEFT: 1>), (4, 5, <Direction.LEFT: 1>), (3, 0, <Direction.TOP: 2>), (0, 5, <Direction.TOP: 2>), (0, 3, <Direction.LEFT: 1>), (1, 3, <Direction.LEFT: 1>), (4, 5, <Direction.RIGHT: 3>), (4, 2, <Direction.TOP: 2>), (2, 5, <Direction.TOP: 2>), (1, 1, <Direction.LEFT: 1>), (3, 2, <Direction.TOP: 2>), (3, 0, <Direction.LEFT: 1>), (0, 5, <Direction.LEFT: 1>), (3, 4, <Direction.TOP: 2>), (0, 5, <Direction.RIGHT: 3>), (1, 5, <Direction.LEFT: 1>), (4, 0, <Direction.LEFT: 1>), (0, 0, <Direction.TOP: 2>), (4, 1, <Direction.BOTTOM: 4>), (4, 2, <Direction.LEFT: 1>), (0, 4, <Direction.TOP: 2>), (0, 2, <Direction.TOP: 2>), (4, 3, <Direction.BOTTOM: 4>), (4, 4, <Direction.LEFT: 1>), (1, 5, <Direction.RIGHT: 3>), (2, 0, <Direction.TOP: 2>), (3, 2, <Direction.LEFT: 1>), (2, 5, <Direction.RIGHT: 3>), (2, 2, <Direction.TOP: 2>), (3, 4, <Direction.LEFT: 1>), (0, 0, <Direction.LEFT: 1>), (4, 5, <Direction.BOTTOM: 4>), (0, 2, <Direction.LEFT: 1>), (1, 0, <Direction.LEFT: 1>), (3, 1, <Direction.TOP: 2>), (1, 4, <Direction.TOP: 2>), (3, 3, <Direction.TOP: 2>), (2, 4, <Direction.TOP: 2>), (4, 3, <Direction.TOP: 2>), (2, 0, <Direction.LEFT: 1>), (2, 2, <Direction.LEFT: 1>), (1, 2, <Direction.LEFT: 1>), (3, 1, <Direction.LEFT: 1>), (3, 5, <Direction.TOP: 2>), (2, 1, <Direction.TOP: 2>), (4, 0, <Direction.BOTTOM: 4>), (4, 1, <Direction.LEFT: 1>), (4, 2, <Direction.BOTTOM: 4>), (0, 1, <Direction.TOP: 2>), (0, 3, <Direction.TOP: 2>), (2, 4, <Direction.LEFT: 1>), (4, 4, <Direction.BOTTOM: 4>), (1, 3, <Direction.TOP: 2>), (2, 3, <Direction.TOP: 2>), (3, 5, <Direction.LEFT: 1>), (3, 5, <Direction.RIGHT: 3>)}, 'top_clues': {0: 2}, 'top': {0: 2}, 'right_clues': {1: 1, 3: 3}, 'right': {1: 1, 3: 3}, 'bottom_clues': {0: 3, 1: 1, 2: 0}, 'bottom': {0: 3, 1: 1, 2: 0}, 'left_clues': {0: 1, 1: 3, 3: 3}, 'left': {0: 1, 1: 3, 3: 3}}
res = []
# cell
for (r, c), clue in E["clues"].items():
    if not isinstance(clue, list):
        clue = f'"{clue}"'
    res.append(f'"{r*2+1},{c*2+1}": {clue}')

# border
for r, c, d in E["edge_ids"]:
    res.append(f'"{rcd_to_edge(r, c, d)}": "black"')

# left, top, right, bottom
for key in ["left", "top", "right", "bottom"]:
    if not key in E:
        continue
    clues = E[key]
    for x, clue in clues.items():
        if not isinstance(clue, list):
            clue = f'"{clue}"'
        if key in ["left", "right"]:
            r = x
            c = -1 if key == "left" else E["C"]
        else:
            c = x
            r = -1 if key == "top" else E["R"]
        res.append(f'"{r*2+1},{c*2+1}": {clue}')

print(", ".join(res))
