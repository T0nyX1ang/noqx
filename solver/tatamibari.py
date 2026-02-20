"""The Tatamibari solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Point, Puzzle
from noqx.rule.common import display, edge, grid
from noqx.rule.helper import fail_false, reverse_op, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected
from noqx.rule.shape import all_rect_region, avoid_edge_crossover, count_rect


def tatamibari_cell_constraint(op: str, src_cell: Tuple[int, int]) -> str:
    """Generate a cell relevant constraint for tatamibari."""
    tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
    rop = reverse_op(op)

    src_r, src_c = src_cell
    count_r = f"#count {{ R: {tag}({src_r}, {src_c}, R, C) }} = CR"
    count_c = f"#count {{ C: {tag}({src_r}, {src_c}, R, C) }} = CC"

    return f":- {count_r}, {count_c}, CR {rop} CC."


def encode_symbol_to_text(puzzle: Puzzle) -> None:
    """Encode the symbol clues to text clues for tatamibari."""
    for (r, c, d, label), symbol_name in puzzle.symbol.items():
        validate_direction(r, c, d)
        validate_type(label, "normal")
        if symbol_name == "line__1":
            puzzle.text[Point(r, c, d, label)] = "-"

        if symbol_name == "line__2":
            puzzle.text[Point(r, c, d, label)] = "|"

        if symbol_name == "line__5":
            puzzle.text[Point(r, c, d, label)] = "+"


class TamamibariSolver(Solver):
    """The Tatamibari solver."""

    name = "Tatamibari"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VZtb7JIFP3ur2jmaydZBnxBks3GWu22a61tNa4SY9Ci0oLj8mK7mP733jv4CIPYzbObNP2wQW7uPWe4nLmEg8FfkeXbtA6HplOFMjg0XRGnXsafsj/6TujaxhltROGK+5BQetdu04XlBja9Ga06Td54vWz8udXD8ZhdKdG1MnxuP58/eH9cO5rP2l29d9u7ddRl4/fmxX21dV7tRcEgtLf3Hrt4Hoz7i95wWVf/bnXH5Xh8p1Ruxotfto3BryVzr2FS2sV1I27Q+MowiUqoOBmZ0Pje2MW3Rjyi8SNQhDLAOpAxQlVIW2k6FDxmzQRkCuTdfQ7pyDDjjsh6kPUpwf4X4ipMice3NkmWi3rOvZmDwMwKYUTBytnsmSB64i/Rfi00JF7khs6cu9xHELF3GjcS6a0C6VoqHdNEOmanpRPPClfTq6T+yQ3YT0s7iGZF6uvF6t/hiTyA/qlh4lYGaaqn6aOxg9g1dkRT8crf4NLksRFdyQN6DmBaVUKgExP9RtBPxdUqjEtMV8Nm7FCVoaocKuxyWFmRuCqqOnC6xDEFL0xLJrNiQ5kS2UMnpknyWBn17RfDBtpiG6qIfZgUjTURL0VURKyI2BFrWiIORWyKWBaxKtbUcNY/9TSyk/x3cmCqMJ26DuOtwc4xYeAYrF4jhgZ5nVFVAUL7R92mqgvryR6V74VMSiZpwQty1uW+Z7nwknQjb2b7af24sjY2AZMiAXenQeQvrLk9td+seUiMxCezjIStRS8JcjnfuM66qMMPSgKd5Zr7diGFIL7cJ1ohVdBqxv2nnKZXy3XlvYjvhwTNHX/uylDog79kasv3+auEoGtJQMZMpU72OjfM0JIlWi9W7m5eOo73Enkj4jQ1eKjl/78o3++Lgk9H+WIn+6/GasKwD95H4ztKNtHUmsLWCPxtoQm9t8NiGqz0BFErHxFfvnvxHnH/E1NLyTxcYG2AfuJuGbYIP2FkGTaPH7kWij02LkALvAvQvH0BdOxgAB6ZGGAnfAy75q0MVeXdDG91ZGh4q6ynmZPSBw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        encode_symbol_to_text(puzzle)
        fail_false(len(puzzle.text) > 0, "No clues found.")
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_rect_region())
        self.add_program_line(avoid_edge_crossover())
        self.add_program_line(count_rect(len(puzzle.text)))

        all_src: List[Tuple[int, int]] = []
        tag = tag_encode("reachable", "bulb", "src", "adj", "edge", None)
        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(bulb_src_color_connected((r, c), color=None, adj_type="edge"))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if clue == "+":
                self.add_program_line(tatamibari_cell_constraint("eq", (r, c)))
            elif clue == "-":
                self.add_program_line(tatamibari_cell_constraint("lt", (r, c)))
            elif clue == "|":
                self.add_program_line(tatamibari_cell_constraint("gt", (r, c)))

            all_src.append((r, c))

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
