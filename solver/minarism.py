"""The Minarism solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Puzzle
from noqx.rule.common import defined, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_type


class MinarismSolver(Solver):
    """The Minarism solver."""

    name = "Minarism"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VRNb5tAEL3zK6I9z2G/wMDNTdNeUvphR5GFkIVTIqPYwbVN1a7Ff+/smBTisqoiNeklWhg95s3sPnZnZ/etzrcFjHCoEDgIHIpregNun4cxLferIj6Dcb1fVlsEAB8TuM1Xu8JL26DMO5goNmMw7+OUCQZM4itYBuZzfDAfYjMDM0GKgUDf5TFIIrzo4DXxFp0fnYIjThAHDAKEM4TlfYHKV+X+5zH0U5yaKTC70hvKt5Ctq+8Fa5XY75tqvSitY5Hv8W92y3LTMrv6a3VXt7Eia8CMj4KTAcGqE6x+C1YDgts/enbBUdY0uPVfUPI8Tq36qw6GHZzEh8YqOzAZBG1uALivOKES3Hr8nkdSjOp5IorRnUdz8gQ9j1CnHvlHjJQnq2tfPZoZZQoSO7NiR3YCCY82Ec+DyTBEQsPp7jIZDWRYAut6OENx30EI6SCkdqwRjpAQQ0ToICLpImyGGiKiYUILPTyVlsqRoXwHoR2qtFYuwrW4P7gGnu87OmVJdopVCkaRfUuWk/XJXlLMBdlrsudkNdmAYka2zp94E3Rb5JI6Vb/wnkleKjX12Yfh//uvzEtZUq8XxfYsqbbrfIVdY7LMNwXDFt147AejF09EgH7t2v+xa9tj4E+q2Beo0L/ISXF/sYZ7twbYpp7n85sKC41nLy4X71Tm/QI=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(defined(item="white_h"))
        self.add_program_line(defined(item="white_v"))
        self.add_program_line(defined(item="black_h"))
        self.add_program_line(defined(item="black_v"))

        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, n + 1)))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(unique_num(_type="col", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.LEFT and c > 0 and symbol_name == "inequality__1":
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N < N1.")

            if d == Direction.TOP and r > 0 and symbol_name == "inequality__2":
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N < N1.")

            if d == Direction.LEFT and c > 0 and symbol_name == "inequality__3":
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), N > N1.")

            if d == Direction.TOP and r > 0 and symbol_name == "inequality__4":
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), N > N1.")

        for (r, c, d, label), num in puzzle.text.items():
            validate_type(label, "normal")

            if d == Direction.CENTER:
                fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
                self.add_program_line(f"number({r}, {c}, {num}).")

            if d == Direction.TOP and r > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r - 1}, {c}, N1), |N - N1| != {num}.")

            if d == Direction.LEFT and c > 0 and isinstance(num, int):
                self.add_program_line(f":- number({r}, {c}, N), number({r}, {c - 1}, N1), |N - N1| != {num}.")

        self.add_program_line(display(item="number", size=3))

        return self.program
