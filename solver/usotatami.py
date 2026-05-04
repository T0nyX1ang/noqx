"""The Uso-tatami solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.shape import all_rect_region, avoid_edge_crossover, count_rect


def rect_constraint() -> str:
    """Generate a cell relevant constraint for rectangles with the width/height of 1."""
    return f':- rect(R, C, "{Direction.TOP_LEFT}"), rect(R + 1, C, "{Direction.LEFT}"), rect(R, C + 1, "{Direction.TOP}").'


class UsotatamiSolver(Solver):
    """The Uso-tatami solver."""

    name = "Uso-tatami"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVdb9owFH3Pr6ju832I7Xz6ZWId9IXRbaWqqihCgWYrKihdQqbJKP991zdAkAarWib2Mlk+Oj7Xdo5vfJPqe52VOUbUVIQuCmrKk9ylG3N3N208Xy1yfYG9evVYlEQQrwcD/JotqtxJNrNSZ21ibXpornQCEpC7gBTNZ702H7UZobmhEKAgbUhMAEqi/Y7ecdyyy1YULvHRhhO9Jzqbl7NFPhm2yiedmDGCfc57Xm0pLIsfObTLeDwrltO5FabZig5TPc6fN5Gqfiieatg+okHTa+32D9hVnV21s6sO25V/w27+8C2v6ukhr3HaNJTzL+R2ohNr/LajUUdv9LqxptYgA7v0HRlpXwzI0ArhnhBZIdgTYiv4naBcK3h7grCC2hMktBdgJ6htdlkgM4It3TMOGCXjmByjUYwfGF1Gn3HIc/qMd4yXjB5jwHNCe+ZXZeV0O5QCD3Qc0en8CEVIGVIvWkxkwDXXNf+849RJoE+362JUlMtsQTdsVC+nebkdUz03DvwE7omiJd7/Ev8XJW7z7575Sp9aYQmldlcNaK4RnutJNpkVdM8of204pL9OJI+GI4ki9o6G/Zg2F0fDAW0eHt88oAoI1ZvDf978BWunnJs+Nb8Fzv7u6euVOr8A"
        },
        {"url": "https://puzz.link/p?usotatami/8/8/7b23b6b4b2f2d4a21a2b4b3a3e8e5b3b2b32b3", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(rect_constraint())
        self.add_program_line(avoid_edge_crossover())
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
                self.add_program_line(count_reachable_src(("ne", num), (r, c), main_type="bulb", color=None, adj_type="edge"))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
