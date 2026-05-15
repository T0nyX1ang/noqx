"""The View solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_num, grid, invert_c
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent
from noqx.rule.reachable import grid_color_connected


def bulb_num_color_connected(color: str = "white", adj_type: int = 4) -> str:
    """Generate a constraint to check the reachability of {color} cells starting from a bulb."""
    tag = tag_encode("reachable", "bulb", "branch", "adj", adj_type, color)

    initial = f"{tag}(R, C, R, C) :- number(R, C, _)."
    bulb_constraint = f"{color}(R, C), adj_{adj_type}(R, C, R1, C1), (R - R0) * (C - C0) == 0"
    propagation = f"{tag}(R0, C0, R, C) :- number(R0, C0, _), {tag}(R0, C0, R1, C1), {bulb_constraint}."
    constraint = f":- number(R, C, N), {{ {tag}(R, C, _, _) }} != N + 1."
    return initial + "\n" + propagation + "\n" + constraint


class ViewSolver(Solver):
    """The View solver."""

    name = "View"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VTBboJAEL3zFWbOe2AXUOBmrfZita02xhBC0NJoqsGiNGYN/97ZgUJN9WBT9dJs9uW92Vn3Mbvj+j0Nk4jZOAyb6YzjMExBU+gOTb0Yw/lmEbk11kw3szhBwli/02Gv4WIdaV6R5Ws76biyyeSd6wEHBgInB5/JR3cn713ZY3KAS8A4xrp5kkDaruiI1hVr5UGuI+8VHOkY6XSeTBdR0M0jD64nhwzUOTe0W1FYxh8RFD6UnsbLyVwFJuEGP2Y9m6+KlXX6Er+l8HVExmQztzs+YNeo7BqlXeOwXVHYjbdB+wxWHT/LsORPaDZwPeX7uaJ2RQfuLlOediAc3CrwnulWwLT2pCVQcr3UdVvpUjZUdr2UDt/b7Ownc26iNguNx3MyMSbsEArCIXpk0iC8JdQJLcIu5bQJR4QtQpOwTjkN9ZUn1eG7HRC58eqSwOJkvYycybEn6tRz1bAuq33Ng166nERJrRcny3CBj2wwC1cRYCdnGmyBpmdgsvnf3FdoblV+/ddP+zqd5mFl8WXLPoNVGoTBNMZ3hXWjeONI/NT8I3GL/83vCPtH/OJVxj8IX/sE",
        },
        {"url": "https://puzz.link/p?view/9/9/g0i0t0i0q0h0i0p0i0q0g0i0j", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_num(_range=range(0, puzzle.row + puzzle.col), color="white"))
        self.add_program_line(invert_c(color="white", invert="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(avoid_same_number_adjacent())
        self.add_program_line(bulb_num_color_connected(color="white"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "ox_E__1":
                self.add_program_line(f"not white({r}, {c}).")
            if symbol_name in ("ox_E__4", "ox_E__7"):
                self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
