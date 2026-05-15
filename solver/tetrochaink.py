"""The Tetro Chain-K solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class TetroChainKSolver(Solver):
    """The Tetro Chain-K solver."""

    name = "Tetro Chain-K"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VXfj9JAEH7nrzD7vA/dn5R9w/P0Be/UcrmQpiE97AUipAjUmCX8785Oi+Rg1hjjRU1M2enHt9PZ+WZ/bT835abiIgk/lXJ4w6NFik2mFlvSPePFblm5F3zY7Ob1BgDntzf8sVxuK97LO6+it/cD54fcv3E5E4wzCU2wgvv3bu/fOj/hPoMuxkXB2apZ7hazellv2JHzo/ZDCfD6BO+xP6CrlhQJ4JsOA5wAnC02s2U1zbLW853L/ZizMPhL/DxAtqq/VKxLLvyf1auHRSAeyh0o3M4Xa8YVdGybj/Wnhh2HOHA/bCVkRwnpjyWokwT1XYKiJcinEka/X8GgOBxgdj6AhqnLg5y7E0xPMHP7Q0grWIF24vbMGggj+VmJmVACeHHBS2lJf6k08OaS15E4uk/zpk/HMQOa7ws6n76i46cxno6vkoT0V0LTvJZkHJPYCE/rNYKupxGGHNdE6m+UoflYnlqR9bRiQI5rpSDjWKkiPJ2/tZE4lqoPrN3XuIIl2jEscO4V2ldoE7QG7Qh9rtHeo71Cq9Fa9OmHLfKTmwjWBHNpWALMycsd9Uy55ao9xZ8+5t/jil7OsmbzWM4qOOayebmuGNwuhx77yrDlisvg9v/C+ZsvnDBTya9fO3gO+9vuAGkBMn9ma+cwFbDBQh7rZlpOYRqwbiSvIvzRX0T8z3nd8fKMNxF/2/LaRsY9j6Mi/rqIzstzVR/Or6L3DQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8, grid_size=(puzzle.row, puzzle.col)))

        self.add_program_line(all_shapes("omino_4", color="gray"))
        self.add_program_line(avoid_same_omino_adjacent(4, color="gray", adj_type=4))
        for i, o_shape in enumerate(OMINOES[4].values()):
            self.add_program_line(general_shape("omino_4", i, o_shape, color="gray", _type="grid", adj_type=4))

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

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
