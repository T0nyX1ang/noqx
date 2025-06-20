"""The Tents solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_adjacent_color


def identical_adjacent_map(known_cells: List[Tuple[int, int]], color: str = "black", adj_type: int = 4) -> str:
    """
    Generate n * (n - 1) / 2 constraints and n rules to enforce identical adjacent cell maps.

    A grid fact and an adjacent rule should be defined first. n is the number of known source cells.
    """
    rules = "\n".join(
        f"{{ map_{r}_{c}(R, C): adj_{adj_type}(R, C, {r}, {c}), {color}(R, C) }} = 1 :- grid({r}, {c})."
        for r, c in known_cells
    )  # n rules are generated

    constraints = ""
    for i, (r1, c1) in enumerate(known_cells):
        for j in range(i + 1, len(known_cells)):
            r2, c2 = known_cells[j]
            constraints += f":- map_{r1}_{c1}(R, C), map_{r2}_{c2}(R, C).\n"

    return rules + "\n" + constraints.strip()


class TentsSolver(Solver):
    """The Tents solver."""

    name = "Tents"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZNj9owEL3nV6x89iF2PpzkUtHt0gvNtoXVCkURCjQVqNBQIFVlxH/fmUlW2Ti+FKnby8p4NPM89rwZ2zHHX3VxKLkI8OdF3OUCWuhG1EUENvTnNtuctmVyw0f1aV0dQOH8fjzm34vtsXQynAktd846TvSI649JxgTjTEIXLOf6S3LWnxKdcj2FIQa+XE8aJwnqXac+0jhqtw0oXNDTVgd1Dupqc1hty8WkQT4nmZ5xhnHe02xU2a76XbKWB9qrarfcILAsTpDMcb3ZtyPH+lv1o259RX7hetTQnVvoeh1dVBu6qFnoYhZI91T+PB2v4trOHNKM88sFyv0ViC6SDDk/dGrUqdPkDDJNzswXMFXCPtGOMF+C6XWmhwu/A5LPgN8fD8HEXW7MwO2NBrj2C7O/dhD3IqvICCUCjNU5iBjnd7aM1Iv1IB1BSc0hqRADA95VmIWYiQEhgT6khhOjYADFSLUPCRdTNzGLn7D4SUzMxDB5A/MwYQPzLRhV1sAsJRGWmghliRs1u9zDYhs2jCvdYW7SG8aVltwknU0DU8P6ScuuSWWJa8lNquH2SjXMTdLxNDFLvpHJD47kmA6mJDmDC8i1R/IDSZdkQHJCPnckH0nekvRJhuSj8Ar/1SXv3Q0iKP89wSxs3g5bU28j14zkTsbSercsDzdpddgVW3gCputiXzJ4Yy8O+8Oo0zfRf3t2X/nZxdK7V9/L//OZyKCq8H9O33O2rxfFYlXBmXLzV2cJn4u2urnzBA==",
        },
        {"url": "https://puzz.link/p?tents/13/13/h3g03h1g2j3h32g24g2g55233hi11131331f78625243a872550", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="tents__2"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_adjacent_color(color="tents__2", adj_type=8))

        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int) and isinstance(num, int):
                self.add_program_line(count(num, color="tents__2", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int) and isinstance(num, int):
                self.add_program_line(count(num, color="tents__2", _type="row", _id=r))

        all_trees: List[Tuple[int, int]] = []
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "tents__1":
                all_trees.append((r, c))
                self.add_program_line(f"not tents__2({r}, {c}).")
            if symbol_name == "tents__2":
                self.add_program_line(f"tents__2({r}, {c}).")

        self.add_program_line(identical_adjacent_map(all_trees, color="tents__2", adj_type=4))
        self.add_program_line(count(len(all_trees), color="tents__2", _type="grid"))
        self.add_program_line(display(item="tents__2"))

        return self.program
