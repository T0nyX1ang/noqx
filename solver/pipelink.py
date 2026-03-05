"""The Pipe Link solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.route import crossing_route_connected, route_crossing, single_route
from noqx.rule.variety import straight_at_ice


class PipeLinkSolver(Solver):
    """The Pipe Link solver."""

    name = "Pipe Link"
    category = "route"
    aliases = ["pipelinkr", "pipelinkreturns"]
    examples = [
        {
            "data": "m=edit&p=7Zbfb9owEMff+SsqP9+DfzvOG+vGXli7rUxVFSFEaaZGC0sHZJqC+N93dpwflVo0Koo2aQo+Pvic+L5nm8v6RzlfpcCo+4gI8BsvySLfeKR9o+GaZJs8jc9gWG7uixUCwOVoBF/n+TqFQRKGTQfbysbVEKr3cUI4Ad8YmUL1Kd5WH+JqDNUVuggw7BsjKQIc8R0iq/Ha+x2d152MIl8ERrxBXGSrRZ7OxnXPxzipJkDcPG/83Q7JsviZkvo2/3tRLG8z13E736Ca9X32EDzr8q74VpJ2CrIs8022KPJiRUK0O6iGz0sQnQTRShBPS+CvL8E+LWGHy/MZRczixOn50mHU4VW83blYnWXe3ng78pZ7O8GhUAlv33pLvVXejuMtEQo0FyTm4FBy41HaRyhZg1roDsMAjSg6lB4VQ7QNSlkP0BpRNqhV6OWgpW1RUY9Ggta8QanriSMD2sgOVYNSd2jqhzFKkaOObf04xi0YpntsWla0x7zWzaQEI/rMW1a8xyE5TFMw0rSsRIgB89NnE3LFmMF5bcuGqhAz6ra6ZR3it5hQbRvUQa2JMF+qQanq+ywuqhEtRiEqioOt6rFuWUYdK0pDNnBKa1s2NKgQAgynPW6yhFkN+8Ox8jto586e25bX3p57K73VfkMat7NPt/clx/zb6A/DSkT9z/v4Uv9e33SQkHH2PT27KFbLeU6wGOwG5BfxLRGuuPyvD395fXBLRU92Uo5zcBPMOB45qC6BPJSz+QxFEXwXgaM71MGOU0QlDnRgKT3QccRwCdYziQfiJU6sM/r0TvcSss/L94h5uXf/k5+J6uQHE6vXdPAb",
        },
        {
            "data": "m=edit&p=7ZVZi9swEMff8ykWPc+Dbkt+S7dNX9LtkZRlMWHJpi4xdeptjlIc/N07knwtaKEtFFIojsa//DWSZnRYh2+n9T4HRt1PGMA3PpIZX7jRvtD2WRbHMk+vYHo6bqs9AsDb2Qw+r8tDDpOsdVtNzrVN6ynUr9OMcAK+MLKC+n16rt+k9RzqBVYRYKjNkRQBjvgKkQW89fWOroPIKPJNy4h3iJtivynz+3lQ3qVZvQTixnnhWzsku+p7TkIz/39T7R4KJzysj5jNYVs8tjWH06fqy4n0Q5DdqTwWm6qs9qSNtoF6+nwKYkhB9CmIeAr876dg4yk0uDwfMIn7NHP5fBzQDLhIz42L1Vnm7V16JonEXhg8DZokKqqaqGpjqkliqmVRNRoDo1FnRp/xjgbHmI7L0fAYp3E5EgnO38zPIvd2iZMMtfD2pbfUW+XtHGdaKtBCkJSDQymSgAmqckDlUTPQ0nQoVWiWCETWodYBGeWgjR3Y0sCCQcLMiG3Pio6Yh96ZFMis50R0rJHFiGXLBln1rLhu+0Sfrk/PrT+1GJvuWdEufszbyhGrnqUZse1y1OgjRix7lmbENuRuOciE9th6GDettsck9Kdw+oTtUMrgq3A1hBnQdij5gDL0oHGNJOtQKzdw474hbpPcenvtrfRW++2RuBP6x2f4d3fiL4aTiXBzPH3Uv6etJhmZF1/zq5tqv1uX+F1dbNePOcFLrZmQH8SXTAB3rv/vuYu+59xS0Us7KZcWDp7d1eQn",
            "config": {"pipelinkr": True},
        },
    ]
    parameters = {
        "pipelinkr": {"name": "Pipelink Returns", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", crossing=True))
        self.add_program_line(crossing_route_connected(color="grid"))

        if puzzle.param["pipelinkr"]:
            for (r, c, d, label), symbol_name in puzzle.symbol.items():
                validate_direction(r, c, d)
                validate_type(label, "normal")
                validate_type(symbol_name, "circle_L__1")
                self.add_program_line(f"ice({r}, {c}).")

            self.add_program_line(shade_c(color="crossing", _from="ice"))
            self.add_program_line(straight_at_ice(color="grid"))
        else:
            self.add_program_line(route_crossing(color="grid"))

        crossing_points = set()
        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")

            if not draw:
                self.add_program_line(f':- line_io({r}, {c}, "{d}").')

            else:
                cnt = 0
                for d in (Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT):
                    if puzzle.line.get(Point(r, c, d)) is True:
                        self.add_program_line(f'line_io({r}, {c}, "{d}").')
                        cnt += 1
                    else:
                        self.add_program_line(f'not line_io({r}, {c}, "{d}").')

                if cnt == 4 and (r, c) not in crossing_points and puzzle.param["pipelinkr"]:
                    self.add_program_line(f"crossing({r}, {c}).")
                    crossing_points.add((r, c))

        self.add_program_line(display(item="line_io", size=3))

        return self.program
