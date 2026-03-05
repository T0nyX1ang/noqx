"""The Uso-one solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


def uso_one_constraints(adj_type: int = 4, color: str = "black") -> str:
    """Generate the constraint for Uso-one."""
    count_adj = f"#count {{ R1, C1: {color}(R1, C1), adj_{adj_type}(R, C, R1, C1) }}"
    rule = "{ wrong_clue(A, R, C) } :- clue(A, R, C, _).\n"
    rule += ":- clue(A, _, _, _), { wrong_clue(A, R, C) } != 1.\n"
    rule += f":- clue(A, R, C, N), not wrong_clue(A, R, C), {count_adj} != N.\n"
    rule += f":- clue(A, R, C, N), wrong_clue(A, R, C), {count_adj} = N.\n"
    return rule


class UsooneSolver(Solver):
    """The Uso-one solver."""

    name = "Uso-one"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VVNTxsxEL3nVyCffVh/rNfeG9DQC4W2oapQFEUBlhI16dKEVGhR/nuf7Uk2RqnaQEVbqUrW+2Z2xvNmbI/nXxejWcVF5v/Kcrzx08KGR1oTnox+Z+O7SVXu8f3F3U09A+D89OiIX48m86rTJ6tB56FxZbPPm9dlnwnGmcQj2IA378qH5k3ZdHnTwyfGLXTH0UgCdlv4MXz36DAqRQZ8QhjwHLC+Hx5E6W3Zb8448zEOgqeHbFp/qxhx8PJlPb0Ye8XF6A6JzG/Gt/RlvriqPy/Yavolb/Yj1d4WqqqlqtZU1XaqsqXafRLVyfhLVd9vo+kGyyVK/R5Eh2Xfc/7QQtvCXvmw9HwemCrgKrG+YTWYNhDVWsyzVJSpaCFma9GI5KtJpyryxLiwSdzCQRRr0RaJr8sSX5H5SHpDtom5EOaRbJPZhUzTElIlZITWj2ST+utH8bRL7U2+YY9Ci1Du8zAehVGG8QyrwRsVxldhzMKYh/E42HSxSFIoLiVqInFwBM6fygg7YBWxLLjUImKVAWvC8NXkqwWXeU5YA1vC8DXkm+fAjjDOeyEjNvAtyNcgrqW4hfT9gDB8LflaxHUUF/1CZZEz3lyJyA1vrmTkoCRsNNlICxzjQsdVTvZaApuWv17lgrh6pTdtvj6XlX0Ofb7SF23uxue+wrbNPfS5FX/YWLKxdiNH1MHRWjjU3FENHeI6iutMWweHeRzN4zCPo3mca+vjayJywjmwIYz6iIJwAUx1Q09WwlHdFOpJtZK+tjSPxDzStHWmvYQ31X/pe5bfbodh1GE0YRsWvmX8YlNhtDH93rOxw2xu/9heCt62vtg0RKt52gn5Kf2+irdY+sv/Pd2g02e9xex6dFnhAuhefar2TurZdDSBdLKYXlSzVu7djG4rhrt32WH3LDyha+n/1/ELXse+7NlOl/Lzb4znHud+c87R75tTzm4Xw9HwssZ+Qs28Hv31j+j/Nj678tyu73HcYzvod53/d+XVwwW1m/5HeW2xf/Hdjwth0PkO",
        },
        {
            "url": "https://puzz.link/p?usoone/10/10/h0finm9ud78hcsnn18e8h34l4kautm6h8ok4ibgcgahdcgdjc2ddg7dhcgb7ablccgdk3eg11cl",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="clue", size=4))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_color_adjacent(color="gray"))
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(uso_one_constraints(color="gray"))
        self.add_program_line("ox_E__1(R, C) :- grid(R, C), clue(_, R, C, _), not wrong_clue(_, R, C).")
        self.add_program_line("ox_E__7(R, C) :- grid(R, C), clue(_, R, C, _), wrong_clue(_, R, C).")

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            for r, c in ar:
                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                    self.add_program_line(f"not gray({r}, {c}).")
                    self.add_program_line(f"clue({i}, {r}, {c}, {num}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f":- wrong_clue(_, {r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f":- not wrong_clue(_, {r}, {c}).")

        self.add_program_line(display(item="gray"))
        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__7"))

        return self.program
