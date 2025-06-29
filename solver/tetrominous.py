"""The Tetrominous solver."""

from typing import Dict

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def avoid_adj_same_omino(omino_num: int = 4, color: str = "grid") -> str:
    """
    Generates a constraint to avoid adjacent ominos with the same type.

    An split by edge rule, an omino rule should be defined first.
    """
    t_be = tag_encode("belong_to_shape", f"omino_{omino_num}", color)
    constraint = "split_by_edge(R, C, R + 1, C) :- grid(R, C), grid(R + 1, C), edge_top(R + 1, C).\n"
    constraint += "split_by_edge(R, C, R, C + 1) :- grid(R, C), grid(R, C + 1), edge_left(R, C + 1).\n"
    constraint += "split_by_edge(R, C, R1, C1) :- split_by_edge(R1, C1, R, C).\n"
    constraint += f":- grid(R, C), grid(R1, C1), {t_be}(R, C, T, _), {t_be}(R1, C1, T, _), split_by_edge(R, C, R1, C1)."
    return constraint


class TetrominousSolver(Solver):
    """The Tetrominous solver."""

    name = "Tetrominous"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VNNj9owEL3nV6x8nkM+TADf6BaqSjS0hWq1iiIUstkuKijbQKrKiP/Om3FoDqXqx6rbS2X5+XlmnLwZe3afm7wuKcaIBuRTgBHGscxAa5l+Oxbr/aY0VzRq9g9VDUI0m0zoPt/sSi9tozLvYIfGjsi+MqkKFckMVEb2nTnYN8YmZOdwKdKwTcECRSHouKM34md27YyBD560HPQWtFjXxaZcTp3lrUntghT/54WcZqq21ZdSuWOyL6rtas2GVb5HMruH9WPr2TV31aemjQ2yI9mRkzu+IDfq5DJ1cpldkMtZ/GW5w+x4RNnfQ/DSpKz9Q0cHHZ2bgwpDZTSpyC3aLT1eEJBwgOavziDTXZvSfTa87gxxjw3zztCXI5zZ2SARi7MBXw7MAXgrOBEMBRdQRjYSfCnoC/YEpxIzFrwRvBbUgrHE9Dm3X8zepfh0OSgSijIcILsYPcL5R8wjwr7lsHOhop9KT8NQ2s6N3p/zzMOtNPV9XpR4JeO7j+VVUtXbfINd0mxXZX3eo0mPnvqqZKZQjcf9v2//Td/yFfjP/H6f2k4pqvvt6ZOdkXpslvmyqPDUUMLW7brhh27XIJfdkY5/04GO/M7x7FVDM2feCQ==",
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
        self.add_program_line(avoid_adj_same_omino(omino_num=4, color="grid"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                direc = "left" if c1 != c else "top"
                self.add_program_line(f"{prefix}edge_{direc}({r2}, {c2}).")

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
            self.add_program_line(f":-{' not' * draw} edge_{d}({r}, {c}).")

        self.add_program_line(display(item="edge_left", size=2))
        self.add_program_line(display(item="edge_top", size=2))

        return self.program
