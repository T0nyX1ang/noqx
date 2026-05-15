"""The Hinge solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, count, display, grid, shade_c
from noqx.rule.helper import full_bfs, tag_encode
from noqx.rule.neighbor import adjacent, area_border


def hinge_symmetry(color: str = "black") -> str:
    """Generate the symmetry rule of Hinge."""
    rule = f'symmetry(R, C, R0, C0, "H") :- grid(R, C), {color}(R, C), {color}(R - 1, C), edge(R, C, {Direction.TOP}), symmetry_axis(R, C, R0, C0, "H").\n'
    rule += f'symmetry(R, C, R0, C0, "V") :- grid(R, C), {color}(R, C), {color}(R, C - 1), edge(R, C, {Direction.LEFT}), symmetry_axis(R, C, R0, C0, "V").\n'
    rule += f"symmetry(R, C, R0, C0, D) :- grid(R, C), {color}(R, C), adj_4(R, C, R1, C1), symmetry(R1, C1, R0, C0, D).\n"

    rule += f":- grid(R, C), {color}(R, C), symmetry(R, C, R0, C0, D0), symmetry(R, C, R1, C1, D1), (R0, C0, D0) != (R1, C1, D1).\n"
    rule += f":- grid(R, C), {color}(R, C), not symmetry(R, C, _, _, _).\n"

    rule += ':- symmetry(R, C, R0, C0, "H"), not symmetry(R0 * 2 - 1 - R, C, R0, C0, "H").\n'
    rule += ':- symmetry(R, C, R0, C0, "V"), not symmetry(R, C0 * 2 - 1 - C, R0, C0, "V").\n'
    return rule


def hinge_avoid_isolated_edge(rows: int, cols: int, color: str = "black", adj_type: int = 8) -> str:
    """A rule to avoid the region border not continuously separating a block."""
    tag = tag_encode("reachable", "border", "adj", adj_type, color)
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    initial = "\n".join(f"{tag}({r}, {c}) :- {color}({r}, {c})." for r, c in borders)
    propagation = f"{tag}(R, C) :- {tag}(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    constraint = f":- grid(R, C), area_border(_, R, C, _), {color}(R, C), not {tag}(R, C)."
    return initial + "\n" + propagation + "\n" + constraint


class HingeSolver(Solver):
    """The Hinge solver."""

    name = "Hinge"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZdT+NGFH3Pr0B+nof5tGf8smIp7Asbtg0rhKwoCsGUqIlCE7KqHOW/c+71NUYpK7qqSqWqSjxzfDK+c+65MxNvft9O17Uyhr4uKq2AlA85X8ZYvrR8LuePi7o8Usfbx/vVGkCpi7MzdTddbOpBJaPGg12TyuZYNZ/KKjOZyiwuk41V83O5az6XzUg1I/yUqQjuvB1kAU97eMW/EzppSaOBh4IBrwFn8/VsUU/OW+ZLWTWXKqN5PvLTBLPl6ludiQ66n62WN3MibqaPSGZzP3+QXzbb29VvWxlrxnvVHH9fruvlEmzlEnpFLmXxD8tN4/0etv8CwZOyIu1fexh7OCp3aIflLnOWHvXQ0tYmc5EIlKojvDkgcn7kJeF5et0zURMTXxA5ER96IjGR94TRxYES4w5nNuFQrSkOxZgiEPMsBnkazvaa2zNuLbeXMEM1jtufuNXcBm7PecwpPLKFUZYmsljDhQV2gh0wkmfsgTE14wCMBBnnwEiNcQEMfxlH4CQ4KUuWEQ5a2Vzi5IjT8RF8Ej4F5WA3YfTK2ZZHr5wX3oMPwgfwhfAF+NjphP4oemJUTrd5oUf8lkevnBPegffCe/C58Dl4yQu9ckn45JTXL3jJFz00iB7k5SIKzZjOntZn9MASJyJ+bH1G/6wfPXDrM3pg8Rn+WFpgjOF/ann2hJYzY8zlpaYedaFVzZ5TfSWOR02D1CigRlJrZzCXkZim6L3KEVPioO/9obxED3rlTZcvckniSUrgZS1F+KNlLo0xRsYY8E54B94L78HTJuR5wcv6QQ8s8+bQnIvmHJrzTjPVUeIEelawQ8wgMS14J7wGb0VnAq/FH9Qa94LhoawBm7B3knibaA23uVOOuJeY0GkFW9TIiX4HPgiPfeGC+BbgJx0FjOFz6NYncumwxZqhs4zjg7fd2kbu3ZrU8ISOnU6DJq+w6a94659w67nN+Ugo6PT8i+crn6yRRLUxcdj+/aPoTW2Vwz/1K5/w32XHgyobbdd301mNv8TT21/ro+FqvZwucDfcLm/qdXePN5L9IPsj46ty9ILz/0vKv/SSQiXQP/Sq8g675w05FdzF/mouVPawnUwnsxXWGLxj3v2Jf3f12P7jwRM=",
        },
        {
            "url": "https://puzz.link/p?hinge/14/12/k1ag51905514k4kgii2i8qa29800a010000rtg060s007o0007o30e0o0cfjg00-2bh26262626g2h",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c("gray"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(hinge_symmetry(color="gray"))
        self.add_program_line(hinge_avoid_isolated_edge(puzzle.row, puzzle.col, color="not gray", adj_type=8))

        # horizontal symmetry axis check
        for r in range(1, puzzle.row):
            c = 0
            while c < puzzle.col:
                if Point(r, c, Direction.TOP) in puzzle.edge:
                    c0 = c
                    while c < puzzle.col and Point(r, c, Direction.TOP) in puzzle.edge:
                        self.add_program_line(f"edge({r}, {c}, {Direction.TOP}).")
                        self.add_program_line(f'symmetry_axis({r}, {c}, {r}, {c0}, "H").')
                        c += 1
                c += 1

        # vertical symmetry axis check
        for c in range(1, puzzle.col):
            r = 0
            while r < puzzle.row:
                if Point(r, c, Direction.LEFT) in puzzle.edge:
                    r0 = r
                    while r < puzzle.row and Point(r, c, Direction.LEFT) in puzzle.edge:
                        self.add_program_line(f"edge({r}, {c}, {Direction.LEFT}).")
                        self.add_program_line(f'symmetry_axis({r}, {c}, {r0}, {c}, "V").')
                        r += 1
                r += 1

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            if rc:
                num = puzzle.text.get(Point(*rc, Direction.CENTER, "normal"))
                if isinstance(num, int):
                    self.add_program_line(count(num, color="gray", _type="area", _id=i))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
