"""The Tetrominous solver."""

from typing import Dict

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class TetrominousSolver(Solver):
    """The Tetrominous solver."""

    name = "Tetrominous"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VNNj9owEL3nV6x8nkNimwC+0S1UlSi0hWpVRREK2WwXFZRtIFVllP/e53HYVFpW/Vh1e6ksj5/f2Mmb8cz+S51VBcUYakAhRRgyjnlGWvMM27HcHLaFuaBRfbgtKwCi+WRCN9l2XwRJeyoNjnZo7IjsK5MIKYhnJFKy78zRvjF2RnYBlyANbgoUCZKA4w5esd+hS09GIfCsxYAfAfNNlW+L1dQzb01ilyTcf17wbQfFrvxaCH+N93m5W28csc4OCGZ/u7lrPfv6uvxci9MvGrIjL3d8Rq7q5Kp7ueq8XPn35Q7TpkHa30PwyiRO+4cODjq4MEchpTCahPKL9kvPLY2TjAPafXUOmf7ZhO474nVHxD1HLDqiz1emPxB8Ynki8OXIHBuXB2cnbCXbJZSRVWxfsg3Z9thO+cyY7RXbS7aabcxn+i62X4zeh/h0OUgSkjIcILoYPeLiVw4rwr7F4F2i1E+lJ1Jy2/nR+3OcBniVurrJ8gJVMr7+VFzMymqXbbGb1bt1UZ32aNImEN8EzwSqUdz/+/bf9K17gvCZ6/ep7ZQgu/elT3ZO4q5eZau8RKkhha3bd8Ojbt8g591Kx7/pQEc+cDx71tDMafAd",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        shaded = len(puzzle.surface)
        fail_false((puzzle.row * puzzle.col - shaded) % 4 == 0, "The grid cannot be divided into 4-ominoes!")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_shapes("omino_4", color="grid"))
        self.add_program_line(avoid_same_omino_adjacent(4, color="grid", adj_type="edge"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        shape_dict: Dict[str, int] = {}
        for i, (o_name, o_shape) in enumerate(OMINOES[4].items()):
            shape_dict[o_name] = i
            self.add_program_line(general_shape("omino_4", i, o_shape, color="grid", adj_type="edge"))

        for (r, c, d, label), shape_name in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(shape_name in shape_dict, f"Shape {shape_name} is not defined!")
            t_be = tag_encode("belong_to_shape", "omino_4", "grid")
            self.add_program_line(f":- not {t_be}({r}, {c}, {shape_dict[str(shape_name)]}, _).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
