"""The N Cells solver."""

from typing import List

from .core.common import display, edge, grid
from .core.helper import extract_initial_edges, tag_encode
from .core.neighbor import adjacent, count_adjacent_edges
from .core.penpa import Puzzle, Solution
from .core.reachable import grid_branch_color_connected
from .core.solution import solver


def count_reachable_edge(target: int) -> str:
    """
    Generates a constraint for counting grids in a region divided by edges.

    An edge rule and a grid_branch_color_connected rule should be defined first.
    """
    tag = tag_encode("reachable", "grid", "branch", "adj", "edge")

    return f":- grid(R0, C0), #count {{ R, C: {tag}(R0, C0, R, C) }} != {target}."


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.param["region_size"].isdigit(), "Invalid region size."
    size = int(puzzle.param["region_size"])
    assert puzzle.row * puzzle.col % size == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(grid_branch_color_connected(color=None, adj_type="edge"))
    solver.add_program_line(count_reachable_edge(size))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(count_adjacent_edges(num, (r, c)))

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "N Cells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VRNb9pAEL37V0R7nsMOaxuzN5pCL9T9CFUUWVYExG1QjZwaXFWL+O+ZnXXKsuTSQ6Ooqiw/HuO3s29m7dn+6BZtBSgBEVQG9EtXjBnESQpDFfMt+2u+3tWVvoBxt7tvWiIAH6ZT+Lqot1VU9Koy2puRNmMw73QhBgL4RlGC+aT35r02OZgreiQAKTYjhgIGRCdHes3PLbt0QZTE854TvSG6WrerurqduchHXZg5CLvPG15tqdg0PyvhlvH/VbNZrm1gudhRMdv79UP/ZNvdNd+7XovlAczY2Z08Y1cd7Vrq7Fr21+zWD81zRkfl4UAN/0xWb3VhXX850uxIr/SeMNd7EadPNbpTEfHQBuiQfgcyG1BeYBQsSWSwJMEgkLLCW5ImgWIYB7tkvK2nQDkIkqBUZxpOc6LhnbzEKMOSUYY1I7LGjwy4Jj+PCotCFVaF8Zkf1z0/TxI2GBPW+HlcA31NeuYnPetPetofOnLkg79hnDIOGOf0XoBRjG8ZJWPCOGPNhPGa8ZIxZkxZM7Rv1h+9ey9gp1BuhJ1eyb8RK6NCTO6+VRd5024WNc2DvNssq/bpP43eQyR+Cb4LZSf5/2n84tPYNl++tu/itdmhL7WMHgE=",
        },
    ],
    "parameters": {"region_size": {"name": "Region Size", "type": "number", "default": 5}},
}
