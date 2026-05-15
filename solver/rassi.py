"""The Rassi Silai solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Point, Puzzle
from noqx.rule.common import area, count, defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_border, avoid_same_color_adjacent
from noqx.rule.reachable import area_color_connected
from noqx.rule.route import count_area_pass, single_route


class RassiSilaiSolver(Solver):
    """The Rassi Silai solver."""

    name = "Rassi Silai"
    category = "route"
    aliases = ["rassisilai"]
    examples = [
        {
            "data": "m=edit&p=7ZZNb9NAEIbv+RXVnufg/fDnLYSkl9ACCUKRFUUmdcHCwcWOUeUo/51312sbkaCWIioOyPLo8ezseuf17MjV1zopUwpwyYAc4rikEuYWTmhux17LbJ+n0QWN6/2nogQQXc9mdJvkVUqj2IatR4cmjJoxNZdRzAQjc3O2puZNdGheRc2UmgWGGPE1sV2d77NtkRcl63zNHMQZCeB0wPdmXNOkdXIHfGUZuAJus3Kbp5t563kdxc2SmH73CzNbI9sV31LWTjPP22L3IdOOMqmqrMryPMkYSYxU9U3xuWbdK47UjNsU5o9JQZlFuhRkn4I8n4L4+ymE6+MRn+ctkthEsc7n3YDBgIvowELOInXUuzvAcmNXxs6MFcYuMYEaaexLYx1jXWPnJmaK1biP2goEiwRqwXfBvmUPHLQcCOKhsizBrmXEhzY+8MGh5QD16bQcKrBnGD4SXFj2wO368JEQyjLmynauEIiXNl4gRtoYIcHtHhBLQtkYiRhlY6QLbvcm9Jlx7f51vj63jFPld7kjR19aRo5+F6/A7qCP7w06BJ0miAncPt9en1BrYjUMg14fkyPvGGdZOEOOQg45dpoIaCjcIUdpY6QcNJFq0ESBVcdaB6u/8npNeAh29N6Ouvx1OUyMVcZ6pkx8XXWPrMvTimScI6+YEyvuN5f2nP5WjTKlFYNyTKunV5Nt2T6451h4pmUOl/u8z+tRzBZ1eZtsU7SCefYlvbgqyl2S42l68/GHp0mxuyuqbJ8ydOjjiN0zc8f4tnqZ/037n27a+lM5Tz4iT2vaf3piYxRN3wCouSZ2V2+SDURn+E2gB4dX+iz+NCD0wLw/qOenecG5WWf8UvsXp371C7/bvh3t4uTFz649ms969B0="
        },
        {"url": "https://puzz.link/p?rassi/10/10/40a74aa64cki6kd0800u700v30oc3if00u3v00010100000000000000", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="dead_end"))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line("ox_G__1(R, C) :- dead_end(R, C).")
        self.add_program_line(area_color_connected(color="grid", adj_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="dead_end", adj_type=8))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(0, _id=i))

            if len(ar) == 1:
                fail_false(
                    puzzle.surface.get(Point(ar[0][0], ar[0][1], "center", "normal")) in Color.DARK,
                    "Single-cell area must be a hole.",
                )  # compatible with puzz.link
            else:
                self.add_program_line(count(2, color="dead_end", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "ox_G__1")
            self.add_program_line(f"dead_end({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="ox_G__1", size=2))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
