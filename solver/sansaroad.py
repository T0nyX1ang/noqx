"""The Sansa Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent, count_adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect


class SansaRoadSolver(Solver):
    """The Sansa Road solver."""

    name = "Sansa Road"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7ZZbb+o4EIDf+RUrv9bSxrmQi7QPlNJuu0BpAbEQRShAgLQJYUMCPUH8946dVJDEqarV2ctDBRkN35jxzDgee/dXbIcOJiL9ShoWMIGPrMvskVSFPUL2GbiR5xi/4EYcrYMQFIwfu3hpezsHP4zX7WbQONw0/txr0WRC7oT4Xhi93L5cPft/3LtSSG67Wq/T67jiqvF78/qp3rqq9+LdMHL2Tz65fhlOBsveaKWLP1rdiZxMHgXlYbL8dd8Y/lYzsxCs2jHRjaSBkzvDRARhJMJDkIWTJ+OYdIxkjJM+mBDWLIz82IvceeAFIWKMwLh2+kcR1NZZHTE71ZopJALo3UwHdQxqFLqL4LCZdtKRPcNMBhjRya/Z36mK/GDv0NlocPT3PPBnLgUzO4Ly7dbuFmEJDLt4EbzG2VBinXDSSFPofzEFcPKRAlXTFKjGSYHGS1OYu+Hcc6bt1NHPzEC3TidYnWfIYWqYNJ3hWdXOat84guwySZgcG0ekSOCG4EKJkVLn4rqQ4iybfj/FGt+JTkeLpdFEVLjDiUT4XBW5XBQqOOH7F1k85eglgR+nROQKnhWnyOWsDEWuaBVc5/tXK/yoFfGoNB4eV/l+NMoVDqdxcrhO14XjX8/qX+L8+shsvcr+ZZHvXxb5+coSP19Z4a+jzN7aMldkfr4K2xMcXqfxlLkq0HXkcPb+lLlG+PNq3PcT9ukt260ikwPYzDiRmLxhUmBSYbLNxrSYHDHZZFJmss7GqLQdfLFhwDuNDKicAiuklbvHPxSbKcnsOCx/lG9OP1bNRP04XNpzB46K/treOghOaLQLvOku5VPnzZ5HyEgvCZeWHNvE/syBE+4CeUGw9dwNz8OHKQfd1SYIHa6JQmexqnJFTRxXsyBcFGI62J6Xz4Xdn3Io3TU5BAdA7rcdhsEhR3w7WufAxVGb8+RsCsWM7HyI9qtdmM0/l+NUQ2+IPaaE4c73fZ36f1+n6EoJf/tS9d+0bBMKDo0zecRoG0/tKRSb1YtyhRS4ZP3r0bM9EYSfNKizsYg5bQroJ53qwsrjFU3pwlrkpQ5Egy03IaCcPgS02IoAlbsRwFJDAlbRk6jXYluiURU7E52q1JzoVJf9ybRq7w==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(fill_line(color="not gray"))
        self.add_program_line(single_route(color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type="line"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(
                not (d == Direction.CENTER and symbol_name == "circle_SS__5"),
                f"Gray circle cannot be placed in the center of ({r}, {c}).",
            )
            target = 2 if d == Direction.TOP_LEFT else 1

            if d == Direction.CENTER and symbol_name == "circle_SS__1":
                self.add_program_line(f"not gray({r}, {c}).")

            if d == Direction.CENTER and symbol_name == "circle_SS__2":
                self.add_program_line(f"gray({r}, {c}).")

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

            if d == Direction.CENTER and symbol_name == "tridown_M__1":
                self.add_program_line(f"pass_by_route({r}, {c}).")
                self.add_program_line(count_adjacent(3, (r, c), color="not gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
