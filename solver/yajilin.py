"""The Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route
from noqx.rule.variety import yaji_count


class YajilinSolver(Solver):
    """The Yajilin solver."""

    name = "Yajilin"
    category = "route"
    aliases = ["yajirin"]
    examples = [
        {
            "data": "m=edit&p=7VVRb9MwEH7Pr5j8fA9x7GapX1AZKy+hA9ppQlEVpSXTIlIy0gZNrvrfuTunpIMUFW1CICHX5/N3Z/s+X3xdf2myOgfp009FgCM2LSPuQRRy99s2KzZlbs5g1GzuqhoVgKvxGG6zcp2Dl7Ruc29rh8aOwL42iQgEcJdiDvad2do3xk7BTtEkIEIsRk0KCFC97NQbtpN24UDpoz5xG0pUP6C6LOplmaexQ96axM5A0DkveTWpYlV9zYXbgufLarUoCFhkG2SzvivuW8u6+Vh9alpfSUubclMsq7KqBe8n5zuwI0ch3lPQHQXVUVDfKah+CsFzUCiLz/lDX/TD/uh3mJn3GH9qEqJy3alRp07NVgykMBGIUPEQ+TwMAx6k71ApB25ULa41jjtiuBXKp0Nf4KmUfYyGdsTQUtlBtHsiVKo6KPKd1wFEp5LXwUKOAG8xDQ4wiuZHTLVr/QOMoiS/QywcPIoWOUiz3VGCSI5ZBixneEdgFctXLH2WA5Yx+1yyvGF5wVKzDNnnnG751DzoUBjtrvQpQQkd4E0MKaMycorWoJG1AqGk006MPFGuRjxug38Pm3uJmDb1bbbM8QnF+JTOJlW9ykqcTZrVIq/3cyxoO088CO6JogL5v8b9vTWOsuSf+MKe/rae58En+L3oEOwViPsmzVLkJPCfFH6Jnx/Bo9/Ej+3Te268rx1HjK6c9Bux+vQbsD79ZPjjGcLaNve+AQ==",
        },
        {
            "data": "m=edit&p=7ZZLU9swEMfv+RSMzjroacm+AYVeKH1Ap8N4MkwAU9ImNXWSPpzJd+9qtVh1oDTp9EBnOsbaH+v16r96xJp9XoyaiksV/rTngku4TG7w1s7iLeg6Hc8nVbHDdxfzm7oB4Pzl4SG/Hk1mFR+UFDYcLNu8aHd5+7womWScKbglG/L2dbFsXxTtGW9P4BHjGnxHMUgBHiR8h88D7UenFMDHxIBngKOmqb+eX9eLprp6X53vxRdeFWV7ylnobw+zBGTT+kvFSE/4/7KeXoyD42I0h6pmN+NbejJbXNUfF6zrik0Xk/n4sp7UDcN8crji7S6WQmnu6pGpHp3q0V09+uF61N+s5/vow3gy/oSd9WvJH65lBfP1Bqo5L8pQ2NuEPuFJsWTWsEJz5hQab9HkAo0UmqyPVmbRKhmtNmTzaI2L1sZsMovppKN8PuZTIry/CkMVBZRMgOq4nlBKHE1yBFE9R5DXc6DQMizJ5PHrMUF836PN+luhkH5MKKnvyez6W+6eHq/XPFhyyfSdB4qXxXIVlggNAe402W1LWEkPL504PqVIkeGtX0bj4G0cjSNb9nQ8Eh2HfYtwv1U4TljZE/5YuDbbhedbicF1sHl4ZrcS48Q2KyAur43D49rbUAwsyUNcmArbU/il4K3G9hm2AluL7RHGHMASVrnmKocZUBxZixwZLNdSkN90rKUEVomVi6wcsCe/SqwgjxaJjY1s4GtmsshaJDaQx/jEmY6cgbbMkN8nVqBN2cSG+jIhpyS/TWxAm9GJLfVlIael2o1OnEGeTCZ2pNNlwFR7JhM7yOPyxDS2OoxhTjpdntiCNpsldtSXCzlpnG2W2IE2ZxJ76suHnFS7M4lzyJOrjo2IOsECU+256tjAvBuaa2QaW7DAUSc871h70OZdx0YoejfkpHH2rmMj4DQjbGJFfamQU5LfJlaQR+nEmnTC+cjonPw6Mcy7oblGprEFC0y1G0m8CmeBsBX2sTXYZrhFXPjUbvgxjl/Enz8Nf7Ybfyun1AbPhPcv+98fruGgZMeL6UXV7BzXzXQ0gQPZyc3otgK7X09v69l4XjE4FK8G7BvDu9Twq6r/n5P/tXNymDvx1DboU5MDPxnDwQ8=",
        },
        {
            "url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y",
            "test": False,
        },
        {
            "url": "https://puzz.link/p?yajilin/b/16/16/0.210.0.0.0.0.220.0.0.0.0.0.0.0.42n0.0.n0.0.b0.a0.c0.a0.c0.0.a41e0.f0.0.f0.e31a0.0.c41a31c21a21b0.0.n0.0.n0.0.b11a2.c0.a0.c0.0.a41e0.f0.0.f0.e31a0.0.c11a11c0.a0.b0.0.n0.0.n320.0.0.0.0.0.0.0.120.0.0.0.0.110.",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(fill_line(color="not black"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="not black", adj_type="line"))
        self.add_program_line(single_route(color="not black"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(f"hole({r}, {c}).")

            # empty clue or space or question mark clue (for compatibility)
            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
                continue

            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(yaji_count(int(clue), (r, c), arrow_direction, color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black({r}, {c}).")

            if color == Color.GRAY:
                self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
