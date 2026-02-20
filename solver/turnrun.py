"""The Turn and Run solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, count_reachable_src
from noqx.rule.route import crossing_route_connected, directed_route, route_straight, route_turning


class TurnRunSolver(Solver):
    """The Turn and Run solver."""

    name = "Turn and Run"
    category = "route"
    aliases = ["turnandrun", "totsugekiloop"]
    examples = [
        {
            "data": "m=edit&p=7VXvT+JKFP3OX2Hmq5O8dvhhabLZIIKrDxEVwkJDSIEBqi3Dm7aoJf7v3juFlBYkTzf78j5sSm9Oz23v3DM/Dv4/oS05LcKVN6hGdbgYM9Rd0PC3vdpO4HLzhFbCYC4kAEpv63U6tV2f0+vevFEVleeLys+VEfT7+qUWXmndx/rj6b3395WTl3q9abRuWjcOm1V+VM/vSrXTUiv0OwFf3Xn6+WOn3562urMye601+4Wof6sVr/vTv1aVzrectelhkFtHZTOq0OjStAgjVN06GdDozlxHN2bUpNEDpAjVgWsA0gllAGsJ7Ko8ompM6hrg5gYD7AEcO3Ls8mEjZlqmFbUpwXHO1dcIiSdWnMSfqeex8EYOEq6z4BNHEpoH1g8n4incvAfFiBe6gTMWrpBIIvdGo4pqf1Niq6GYaDASDVB0owHRAQ0o7TdqKB/W8AZrcw8qhqaFgjoJNBL4YK4hNs01YTp+CcunxwtI8gyJ7wlRUARq2xDFEhKFLQGFdFWup2JdRaZiG0ajUV7FCxU1FYsqNtQ7NRW72IoBW96A0RjULTPKNOiNQbKqXimoWFKfnqGMTwnd7ZKwchkknFECkwvnznWCV1yuz3ZPdAOmomzA9i8psCvnSN8Wi883XsV/hwY5i3Rt14Xt0Qy9EZcnTSE9G5+rwlsK3wk4gWNJfOEO/VBO7TEf8hd7HBAzdobdTIpbqHopyhViiRvvQIVtipiBDDecM1sIyZNM5nU+mX1UCVMpMi41EnKSaekZxaekKMNMUfFBS1GBhFO082xLKZ5TjGcH8xQxsgMwWH/uLNOV+CIzl4GdbtF+sjOjecl0vOXIC1G3lacMF/SPhf5/LRTXSfuyv/yKC37d7qyoQcHYaHRLyTIc2kMQReC/mh5J9D6dgFKl0uEEuOFe4j+fI3XuhDzigUkySx9wQmCPmOFO9hD/gfHtZLP8nsths/tGB+wBrwM2a3dA7TsekHumB9wHvodVs9aHXWXdD4faM0AcatcDrUHuHQ==",
        },
        {
            "data": "m=edit&p=7ZZvb9owEMbf8ykqv62lxQkJIdI0UQpdO0ppC2IlQiiAgbQJZk5Cu6B+954duvyBtqq0TZ00hRyX38XnO4c8JvgROZxiooiPZmL4hqNMTHmqpiFPZXt03dCj1gGuReGCcXAwvmg28czxAorPbhatOqvdH9e+r81wMCAnSnSq9G+bt4dX/rdTV+Ok2TY7551zV53XvtaPLo3GodGJgl5I15c+ObrtDbqzTn9eVX822oNyPLhQ9LPB7NO61vtcsrc1DEubuGrFNRyfWDZSEZYnQUMcX1qb+NyK+zi+hhDCBFgLPIKwCm4jdfsyLrx6AokCfnvrg3sD7sTlE4+OWgnpWHbcxUjMcyRHCxf5bE1RMkxeT5g/dgXw3CWduhxhDWgQTdldtL0PkiE/8kJ3wjzGBRTsEcc1Wf42xXMPetqDmfYASbc9CG9PD6K1P9hDdX8Pj/BsrqCLkWWLhnqpa6butbUB27Y2yFDESB2GJg8QGXoBVCTQMsAsAEIqRaLKtFmiSfIlS4ozkaSYX/dAiUQWeiNtU1pV2i70gWNN2mNpFWl1aVvynoa0fWiyXK1gnRBkqRjpqoH1MkwEfkXTcUUzEl8xcEWBRlQYVJdDy9IaMmVFLNy7lvZ3Vf9KObaWSEX+0P89NizZqO94Hvz625E/pvygzbjviOs681cscEOKQHVQwLxREPGZM6Ej+uBMQmQlwpeN5NhS5sshj7GVeK/2ZHgOISvk0Za58yXjNI0UbqfT+UuZRCgHk1RjxqeFku5F87lW5J6QQ4mO5FDIQSQy1w7n7D5HfCdc5MDYCWH/CBbuKp+JLgtrGTr5Ep07pzCbny7HYwk9IHnaGjxQ7f8O8ZF3CPGclI8mZm+UY8ctsdNUsdhbcHyB0SoaOSNoDcEfEvxmuJ9K/HvDf30l5NvF+CtKlwaLeI/eAX1F8jLRffwFectEi3xHy0Sxu3IGdI+iAS2KGqBdXQO4I23AXlA3kbUocKKqosaJqXZkTkyVVTp7WHoC",
            "config": {"visit_all": True},
        },
    ]
    parameters = {"visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        if puzzle.param["visit_all"]:
            self.add_program_line("white(R, C) :- grid(R, C).")
        else:
            self.add_program_line(shade_c(color="white"))

        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(directed_route(color="white", crossing=True))
        self.add_program_line(crossing_route_connected(color="white", directed=True))
        self.add_program_line(route_turning(color="white", directed=True))
        self.add_program_line(route_straight(color="white", directed=True))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"white({r}, {c}).")
            self.add_program_line(f":- not turning({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(bulb_src_color_connected((r, c), color="straight", adj_type="line_directed"))
                self.add_program_line(
                    count_reachable_src(num, (r, c), main_type="bulb", color="straight", adj_type="line_directed")
                )

        crossing_points = set()
        for (r, c, d, label), draw in puzzle.line.items():
            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label == "normal" and draw:
                for _d in (Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT):
                    fail_false(puzzle.line.get(Point(r, c, _d)) is True, f"Invalid crossing mark at ({r}, {c}).")

                if (r, c) not in crossing_points:
                    self.add_program_line(f"crossing({r}, {c}).")
                    crossing_points.add((r, c))

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
