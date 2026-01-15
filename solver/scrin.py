"""The Scrin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_color_connected
from noqx.rule.shape import all_rect, count_rect_size, no_rect


def ensure_scrin_loop(color: str = "black") -> str:
    """A rule to ensure the shaded rectangles form a single loop."""
    rule = f'rect_id(R, C, R, C) :- rect(R, C, "{Direction.TOP_LEFT}").\n'
    rule += f'rect_id(R, C, R, C0) :- rect(R, C0, "{Direction.TOP}"), rect_id(R, C, R, C0 - 1).\n'
    rule += f'rect_id(R, C, R0, C) :- rect(R0, C, "{Direction.LEFT}"), rect_id(R, C, R0 - 1, C).\n'
    rule += f'rect_id(R, C, R0, C0) :- rect(R0, C0, "{Direction.BOTTOM_RIGHT}"), rect_id(R, C, R0 - 1, C0 - 1).\n'
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), #count {{ R2, C2: rect_id(R, C, R1, C1), not rect_id(R, C, R2, C2), adj_x(R1, C1, R2, C2), grid(R2, C2), {color}(R2, C2) }} != 2.'
    return rule


def border_color_unspawn(rows: int, cols: int, color: str = "black", adj_type: int = 4) -> str:
    """A helper rule to generate all the {color} cells not connected to the border with the `white_unspawn` predicate."""
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    rule = "\n".join(f"white_spawn({r}, {c}) :- {color}({r}, {c})." for r, c in borders) + "\n"
    rule += f"white_spawn(R, C) :- white_spawn(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    rule += "white_unspawn(R, C) :- grid(R, C), white(R, C), not white_spawn(R, C)."
    return rule


class ScrinSolver(Solver):
    """The Scrin solver."""

    name = "Scrin"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZbb+pGEH7nV0T7mpXq9Q1jqQ+EQ9KcEoccQDRYCBliwImNU19IasR/z8wajq/QVq1O+xBZHma+2Z2di/wt4e+xFdiUNSljVNKoQBk8qiZTWVEpUwCHVzg8Qydybf2CtuNo7QegUHpv0KXlhjb9+rjudfz225f2b1stmkzYjRDfCuPn6+fLb96vt44UsGtD69/17xxx1f6lc/Wgdi/VfhyOInv74LGr59FkuOyPVy3xj64xkZPJvaB8nSx/2rZHPzfMQwrTxi5p6UmbJje6SSRCCYNXJFOaPOi75E5PDJoMwEUom1LixW7kLHzXD8gRS3qgwSYR1G6mjrkftU4KMgF0I9VVUB9BXTjBwrVnvTRQXzeTISV49hXfjSrx/K2Nh2FeaC98b+4gMLci6F64dl4JlcARxk/+S3xYyqZ7mrTTCgbHCrTzFUCQYwWophWgVlMBFvaPK7CfVvZ7TfKt6X4Pc/kG6c90EysZZaqWqQN9B9LQd0RWYKtEVRwfRGsKYMrfTY1h4Avo+wFoSYXlTMQFas5uFf2yDLaS2UqzFJCpeKKW2TyDXIQmRsgyEhkmLOZsDWz4UI42zyjbL4q4P3+iKGENBaSSlaiquSjQKsYb9sjlNZcil0PoJ00kLr9wKXCpcNnja7pcjrnscClzqfI1TZzIX5wZn5ZGiQzZ4Q+kDT8qguk4f0CmpixzZjr3KJ8r/u0V04ZJBnGwtBY2kEEXvv8Lww88ywXLiL25HRxtIGYS+u4sTFfP7HdrERE9vRvyngK24TEKkOv7r66zqYtwdBVAZ7XxA7vWhSBy1olQ6KoJNfeDp1JOb5brFmvh12YBSpm1AEUB0GbOtoLAfysgnhWtC0DukihEsjelZkZWMUXrxSqd5mXt2DfIO+EvsIuIY/28Rf+ftyjOSPhbd+l/f02Y0GtZpck9Ja/xzJpBn3mrOK6cwJslHNqBOP7brN0Ad2P9jqpD/pNQajWnH95R/oX6wRm6zJxluIY0AT3DmzlvHX6CInPeMl7hQ0y2SomA1rAioGViBKjKjQBW6BGwEwyJUcskiVmVeRKPqlAlHpVnS5OEi8DZkGnjAw=="
        },
        {"url": "https://puzz.link/p?scrin/15/15/v3o3x3l3k3y3k3q3k3p3q3j3q3q3j3q3v3m3q3v", "test": False},
        {"url": "https://puzz.link/p?scrin/18/10/p.m3k.n2m3l5l4l.v2o64o.v.l4l1l3m.n2k1m4p", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(invert_c(color="gray", invert="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8))
        self.add_program_line(all_rect(color="gray"))
        self.add_program_line(ensure_scrin_loop(color="gray"))
        self.add_program_line(border_color_unspawn(puzzle.row, puzzle.col, color="white", adj_type=4))
        self.add_program_line(no_rect(color="white_unspawn"))

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "gray")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="gray", adj_type=4))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_rect_size(num, (r, c), color="gray", adj_type=4))

            all_src.append((r, c))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program

    def refine(self, solution: Puzzle) -> Puzzle:
        """Refine the solution by adding edges around shaded cells."""

        for (r, c, _, _), color in solution.surface.items():
            if color in Color.DARK and solution.surface.get(Point(r - 1, c)) not in Color.DARK:
                solution.edge[Point(r, c, Direction.TOP)] = True

            if color in Color.DARK and solution.surface.get(Point(r + 1, c)) not in Color.DARK:
                solution.edge[Point(r + 1, c, Direction.TOP)] = True

            if color in Color.DARK and solution.surface.get(Point(r, c - 1)) not in Color.DARK:
                solution.edge[Point(r, c, Direction.LEFT)] = True

            if color in Color.DARK and solution.surface.get(Point(r, c + 1)) not in Color.DARK:
                solution.edge[Point(r, c + 1, Direction.LEFT)] = True

        return solution
