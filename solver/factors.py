"""The Rooms of Factors solver."""

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


class FactorsSolver(Solver):
    """The Rooms of Factors solver."""

    name = "Rooms of Factors"
    category = "num"
    aliases = ["roomsoffactors"]
    examples = [
        {
            "data": "m=edit&p=7ZRNb9swDIbv+RWFzjpY1EcS37Iu2SXLPtpiGAwjSFJvDZbAXRIPgwP/972UmRoFuhXr0O0yCCJI+pH8SqK0/1otdoUOaHagE23QKITYjXOxJ9Iu14dNkZ7pUXW4KXdwtH4zmehPi82+6GVC5b1jPUzrka5fpZkySitCNyrX9bv0WL9O65muL/BJaYPctIUI7rhzP8Tv7J23SZPAn8G37bCPcFfr3WpTzKdt5m2a1Zda8X9exNHsqm35rVCig+NVuV2uObFcHLCY/c36Vr7sq+vySyWsyRtdj34u13Zy7Z1c+4BcWc8zyx3mTYNtfw/B8zRj7VedO+jci/TYsC62Jj0qNxhgBkOsSLkhIaAkBj5JEDgJHAfkYhDIIbCJBDyBDW3g4myDNohTxzENr59/OYmWor2EIl3baF9Gm0Tro51GZgyJhtURlBGKyFj4VnxMzVLYJzBWGAJjheHfW2EsGCeMBeOEcV4b78XHQnxofY+xQcZ6MEEYDyYIE8D0hQlg+sLw3emHTgNJnsDQKQ+G+qKHdQpjwVhheGOtMM50+h3d1+9Cp98J78F74T14L7zH2v1JM5ggTAAThAlW1t5wbfNRnEfrog3xiPpcUr9VdIqPMVMBV6J9EJQlKeBTwsUEnRJtmf5J/Ty6gIxr5675p/t5L1Pj68/F2azcbRcbXNNZtV0Wu1OMd7Hpqe8q9gwbrN3/p/IfPZV8BMkTHsxnrcRH5GTYXdTqvftzW80X81WJYsMmMmAZML8AHAP0MPDXF4zbl/d+AA==",
        },
        {
            "url": "https://puzz.link/p?factors/15/15/77kfnev5ulvdbs9vs5tpnrfblfbalfcf6iuuuapp9jsceghsd7jnsffo7v7jvhjo9u3u3dkojbsguffds7us-84+780-1a=110*6db0-9c-87-14=518*378c+5dc-62-164+1ef+120-75-28+1ef-a5+118-7e+9e76-48-62-18+1f8+738+168+24c+5a0-28%aa8+144+384-2c2-96-27+6e4+104-14+160-5a-23*ebb0*15cc+4eca$22c6cc$22550$38f30+270-1c-9a-1be-96+738-f0-2d-60-82-a2+555+168+1b8-1e+3d4-20-7e-8f",
            "test": False,
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
            self.add_program_line(area_product_aggregate(_id=i, src_cells=ar))

            for r, c in ar:
                if Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, f"corner_{Direction.TOP_LEFT}")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f":- not area_product({i}, {len(ar) - 1}, {num}).")
                    self.add_program_line(number_exclusion(int(num), grid_size=n, _id=i))

                if Point(r, c, Direction.CENTER, "normal") in puzzle.text:
                    num = puzzle.text[Point(r, c, Direction.CENTER, "normal")]
                    fail_false(isinstance(num, int), f"Clue at ({r}, {c}) should be integer.")
                    self.add_program_line(f"number({r}, {c}, {num}).")

        self.add_program_line(display(item="number", size=3))

        return self.program
