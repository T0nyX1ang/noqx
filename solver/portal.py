"""The Portal Loop solver."""

from typing import Dict, List, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_straight, single_route


class PortalLoopSolver(Solver):
    """The Portal Loop solver."""

    name = "Portal Loop"
    category = "route"
    aliases = ["portalloop"]
    examples = [
        {
            "data": "m=edit&p=7VZtb+JGEP7Or4j2a1aq1zbGtnQfCAfppYSQC4gGCyFDDDhnY+oXkhrlv9/sLHdeGydN39RWqsCzs8+MZ2dml2dJfsnc2KNM4V/NpDDCR2cmPqpp4KMcPyM/DTz7jLazdBPFoFB60+vRlRskHr263/Q7UfvpY/vnvZlOp+xSyT4pk8fe4/nn8KdPvhaz3sAcXg+vfXXd/rFzcWt0z41hloxTb38bsovH8XS0Gk7WlvprdzDV8+mN0ryarn7Yt8cfGs4xh1njkFt23qb5pe0QlVB8GJnR/NY+5Nd2PqD5HZgI1QHrg8YIVUHtFuoE7VzrCJApoA+EboB6D+rSj5eBN++DFZCh7eQjSvg6F/g2V0kY7T0iXsP5MgoXPgcWbgqtSjb+7mhJsofoS3b0hYAkzILUX0ZBFHOQYy80b4sS+jUlaEUJXBUlcO3vKiHwt95zXfZWffYvsDOfIf+57fBSxoVqFuqdfSAtldg6JS0NB9MQQwsHppjH0RKjKpyZyr0hwAACaIDh3hti54kGLztEK4AmRBGdOAIGeugF0NJF4t/nTT5vSgDkVXLACKYE4BrSHDKW5ybapSUtKEF2YArWIaXNFFxEqoyxShqMoUtLRiqJMIaZSNUzVam4qIwDhoxgFKk+JroqtYSJtsprG1jT9ziwQcw+gLxH2UOpohzBAaC5hvIjSgVlE2UffbooJyg7KHWUBvq0+BF65yETJ+XPpEMMfswskxJdp7xw7Z0JOpog0fKn+d/DZg2H3GXxyl16QAN9oIOzQRSHbgCzQRYuvPjbHEiZJFEwT4T33Ht2lymxxb0gW0rYFmOUoCCKdpx3aiJ8M5VAf72NYq/WxEHvYf1aKG6qCbWI4odKTk9uEJRrwTuzBAmiLUFpDCwqzd04jp5KSOimmxIgXRqlSN620szULafofnErq4VFO14a5Jng42hU5dv6/w36b71B+S4pv4viKvfUP0/ADvSeWDq14OLIbyjZZXN3DnUS+O9Gf9sIZKv/YSPQdL0RuPzE8JfdFO/tG/4wo/gNliyMVbiGKwF9gy4lax3+CjNK1ip+QoM82VMmBLSGDAGt8iFAp5QI4AkrAvYKMfKoVW7kWVXpkS91wpB8KZkkHZL44S7wzngDyKzxFQ==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line(route_straight(color="grid"))

        all_src: List[Tuple[int, int]] = []
        locations: Dict[Union[int, str], List[Tuple[int, int]]] = {}
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if isinstance(clue, int):
                locations.setdefault(clue, [])
                locations[clue].append((r, c))
                all_src.append((r, c))
            else:
                self.add_program_line(f":- not straight({r}, {c}).")

        fail_false(len(locations) > 0, "No clues found.")
        for n, pair in locations.items():
            fail_false(len(pair) == 2, f"Portal {n} is unmatched.")
            r0, c0 = pair[0]
            r1, c1 = pair[1]
            self.add_program_line(f"dead_end({r0}, {c0}).")
            self.add_program_line(f"dead_end({r1}, {c1}).")
            self.add_program_line(f"adj_line({r0}, {c0}, {r1}, {c1}).")
            self.add_program_line(f"adj_line({r1}, {c1}, {r0}, {c0}).")

            # the momentum must be preserved
            self.add_program_line(f':- line_io({r0}, {c0}, "{Direction.LEFT}"), not line_io({r1}, {c1}, "{Direction.RIGHT}").')
            self.add_program_line(f':- line_io({r0}, {c0}, "{Direction.RIGHT}"), not line_io({r1}, {c1}, "{Direction.LEFT}").')
            self.add_program_line(f':- line_io({r0}, {c0}, "{Direction.TOP}"), not line_io({r1}, {c1}, "{Direction.BOTTOM}").')
            self.add_program_line(f':- line_io({r0}, {c0}, "{Direction.BOTTOM}"), not line_io({r1}, {c1}, "{Direction.TOP}").')

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
