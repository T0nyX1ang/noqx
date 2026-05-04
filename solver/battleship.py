"""The Battleship self."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.shape import OMINOES, all_shapes, count_shape, general_shape


class BattleshipSolver(Solver):
    """The Battleship solver."""

    name = "Battleship"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VRNj9owEL3nV6x89sFj5/tSsdully3bFqoViiIUtqlABYUCqSoj/ntnJlCCiVTtYbdbqQoePd6M7efxeDbf62JdSgD6mVgqiUj6QcgDQPNQh2803y7K9Er26u2sWiOQ8r7fl1+Lxab0MuDZKvd2NkltT9p3aSZASKFxgMil/Zju7PvUDqQdoktIQO6uCdIIb0/wgf2EbhoSFOLBASMcI5wWW9Szmc1Xk+uG/ZBmdiQF7XXNKxAUy+pHKQ5a6P9jtZzOxdkCB8+m/lJ9q8Vxm720vUbyuEOyOUk2vyWbbsn6ZSQn+X6P6f+EoidpRvo/n2B8gsN0tydtO2EMTX2DWpo7EsY/Hv9IBEToFhG6RESEahExEX6LSJwpvnJ28YEI0yK0OyVylIZuRBQ5iybaEQYqcuaA1o5WMO4yELg7QXgRE+uzA2B6gZM8xiQHFB3Iy9sXIeUy7PKAopyZTpcml+50cer9TldMVx11uhLKPly6UH+fT6HZjrB6pDVs37JVbAO2dxxzy/aB7Q1bn23IMRHV35MqtJ3IZ5KT+TG3vfMv/Pe43MvEoF5Oy/XVoFoviwX2iOGsWJUCm/LeEz8FD6wq7PH/+/Rf7tN0Feq1vYU/yMkww/ha7L0Uq3pSTB4rrDHM3xP5Fz8VPvLc+wU=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        fleet_name = "battleship_B"  # set a default battleship fleet name
        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            shape, style = symbol_name.split("__")
            validate_direction(r, c, d)
            fail_false(shape.startswith("battleship"), f"Invalid battleship shape: {shape}.")
            fail_false(fleet_name in ("", shape), "Multiple fleet shapes are not allowed.")

            fleet_name = shape
            if style not in ("7", "8"):
                self.add_program_line(f"{fleet_name}({r}, {c}).")
            else:
                self.add_program_line(f"not {fleet_name}({r}, {c}).")

            if style == "1":
                self.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
                self.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
                self.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
                self.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")

            if style == "2":
                fail_false(0 < c < puzzle.col - 1 and 0 < r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- #count {{ R, C: {fleet_name}(R, C), adj_4({r}, {c}, R, C) }} != 2.")

            if style == "3":
                fail_false(c < puzzle.col - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r}, {c - 1}), {fleet_name}({r}, {c - 1}).")
                self.add_program_line(f":- grid({r}, {c + 1}), not {fleet_name}({r}, {c + 1}).")

            if style == "4":
                fail_false(r < puzzle.row - 1, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r - 1}, {c}), {fleet_name}({r - 1}, {c}).")
                self.add_program_line(f":- grid({r + 1}, {c}), not {fleet_name}({r + 1}, {c}).")

            if style == "5":
                fail_false(c > 0, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r}, {c + 1}), {fleet_name}({r}, {c + 1}).")
                self.add_program_line(f":- grid({r}, {c - 1}), not {fleet_name}({r}, {c - 1}).")

            if style == "6":
                fail_false(r > 0, f"Ship at ({r}, {c}) is outside of the board.")
                self.add_program_line(f":- grid({r + 1}, {c}), {fleet_name}({r + 1}, {c}).")
                self.add_program_line(f":- grid({r - 1}, {c}), not {fleet_name}({r - 1}, {c}).")

        self.add_program_line(shade_c(color=fleet_name))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(avoid_same_color_adjacent(color=fleet_name, adj_type="x"))
        self.add_program_line(general_shape("battleship", 1, OMINOES[1]["."], color=fleet_name, adj_type=4))
        self.add_program_line(general_shape("battleship", 2, OMINOES[2]["I"], color=fleet_name, adj_type=4))
        self.add_program_line(general_shape("battleship", 3, OMINOES[3]["I"], color=fleet_name, adj_type=4))
        self.add_program_line(general_shape("battleship", 4, OMINOES[4]["I"], color=fleet_name, adj_type=4))
        self.add_program_line(all_shapes("battleship", color=fleet_name))
        self.add_program_line(count_shape(4, "battleship", 1, color=fleet_name))
        self.add_program_line(count_shape(3, "battleship", 2, color=fleet_name))
        self.add_program_line(count_shape(2, "battleship", 3, color=fleet_name))
        self.add_program_line(count_shape(1, "battleship", 4, color=fleet_name))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")

            if r == -1 and 0 <= c < puzzle.col and isinstance(num, int):
                self.add_program_line(count(num, color=fleet_name, _type="col", _id=c))

            if c == -1 and 0 <= r < puzzle.row and isinstance(num, int):
                self.add_program_line(count(num, color=fleet_name, _type="row", _id=r))

        self.add_program_line(display(item=fleet_name))

        return self.program

    def refine(self, solution: Puzzle) -> None:
        """Refine the solution."""
        for (r, c, d, label), _ in solution.symbol.items():
            has_top_neighbor = (r - 1, c, d, label) in solution.symbol
            has_left_neighbor = (r, c - 1, d, label) in solution.symbol
            has_bottom_neighbor = (r + 1, c, d, label) in solution.symbol
            has_right_neighbor = (r, c + 1, d, label) in solution.symbol

            fleet_name = solution.symbol[Point(r, c, d, label)].split("__")[0]

            # center part
            if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__1"

            # middle part
            elif (has_top_neighbor and has_bottom_neighbor) or (has_left_neighbor and has_right_neighbor):
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__2"

            # left part
            if {has_top_neighbor, has_bottom_neighbor, has_left_neighbor, not has_right_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__3"

            # top part
            if {has_top_neighbor, has_left_neighbor, has_right_neighbor, not has_bottom_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__4"

            # right part
            if {has_top_neighbor, has_bottom_neighbor, has_right_neighbor, not has_left_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__5"

            # bottom part
            if {has_bottom_neighbor, has_left_neighbor, has_right_neighbor, not has_top_neighbor} == {False}:
                solution.symbol[Point(r, c, d, label)] = f"{fleet_name}__6"
