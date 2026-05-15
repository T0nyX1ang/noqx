"""The Border Block solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def border_block_constraint() -> str:
    """Generate a border block constraint."""
    mutual = f'edge(R, C, "{Direction.LEFT}"); edge(R - 1, C, "{Direction.LEFT}"); edge(R, C, "{Direction.TOP}"); edge(R, C - 1, "{Direction.TOP}")'
    rule = f":- ndot(R, C), {{ {mutual} }} = 1.\n"
    rule += f":- ndot(R, C), {{ {mutual} }} > 2.\n"  # 0 or 2 connected edges
    rule += f":- dot(R, C), {{ {mutual} }} < 3.\n"
    return rule


class BorderBlockSolver(Solver):
    """The Border Block solver."""

    name = "Border Block"
    category = "region"
    aliases = ["borderblock"]
    examples = [
        {
            "data": "m=edit&p=7VTbjtowEH3nK1bzPA+xnftLxW5pXyjbFlarVRShwKYFNSg0kKoy4t87ngCBNNH2plUrVcbDyfH4cmbs2XwukyJFYZmf8pH+qdnC5y59l7t1aJPlNkvDK+yX20VeEEC8HeGHJNuk2IsOXnFvp4NQ91G/DiOQgNwFxKjfhTv9JtQj1GMaAhQxwqrMtst5nuUFHDk9JCQAJcFBDe953KCbihQW4dEBE3wgOF8W8yydjscV9TaM9ATBbH7N0w2EVf4lhWoef8/z1WxpiFmyJYWbxXINqGhgUz7mn0o4brFH3a8kDH5QgqolqJME1S5BXkoY/nkFQbzfU3bek4ZpGBk5dzX0azgOd3tzrB0ocRRfpRBsF6qsngi/4eHahlA14SlD2GeE05jieYZwaiKwDOHWhLCsxiJCeI1VhAgaZxNSGsY7Y5TT2ErYfLwX54xzwVAoBAfkgQIilXGX2LhoxAftvON38B3+nuzgnXbe7/D3O87pd6wTiFZeWW3rUDBecUgk2wldG9SK7Uu2FluH7ZB9Bmzv2d6wtdm67OOZi/dTV/M8K792HHAF5SbwOYjIAVNPHjFSVYm8bM6/x8W9CAaPH9OrUV6skozqyKhczdKi/h4vknUKVM73PfgK3COF8n+F/9srvMmU9cyP6XffdkQBp/eI+hZhXU6TKUUb6KqhGTg90O+Gn10FVYC49w0=",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="dot"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(f"vertex(0..{puzzle.row}, 0..{puzzle.col}).")
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))
        self.add_program_line("ndot(R, C) :- vertex(R, C), not dot(R, C).")
        self.add_program_line(border_block_constraint())

        for (r, c, d, _), _ in puzzle.symbol.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            self.add_program_line(f"dot({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
        for (r, c, d, label), letter in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if letter != "?":
                self.add_program_line(grid_src_color_connected((r, c), color=None, adj_type="edge"))

            for (r1, c1, _, _), letter1 in puzzle.text.items():
                if (r1, c1) == (r, c) or letter == "?" or letter1 == "?":
                    continue
                if letter1 == letter:
                    self.add_program_line(f":- not {tag}({r}, {c}, {r1}, {c1}).")
                else:
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
