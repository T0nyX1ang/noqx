"""The Ant Mill solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import nori_adjacent


def ensure_antmill_loop(color: str = "black") -> str:
    """A rule to ensure the shaded 1x2 rectangles form a single loop."""
    rule = f"adj_count(R, C, N) :- grid(R, C), {color}(R, C), #count {{ R1, C1: {color}(R1, C1), adj_x(R, C, R1, C1) }} = N.\n"
    rule += f":- grid(R, C), grid(R1, C1), {color}(R, C), {color}(R1, C1), adj_count(R, C, N), adj_count(R1, C1, N1), adj_4(R, C, R1, C1), N + N1 != 2."
    return rule


class AntMillSolver(Solver):
    """The Ant Mill solver."""

    name = "Ant Mill"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VRLj5swEL7zKyqf54AfGMItu932ku62TapVhBBiKaugEpGSUK0c8d87NmxRcKiiqk+pcjwM34w938yE2X9u0joH6uofDwCfuAQNzGaBNNvt16o4lHn4AubNYVPVqADc3cJjWu5zcKLeK3aOahaqOajXYUQoAcJwUxKDehce1ZtQrUEt0UQgiIFsm/JQZFVZ1cRgFP0W3UGG6s2g3hu71q47kLqo3/Y6qmtUq6fkqnt7G0ZqBUTHvTIntUq21Zec9Lz0e1ZtHwoNPKQHTG6/KXYEOBr2zcfqU0Oeb29BzTv2ywvZ84E9/8aen2fPevZZUWdlnix+fgazuG2xMe8xhySMdDofBjUY1GV4bDUtLamR6/BIhGB4j4ChvER4ZyDfgqQ3hjzXtaHAgihHiJ9AzIIk9y1IWHdJQ/XUS9Kxl+/OLIgG44M+s9L2OT+FsGivTOmYkSusLChu5EsjXSM9IxfG58bIeyOvjRRGSuPj695c2D3CsbwMM8RHoMnhw+7oL6IY8W6AnC7v38NiJyLLpn5Msxw/s+Um3eUEB1vrkCdiNv4rmHb7P+v+0lmnm+T+8MT7M59whAUXHqg7ILsmSRMsNtbLj+G8IegM0h0ZvN7gi7Fh1hvGV0m3v4qODXQihmQTMSSfiiGmYngTMdj3cX6p/zMjbvn/9v7jiIydrw==",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(nori_adjacent(color="gray", adj_type=4))
        self.add_program_line(ensure_antmill_loop(color="gray"))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.TOP and r > 0:
                if symbol_name == "ox_B__3":
                    self.add_program_line(f":- gray({r}, {c}), not gray({r - 1}, {c}).")
                    self.add_program_line(f":- not gray({r}, {c}), gray({r - 1}, {c}).")
                if symbol_name == "ox_B__4":
                    self.add_program_line(f":- gray({r}, {c}), gray({r - 1}, {c}).")
                    self.add_program_line(f":- not gray({r}, {c}), not gray({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0:
                if symbol_name == "ox_B__3":
                    self.add_program_line(f":- gray({r}, {c}), not gray({r}, {c - 1}).")
                    self.add_program_line(f":- not gray({r}, {c}), gray({r}, {c - 1}).")
                if symbol_name == "ox_B__4":
                    self.add_program_line(f":- gray({r}, {c}), gray({r}, {c - 1}).")
                    self.add_program_line(f":- not gray({r}, {c}), not gray({r}, {c - 1}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))

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
