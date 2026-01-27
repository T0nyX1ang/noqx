"""The Aquarium solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, validate_direction, validate_type


def area_gravity(color: str = "black") -> str:
    """Generates a constraint to fill the {color} areas according to gravity."""
    target = f":- area(A, R, C), area(A, R1, C1), R1 >= R, {color}(R, C), not {color}(R1, C1)."
    return target.replace("not not ", "")


class AquariumSolver(Solver):
    """The Aquarium solver."""

    name = "Aquarium"
    category = "shade"
    aliases = ["aquarium"]
    examples = [
        {
            "data": "m=edit&p=7VdtT+NGEP7Orzj5661U765f1pGqKnBwvSsEOECURCgywUC4BFMngasR//2eWe/itZMcraqerlKVeP342dnZefPYnv2xSIuMcU5/qZjPgFgQRvrgXOjDN7/j8XySdd6w7mJ+kxcAjO3v7LCrdDLL2Mezm92tvPv4rvv7g5r3+/y9v/jgn97u3L79NP3tw1gWfKenDvYO9sbiuvvr1uZhtP02OljMTubZw+GUb96e9I+vDk6vE/Hndq8flP19P/zYv/rpoXvy88aAa9v8842nMumUXVa+7ww87jFP4ODeOSsPO0/lXqfssfIIUx7j4HYrIQG4XcNTPU9oqyK5D9wzGPAMcDQuRpNsuFsxB51Becw82mdTryboTfOHzDN20PUon16MibhI5wjV7GZ8b2Zmi8v888LIQqE3XUzm41E+yQsiiXtmZbdy4ci6ENYuyNoFgpULhFa4QJ79yy4kq114Rno+wYlhZ0D+nNRQ1fCo84Sx13nypKSVAZZWOfRkQMQvDhG2JaI2ERMhHUIRETpE0iICn4jEIXhbQhARO4TexTEs0hKOHbGWQDVaItESjlLut0W4aGvhlTvuqlDLKIeJtIxjHVda5sUjhJfrIJ/pcUePQo/HyAErpR7f6dHXY6jHXS2zjdQIFTOhEEqBW0wpYESRcBw0cYwMEY78GquEiQRBJpz4TPoVjzMwEqh5NByL4wjyyIHGIfQYPhLAcFbzsIdCqtcKrK14nIGNnYmscQybE9SXXRtbGeh84SETG18i8sX6RfajFLU8+MT6BR8tjmCnsj4CJ8ZmxWscwS9l/ErIR+ML5CWv1uIMXMngDGx9DOBLZQ/OTIrKHpyBTTwF9IhqL73WYhExSTVNOABP5WzX0t1AWEIn3QhaBja8yAOHRn8I/aHRieeBDE3MQ+iJjJ4IepSxTYFXZq3CWmXWKqxVzlpXf2xsiLGvXUt7xcaemB5MtZ7Ar3icWcAtH4Kv9OAM3tqAvRJjZ6IaOOBVDQR4vlksE9RSUtWJVKgxky+NlZFRqDHrL3L6IkM5NXmXqBNc19jUAM7AJheQD2wNUK6tPNWwqT1JdW5qVeJekJHFkImMDOpWmrqVqOcGtms5/OLGLx9rDab7GtemHqCf+rHGkAmMfACZwNYM9nIxdWddV/DRYk61avzyIcNtDVM9O/LCxMRHDC0WiA81eK2f6s3wIdWkgyOjB/egjIw87rWXOBOmJqkxfI+MLyHFzcGhiWEI30PrO+Sp5Wp7KCZOn6F2rTFiIoy8gB57b+INqr6/gLVONNRT3Va39BjoMdLtNqYH4l98ZHomIVQDYfX8/Odt/lXbBkg/vRI2f3g1/K9x5xsD72hRXKWjDO8z25fX2ZteXkzTCa56i+lFVthrvGJ6s3wynFXSw+xLOpp7neot151pcHdaR4Oa5Pn9ZHy3SoOdapDj67u8yFZOEZnB5jWqaGqFqou8uGzZ9JhOJk1f9BdAg6peGxvUvMA7oXOdFkX+2GCm6fymQTjvjw1N2V0rmPO0aWL6OW3tNq3D8bzhffH0MZD0pfL/98AP/j1AqfL/1lfBd+hqr5gzQMTxiC33mXe/GKZD+OTh05MRj364mk9aPIKu9QQtHjlaKR+skUfOV+4breHjNfw6e16xcykOwfl3z5ZuAnnxjY5cT7bpFX0Z7DdaszO7il/ThZ3ZNr/UcsnY5a4LdkXjBdvuvaCW2y/IpQ4Mbk0TJq3tPkxWtVsxbbXUjWkrtyEPzje+Ag==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="blue"))
        self.add_program_line(area_gravity(color="blue"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color="blue", _type="row", _id=r))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK or color != Color.BLUE)} blue({r}, {c}).")

        self.add_program_line(display(item="blue"))

        return self.program
