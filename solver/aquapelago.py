"""The Aquapelago solver."""

from typing import List

from .core.common import display, grid, shade_c
from .core.neighbor import adjacent, avoid_adjacent_color
from .core.penpa import Puzzle, Solution
from .core.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected
from .core.shape import avoid_rect
from .core.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(shade_c(color="black"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="x"))
    solver.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
    solver.add_program_line(avoid_rect(2, 2, color="not black"))
    solver.add_program_line(grid_color_connected(color="not black", adj_type=4, grid_size=(puzzle.row, puzzle.col)))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue must be an integer."
        solver.add_program_line(grid_src_color_connected((r, c), color="black", adj_type="x"))
        solver.add_program_line(count_reachable_src(num, (r, c), color="black", adj_type="x"))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"black({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not black({r}, {c}).")

    solver.add_program_line(display(item="black"))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Aquapelago",
    "category": "shade",
    "examples": [
        {
            "data": "m=edit&p=7VVRa9swEH73ryj3rAfLlh1bb13X7CXz1iWjFGGKk7nU1Jk7Jx5DIf+9dyetrqGDwWArozj67vLdSfpOEtLu21D1tZAp/eJMhELil6qUW5Ll3EL/rZp9W+sTcTrsb7seHSE+zOfipmp3dWB8VhkcbK7thbDvtAEJAiJsEkphL/TBvte2EHaJIRAKuYVLitA9H91LjpN35kgZol84n7pdobtp+k1bXy8wisxHbexKAM3zhnuTC9vuew1eB/3fdNt1Q8S62mMxu9vm3kd2w5fubvC5sjwKe8pyfZefmmkqrzkeNZPrNJP3jGYq5c81t/fdc2rz8njEVf+Eeq+1IemfRzcb3aU+gIpAKwFqxiZJ2GQpm1yykdIF5cxFZR6zjUKXFkXK2cyNFYeZs9LlxcrF48THExoP5y/8/CiattGdCpbi9tUTJGpCkDwDaiRIqIHZSLDkSR8Wb+jsPTJUBuY8obiiqRoubtKPyzQQjwwXPGWo9Mn8vAiTcXg5DCRPGVb9OA4ukdQHxCvGOWPEuMIdFDZmfMsYMiaMC845Z7xkPGNUjCnnzOgM/OYpcXv1F+QYFfGN8+sveY3/z/EyMLAc+ptqU+PNVgzbdd2fFF2/rVrAl+QYwA/gZmJMV6+Py795XGgHwpd2ebw0OXidwdehb+6qdQ1l8AA=",
        }
    ],
}
