"""The N Cells solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import extract_initial_edges
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    assert puzzle.row * puzzle.col % 5 == 0, "It's impossible to divide grid into regions of this size!"

    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(edge(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent(_type="edge"))
    solver.add_program_line(extract_initial_edges(puzzle.edge, puzzle.helper_x))

    for i, o_shape in enumerate(OMINOES[5].values()):
        solver.add_program_line(general_shape("omino_5", i, o_shape, color="grid", adj_type="edge"))

    solver.add_program_line(all_shapes("omino_5", color="grid"))
    solver.add_program_line(count_shape(target=puzzle.row * puzzle.col // 5, name="omino_5", color="grid"))

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(count_adjacent_edges(num, (r, c)))

    solver.add_program_line(display(item="edge_left", size=2))
    solver.add_program_line(display(item="edge_top", size=2))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "FiveCells",
    "category": "region",
    "examples": [
        {
            "data": "m=edit&p=7VZLb9swDL7nVxQ662DSdmz5lnXZLpn3aIeiMIwiSb01WAJ3eQyDg/z3UlSyKFR32GFFDoUjgv5ESh8fUrz6uRkvGw2p/cW5jjTQ049yHpDTO43Dcz1bz5viQg8264d2SYrWH0v9bTxfNb1qb1T3tp0puoHu3heVQqV5gKp197nYdh+KrtTdFU0pDYSNSAOlkdThUb3heatdOhAi0su9TuotqdPZcjpv7kYO+VRU3bVWdp837G1VtWh/Ncq58fu0XUxmFpiM1xTL6mH2uJ9Zbe7bH5u9LdQ73Q0c3eEzdOMjXas6ulb7b3Tnj+1zRE2921HCvxDVu6KyrL8e1fyoXhVbkmWxVf3oEKOriuqDBahIfwCUQGyB2AMSC0QekEqLvtwlkxa5tDDCImOmHo9MMs0k04zX8ADDLt6ihrf1LABkQgAkV0Be17eJZYCQBOskvPkJwoT9lRPOrc8n4eSeIMzZ90plviGV2YOgauBq4PPJeC/fJgvykzNnr9iQc+y+lwn2MjKHGMlSYMRReHshyPwgyDyjq86Jl2wlBNkHiLKZEGXsGAcMXXW82DHldXzEHRffK+hkzGXnYi5rinnA2QScXTv7kRp5BDCoBRp5XNHI/kET5DmsoDs7JzYy0jg65UyXDvDVc8vyHUtkeU03k+5ilm9ZRixTliO2GbK8YXnJMmHZZ5vM3m3/dPu9AJ0qcf+hf3von/Z19rxn616lhvffm4uyXS7Gc/rfLTeLSbM8vNMnzq6nfiseVUwuyetXz4t/9djkR+d2+s+NDt1Hde8J",
        },
    ],
}
