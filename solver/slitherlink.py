"""The Slitherlink solver."""

from typing import Tuple

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import direction, display, fill_path, grid, shade_c
from noqx.rule.helper import fail_false, target_encode, validate_direction, validate_type
from noqx.rule.loop import convert_direction_to_edge, separate_item_from_loop, single_loop
from noqx.rule.neighbor import adjacent, count_adjacent_edges
from noqx.rule.reachable import grid_color_connected


def passed_vertex() -> str:
    """Generate a rule to get the cell that passed by the loop."""
    rule = "passed_vertex(R, C) :- edge_top(R, C).\n"
    rule += "passed_vertex(R, C) :- edge_left(R, C).\n"
    rule += "passed_vertex(R, C) :- grid(R, C), edge_top(R, C - 1).\n"
    rule += "passed_vertex(R, C) :- grid(R, C), edge_left(R - 1, C).\n"
    return rule.strip()


def count_adjacent_vertices(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Return a rule that counts the adjacent vertices around a cell.

    An edge rule should be defined first.
    """
    src_r, src_c = src_cell
    rop, num = target_encode(target)
    v_1 = f"passed_vertex({src_r}, {src_c})"
    v_2 = f"passed_vertex({src_r + 1}, {src_c})"
    v_3 = f"passed_vertex({src_r}, {src_c + 1})"
    v_4 = f"passed_vertex({src_r + 1}, {src_c + 1})"
    return f":- {{ {v_1}; {v_2}; {v_3}; {v_4} }} {rop} {num}."


def count_adjacent_segments(target: int, src_cell: Tuple[int, int]) -> str:
    """
    Return a rule that counts the adjacent segments around a cell.

    An edge rule should be defined first.
    """
    rop, num = target_encode(target)

    # segment count = vertex count - edge count
    vertex_count = count_adjacent_vertices(target, src_cell).replace(f"{rop} {num}.", "= C1").replace(":-", "").strip()
    edge_count = count_adjacent_edges(target, src_cell).replace(f"{rop} {num}.", "= C2").replace(":-", "").strip()
    return f":- { vertex_count }, { edge_count }, C1 - C2 {rop} {num}."


class SlitherlinkSolver(Solver):
    """The Slitherlink solver."""

    name = "Slitherlink"
    category = "loop"
    aliases = ["slither", "touchslither", "vertexslither", "sheepwolfslither"]
    examples = [
        {
            "data": "m=edit&p=7VRNb9pAEL3zK6I978Efa7B9oyn0Qp22oYoiy0KGuMWKqVODq2gR/z1vxqaLVUdRRcWpMh692fdmmZ3Z8fZnnVaZHOFRnrSkjccdWvw2v+Mzz3dFFl7Jcb1blxWAlDfTqfyWFttsELeqZLDXQajHUn8IY+EKKWy8jkik/hzu9cdQR1LfghLSxtoMCAIHcGLgHfOErptF2wKOWgx4D7jKq1WRLWbNyqcw1nMp6H/ecTRBsSl/ZaIJY39VbpY5LSzTHQ6zXedPLbOtH8rHutXayUHqcZPupCdd16RLsEmXUE+6dIqz080evmfPfZkGyeGAin9BroswprS/GugbeBvuYaNwLxwPoS6ajHDs5gRwqeeN6xLrGHcIl+5E6466bDdWWR2xsjtiRbFG7HXZIW1lshq5XZdYI/bpj8xWPm1lxD7FnrCq63aPH1CsYYPT46NgNpftnu2UrcN2jqpK7bJ9z9Zi67GdsWbC9o7tNVvFdsiaEfXlrzp3fjroPc4X+Oicj8YSsF0lbYVVt8V0ARh7WIeIsDpq3jxP7EB68mCTf+0lg1hMMA5XUVlt0gJDEdWbZVYdfXyADgPxLPjlTqv/36TLf5Oo+taF7/e54xajsL8nQuobKZ7qRbpYlbhlqJ6hMSSv0s3c9NOYv34C8/jahu3w/UFfvHaYbrEt8t06q4r8x6NIBi8=",
        },
        {
            "data": "m=edit&p=7VVNb9NAEL37V1R73sPO+iO2b21JuIRASVBUWVaVpIZGJArkA1WO8t87+5zAegLlgEBIoI1Hk+eZ5zezX5vPu8m60hmPKNZGE48oNnjSyP3McYzm20WVX+jL3fZhtWZH69e9nn4/WWyqoDhGlcG+zvL6Rtcv80KFSivix6pS1zf5vn6V1wNdD/mV0sRYnz0OCNntNq5ld4z3DrxuIg27g+a9y7pldzZfzxbVXb/JeJMX9Ugr95krpDhXLVdfKtWk4f9stZzOHTCdbLmWzcP80/HNZne/+rg7xlJ50PVlo7b7vFrnPqfWaftltdX9h+rxe0Kz8nDgfr9lqXd54VS/++YO8z3bQb5XNnXxPBfkZoNJbHaq9AiE5ICh0ukJCCUQy5REABE4rAdYB4xdQ04IWP2cjgQgtZUDrZ74WCqJocSPAKtPEoPW0xaD1Q9JjAhJZD0JaL2eJGckHUnSQQ98AC1o5aAejzZFjldgGskIWXEmpysDqf+ZTM5Xhp74wFk5ZOS6ICNnjIxcXWTOiQiNMV4QgbodJJtFhLpaCLh9xIK6RWTl1JGVi4Ys+tFOO6stPFPUbIwWIuePQrlQKJQbjqJ2Q3inEvbrLWwP1sKOeDvrOoR9AWtgY9g+YrqwY9hr2Ag2QUwHNj0dDT8+Mr6GeKfHb1d2CAqb4trxR/x3IWVQqC4fwxeD1Xo5WfBhPNgtp9X69J+vvUOgHhWewmob84Xw/yr8w1eha775+YX4T282XqdFGTwB",
            "config": {"swslither": True},
        },
        {
            "data": "m=edit&p=7VTLbtswELzrK4o98yDqYVO8uW7ci5s+7CIIBCFwHKYWIlepHkVAw/+e3ZUAmkGAoijQ+lDQGsxyZ8kR12L7o980RmQ4YiVCIXHEKuRHJfQLx7Euu8roN2LWd7u6QSLEx8VC3G+q1gT5qCqCg820nQn7XucQgwCJTwSFsJ/1wX7QsK33tyUIu8I8CImJJTJURUgvHL3iPLH5MClD5JcjR3qNdFs228rcLIeZTzq3awG02VuuJgr7+qeBoYzjwQBO3G46fKN2Vz6Omba/qx/6USuLo7CzX3iOnWeig2dir3imV/ljz+bum3l6zW5WHI949l/Q8I3OyftXR5WjK31AvNQHiDIsjbDdWI6rxSmG1P0hTGIMYxe+yE692pSyTpxS1olT2shlJ9Krnfjiqb+R8sXKd6X8fRUt5cKMxK4287My9JeWofJ2ljLy4+hlnJysh2cq+WSvGReMEeMaD17YmPEdY8iYMi5Zc8F4xThnTBgnrJlS636ruX/BTh4pvixOR3peM0WQw6pv7jdbg5/MvN4/1m3ZGcBL6hjAE/DDLUz+31v/8t6iPoTn9gc/Nzv4yUFbld3ONFX5/QGK4Bk=",
            "config": {"tslither": True},
        },
        {
            "data": "m=edit&p=7VRdb5swFH3nV1R+9gOYr+K3rCN7ydhHM1UVQhFJvQUVxsbHVBnx33vvhc5Bysu0qcrD5HB0jn0Mx9eO25993igeQvN8bnMHmhvY9Ey/l7YtulLJK77qu2PdAOH8w3rNv+Zlq6x0dmXWoCOpV1y/kylzGWcOPIJlXH+Sg34vdcL1LQwx7kDfBhgYBNDY0DsaR3YzdTo28GTmQO+BHormUKrdZur5KFO95Qy/84ZmI2VV/UuxaRrpQ13tC+zY5x0spj0WP+aRtn+oH/vZ62Qj16spbnwmrmviIp3iIjsTF1fx13HVwzf1dC5plI0jVPwzZN3JFGN/MfTa0Fs5ACZyYMKDqQI2GabD20QAEvd8ltcL6doLs4fmE4lmI300m7m+AOn9lsHSHKLZNXJpDjGkkRGaTySazasiNJvvRqcrgkU7tPR7wjWhINxCZbh2Cd8S2oQ+4YY8MeEd4Q2hRxiQJ8Ta/lH1XyFOKrBQpvn/XmVWymI4kVdJ3VR5Cecy6au9al403AGjxZ4YPbTJ3v9r4fWvBay+fWnH89LiwB+GtWXRHVVTFt8fWWY9Aw==",
            "config": {"vslither": True},
        },
        {
            "url": "http://pzv.jp/p.html?slither/25/15/i5di5di6bg3ad13dc13bd3cg5bi7ci7dhai6bi6ci7b02bd33cc23d8ci8ai6cibh6di6bi7dg1ca31ab10dc3dg6bi6ai6chai7ci7ci8d33dc33cc20d8bi7di7cidh8di5ci6cg3dd03cb02ad3dg6bi7ci6bg",
            "test": False,
        },
    ]
    parameters = {
        "swslither": {"name": "Sheep/Wolf Variant", "type": "checkbox", "default": False},
        "tslither": {"name": "Touch Variant", "type": "checkbox", "default": False},
        "vslither": {"name": "Vertex Variant", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row + 1, puzzle.col + 1))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="slither"))
        self.add_program_line(fill_path(color="slither"))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="slither", adj_type="loop"))
        self.add_program_line(single_loop(color="slither"))
        self.add_program_line(convert_direction_to_edge())

        if puzzle.param["vslither"] or puzzle.param["tslither"]:
            self.add_program_line(passed_vertex())

        if puzzle.param["swslither"]:
            self.add_program_line(separate_item_from_loop(inside_item="sheep", outside_item="wolf"))

        for (r, c, d, pos), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if puzzle.param["swslither"] and clue == "W":
                self.add_program_line(f"wolf({r}, {c}).")
            elif puzzle.param["swslither"] and clue == "S":
                self.add_program_line(f"sheep({r}, {c}).")
            else:
                fail_false(isinstance(clue, int), "Clue should be an integer or wolf/sheep with varient enabled.")

                if puzzle.param["vslither"]:
                    self.add_program_line(count_adjacent_vertices(int(clue), (r, c)))
                elif puzzle.param["tslither"]:
                    self.add_program_line(count_adjacent_segments(int(clue), (r, c)))
                else:
                    self.add_program_line(count_adjacent_edges(int(clue), (r, c)))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f":-{' not' * draw} edge_{d.value}({r}, {c}).")

        self.add_program_line(display(item="edge_top", size=2))
        self.add_program_line(display(item="edge_left", size=2))

        return self.program
