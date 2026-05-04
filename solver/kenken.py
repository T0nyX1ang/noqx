"""The Kenken solver."""

from typing import Iterable, Tuple

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, full_bfs


def area_product_aggregate(_id: int, src_cells: Iterable[Tuple[int, int]]) -> str:
    """Generate a constraint to aggregate the product of the numbers in the area."""
    rule = ""
    for i, (r, c) in enumerate(src_cells):
        if i == 0:
            rule += f"area_product({_id}, {i}, N) :- number({r}, {c}, N).\n"
        else:
            rule += f"area_product({_id}, {i}, N1 * N2) :- area_product({_id}, {i - 1}, N1), number({r}, {c}, N2).\n"
    return rule


def number_exclusion(target: int, grid_size: int, _id: int) -> str:
    """Generate a constraint to exclude the number from the cells."""
    rule = ""
    for num in range(1, grid_size + 1):
        if target % num != 0:  # exclusion for non-factorable numbers
            rule += f":- area({_id}, R, C), number(R, C, {num}).\n"
    return rule


class KenkenSolver(Solver):
    """The Kenken solver."""

    name = "Kenken"
    category = "num"
    aliases = ["tomtom", "kendoku", "calcudoku"]
    examples = [
        {
            "data": "m=edit&p=7VfNjts2EL77KRa8lgX0R0rWbZvu5rJ12u4WQSAsDO/GbYzacGqvi0KG7z330kfpA+RN+iT5hhz5byQqSRugh8IQ8XHmG4oz31Cy1r9sJquptjrXaaEjHeOXWKvTKIPBXxH/7mZP82l5oS83T2+WKwCtX1xf6x8n8/VUD6rY0+4H23pY1pe6fl5WKlZaJbhida/r78pt/U1Zj3R9C5fSFrYbT0oArw7wpfMTeuaNcQQ8Ak6BAV8BPkxW6/FzT/u2rGqjFd3lKxdLUC2Wv04V74Lmj8vFw4wMD5Mn5LJ+M3vLnvXm9fLnDXNxA7XYzJ9mj8v5ckVGsu10fXmWAO2EE0gPCRD0CRA6T4AzpAQeZ6vH+XR8c0jh7t9KYdiewg7ifI8kxmVF+fxwgLflFuOo3KokJ/o2/tLuEKOVVeSP4TG2cMtH7/70RTJ5Qobk79//YEORkaH4wk9tEtE02/tt4lYomgVs5ua24Rd8A54O/fLv/vLzPHLL+RbAzN+LZ5m/VTPz9+GZ37dlFV+5VK/dmLjxDjXQderGr90YudG48cZxrlCA2OB8GGwqQUdnyQGnwFmDM2BsreFkKeP0YLewW7Yb2PeY1mRscS/La1ricKzB+g3OgM0RzgxjAztjA2wZW4o9shvLfHvAKXDWYHD2a5IdveHWoTWZg6dFbBs7cM72nDDbCRdsLxDb4JxwszfgnDFxhoxz7LmxE6YWcxzgYVNP4jDOUas9Rj3zpp6EuZ5kLxgXqPMek535BdYZEob4L10LPHNj5kbrWiN3Y9Eco+7jtaccn7QUVaiUwfF3D0h/yv5Jg/bsdDeoqFH3PxT5U/H9oFJXr3+aXoyWq8VkjkfQaLN4mK6aOd4Cu4H6TbmrSvBOwcPw/zfDf/nNQEpF/e+H03fBReqe1Z+xaT/meFU1mtQWulLYFSqn3m7GkzESdbMjr3BDj2O3l+LIj4Y88QtCfk4QjEIwBAXanFMEh9pFkCQLDShZknZWFqZJ3nl9OolZB1EyTRdTUkX1A1wpRIDcokmA3SZPNz1pFSrAb5csENAhXiCiS8ZASKeggZhuaQNBAZEDUSG5A2FB4QNx4RboDkx7mqEzrq8pOsJ6W6M1qr89WoI+oUHS/gYRIb3tISL6WkME9DSF4H/c8yALtoBgh4QX5IDcgtstsqB+8MM86xJUEDtkFLx28QStVTLB+pD3qmmRR3CkKIIipBCMvv8a5qzswn9abOE+KnH94sTDRcV39ZmHcydHpehz+3TJI/dpnEt2hMOJsP13zGlky5/Hz/qJg++O6n7wHg==",
        },
        {
            "data": "m=edit&p=7VTvaxNNEP6ev6Ls5xVuf10u963W1i81fV8bKeUIJU1PG7xweklENuR/7zNzs0kVhYooCnJk8szs7OwzszO7+riZdbUOOteu0Jk2+KwttM1z/Gf8S99ksW7q8kgfb9b3bQeg9cXZmX47a1a1HlSmd5sOtnFUxmMdX5aVMkori59RUx3/L7fxVRnHOl5iSekctvPeyQKeHuAVrxM66Y0mAx4DO2DAa8D5ops39c157/hfWcWJVnTOc95NUC3bT7USHqTP2+Xtggy3szWyWd0vPsjKanPXvt+IL45Qy02zXszbpu3ISLadjsffT8EdUiDYp0Do6xQkx1+cwujbKexwPa+RxE1ZUT5vDvCy3EKOy62ynty35lnYYY9WuaJ1gxU/zGkp6yvkC3YssmxvKPh0UUNgb4MGYLV3z0Ub8aJouc04lGjO7jWcfM3MzlhalhNQ1tGxfMEyYxlYnrPPKfiabKQN6JQWLWjQ3sYIRqODV48tsBPsgEGTsdfGit3CTqQIO/h7ieMRJ0j8gPhhJLh4hIfAKAzjHHgoOACjCIxxVggHblQOxuD/BZY4FjETJv5W+FjaKzwt7E7sDvbE3yKOS3EIS3wH/k44O9i92D3sKV88EsYLf095CX/2l5ieck8+5C8xPXxSrRz2Jg4ONXHJH3gfH/XxEp9wkHshfy+1ojo48TE4y8pevneKj0a44nY4YelZ5twmQ5ZFmoAnTEY/BT/TkT9Cp6LLkQ/pPwVNB5U6vXtXH43bbjlr8C6MN8vbuks6HufdQH1W/KssnnmU79+L/Ye/2HRZ2e/ozsNcxotHg8lKmsxekdHcKzSb+z00nKyk6WQljScraT7jxV88oJilajp4AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")
        n = puzzle.row
        self.add_program_line(grid(n, n))
        self.add_program_line(fill_num(_range=range(1, n + 1)))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(unique_num(_type="col", color="grid"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))

            for r, c in ar:
                if Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}") in puzzle.text:
                    clue = puzzle.text[Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                    if isinstance(clue, int):  # deal with unknown operator
                        if len(ar) == 1:
                            self.add_program_line(f":- not number({r}, {c}, {clue}).")

                        if len(ar) > 1:
                            self.add_program_line(area_product_aggregate(_id=i, src_cells=ar))
                            if clue >= len(ar) * n:  # must be product operator
                                self.add_program_line(f":- not area_product({i}, {len(ar) - 1}, {clue}).")
                                self.add_program_line(number_exclusion(clue, grid_size=n, _id=i))
                            else:
                                self.add_program_line(
                                    f":- S = #sum {{ N, R, C : area({i}, R, C), number(R, C, N) }}, area_product({i}, {len(ar) - 1}, P), M = #max {{ N: area({i}, R, C), number(R, C, N) }}, number(_, _, M), (S - {clue}) * (P - {clue}) * (S + {clue} - 2 * M) * (P * {clue} - M * M) != 0."
                                )

                    else:
                        fail_false(str.isdigit(clue[:-1]), f"Invalid clue at ({r}, {c}).")
                        num = int(clue[:-1])
                        operator = (
                            clue[-1].replace("x", "*").replace("\u00d7", "*").replace("\u2212", "-").replace("\u00f7", "/")
                        )  # normalize operators

                        if operator == "+":
                            self.add_program_line(f":- #sum {{ N, R, C : area({i}, R, C), number(R, C, N) }} != {num}.")

                        if operator == "-":
                            self.add_program_line(
                                f":- S = #sum {{ N, R, C : area({i}, R, C), number(R, C, N) }}, M = #max {{ N: area({i}, R, C), number(R, C, N) }}, number(_, _, M), 2 * M != S + {num}."
                            )

                        if operator == "*":
                            self.add_program_line(area_product_aggregate(_id=i, src_cells=ar))
                            self.add_program_line(f":- not area_product({i}, {len(ar) - 1}, {num}).")
                            self.add_program_line(number_exclusion(int(num), grid_size=n, _id=i))

                        if operator == "/":
                            self.add_program_line(area_product_aggregate(_id=i, src_cells=ar))
                            self.add_program_line(
                                f":- area_product({i}, {len(ar) - 1}, P), M = #max {{ N: area({i}, R, C), number(R, C, N) }}, number(_, _, M), M * M != P * {num}."
                            )

                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
