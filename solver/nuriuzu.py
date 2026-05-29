"""The Nuri-uzu solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected
from noqx.rule.shape import avoid_rect


def nuriuzu_constraint(glxr: int, glxc: int, adj_type: int = 4, color: str = "black") -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", adj_type, color)
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1).\n"
    return rule


class NuriuzuSolver(Solver):
    """The Nuri-uzu solver."""

    name = "Nuri-uzu"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZRb5swEH7nV0z3fA82mAR4y7puL126jUxVhaKIUHdBIyKFME2O8t97PpiQViNNm7b1oSL+9PHdYe6z0TntQ5c3GmVof0GEAiVdMxHxkBHd0/hxrcpjpZNXuOiOu7ohgni9xPu8ajV62ZC19k4mTswCzbskAwkIPg0JazQfk5N5n5gUTUohQEXaVZ/kE70c6Q3HLbvoRSmILwdO9JZoUTZFpTdp2ksfksysEOyLXvPjlsK+/qZhKMTeF/V+W1phmx/JTbsrD0Ok7e7qr92QSxPCvquOZVFXdWNFq53RLH7yYGscPASjB0t7D5Y5PNjH/tyDvvui227rMhC7DZxpdz6RhU2SWTefRxqNNE1OhEtGyXibnCBUNIukt48lkwuIQrc8d8pSztx6JCZ09zy+cFcTiNipzyPpLlNMlB+79ThwvzeemD+emEf6QTQRUFOB0G1NBr5r7WjX3vLe+Ywr2lo0AeMbRsEYMl5xziXjDeMFo2Kccc7cfhy/+PmAopIUgqJV8Z9+S3+ptkz1/Wvqoi73En3e0bWXQdo193mhqaulu/yggU6UswffgUcWUJp6OWSe9yFjd0r89lHzf1pXRutNDcRcIxy6Tb4hT0B/Z5B1+UT/59VTf1t7jw==",
        },
        {"url": "https://puzz.link/p?nuriuzu/10/10/iaaeztepexewezwepexewezzseezzj", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(avoid_rect(2, 2, color="not black"))

        reachables: List[Tuple[int, int]] = []
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            # there are no category = 1 for nuriuzu, because it is conflicting with the no 2x2 white rule.
            if d == Direction.CENTER:
                reachables.append((r, c))
                self.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2 + 1, color="not black"))
                self.add_program_line(f"not black({r}, {c}).")

            if d == Direction.TOP:
                reachables.append((r - 1, c))
                self.add_program_line(nuriuzu_constraint(r * 2, c * 2 + 1, color="not black"))
                self.add_program_line(f"not black({r - 1}, {c}).")
                self.add_program_line(f"not black({r}, {c}).")

            if d == Direction.LEFT:
                reachables.append((r, c - 1))
                self.add_program_line(nuriuzu_constraint(r * 2 + 1, c * 2, color="not black"))
                self.add_program_line(f"not black({r}, {c - 1}).")
                self.add_program_line(f"not black({r}, {c}).")

        fail_false(len(reachables) > 0, "Please provide at least one clue.")
        for r, c in reachables:
            excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type=4, color="not black"))

        tag = tag_encode("reachable", "grid", "src", "adj", 4, "not black")
        spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
        self.add_program_line(f":- grid(R, C), not black(R, C), {spawn_points}.")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display())

        return self.program
