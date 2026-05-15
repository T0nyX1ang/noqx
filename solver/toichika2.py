"""The Toichika 2 solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid
from noqx.rule.helper import fail_false, full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_adjacent


def num_appear_less_than_three() -> str:
    """Generate a rule to enforce that no number appears three or more times in a row / column."""
    rule = ":- number(R, C1, N), number(R, C2, N), number(R, C3, N), C1 < C2, C2 < C3.\n"
    rule += ":- number(R1, C, N), number(R2, C, N), number(R3, C, N), R1 < R2, R2 < R3.\n"
    return rule


def toichika2_pair(color: str) -> str:
    """Generate a rule to create Toichika 2 pairs and constraints."""
    rule = "pair(R, C1, R, C2, N) :- number(R, C1, N), number(R, C2, N), C2 - C1 = N + 1.\n"
    rule += f":- pair(R, C1, R, C2, _), grid(R, C), C1 < C, C < C2, {color}(R, C).\n"
    rule += "pair(R1, C, R2, C, N) :- number(R1, C, N), number(R2, C, N), R2 - R1 = N + 1.\n"
    rule += f":- pair(R1, C, R2, C, _), grid(R, C), R1 < R, R < R2, {color}(R, C).\n"

    # every number should belong to a pair
    rule += ":- number(R, C, N), not pair(R, C, _, _, N), not pair(_, _, R, C, N).\n"

    # paired numbers must not be in adjacent rooms
    tag = tag_encode("area_adj", 4, None)
    rule += f":- pair(R1, C1, R2, C2, _), {tag}(A1, A2), area(A1, R1, C1), area(A2, R2, C2).\n"
    rule += f":- pair(R1, C1, R2, C2, _), {tag}(A2, A1), area(A1, R1, C1), area(A2, R2, C2).\n"

    return rule


class Toichika2Solver(Solver):
    """The Toichika 2 solver."""

    name = "Toichika 2"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VRLb9NAEL7nV1RznsPujk1j30KbcAkpkFSosqzISV0a4cjFiRHayP+d2YfjUhK1BRX1gNY7+nZeu/PwbL7VWZVjyIv6KFDyUqpvdyDM167Zalvk8QkO6u1tWTFAvBiN8CYrNjn2Eq+W9nY6ivUA9bs4AQkIireEFPXHeKffx3qCesoiwH6KsK6L7WpZFmUFlidZb+wMFcNhBz9buUFnjikF4wljcmZXDJeralnk87HjfIgTPUMwd7+11gbCuvyeg3+bOS/L9WJlGItsyxFubld3gMSCTX1dfq29qkwb1IPnRUBdBLSPgA5E4EN82QiitGm4OJ84hnmcmHAuO9jv4DTeNeZZhsp4B0GoYJ9lCN2pzciVVRtZqiydsRfUZOm5pcLS0NKx1RmyWym42YSEWHF7CG47oTxWjMljYhx4HDAOLY7oV3Xp3UjxAEceRyiVcFgxX7U6qsPmKul9Kn4OeX1ifYru2bY46nT4X+n4jOnUY+OfOkz+LmL/gbFtTFeYjJxZGlj6xmbq1FTjifUC47jvqgZEvlzK/neuin9TqkcfmSg3N8wKn4bSXgLTurrJljk38fD6S34yKat1VvBpUq8XedWeeaA0PfgBdifEUcn/M+ZVzxhTKPEHk+ZFe/SR5yR6itzF+gLhrp5nc062zc5BvjL8Ie5H2AOx2IvdVDsqdoPuqNjNvqNiNw6Pil/n06bIs+9ANidICu9Nrd8MrcIBh8yn44b/vMt4GKa9nw==",
        },
        {"url": "https://puzz.link/p?toichika2/7/6/afg00v50l2nvt8l2g4g3h1", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(adjacent())
        self.add_program_line(area_adjacent())
        self.add_program_line(num_appear_less_than_three())
        self.add_program_line(toichika2_pair(color="not gray"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(
                fill_num(_range=range(1, max(puzzle.row, puzzle.col) + 1), _type="area", _id=i, color="gray")
            )
            self.add_program_line(count(1, color="not gray", _type="area", _id=i))

            for r, c in ar:
                if Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f":- area({i}, R, C), number(R, C, N), N != {num}.")

                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f":- not number({r}, {c}, {num}).")
                    self.add_program_line(f"not gray({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="number", size=3))

        return self.program
