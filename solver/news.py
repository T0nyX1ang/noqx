"""The NEWS solver."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import area, count, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type


def news_constraint() -> str:
    """Generate a constraint for NEWS."""
    mutual = "area(A, R, C), area(A, R1, C1)"
    rule = f":- {mutual}, number(R, C, 1), number(R1, C1, N1), N1 != 1, R1 <= R.\n"  # northest in area
    rule += f":- {mutual}, number(R, C, 2), number(R1, C1, N1), N1 != 2, C1 >= C.\n"  # eastest in area
    rule += f":- {mutual}, number(R, C, 3), number(R1, C1, N1), N1 != 3, C1 <= C.\n"  # westest in area
    rule += f":- {mutual}, number(R, C, 4), number(R1, C1, N1), N1 != 4, R1 >= R.\n"  # southest in area
    return rule


class NewsSolver(Solver):
    """The NEWS solver."""

    name = "NEWS"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7ZRdb9owFIbv8ysqX/uC+Cs0d7QNu+nSbTBNVYRQaLOBBgoDMlVG+e977bg1a1hRI7VXk+WjJyfHx69PTrz9VeWbgioM3qc9GmIwpewMhbCz58Z4sVsW8RkdVLt5uQFQejMc0u/5clsEmYuaBHt9HusB1R/ijISEEoYZkgnVn+O9/hjrhOoRXhHah++6CWLAxOM3+97QZeMMe+DUMfAWWD5ML5qnT3Gmx5SYPS7sSoNkVf4uiNNgnu/K1WxhHLN8h4Ns54u1e7Ot7sufFXlMX1M9aKSmR6RyL5U/SeXHpTIvNXkDqeeTuka5v0DsNM6M7q8e+x5H8b42mowNrb2N94RFSCOoryPhrOWRzz2CP/dI0fK0MqtWnqi1V6T+9kDm0Ipl1o5xFqq5tVfW9qyV1l7bmATHCiV6WCI7Q9sJ5pmDhWMG5gfMuGMOFo7R/Uw2HErPDMwdc8PKMf4YHnm/cDECLB1LccDYS7q9hGGngYPFAXMXw4XfVzIfb/IoxwocPfqxr3LxChxJ75dOs4Rm87VYbTrZlPDSWmGtsqWNTBO9qs2IKWFG0PLM/vqHbdftq56Ul5mv+DRkd54EEH7/ozhLy80qX+K3S6vVrNj459E8XxcE91wdkAdiZ4ayU/H/6nvnq8+Uvtf5AnyjTjwhJ0Nl0atNjZruIOtqmk/vSjQXCmgD+KkARvXNcX9G0pczH1/Iuy58SUnR9QhJl4Xi3wvfvQlwI02CPw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        news_dict = {"N": 1, "E": 2, "W": 3, "S": 4}
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(unique_num(color="grid", _type="row"))
        self.add_program_line(unique_num(color="grid", _type="col"))
        self.add_program_line(unique_num(color="grid", _type="area"))
        self.add_program_line(news_constraint())

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(fill_num(_range=range(1, 5), color="white", _type="area", _id=i))
            self.add_program_line(count(len(ar) - 2, color="white", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
            self.add_program_line(f"white({r}, {c}).")

        for (r, c, d, label), letter in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(letter in ("N", "E", "W", "S"), f"Clue at ({r}, {c}) must be in 'NEWS'.")
            self.add_program_line(f"number({r}, {c}, {news_dict[str(letter)]}).")

        self.add_program_line(display(item="number", size=3))

        return self.program

    def refine(self, solution: Puzzle) -> Puzzle:
        """Refine the solution."""
        rev_news_dict = {1: "N", 2: "E", 3: "W", 4: "S"}
        for (r, c, d, label), num in solution.text.items():
            solution.text[Point(r, c, d, label)] = rev_news_dict[int(num)]
        return solution
