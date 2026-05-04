"""The Tentaisho (Spiral Galaxies) solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false, tag_encode
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_src_color_connected


def galaxy_constraint(glxr: int, glxc: int) -> str:
    """Generate a constraint for spiral galaxies."""
    r, c = (glxr - 1) // 2, (glxc - 1) // 2
    tag = tag_encode("reachable", "grid", "src", "adj", "edge")
    rule = f":- grid(R, C), {tag}({r}, {c}, R, C), not {tag}({r}, {c}, {glxr} - R - 1, {glxc} - C - 1)."
    rule += f':- grid(R, C), {tag}({r}, {c}, R, C), edge(R, C, "{Direction.TOP}"), not edge({glxr} - R, {glxc} - C - 1, "{Direction.TOP}").\n'
    rule += f':- grid(R, C), {tag}({r}, {c}, R, C), edge(R, C, "{Direction.LEFT}"), not edge({glxr} - R - 1, {glxc} - C, "{Direction.LEFT}").\n'
    return rule


class TentaishoSolver(Solver):
    """The Tentaisho (Spiral Galaxies) solver."""

    name = "Tentaisho"
    category = "region"
    aliases = ["spiralgalaxies"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb9owEH7nr6j87Af/TJy8sY7tpaPbwlShCKFA04EGCgMyTUH87zvbodnEuZ26qtOkKeTuy93l8vnss9l9rYttSTmzP2koaLgUN+4WJnI3a6/Rcr8q0wvar/eLaguA0ushvStWu7KXt0GT3qFJ0qZPm7dpTgSh7uZkQpsP6aF5lzZj2mTgIlSB7QoQJ1QAHHTwxvktuvRGzgAPWwxwDHC+3M5X5TTLvOl9mjcjSuyHXrnXLSTr6ltJ/HvueV6tZ0trmBV7GMxusdy0nl19W32pyekbR9r0Pd/BiS/v+MqOr7znK3G+4ln4lrefy109w8gmk+MRqv4R6E7T3DL/1EHTwSw9kIiTVFESCa+kV8qpuFWJU8Y4lfgQzkSrY6951GofzYVPzOVJt/GyfV/65FzZ+KMtzgEkd3IMxCTYc05/rhIUjmiBmiMGZnFu1qjZcDSJSdBoLvEsXEa4XUdoem6ri8UbjcZLhY9V2nlB7EoE7BLno4xC+WgRKH2gDjpQZR3jZY6EwCcrUM8oMN4oNrjd4HWLGc4z5jFujyWSB5bnG7dIhZMjaCXaSCdfO8mc1E5euZiBkzdOXjqpnIxcTGyb8Tfb9bxPnkaHaAYNkxiYJK5aIEwL7LKzQPKYStu+0mIDGBzy0ZHk0h8av17637NNejnJ6u1dMS9hlx3AfnsxrLbrYgVP2aLYlATOtmOPfCfuzqU9Kf8fd3/nuLMzwF64i/60qXNYCzzmtLmmZFNPi+m8grUFpXvAMYAFJeBfmGIk6E6okE90KyECDs1CCRWjQqtnTPjI+B783v2uFXT7jQx3w24YcLAAW9g2Aw51PvAXX3+wG096PwA=",
        },
        {
            "url": "https://puzz.link/p?tentaisho/19/22/hafheneweo2ffneneyerfgezy0eg4fifhafnezgfnfmegepel3epfzzt6989ezq7ehfehfwfnezk2dezq4b88fzveweofznfhefezzu54ffzzmedb4b3ezuejflexezg4fl7ezel72eregfztflefzzheifhbeztewen9ekejemer6eret8fpe",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))

        reachables = []
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            fail_false(symbol_name.startswith("circle_SS"), "Invalid symbol type.")

            if d == Direction.CENTER:
                reachables.append((r, c))
                self.add_program_line(galaxy_constraint(r * 2 + 1, c * 2 + 1))

            if d == Direction.TOP_LEFT:
                reachables.append((r - 1, c - 1))
                self.add_program_line(galaxy_constraint(r * 2, c * 2))
                self.add_program_line(f'not edge({r}, {c - 1}, "{Direction.TOP}").')
                self.add_program_line(f'not edge({r}, {c}, "{Direction.TOP}").')
                self.add_program_line(f'not edge({r - 1}, {c}, "{Direction.LEFT}").')
                self.add_program_line(f'not edge({r}, {c}, "{Direction.LEFT}").')

            if d == Direction.TOP:
                reachables.append((r - 1, c))
                self.add_program_line(galaxy_constraint(r * 2, c * 2 + 1))
                self.add_program_line(f'not edge({r}, {c}, "{Direction.TOP}").')

            if d == Direction.LEFT:
                reachables.append((r, c - 1))
                self.add_program_line(galaxy_constraint(r * 2 + 1, c * 2))
                self.add_program_line(f'not edge({r}, {c}, "{Direction.LEFT}").')

        fail_false(len(reachables) > 0, "Please provide at least one clue.")
        for r, c in reachables:
            excluded = [(r1, c1) for r1, c1 in reachables if (r1, c1) != (r, c)]
            self.add_program_line(grid_src_color_connected((r, c), exclude_cells=excluded, adj_type="edge", color=None))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        tag = tag_encode("reachable", "grid", "src", "adj", "edge")
        spawn_points = ", ".join(f"not {tag}({r}, {c}, R, C)" for r, c in reachables)
        self.add_program_line(f":- grid(R, C), not hole(R, C), {spawn_points}.")

        self.add_program_line(display(item="edge", size=3))

        return self.program
