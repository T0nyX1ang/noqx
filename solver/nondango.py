"""The Nondango solver."""

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import area, count, defined, display, grid, invert_c, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.shape import avoid_rect


def avoid_diagonal_3(color: str = "black") -> str:
    """Generate a constraint to avoid diagonal in a row of three."""
    rule = f":- {color}(R, C), {color}(R + 1, C + 1), {color}(R + 2, C + 2).\n"
    rule += f":- {color}(R, C), {color}(R + 1, C - 1), {color}(R + 2, C - 2).\n"
    return rule


class NondangoSolver(Solver):
    """The Nondango solver."""

    name = "Nondango"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZNT9tAEL3nV6A978Gza8de3yiFXvhoCxVCVhSF4BbUoNBA2spR/jtvZreKUQchtSWnyvLsy2Q8++bt7Nr335aTRWsrXL6ymSVcPndyuyzInaXr7OZh1tY7dnf5cD1fAFh7cnBgP09m9+2gSVGjwaoLdbdru3d1Y8hY43CTGdnuQ73qjuruwnan+MtYgu8wBjnA/Q08l/8Z7UUnZcDHCQNeAE5vFtNZOz6Knvd1051Zw/O8kacZmtv599YkHvx7Or+9vGHH5ezHdfLdL6/mX5cpikZr2+0+T9RviDKMRBkpRJn/qxENo/UaUn8E1XHdMOtPG1ht4Gm9gj0WS2Iv6pVxQ6TJMU2fmnGV5vWZ6vWqN2jenFRvrnoLzVuoHAqnevUMasVFqXmHqg5DtbZSraJUOZTqbKU6W6nOVqk6VGptlTpbpc4W1LxBXbegqh7Ufgj6bGptlKnTUaZmpkwVnkithEglTaTnpmdyqzoTKUJjnx3IbnNiz7AZbefFvhWbiS3EHkrMPvYlVTiAK3B1yFs5YBAU7IHBSnAOjAYTXACDluAhMLgILoEhvuAKGJIDu6zAkR7jMQLHeIzAMR4jH/sJ4xXAkjKmDBhrJJiAI0+MwJGnc4jnA4OxR7xP8R7xPsV7xPPxIdgDx7owAse6MAInnh48faqrCJbKmBPjU31C0iRwjb26KNVCzK3HJ08ccnDgQ4OfHSJnmXKWrHlP55A4BNaqp49LOR3X2KuLjzLJDz580Eh+5OTDQfLz2vXWi7eF5GfNezq7X9qyVj198lRjDj4FP4smOpdW2hObix1Ki5X8NvjL9wXmUk57+heN/yLzxqG5n1wQb5u/R4PG7F99aXeO54vbyQyv5NPryV1r8L2zHpifRu4Gq2vz/59AW/wEYtmzP27sV+rWF+g00BX93J1Yc7ccT8bTOfoJqrHfh9/8W2eP7TYaPAI=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_c(color="circle_M__1"))
        self.add_program_line(invert_c(color="circle_M__1", invert="circle_M__2"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__1"))
        self.add_program_line(avoid_rect(1, 3, color="circle_M__2"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__1"))
        self.add_program_line(avoid_rect(3, 1, color="circle_M__2"))
        self.add_program_line(avoid_diagonal_3(color="circle_M__1"))
        self.add_program_line(avoid_diagonal_3(color="circle_M__2"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="circle_M__2", _type="area", _id=i))

        for r in range(puzzle.row):
            for c in range(puzzle.col):
                symbol_name = puzzle.symbol.get(Point(r, c, label="nondango_mark"))

                if symbol_name == "circle_M__1":
                    self.add_program_line(f":- circle_M__2({r}, {c}).")

                elif symbol_name == "circle_M__2":
                    self.add_program_line(f":- circle_M__1({r}, {c}).")

                elif symbol_name != "circle_M__4":
                    self.add_program_line(f"hole({r}, {c}).")

        self.add_program_line(display(item="circle_M__1"))
        self.add_program_line(display(item="circle_M__2"))

        return self.program
