"""The Dotchi-Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, route_turning, single_route


def dotchi_constraint() -> str:
    """Generate a constraint for the Dotchi-Loop puzzle."""
    rule = "turning_area(A) :- area(A, R, C), white_clue(R, C), turning(R, C).\n"
    rule += "straight_area(A) :- area(A, R, C), white_clue(R, C), straight(R, C).\n"
    rule += ":- area(A, _, _), turning_area(A), straight_area(A)."
    return rule


class DotchiSolver(Solver):
    """The Dotchi-Loop solver."""

    name = "Dotchi-Loop"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VbBThsxEL3nK5DPPnhsr9e7N0qhlxTaQlWhKIpCSEvU0NCEVNWi/Huf7aEBMYi2qpAqVck6LzP2+M2zx97V1/V4OdVk0tdFjV98PMX82BjyY/hzMrueT9sdvbu+vlgsAbQ+OjjQH8fz1bQ34F7D3k3XtN2u7l61A2WVzg+poe7etjfd67Y71d0xXEoTbH0gUtoC7m/hh+xPaK8YyQAfMgY8BZzMlpP5dNQvljftoDvRKs3zIo9OUF0uvk1VGZb/TxaXZ7NkOBtfI5nVxeyKPav1+eLzWt1OsdHdbqHbF+i6LV33k66T6dq/QXc++zL9LjFthpsNFH8HrqN2kGi/38K4hcftzSZRSi3l9rS9UY4QhvR9bso50VqJ1lqyei9aA6z2gTVK1sqK1kayBjGL4MS+Qepbi3xrsW80orWWZouN1LchqW8j8m1E1cmIJMiIqpHxslnMj4y4IERybyuKT1bcQ2SjaHYybycuCzlxH5EXBSR5L5IXF4y8uMOokrMM8jIE+9CMijvIdWdze4Ky1J3L7cvcmtxWue3nPvuoUEte26QaOFnCeewM4xqYCrY4q70t2Blgz5iAq4K91bYKjBGz4pi+Am4KrhC/5vgVYtYcs7bpHigY94EzpQ9+tSPP2AKXPo6cdrZm7IEjY4xl/vBr54lxBC5zwQ/MMT1pV1WMEZ/5ww/M/KtG28CcA3IPrElA7oH5B/BPx0HG0C3w2IAcA+cemm3uEWMjj40pdx4bHTBrG6FhZG1jdU8fG2vGmCvyXDHdpzxXxFwNz9WAc0NbDY1jDA3NrbbI17AOpoHOrGG6tInHErQi1pDSWqQ4m3Q3pa20l1uf25C3WJ3uhT++OX53Nytvwa2J6bCOBWAR0950ie8dlI4Cl71phV0pgyfzGLjy6nL/U/17tmFvoPq47HcOF8vL8RxX/v75pzv/ji/GV1OFl6xNT31X+Rm49M72/73r+d+7kvrm2WroF0vhCToDCMu1p7sjra7Wo/FossDegnbZWcpRdqJ6ZQfq+/FwqOlHnKXMHzifXTOcIMPeDw==",
        },
        {
            "url": "https://puzz.link/p?dotchi/11/11/00g5g5k5k5k5k5k5k1k100fv003v0000000000vo00vu13a0b3j3a6a6j6j6a3a3j6b6b3a3a3b6j6j393a30",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_straight(color="white"))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(dotchi_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_L__1":
                self.add_program_line(f"white_clue({r}, {c}).")
                self.add_program_line(f"white({r}, {c}).")
            if symbol_name == "circle_L__2":
                self.add_program_line(f"not white({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
