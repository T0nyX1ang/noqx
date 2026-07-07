"""The Turn and Run solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c, shade_cc
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
            "data": "m=edit&p=7VXBbtswDL37KwqeebDl2LV9GbKu6SVLtzVDEBhB4KYuZkyuOsceNgX+95K0UxdYUCwdNuxQKCKeHyWKTxSR7bcmq3IMaPgRuujRUCqSOXL5tx/zotZ5coLjpv5iKgKIl5MJ3mZ6m6OT9stWzs7GiR2jvUhSUIAyPVih/Zjs7PvEztBekQvQI25KyANUBM8HuBA/o7OO9FzCsx4TXBLcFNVG5+tpx3xIUjtH4HPeym6GUJrvOXTb5HtjyuuCCV3c5TdFBegTu21uzNcGHsND2ei62BhtKugzbdGOJf0+xF5DMGiIBg3+owb/sAb1dzXEhzW0VJtPpGKdpCzo8wCjAV4lu5bz3IHyoCuh1xUQfMXEm4EYqf2l9UQQMjHaExTIk3BLsROxSuycTkPri30n1hUbiJ3KmnOxC04lolcZ0WmK4sYKlUu5qZbvlpeMxIay9ZRlHCX0aZag4pgknCLQ5VJr6KL+yeU6NnvwIrqKOKLnHwp4KueZvFPVtSCP4PfQyklhkWlNz2PWlNd5dTIzVZnx95kp7822qHOgtmwd+AEyUx8V73vt1P+3U7lO7ouf8Z8028u7KrVTpP5Be4lw36yzNYkC+kvAZxzLox0UKgwPO6jpfnH88zuiJl45Dw==",
        },
        {
            "data": "m=edit&p=7VVNb5tAEL3zK6I5z2E/vIC5VG4a5+I6beMKRciyiENVFCgpNlW1Fv+9swMNCYoaRWqjRKqWfTze7izzds14971J6wylcJcOke7UJjLkrkKfu+jbKt8XWXSEs2b/taqJIJ7N5/glLXYZekk/be0d7DSyM7SnUQIKkLuENdqP0cG+j2yM9pyGACVpC2ISUBE9GWjM444dd6IUxJc9J3pBdJvX2yLbLDrlQ5TYFYJ7z1uOdhTK6kcGXRg/b6vyMndCkX/LrvIaUJO6a66q6wZul4eyKfb5tiqqGvpMW7QzTr9f4rcHM3gIBw/61oN+2IP6tx6mD3to6Ww+kYtNlDhDnwcaDvQ8OrQuzwP4wkUaCu0OEHwzEgIW9B0hHAlSBmNFibGiWXlzVxm/Sfr351CKkhO9YJwzKsYV+UCrGd8xCkbDuOA5J4wxmZxMAzRSQqQQjPLRTATzQBsMtN9x4WMgyIhq3Wm60Amjz0sGbuOetLV/K/s/pJPo7mu+38zr09ZeAnFaFPTrXzblZVYfLau6TN3zcVXeVLt8nwFVndaDn8A90RSn/xeil1yI3DmJl/bNPJJOYheuoE3RlTC0Zwg3zSbdkDWg/z18dDgeKslTh599J6iArL1f",
            "config": {"visit_all": True},
        },
    ]
    parameters = {"visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["white"]) if puzzle.param["visit_all"] else shade_c(color="white"))
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
