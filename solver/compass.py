"""The Compass solver."""

from typing import Set, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, grid_src_color_connected


def compass_constraint(r: int, c: int, label: str, num: Union[int, str]) -> str:
    """Generate a compass constraint."""
    tag = tag_encode("reachable", "grid", "src", "adj", "edge", None)
    constraint = {
        f"corner_{Direction.TOP}": f"R < {r}",
        f"corner_{Direction.LEFT}": f"C < {c}",
        f"corner_{Direction.BOTTOM}": f"R > {r}",
        f"corner_{Direction.RIGHT}": f"C > {c}",
    }
    rule = ""
    if label in constraint:
        rule = f":- #count{{ (R, C): {tag}({r}, {c}, R, C), {constraint[label]} }} != {num}."

    return rule


class CompassSolver(Solver):
    """The Compass solver."""

    name = "Compass"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VRNj9MwEL33V1Q+++CvJk4uqCwtl6ULtGiFoqhKu1la0SqlaRBylf/OeBJvahG0CFDFATkZzZvxTJ4n4ym/VNkxpxEsqSmjHJbUDF+t7MPatdiednk8pOPqtCmOoFB6N53Sx2xX5oOk3ZUOziaKzZia13FCBKH4cpJS8y4+mzexmVEzBxehCmy3oHFCBaiTTr1Hv9VuGiNnoM9Aj0AH9SOo62J/yMqyMbyNE7OgxH7mJQZbleyLrzlpMiCGkNXWGlbZCc5SbraH1lNWD8Xnqt3L05qaccN24tjyjq3s2MontrKfrfgLbPOHT3lZrfqoRmldQ8XfA9llnFjeHzpVd+o8PhOuGIlVbamdQXJrGglmMw2Rl4XchwJg4IAEELVAKW+jGvkwAKgdCC99gbaRIwdsHHcg8Dd6cSFjPrRMhQPC90kPCu3DCGDYAmmzSge802s8I3PAMlUOBN3HNZ7PgaBh+cLlCPyUgfChbJPWtkvORAksh9ctROkeo5Z9xrDHGKkeIxd98Vz8mACYTbFfBMoF9BM1EuUrlAzlCOUt7pmgvEd5g1KhDHBPaDvyF3v2slmbEv0eHSJD+OmRhiNGIRUcfpJ8lmIiNE7DyzX6tyzpICHz6viYrXOYDhOYE8NZcdxnO0Czar/Kjx2eb7JDTmA+1wPyjeBrGx/G8P+RffWRbavPrnwJ/vROJlDZp/tDzR0lh2qZLdcFdBeUz7rhmvU7non7ufvqNYB7nw6+Aw==",
        },
        {
            "url": "https://puzz.link/p?compass/10/10/j.222h.112i2122t1211g2212g11.1i2222m2222t2111g222.g2222h2212q1222l2221k111.2..2l1.21h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(avoid_unknown_src(color=None, adj_type="edge"))

        all_src: Set[Tuple[int, int]] = {(r, c) for (r, c, _, _) in puzzle.text}
        fail_false(len(all_src) > 0, "No clues found.")
        for r, c in all_src:
            self.add_program_line(f"not hole({r}, {c}).")
            current_excluded = [src for src in all_src if src != (r, c)]
            self.add_program_line(
                grid_src_color_connected((r, c), exclude_cells=current_excluded, color=None, adj_type="edge")
            )

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            if label and isinstance(num, int):
                self.add_program_line(compass_constraint(r, c, label, num))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
