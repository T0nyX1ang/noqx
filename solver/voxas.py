"""The Voxas solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def voxas_constraint(r: int, c: int, r1: int, c1: int, symbol_name: str) -> str:
    """Generate a constraint for the voxas puzzle."""

    tag = tag_encode("belong_to_shape", "voxas", "grid")

    rule = ""
    if symbol_name == "circle_SS__1":  # white circle, shape and orientation are the same
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 0."

    if symbol_name == "circle_SS__2":  # black circle, shape and orientation are different
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 2."

    if symbol_name == "circle_SS__5":  # gray circle, either shape are different or orientation are different
        rule += f":- {tag}({r}, {c}, T, V), {tag}({r1}, {c1}, T1, V1), |T - T1| + |V - V1| != 1."

    return rule


class VoxasSolver(Solver):
    """The Voxas solver."""

    name = "Voxas"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVNj9owFLzzK1Y++xD7xU7IjW5pL1u2LawqFEWIZdOCCoLyUVVB/PeO7aeNaI1WWqlfUhXyPIxfJuPn2N59OUy3tVSJ+1Eu0eJKVe5vnVt/J3yNFvtlXVzJ3mE/X28BpLwdyI/T5a7ulJxUdY5Nt2h6snldlEIL6W8lKtm8K47Nm6IZy2aILiEVuBsgJaQG7Lfwg+936DqQKgEeAFN4bAw4W2xny3oyHIbMt0XZjKRwL3rhH3dQrNZfaxE0/P/ZenW/cMT9dI/B7OaLDffsDg/rzwfOVdVJNr3gtx/xS61fevRLEb88oF/tt1udTij8ezieFKUzf9fCvIXD4nhyxlxUPo6Lo0iNgo6WP1gEby/wOXj1M5+pKG90XN9oAm8ivL3Ax99ryUT1rUmjOtbG9W0W188SHc3PEhPnVRLnScf1KYvwmJxXfoq0jyPMoGzIx5c+Jj4aH298Th+TqTUWbQoDqAdaqV0RHDYpsGFspLbdgG1X6ozzjT3HJmMdarFGfkoBkwJmzRSahjUNcizrWHjI2EMGDxnnW3WOrWadvMWE/DTnZ7XbjALGpkQJ63eBVcDkdjEd3oUW2DA2kih4QyuJ60Oo1RnWGevQI9Zd5KswXkoUMGsqaGrWRE2IWIfgIWUPKTxwfQi1OsOkWSdvcYJ85cZ7cpuKm9JrH1MfrZ/qzC3lZy/2531VT9opKRwd55f597iqU4r+w6f6arDerqZLbLbD+XRTC5xrp474Jvxdkjsl/x91f+yoc5OQ/G1r4Ak7JT6HFBtFcyvF5jCZTmZrfF6o3qWO3+4fy7jqfAc=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(general_shape("voxas", 2, OMINOES[2]["I"], color="grid", adj_type="edge"))
        self.add_program_line(general_shape("voxas", 3, OMINOES[3]["I"], color="grid", adj_type="edge"))
        self.add_program_line(all_shapes("voxas", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_type(symbol_name, ("circle_SS__1", "circle_SS__2", "circle_SS__5"))
            fail_false(puzzle.edge.get(Point(r, c, d)) is True, f"Circle must be on an edge at ({r}, {c}).")

            if d == Direction.TOP and r > 0:
                self.add_program_line(voxas_constraint(r, c, r - 1, c, symbol_name))

            if d == Direction.LEFT and c > 0:
                self.add_program_line(voxas_constraint(r, c, r, c - 1, symbol_name))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
