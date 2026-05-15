"""The Lithersink solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent_edges


def limit_adjacent_vertices(r: int, c: int) -> str:
    """Generate a rule that counts the adjacent vertices around a cell."""
    v_1 = f'edge({r}, {c}, "{Direction.TOP}")'
    v_2 = f'edge({r}, {c}, "{Direction.LEFT}")'
    v_3 = f'edge({r}, {c - 1}, "{Direction.TOP}")'
    v_4 = f'edge({r - 1}, {c}, "{Direction.LEFT}")'

    rule = f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} = 2.\n"
    rule += f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} = 0.\n"
    return rule


def border_color_connected(rows: int, cols: int) -> str:
    """A rule to ensure all the color cells are connected to the borders of the whole grid.

    This rule is specially designed for the lithersink puzzle.
    """
    adj_type = "edge"
    tag = tag_encode("reachable", "border", "adj", adj_type)
    borders = [(r, c) for r in range(-1, rows + 1) for c in range(-1, cols + 1) if r in [-1, rows] or c in [-1, cols]]
    initial = "\n".join(f"grid({r}, {c})." for r, c in borders) + "\n"
    initial += "\n".join(f"{tag}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), grid(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


def not_single_tree(rows: int, cols: int) -> str:
    """Generate a rule to avoid the case where all edges are connected as a single tree."""
    return f":- #count {{ R, C, D : edge(R, C, D) }} = {(rows + 1) * (cols + 1) - 1}."


class LithersinkSolver(Solver):
    """The Lithersink solver."""

    name = "Lithersink"
    category = "var"
    aliases = ["lithersink"]
    examples = [
        {
            "data": "m=edit&p=7VZLb9swDL7nVxQ666CHLT9uWZfskqXbmqIoDCNwUm81ZsOdEw+Fgvz3UUxSj1qBbehQbMCgiOEnkhIpkZI3X/qiK7kU7qdjDv/QAhljV7HBLo5tUW3rMj3j435713bAcH4xnfKPRb0p+Sg7quWjnU1SO+b2TZoxzTiT0BXLuX2f7uzb1M65vQQR4zLnrOnrbbVu67ZjpzE7Aw6MFLCTgb1GuePOD4NSAD8/8sDeALuuunVdLmeHkXdpZhecubVfobVjWdN+LdnBDPG6bVaVG1gVW4hwc1fdM65BsOlv2889O62w53Z8iGDyixHoIQL9GIF+OgL1JyIobz+VD084n+T7PZzLB3B/mWYukquBjQf2Mt3tnUc7piWYasgGMIfZtKIwoDAEKAcYUWlMYOBs1QAjAkMBUAxQE9uQTmWokyYgbhjqRqTJzBF1IzJU6tkmRDkWZKHYUJgQmChim9C9kkJ4mEYshfFwQrH05pPGw7GHaShSSQ8rqq9iKteevpcKEg9/2EgZ0MyRgedv4PkXSg9784WeP0Z4mOaENNqTf58kkOwSU/4G6RSpQrqAiuBWI32NVCANkc5QZ4L0Guk50gCpQZ3I1dRvVd3z3WGBO78khhtXKq4UJIP+qYuZPlz8tIX/3lg+ytgErsCzeds1RQ2347xvVmV3wvA27UfsgWGHJFHO5P9z9Xc+V+6MxAuXz3OrOYO9hgrk9oKz+35ZLGGjGXwTcSd4LMkfxC8eBdR8PvoG"
        },
        {"url": "https://puzz.link/p?lither/8/8/g02881d3667c63c338c6b086cid12185bd", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col, with_border=False))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(border_color_connected(puzzle.row, puzzle.col))
        self.add_program_line(not_single_tree(puzzle.row, puzzle.col))

        for r in range(puzzle.row + 1):
            for c in range(puzzle.col + 1):
                self.add_program_line(limit_adjacent_vertices(r, c))  # not very elegant, but works correctly

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
            self.add_program_line(count_adjacent_edges(int(num), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
