"""The Nanro solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, count, display, fill_num, grid
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import avoid_rect
from noqx.solution import solver


def nanro_fill_constraint(color: str = "black") -> str:
    """Generate a constraint for the number filling in nanro."""
    return f":- number(R0, C0, N), area(A, R0, C0), #count {{ R, C : area(A, R, C), {color}(R, C) }} != N."


def nanro_avoid_adjacent() -> str:
    """Generate a rule to avoid adjacent cells with the same number."""
    area_adj = area_adjacent()
    area_adj = area_adj[area_adj.find(":-") : -1]
    return f"{area_adj}, number(R, C, N), number(R1, C1, N)."


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(adjacent())
    solver.add_program_line(grid_color_connected(color="not gray"))
    solver.add_program_line(avoid_rect(2, 2, color="not gray"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.sudoku)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i, color="gray"))

        if rc:
            data = puzzle.sudoku[rc].get(0)
            assert isinstance(data, int), "Signpost clue should be integer."
            solver.add_program_line(count(data, color="not gray", _type="area", _id=i))
        else:
            solver.add_program_line(count(("gt", 0), color="not gray", _type="area", _id=i))

    for (r, c), color_code in puzzle.surface.items():
        if color_code in [1, 3, 4, 8]:  # shaded color (DG, GR, LG, BK)
            solver.add_program_line(f"gray({r}, {c}).")
        else:  # safe color (others)
            solver.add_program_line(f"not gray({r}, {c}).")

    for (r, c), num in puzzle.text.items():
        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    solver.add_program_line(nanro_fill_constraint(color="not gray"))
    solver.add_program_line(nanro_avoid_adjacent())
    solver.add_program_line(display(item="gray", size=2))
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Nanro",
    "category": "num",
    "examples": [
        {
            "url": "https://puzz.link/p?nanro/11/11/9bdcljmcpj6cpj6dpl6mqi46tt8qpltbdmqnljb2nnc4i3g2l23l2n2n2n2n2i3i2n3n3n3n2l43l2g3i",
            "test": False,
        },
        {
            "data": "m=edit&p=7VdNbxs3FLzrVwR75oHk46dubmr34rofdhEEghDYjtIYteFWtopiDf/3zCOHshO0yKEIWhSFpOW8WS75Pobk6u633fl2Y5zTrxRjDZAJMbWfc779LD9nV/fXm+ULc7C7f3+7BTDmu6Mj8+78+m6zWLHXevEw1+V8YOZvlqvJTWby7bc28w/Lh/nb5XS3e3v7y24y8yk6TMbhznHv6gEPn+Crdl/Ry046C3wCLP2x14CXV9vL682b497x++VqPjOTzvZVe1rhdHP7+2aiN2pf3t5cXClxcX6PkO7eX/3KO/SN060fzXzQnJ4P/8RdeXJXYXdX0afuMp4v7G5dPz4i+T/C4TfLlfr+0xM8XT7gerJ8mILX/ppBg6f0ngPrbCnKxxbh5FB3NcMwYzP3d/NHd71LY8xmFvvcFN9GbglVM7S741kJQU2IpJu1DTXuxu7GmDc9exaOv25BHbWrb9czRGtmadev29W2a2zX49bnEOH64IzXTHhoM3hgIRZgeNRwAI7EERiuNZyAM3EGRnwNF+BKXI2PcFZxtMCOGPNqLhvGvInjJIxTyBfwlXzNRjQHwGiN+M6jNUL/0RqJ5CN4LY7iDL6QL9kE23m0JrjOB4elvscRuMcYXADusQcnwD0nAT7AJsZWQd+Cs8A9xmArcI892IJ5e06CVR96roLFvJa+VYxjmduM/BTikozYPiZa5KHzaI0IeQHPuqA1ksgn8Jl8Bl/JV8RFf6QK+B6XVOSq9rgkI4eVOUzgM/1ErWFzXvDUgDjwMmqEuZhPQZ4H9sg/bMaI+rIuDWdqL0N7mdrL0F6m9jK0x1jQAg/N6LMDI2/0zSfojXnwETpMQ4fQZ6Q+oRPYxBiT+mmaH31U2/sxVav0M8HPRD8T+if6meBnop+q84ETxi/0p4DXJd60rbliXfT88ayXB7/XOXBgH6xZiewDnyWTh2aEmkGL+g4dqj6pZwt9Di1V6NP2nEgtqPXQg9a95wTbEPDQZwTm+NAPbNYC+cnMYUZuM/OWkXPdAlu8qMXor+NwXaBFjJ1HixjJB/CRfASfyWfw+3iBC/sU+LPH0HOhnrGHwCbW/FCf8Ac2x6nAY3zkgf4L6gv7Sf+su2B/22NBH+574sALeQveMScFvKVmgH1hfgryU5mfqvmhNrAPeK67ltuBsTY91yZaYGpPazHWMvYc8YzdgxfyAj6Sj+DTiFFjJ580rsHrGh+x635CDUDbsIl1HOYc+zxszgWe+3/Lj5B36DOwRR83fFb/OY7F+NwD0QKPPUT3DeZT9ytitIiXOfc6F3m8xEkkj/PlIzxiwdqETax6G3spfOCZJR680Df13z/jPft7XbMcx+vZNPwBFs4lulePtYz+whiVH2einsVc120vos7budz2JRzar9rR/bJdQ7umdqTndi3jReevX4D2XZ69C/V3n7/zIvEZzx4XKxwU+k796Sf+d9n1YjWd7rbvzi83eE09fPvz5sXJ7fbm/BrWye7mYrN9sk/bC+yw8d/hcTH9MbXfSqtvnPz/h+If/UOhpbCf/1vxxZfSv3mRQ7Wr9eID"
        },
    ],
}
