"""The Nawabari solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, count_rect


class NawabariSolver(Solver):
    """The Nawabari solver."""

    name = "Nawabari"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VXda9swEH/3X1HuWQ/6sB1bLyPtkr5k6bamlGJMcFK3DUtwZ8djKPh/3+mc2FMbGKWjY1AUXX53p4+f7nRy9b3OypwJbn8qYviPzRcRdRmF1Pm+zVbbda5P2LDePhQlAsYuxmN2l62r3Ev2o1JvZ2Jthsyc6wQkMOoCUma+6J35pM2UmUt0ARNomyASwCTCUQ+vyW/RWWsUHPF0jxHeIFyuyuU6n09ay2edmBkDu88pzbYQNsWPHNpppC+LzWJlDYtsi4epHlaPe09V3xbfajhs0TAzbOmOjtBVPV3V0VXH6cq/QTe/vc+renGMa5w2Dcb8K7Kd68QSv+ph1MNLvWssqR0ojlMlJprSAspHVfVq4Hpju88H6Ax+iAbRqYFw1EHgqpGjRgO7mOoXi33HL7g4ZKCzuCsIMXDoCcldv/9kRT92xwehq4fcOb0IxRP/7+HAAAoK4w3JMUlJcoZRZkaR/EiSkwxITmjMiOQ1yTOSPsmQxgxsnl6UydfTgVBJ0HGEVSqw2O3NUH+kmKj2nXBb8P/ZUi+BEVbWybQoN9kaq2tabxZ5edDxLWs8+AnU6ZL478/bv3jebPz5G5fGays1wdB2VcXMBYPHep7NlwXeM4yfdYf4kX2hQ8lnjjc/N74AqfcL",
        },
        {"url": "https://puzz.link/p?nawabari/10/10/b4c1d2b1c2c2j4b0b1a3b3j3b1a2b0b4j2c3c2b1d1c3b", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(count_rect(len(puzzle.text)))

        all_src: List[Tuple[int, int]] = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_adjacent_edges(num, (r, c)))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
