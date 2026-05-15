"""The Battenberg Painting solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type


def batten_constraint(color: str = "black") -> str:
    """Avoid checkerboard pattern at places without battenberg pieces."""

    rule = f"checkerboard(R, C) :- {color}(R, C), not {color}(R, C + 1), not {color}(R + 1, C), {color}(R + 1, C + 1).\n"
    rule += f"checkerboard(R, C) :- not {color}(R, C), {color}(R, C + 1), {color}(R + 1, C), not {color}(R + 1, C + 1).\n"
    rule += ":- grid(R, C), not batten(R, C), checkerboard(R, C).\n"
    rule += ":- grid(R, C), batten(R, C), not checkerboard(R, C)."
    return rule


class BattenbergPaintingSolver(Solver):
    """The Battenberg Painting solver."""

    name = "Battenberg Painting"
    category = "shade"
    aliases = ["battenbergpainting"]
    examples = [
        {
            "data": "m=edit&p=7VTBjpswEL3zFas5zwFskhhu6XbbS5ptm1SrCKGIUFZBBZESqCpH/HvHAy1bBOpWaqMeKsPo+c3Ynuexff5cR2WCHjWp0EaHmlQ2/8o1n921bVpliX+Dy7o6FiUBxPs1PkbZOUErcHisHVoX7fl6ifq1H4ADCIJ+B0LU7/yLfuPrHeoNuQBViJDXWZXGRVaUwJxDcat2oCB418MH9ht025KOTXjdYYI7guf6Y/GpTqq4pd76gd4imMVf8HADIS++JNAlZ/pxkR9SQxyiihSej+kJUJKjnQ2+L9GgXrYSNs+UIHsJ8ocEOS5BdBLitIyzZL/68wq8sGmoOu9Jw94PjJwPPVQ93PiXxqR1AeGZoTNKpS0hSNsQ8gnhDCPEMEIOI9xhxGwQ4TqDCMXLLnrCkz9FULoOJ70zSQuzgIODw0D8fIJX4zyLHeEXE/MsJuZRE/MoMcKTiFcsRbDdUklQS7Yv2dpsZ2xXHHPH9oHtLVuX7ZxjFqaozyw7uJSSogLQ9or2DDzd2r+UW+AKfnX6Nr9uP7QC2NTlYxQndKHWdX5Iypt1UeZRRv3NMTolQO9aY8FX4D+QKMyw/0/dv/zUmUrZv/XgXeGw/yKdgDacroO+RzjV+2hPm02744Y47phNOETHywEvw6vrpfsdWt8A",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(batten_constraint(color="gray"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(symbol_name, "sudokuetc__1")
            self.add_program_line(f"batten({r - 1}, {c - 1}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="gray", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
