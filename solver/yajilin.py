"""The Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, validate_direction
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
            "data": "m=edit&p=7Vbtb7pIEP7uX9Hs125yLCBFkl8u1mqvPWtt1XiVGIIWFQvSQ7Atpv97Z3b1eBGbXnq5/C65ILPDM7vztvCs6z9jO3Qok/Cn6BRGuFSm81vWNX5Lu6vvRp5jnNB6HC2CEBRKb1stOrO9tUOvHxbtRlB/uaj/sdGj0YhdSvGVNFy2lqf3/u9XrhKyVkfv3nRvXHle/61xfqc1T7VuvB5EzubOZ+fLwag/6w7nNfmt2RmpyehWql6PZr9s6oMfFXOXw7iyTWpGUqfJpWESmVB+MzKmyZ2xTW6MpEeTHpgI1QFrg8YIlUFtpuqQ21FrCJBJoHeEQwbqA6hTN5x6jtUWSNcwkz4lGOecr0aV+MHGIcIFf54G/sRFYGJH0Kr1wn3eWdbxY/AU7+aCQ+LHXuROAy8IEUTsnSZ1UUJ7X4KalqCkJaAqSkCtpASs7NsleO7KeS3Lvlae/TvszD3kbxkmljJIVT1Ve8aWVBkxdEo0hQ+6xIeazAcmCZSxqhiVHa6qMIKDDjhQYIlJfoWouPuQDXqE1Cxsww5C7yZRLCWFMBLOykAYFWdlFvIMoIsWvgp7DLMpYpgZrpUyGGaJ87KYxtf+lS3UwIwtyAcuW1zKXPahRzRRuLzgUuKyymWbz2lyOeSywaXKpcbnnGGXv7oPqkYMVbT0O0kRVYZO1HBHmS4UVaUqVK1QogCZoPbFzE1FEFD+qv73sHHFJL04nNlTBz6hNnxKJ50g9G0PnjqxP3HC/TMQGlkHnrUWsy3n1Z5GxBCcmrXksBX3kYO8IHjGb7bEw96UA935KgidUhOCzuP8mCs0lbiaBOFjIacX2/PytfDzJgcJkspBUQgMlHm2wzB4ySG+HS1yQIZwc56cVaGZkZ1P0X6yC9H8tB3vFfJK+G0qeC7+f/r8vKcP7pL0Re77Puv9M1RswvuiajS5peQ5tmwLaiLwH4d+ip8dwfW/iR/zUxq3vWf1I0ZB9OVGOBfKDXByHBj+9R3i33wQfkLAqbEIl9AwoJ8wccZahh8h3Yy1iB8wLCZ7SLKAlvAsoEWqBeiQbQE8IFzAjnAuei3SLmZVZF4MdUC+GCrLvyZ5s5cu9IuMKx8=",
        },
        {
            "data": "m=edit&p=7VffT9tIEH7nr6j8Wktn765/SvcQKPTagxRaEEcihExqIDTBnGNDa8T/3m9mJyROApee7qEnVU68X2ZnZ76ZHY83k7/rrMxdX9FHx67n+rhMYviro4C/nlyHw2qUp6/cTl1dFSWA637Y2XEvstEkd9+fXO1uFZ37N52/7uKq1/PfevU77/h65/r1x/Gf74a69He68f7e/t5QXXb+2No8CLdfh/v15KjK7w7G/ub1Ue/wYv/4MlHftrs90/Q+eMH73sVvd52j3zf6wuF046FJ0qbjNm/TvuM7rqPw9Z1TtzlIH5q9tDlxm0+YclwN2a5VUoDbM3jM84S2rND3gLuCAU8As7Is7s8uirrMP1/mZ5t2wX7abw5dh/xtshWCzri4yx3hQ78Hxfh8SILzrELKJlfDW5mZ1J+LL7XowpUzrkfVcFCMipKEJHt0mw6HImam8RAxiYdCk3gI2ngIrYiHWP9n8XzLroej4Q07a8eSrI7lEfv1EdGcpX0K7GgG4xn8lD44gXFS7TqR4iEOeEg8HnxPyxjb0Q/tqHw7arvY14kdTWTHwFrzQ2vOj8RebO0pj9aDQFcI9B0PrG09MRWbTREQqZaA6LUETLRPJTmTgHJbh8i3JUS/vYoCaetQSG0JBdVeReG1dSjQloRD7jt6KkHwfvqA+8k0Bfyk+U/PPCppdenY/EyfS76w6lltTt7a2pxZaM/xeEHbpv0H1GlP1lfnDZujzsueV+fd/AF12ur1yXAdrK/ORbI+Ga6gtSvAltfa6rb21iSDktzhwlR8P0SncBvN9zd89/ge8H2XdbZRwirRrkqwAwr+gLWH9AJjdLWP6FiOV5tg7fvAqOQpVsgvYRUBo05YjnfjFCvY0bKWsEGCCRu8Kg0KhbD2ZtjAjpG1hEOkjHAIbqHlifkZVuCmxCZhI74M2UT+WE6+BBtwM2KTcCC+AtgMJHYDX1Mcwk4oawlHwjMKgSX2EHmY4gh2IllLWHKLEVh4RsjDFAfgFohNwpH4isim5DkgX4IjcIvEJuFYfMVkU2KPyJfgBHYSWQtsPMsTI7DEnqgnbLDvRvaaseQWI7DlifknrGNwiyV2YONZXxiBJc8x+bLYeDgqeWKTsBJfimza2DE/wwp2lKwlrIUnDl+GWgHL9Qxj343sNWPJLUZgid0gD4zxEBzzo7DFd8P3kB+RiF61a76M7Rtx/tXw757Gf6TT14YPnMtX8EtO1+lG3+nW4/O8fNUtynE2woHs01V2m2PcKsa3xWRY5Q4Oxc6kGJ1N6vIiG+Rn+ddsUDmpPZfPzzhpVdYiumGzLa1RUdzidLfKwHRq3sLw8qYo89nMgjr38tWWaKoltKbOi/LzAqX7bDRqR8L/WFqiwbAcjNqiqsRxde43v2FaknFWXbUEc0f1lqX8ZiGVVdammH3JFryNZ+l43HC+Ovzta7zt9K//L/+3/y+0d97P1jh/Njpc9kX5QgeaTS6KVzQiSF/oRXOzq+TP9J252UX5UpMhsst9BtIVrQbSxW4D0XLDgXCp50D2TNshq4udh1gtNh9ytdR/yNV8C+qfbnwH",
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
        self.add_program_line(defined(item="gray"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line("{ black(R, C); green(R, C) } = 1 :- grid(R, C), not gray(R, C).")
        self.add_program_line(fill_line(color="green"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="green", adj_type="line"))
        self.add_program_line(single_route(color="green"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            self.add_program_line(f"gray({r}, {c}).")

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
                self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, _), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="line_io", size=3))

        return self.program
