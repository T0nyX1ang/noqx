"""The Putteria solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent


def putteria_fill_constraint() -> str:
    """Generate a constraint for the number filling in putteria."""
    return ":- area(A, _, _), #count { R, C : area(A, R, C), number(R, C, N) } != 1."


def avoid_same_number_adjacent(adj_type: int = 4) -> str:
    """Generate a constraint to avoid adjacent cells with the same number."""
    rule = f":- number(R, C, _), number(R1, C1, _), adj_{adj_type}(R, C, R1, C1)."
    return rule


class PutteriaSolver(Solver):
    """The Putteria solver."""

    name = "Putteria"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VVNbxoxEL3zKyKffVh/7npvaUp6SUnbpKoqhBAhpEEFkUKoqkX8977xjmMSgVKpaptDtax5nh173s4bz66+rUfLiQy4TCULqXCZqoh3ZelX8HU5vZ9N6iN5vL6/XSwBpDw/PZU3o9lq0umz16CzaULdHMvmTd0XSkihcSsxkM37etO8rZuubC7wSMgKtrPWSQN2M/wUnxM6aY2qAO4xBvwMOJ4ux7PJ8Ky1vKv7zaUUFOdVXE1QzBffJ4J50Hy8mF9NyXA1usfLrG6nd/xktb5efF2LFGIrm+OWbm8PXZPpmge6Zj9d/efphsF2i7R/AOFh3SfuHzOsMryoN8J4UVdSWBv/XDvzFf62RLl16Isj0Gxli66PDO6pBy1/ZFBFAYvJc6Uxd3muaU+b54aelzwHEVVvtpQ2Gk/jqON4iReRjYnj6zgWcXRxPIs+XbyEQtmqUIpaY8fKAwfGpdREjnAogA1j2FWyV8CKcQDWEetCAVvGGtgxNsC+xQp7asMYdp3sFrhkjFimjaU17Ibt2gFXjMHBKsbgYJmDwVrHay04OOZgEctxLAt/z/4OnD1zdojlOZZDLM+xPPYpeR+PfUrex8OnTD4eODDG/hXvX8KnYp8S3AJzK8E/MH80Eh04JxX4BOYT0GiKhA2wf8h/0gtaQSOVc16YnGfWCPoA7+Q8aUQ5Txop8Fc7+VcpzzrrpUkvm7VI2mn46+QfsnakRdILrVMb5mxIr6RRkXW0KutI2lmOa0nrkLVL+jqsdSrr6JKmpDuvdaT7jr6pHhze15VZX8/+nmogae1zPXhw8Dv6lklH0r3MmqYaKKkGiqxpqocKPhX7VCHXA521VA/QOtcA+ATmE5DzQDnfUkulo3wSRxtHH494SZ3sF3td29B+v5s8S6eP06qeXO5lWQadvrhYL29G4wm+IN3rL5Oj3mI5H80w663nV5NlmuMDvu2IHyLesYfb/9/0f/RNJwmKl1btz9DpNxcS3aQ5l+JuPRwNxwvUGHJHdnSlvXZr99vNAf9D9kP7HIq7h+dfzybax6DzEw==",
        },
        {"url": "https://puzz.link/p?putteria/7/7/4dvovcel0eprhelnrgk.zzi", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_same_number_adjacent())
        self.add_program_line(unique_num(color="not gray", _type="row"))
        self.add_program_line(unique_num(color="not gray", _type="col"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, (ar, _) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(len(ar), len(ar) + 1), _type="area", _id=i, color="gray"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")
            else:  # compatibility with puzz.link
                self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(putteria_fill_constraint())
        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
