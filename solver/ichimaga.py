"""The Ichimaga solver."""

from typing import Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import tag_encode, target_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import convert_line_to_edge, crossing_route_connected, route_crossing, route_turning, single_route


def limit_turning(color: str) -> str:
    """A rule to limit the number of turning points in the route."""
    tag = tag_encode("reachable", "turning", "branch", "adj", "line", color)
    rule = f"{tag}(R, C, R, C) :- grid(R, C), turning(R, C), not intersect(R, C).\n"
    rule += f"{tag}(R0, C0, R, C) :- {tag}(R0, C0, R1, C1), {color}(R, C), grid(R1, C1), not intersect(R1, C1), adj_line(R, C, R1, C1), (R - R0) * (C - C0) = 0.\n"
    rule += f":- turning(R, C), not intersect(R, C), turning(R1, C1), not intersect(R1, C1), {tag}(R, C, R1, C1), (R, C) < (R1, C1)."
    return rule


def bulb_src_color_connected(src_cell: Tuple[int, int], color: str = "black") -> str:
    """A rule to collect all the color cells that are orthogonally connected to a source cell in a grid.

    This rule is specially designed for magnetic ichimaga.
    """
    r, c = src_cell
    tag = tag_encode("reachable", "bulb", "src", "adj", "line", color)
    rule = f"{tag}({r}, {c}, {r}, {c}).\n"
    rule += f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, {r}, {c}), {color}(R, C), adj_line(R, C, {r}, {c}), (R - {r}) * (C - {c}) == 0."  # initial propagation manually
    rule += f"{tag}({r}, {c}, R, C) :- {tag}({r}, {c}, R1, C1), {color}(R, C), grid(R1, C1), not intersect(R1, C1), adj_line(R, C, R1, C1), (R - {r}) * (C - {c}) == 0."
    return rule


def avoid_magnetic(color: str) -> str:
    """A rule to avoid two connected clues have the same number."""
    tag = tag_encode("reachable", "turning", "branch", "adj", "line", color)
    tag_st = tag_encode("reachable", "bulb", "src", "adj", "line", color)
    rule = f"connected(R0, C0, R1, C1) :- turning(R, C), not intersect(R, C), intersect(R0, C0), intersect(R1, C1), {tag}(R, C, R0, C0), {tag}(R, C, R1, C1), (R0, C0) < (R1, C1).\n"
    rule += (
        f"connected(R0, C0, R1, C1) :- intersect(R0, C0), intersect(R1, C1), {tag_st}(R0, C0, R1, C1), (R0, C0) < (R1, C1).\n"
    )
    rule += ":- connected(R0, C0, R1, C1), number(R0, C0, N), number(R1, C1, N)."
    return rule


def count_edges_around_vertex(target: Union[int, Tuple[str, int]], src_cell: Tuple[int, int]) -> str:
    """A rule to compare the number of the edges around a vertex to a specified target."""
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f'edge({src_r}, {src_c}, "{Direction.LEFT}")'
    v_2 = f'edge({src_r - 1}, {src_c}, "{Direction.LEFT}")'
    h_1 = f'edge({src_r}, {src_c}, "{Direction.TOP}")'
    h_2 = f'edge({src_r}, {src_c - 1}, "{Direction.TOP}")'
    return f":- {{ {v_1}; {v_2}; {h_1}; {h_2} }} {rop} {num}."


class IchimagaSolver(Solver):
    """The Ichimaga solver."""

    name = "Ichimaga"
    category = "route"
    aliases = ["ichimaga", "ichimagam", "ichimagax"]
    examples = [
        {
            "data": "m=edit&p=7VVLb5tAEL7zK6w9z2EfgIGbm7q9uKRtXEURQhZ2aIMKIsWmitbiv3d2ICJAoqZyZfVQrXb0zc5jd5gH+x91UqXg4VIecBC4lC1pS+7T5t1aZ4c8DWawqA93ZYUA4DKEr0m+T8GKOq3YOmo/0AvQ74OISQbdjkF/Co76Q6BD0FcoYiBiYEWdH7JdmZcVezzTK0SCgUS47OE1yQ26aA8FRxy22EV4g3CXVbs83axaRx+DSK+BmbvfkLWBrCh/pqw1I35XFtvMHGyTAwa4v8vuGSgU7Ovb8nvdqYq4Ab1oI1i+MgLVRWC3sI1APR+B/BsRpLff0odnHu/HTYN5+YzP3wSRieRLD70eXgXHxrzoyITjoa0AF9Ae3QmXj3iJvHzC2+auGetP5sZCPeHnYw1PTE7U8BZvYuOryYk7sJF87BVreKghxl6llEMN6Yw11MSrcoY2auLVFkMNe/hNpWOP+FEkoxzIQQ4wUYLSdUP0HVFJdI3ZBK2IviXKiTpEV6SzJHpN9IKoTdQlnbmphz+qmNOfwxTHLPgeIFAtwCoEqiP127dG0qXh1S/nvHxsRWyJ/TcLy6pIcmzNsC62afXI42BsLPbAaGNfSGPyf1b+m7PS5Iifuf5PbccIvzV2zBzM7AZ9Cey+3iQb/NwMf8vwOnHbbyeIHf8U8YvOcSS8JJATwdkTg+Mntn4B",
        },
        {
            "data": "m=edit&p=7VVLb9swDL7nVxQ662A9Y/uWddkuWfZoiqIwjCJJvTWYA29OPBQO8t9HMelsEjl0xTDkUNgi+JkfaVI0rc3PZl4XUplwm1hGUsHljMalrMUVHa/ZalsW6YUcNduHqgZFyo9T+XVebgo5yI6sfLBrk7QdyfZ9mgkt5HHlsv2c7toPaTuV7RWYhFS5FOum3K6WVVnV4ulZOwFNCalBHXfqDdqDdnl4qCLQpwfdg3oL6nJVL8vibnII9CnN2pkU4d1v0DuoYl39KsTBDfGyWi9W4cFivoUCNw+rH0IaMGya++p7c6SqfC/b0aGC8TMrMF0F5k8F5nQF+l9UUNx/Kx5PJJ/k+z305Qukf5dmoZLrTo079Srd7UNGO2GUAl8tvQR/CGeUBqx62AE2HdZDyjeW2o2j/sZTvlWUb0M822GnKd9HNJ7XlO/Z+3xC/WMWLzaUH1tmH1J7wvgJ24+E8q2KSDyrLMOO8RMSz2rNcEz9NePj/vfi4X73sGV2y/J1tB/WaWZn+XpWnzfM7kh/7DBiOKb8mL0f+9OLz/pjY9pfm9Dvwyae2el+uUgzTPfHKZqPY/1z2L8+pvvpNJ0npw2p3xlF+WxenOnPFwypwlG9RfkOpUY5g0mWrUH5FmWE0qGcIGeM8gblJUqL0iNnGP4Ff/W3+A/pZMbj2XTqcq+Wl1jyQSbGcGBcTKt6PS/hLJk260VRP2E4yfcD8Shwwaevg8vr4X6eh3voUXRuQ3tu6cBvJB/8Bg==",
            "config": {"ichimagam": True},
        },
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I9z2G/wAs3N7VzcdyPuIoihCLboQkKiBabKlqL/97ZwQle1EN7aOVDtezTezszywzD7u57u25yiHEoAxwEDmU4TaPdw49jVezLPLmAabt/qhskAB/mc/i6Lnc5BOnRLQsONk7sFOxVkjLJ4DgzsJ+Sg71O7BLsDZoYiAxY1Zb7YluXdcNe1+wCmWAgkc4Gekt2xy77RcGRL3seIb1Dui2abZnfL/qNPiapXQFz735H0Y6yqv6Rsz6M9LauNoVb2Kz3WOHuqfjGQKFh1z7Uz+3RVWQd2Glfwew3K1BDBeqtAvUXK8gfHvOXXyQfZ12HffmM6d8nqavky0DNQG+SQ+cyOjBhQowVEAHG43bCGF/HErU80RPU6k1Lzj1/yaWvBff9hfLt0n+fVKP9VOTHK+NrPfLXwstXaj2yx6j1oMORfxj6OtK+fxT7+01G/pPR/rHy840jL17R95MnWo+0X7/ip98LmyiolXeEc0JJuMJOg1WE7wk5YUi4IJ8Z4S3hJaEmjMhn4v6VP/qb/kE6qTR0dZ2O8LxWsiBlMzygF8u6qdYlnt1lW23y5lXjzdkF7IXRxNZKF/L/Mj3Py9T1iJ/bITi3dPBYZsFP",
            "config": {"ichimagax": True},
        },
        {"url": "https://puzz.link/p?ichimaga/14/10/cdlcicdehcg2ddkbhddgdhbjbhcbcj8bg6bbjdhbgcgbbi6cgcbc", "test": False},
    ]
    parameters = {
        "ichimagam": {"name": "Magnetic", "type": "checkbox", "default": False},
        "ichimagax": {"name": "Crossing", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="intersect"))
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="white", crossing=bool(puzzle.param["ichimagax"])))
        self.add_program_line(route_turning(color="white"))
        self.add_program_line(convert_line_to_edge())
        self.add_program_line(limit_turning(color="white"))

        if puzzle.param["ichimagax"]:
            self.add_program_line(route_crossing(color="not intersect"))
            self.add_program_line(crossing_route_connected(color="white"))
        else:
            self.add_program_line(grid_color_connected(color="white", adj_type="line"))

        if puzzle.param["ichimagam"]:
            self.add_program_line(avoid_magnetic(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d, Direction.TOP_LEFT)
            validate_type(label, "normal")
            self.add_program_line(f"pass_by_route({r}, {c}).")
            self.add_program_line(f"intersect({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_edges_around_vertex(num, (r, c)))
                if puzzle.param["ichimagam"]:
                    self.add_program_line(f"number({r}, {c}, {num}).")
                    self.add_program_line(bulb_src_color_connected(color="white", src_cell=(r, c)))
            else:
                self.add_program_line(count_edges_around_vertex(("gt", 0), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
