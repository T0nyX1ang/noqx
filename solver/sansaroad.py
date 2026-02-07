"""The Sansa Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.neighbor import adjacent, count_adjacent, count_covering
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.shape import avoid_rect


class SansaRoadSolver(Solver):
    """The Sansa Road solver."""

    name = "Sansa Road"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7Zbfb7pIEMDf/Ssu+9pNjuWH/EjuwVrba0+trRpPCTGoqLQgHoL2MP7vnV1oFFia5vL93t1Dg0yGz6yzM7PsLLu/Yjt0MBHpT9KwgAlcsi6zW1IVdgvZNXAjzzF+wY04WgchKBg/dvHS9nYOfhiv282gcbhp/LnXosmE3AnxvTB6uX25evb/uHelkNx2tV6n13HFVeP35vVTvXVV78W7YeTsn3xy/TKcDJa90UoX/251J3IyeRSUh8ny131j+FvNzEKwasdEN5IGTu4MExGEkQg3QRZOnoxj0jGSMU76YEJYszDyYy9y54EXhIgxAuPa6R9FUFtndcTsVGumkAigdzMd1DGoUegugsNm2klH9gwzGWBEJ79mf6cq8oO9Q2ejwdHneeDPXApmdgTl263dLcISGHbxIniNs6HEOuGkkabQ/2IK4OQjBaqmKVCNkwKNl6Ywd8O550zbqaMfmYFunU6wOs+Qw9QwaTrDs6qd1b5xBNllkjA5No5IkcANwYUSI6XOxRp/NBEVPpcIn6sil4tCBSd8/6IupDyrbr+fckmgXCxzIlfwLN0il7N8i1zRKrjO969W+FEr4lFpPDyu8v1olCscTuPkcJ2uC8e/ntW/xPn1kdl6lf3LIt+/LPLzlSV+vrLCX0e5zueKzM9XYW85h9dpPGWuCnQdOZy9P2WuEf68Gvf9hJ13y/afyOQAtidOJCZvmBSYVJhsszEtJkdMNpmUmayzMSrd4F9sAfBOIwMqp8AKaeV+8JNiMyWZHXDlS/nm9LJqJurH4dKeO9D8+2t76yA4c9Eu8Ka7lE+dN3seISM99i8tObaJ/ZkDZ9YF8oJg67kbnocPUw66q00QOlwThc5iVeWKmjiuZkG4KMR0sD0vnwv7IsqhdNfkEBwAuWc7DINDjvh2tM6Bi8Mz58nZFIoZ2fkQ7Ve7MJt/Lsepht4Qu00Jw1fc9wfS//sDia6U8I8/k/6blm1CwaFxJo8YbeOpPYVis3pRrpACl6x/PXq2J4LwkwZ1NhYxp00B/aRTXVh5vKIpXViLvNSBaLDlJgSU04eAFlsRoHI3AlhqSMAqehL1WmxLNKpiZ6JTlZoTneqyP5lW7R0=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_rect(2, 2, color="not gray"))
        self.add_program_line(fill_line(color="not gray"))
        self.add_program_line(single_route(color="not gray"))
        self.add_program_line(grid_color_connected(color="not gray", adj_type="line"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            target = 2 if d == Direction.TOP_LEFT else 1

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__1":
                self.add_program_line(count_covering(("lt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__2":
                self.add_program_line(count_covering(("gt", target), (r, c), d, color="gray"))

            if d in (Direction.TOP, Direction.LEFT, Direction.TOP_LEFT) and symbol_name == "circle_SS__5":
                self.add_program_line(count_covering(target, (r, c), d, color="gray"))

            if d == Direction.CENTER and symbol_name == "tridown_M__1":
                self.add_program_line(f"pass_by_route({r}, {c}).")
                self.add_program_line(count_adjacent(3, (r, c), color="not gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
