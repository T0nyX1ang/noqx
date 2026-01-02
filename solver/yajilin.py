"""The Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count


class YajilinSolver(Solver):
    """The Yajilin solver."""

    name = "Yajilin"
    category = "loop"
    aliases = ["yajirin"]
    examples = [
        {
            "data": "m=edit&p=7Vbtb7pIEP7uX9Hs125yLCBFkl8u1mqvPWtt1XiVGIIWFQvSQ7Atpv97Z3b1eBGbXnq5/C65ILPDM7vztvCs6z9jO3Qok/Cn6BRGuFSm81vWNX5Lu6vvRp5jnNB6HC2CEBRKb1stOrO9tUOvHxbtRlB/uaj/sdGj0YhdSvGVNFy2lqf3/u9XrhKyVkfv3nRvXHle/61xfqc1T7VuvB5EzubOZ+fLwag/6w7nNfmt2RmpyehWql6PZr9s6oMfFXOXw7iyTWpGUqfJpWESmVB+MzKmyZ2xTW6MpEeTHpgI1QFrg8YIlUFtpuqQ21FrCJBJoHeEQwbqA6hTN5x6jtUWSNcwkz4lGOecr0aV+MHGIcIFf54G/sRFYGJH0Kr1wn3eWdbxY/AU7+aCQ+LHXuROAy8IEUTsnSZ1UUJ7X4KalqCkJaAqSkCtpASs7NsleO7KeS3Lvlae/TvszD3kbxkmljJIVT1Ve8aWVBkxdEo0hQ+6xIeazAcmCZSxqhiVHa6qMIKDDjhQYIlJfoWouPuQDXqE1Cxsww5C7yZRLCWFMBLOykAYFWdlFvIMoIsWvgp7DLMpYpgZrpUyGGaJ87KYxtf+lS3UwIwtyAcuW1zKXPahRzRRuLzgUuKyymWbz2lyOeSywaXKpcbnnGGXv7oPqkYMVbT0O0kRVYZO1HBHmS4UVaUqVK1QogCZoPbFzE1FEFD+qv73sHHFJL04nNlTBz6hNnxKJ50g9G0PnjqxP3HC/TMQGlkHnrUWsy3n1Z5GxBCcmrXksBX3kYO8IHjGb7bEw96UA935KgidUhOCzuP8mCs0lbiaBOFjIacX2/PytfDzJgcJkspBUQgMlHm2wzB4ySG+HS1yQIZwc56cVaGZkZ1P0X6yC9H8tB3vFfJK+G0qeC7+f/r8vKcP7pL0Re77Puv9M1RswvuiajS5peQ5tmwLaiLwH4d+ip8dwfW/iR/zUxq3vWf1I0ZB9OVGOBfKDXByHBj+9R3i33wQfkLAqbEIl9AwoJ8wccZahh8h3Yy1iB8wLCZ7SLKAlvAsoEWqBeiQbQE8IFzAjnAuei3SLmZVZF4MdUC+GCrLvyZ5s5cu9IuMKx8=",
        },
        {
            "url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="gray"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
        self.add_program_line(fill_path(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(avoid_same_color_adjacent(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="white", adj_type="loop"))
        self.add_program_line(single_loop(color="white"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")

            # empty clue or space or question mark clue (for compatibility)
            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
                continue

            fail_false(isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows.")
            num, d = clue.split("_")
            fail_false(num.isdigit() and d.isdigit(), f"Invalid arrow or number clue at ({r}, {c}).")
            self.add_program_line(yaji_count(int(num), (r, c), int(d), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="grid_io", size=3))

        return self.program
