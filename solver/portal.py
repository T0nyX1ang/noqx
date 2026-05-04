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
            "data": "m=edit&p=7VZLb9swDL7nVxQ882BJji37lnXNLlm6LRmKwQgCJ3NRY87cOfFQKMh/H0W5teMFWPbCNmBQRFIfKZmfHkS2n+q0ylB49qc0kqbmC81d6oC717R5viuy+AJH9e6urMhAvB6P8TYtthkOkiZsMdibKDYjNC/iBCQgdwELNK/jvXkZmymaGbkAfcImZAlASeZVa96w31qXDhQe2VNnB2S+I3OdV+siW07IS8irODFzBPudZzzbmrApP2fgpvF4XW5WuQVW6Y7YbO/y+8azrd+XH+omVtipdbHL12VRVsDricUBzchRmJygoFoK6omC+o0Uivxj9nAq++h09gc6mTeU/zJOLJW3ralbcxbvIZQQ+wihYqUDp0JWwtONjpyWstE2+mAZ7kFJcGcfuJMHFVpAtcBQN7k+AgFH+C0Q+i7xp/HQjocdIOgF8Aq6A+heQHQ81rr3yUgdBwhP9tIWXthjJkQvDSE4JOwiuh8S9dgL6fVCpLBA0EV0j59wu9rZEuG2tfvtQB2tQwck4v3B3j4rxywlyzldADSK5XOWHsshywnHXLG8YXnJ0mcZcExor9CZl8zdlJ9JBwJ7zSKN4PtoiaszE0yUq3PHbfjvYYtBArO6uk3XGZWBCZWDi2lZbdKCRtN6s8qqxzEV5cMAHoB7olDayf/r9N9ap+0ped/1kHrV8M8/84T2HiIfIypP5hrhvl6mS+IJ9A8Bv+2kJ+3/sJOKwWknVYyvHL+sHp27b1SAFoMv",
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
