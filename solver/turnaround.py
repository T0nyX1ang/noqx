"""The Turnaround solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_turning, single_route


class TurnaroundSolver(Solver):
    """The Turnaround solver."""

    name = "Turnaround"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7Vbvb+JGEP3OX3Har1mpXhuIbamqCAfppYSQC4gGCyFDDDixcWpskhrlf8/s2JTdtYnu1JPaSpXxMLyZ3Zn9offY/pG6sUeZxj+GSeEbnjoz8dXNJr5a8Qz9JPDsT7SVJusoBofSm26XLt1g69Gr+3WvHbVePrd+35nJZMIutfSLNn7sPp59DX/74hsx6/bNwfXg2tdXrV/bF7fNzllzkG5Hibe7DdnF42gyXA7GK0v/s9Of1LPJjda4mix/2rVGP9ecoodpbZ9Zdtai2aXtEJ1QfBmZ0uzW3mfXdtan2R2ECDUA64HHCNXB7RzdMca5185BpoHfL3xw78Fd+PEi8Ga9HBnYTjakhNe5wNHcJWG080g+DH8vonDucyDwN95rAW7Th+gpLdJgLhKmQeIvoiCKOcixN5q18u57Fd1zl3cPK2XH9jla0T5P+FHtQwm5e6u6+zc4lK/Q/8x2+FJGR9c8unf2Hmzf3hND4yN/gaH5yRFDP+zOATA4wNd7AJpqxrmS0VCHNLGKCDAOaAKAZcUMnMMQALXKudqpiY0JGRZmCHNYamNMU1OYphZmmqUieilHN9WZSxvJSjvJjLqyDcxoqDl1dWdYo1SrgR2KSL6fYvV8Q//KgfNneAvu0XbR6miHcEloZqD9jFZD20Dbw5wO2jHaNto62ibmnPNr9l0X8e+0Q+r8PCyTXxpYNncMYFC4YgZ6ddhl4xt7diCf0678NP572LTmkB5Qx6d+FIduAKzST8O5Fx9+A3mTbRTMtmm8dBfezHt1Fwmxc/0QIxK2wTkkKIiiZ85RFTMcQsRO4rTA/NUmir1jREn3HlanZuIhCcynmkfxg9LSixsE8lJQWiUo52QJSmIgXOG3G8fRi4SEbrKWgLmbgAxv1/6zPJO3UfYyceUW3SdXqRYet+OtRl4Jvo4BQmv9L7T/SqHlB6R9n9zmAiTIbSFAElLOQXoXkVyAJARFQUROSYmYk0uJhJRq5VIiIXL1f15KHLhCBefT7IaS53TmzuC4CPxJpYcgyEB1EOSjOgByUgr8MNX61pUjOUTxB0R9DKpwBV0D+gFjC9Eq/AQ7C1EVL1Exb7bMxoBWEDKgKicDVKZlAEvMDNgJcuazqvzMu1IpmpcqsTQvJRK1M629Aw==",
        },
        {
            "data": "m=edit&p=7ZRdT+JAFIbv+RVmbp1k+wEITfaiIri6WFEhrDSEFByg2jLutEW3xP/umdOa0g9NNtkYLzaTnpw+Z3rmnU77Br8jRzDagqG3qEJVGHpdw0tT2ngp6Ri6oceMA2pG4ZoLSCi97PXo0vECRs9v1/0ON59OzF/bVjiZqKdKdKaM73v3h9f+zzNXF2rPag0uBheutjJ/dI6vmt3D5iAKRiHbXvnq8f1oMlwOxqu29qdrTerx5FJpnE+W37bm6HvNTjVMa7u4bcQmjU8Nm2iE4qWSKY2vjF18YcQWjW+gRKgOrA+ZSqgGaTdLx1iXWSeBqgK5leaQ3kK6cMXCY7N+QgaGHQ8pkesc49MyJT7fMpI8hvcL7s9dCTx3w55TGER3/CFKp0Ev4kde6C64x4WEkr3Q2EzU9yvUy1Sqh52qmXxJK+TLCf9KPiyRV9+uVv8Ch3IN+meGLbcyytJWlt4YO4iWsSNaWz4pd5OcHKk3CqCpv72uFBwdSaBkQFWUEtFKpJ5rA8urKOIWYw+jhnEIGmmsYzzBqGBsYOzjnC7GMcYOxjrGJs45krv8q/fwCXJsrYk/dDYan3s/rdmkDx/TgcWF73jwnVmRP2fi7R5+ZxJwbxZEYuks2Iw9O4uQGImj7FdybIM9csjj/FF+tRUd3krECEWUMne14YJllcJ0drd6r5Ms5WDSas7FXUHSk+N5+a2g1eZQ8pfmUCjgF9y7d4TgTzniO+E6B+ZOCMYcrN3HfCe2KbzL0MlLdB6cwmp+9jpeauSZ4GXrVJNn+d96v6D1ygNSvprxfDU5+G1z8YHPZMUirnAboB8Yzl61ir9jLnvVIi85iRRbNhOgFX4CtGgpgMquArBkLMDe8RbZtWgvUlXRYeRSJZORS+37jD2tvQI=",
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

        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_turning(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"white({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="turning", adj_type="line", include_self=True))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
