"""The Scrin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import display, grid, invert_c, shade_c
from noqx.rule.helper import tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import bulb_src_color_connected, grid_color_connected
from noqx.rule.shape import all_rect, count_rect_size, no_rect


def ensure_scrin_loop(color: str = "black") -> str:
    """A rule to ensure the shaded rectangles form a single loop."""
    rule = f'rect_id(R, C, R, C) :- rect(R, C, "{Direction.TOP_LEFT}").\n'
    rule += f'rect_id(R, C, R, C0) :- rect(R, C0, "{Direction.TOP}"), rect_id(R, C, R, C0 - 1).\n'
    rule += f'rect_id(R, C, R0, C) :- rect(R0, C, "{Direction.LEFT}"), rect_id(R, C, R0 - 1, C).\n'
    rule += f'rect_id(R, C, R0, C0) :- rect(R0, C0, "{Direction.BOTTOM_RIGHT}"), rect_id(R, C, R0 - 1, C0 - 1).\n'
    rule += f':- rect(R, C, "{Direction.TOP_LEFT}"), #count {{ R2, C2: rect_id(R, C, R1, C1), not rect_id(R, C, R2, C2), adj_x(R1, C1, R2, C2), grid(R2, C2), {color}(R2, C2) }} != 2.'
    return rule


def border_color_unspawn(rows: int, cols: int, color: str = "black", adj_type: int = 4) -> str:
    """A helper rule to generate all the {color} cells not connected to the border with the `white_unspawn` predicate."""
    borders = [(r, c) for r in range(rows) for c in range(cols) if r in [0, rows - 1] or c in [0, cols - 1]]
    rule = "\n".join(f"white_spawn({r}, {c}) :- {color}({r}, {c})." for r, c in borders) + "\n"
    rule += f"white_spawn(R, C) :- white_spawn(R1, C1), {color}(R, C), adj_{adj_type}(R, C, R1, C1)."
    rule += "white_unspawn(R, C) :- grid(R, C), white(R, C), not white_spawn(R, C)."
    return rule


class ScrinSolver(Solver):
    """The Scrin solver."""

    name = "Scrin"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZbb+pGEH7nV0T7mpXq9Q1jqQ+EQHpOCSEBRIOFkCEGnNg49YWkRvz3zKyhvkJb9SjtQ2R5mPlmd3Yu8rcEv0emb1FWp4xRSaMCZfComkxlRaVMARxe4fAM7dCx9AvajMK154NC6V2nQ5emE1j0++O62/Kab9fN37ZaOJmwGyH6JoyfO8+XD+6v32zJZ52e1r/t39riqvlL6+pebV+q/SgYhdb23mVXz6PJcNkfrxriH+3eRI4nd4LyfbL8adsc/VwzDjlMa7u4ocdNGt/oBpEIJQxekUxpfK/v4ls97tF4AC5C2ZQSN3JCe+E5nk+OWNwFDTaJoLZTdcz9qLUSkAmg9xJdBfUR1IXtLxxr1k0C9XUjHlKCZ1/x3agS19taeBjmhfbCc+c2AnMzhPYFa/uVUAkcQfTkvUSHpWy6p3EzqWBwrEA7XwEEOVaAalIBahUVYGH/ugLraWW9VyTfmO73MJcHSH+mG1jJKFW1VB3oO5A9fUdkBbZKVMXxQbS6AKb8p6kxDHwBfT8ADSm3nIm4QM3YjbxflsFWUlupFwIyFU/UUptnkIlQxwhpRiLDhMWMrYENX8rR5hml+0UR92dPFCWsIYeUshJVNRMFWsV4wx657HApcjmEftJY4vKaS4FLhcsuX9Pmcsxli0uZS5WvqeNE/ubM+LQ0SmTIDn8gbfhREUzG+QmZGrLMqenco3yt+NErpjWDDCJ/aS4sIIM2fP8XPc93TQesXuTOLf9oAzGTwHNmQbJ6Zr2bi5Doyd2Q9eSwDY+RgxzPe3XsTVWEoysH2quN51uVLgSRs06EQldFqLnnPxVyejMdJ18LvzdzUMKsOSj0gTYztun73lsOcc1wnQMyl0QukrUpNDM08ymaL2bhNDdtx75G3gl/gV1EHOvXLfr/vEVxRsI/ukv/+2vCgF7LKo3vKHmNZuYM+sxbxXHlBF4v4NAOxPHvZuUGuBurd5Qd8l+EUss5fXpH+Rfq+WfoMnUW4QrSBPQMb2a8VfgJisx4i3iJDzHZMiUCWsGKgBaJEaAyNwJYokfATjAkRi2SJGZV5Ek8qkSVeFSWLQ0SLHx7Q6a1Dw=="
        },
        {"url": "https://puzz.link/p?scrin/15/15/v3o3x3l3k3y3k3q3k3p3q3j3q3q3j3q3v3m3q3v", "test": False},
        {"url": "https://puzz.link/p?scrin/18/10/p.m3k.n2m3l5l4l.v2o64o.v.l4l1l3m.n2k1m4p", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(invert_c(color="gray", invert="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="x"))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(grid_color_connected(color="gray", adj_type=8))
        self.add_program_line(all_rect(color="gray"))
        self.add_program_line(ensure_scrin_loop(color="gray"))
        self.add_program_line(border_color_unspawn(puzzle.row, puzzle.col, color="white", adj_type=4))
        self.add_program_line(no_rect(color="white_unspawn"))

        all_src = []
        tag = tag_encode("reachable", "bulb", "src", "adj", 4, "gray")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")
            self.add_program_line(bulb_src_color_connected((r, c), color="gray", adj_type=4))

            for r1, c1 in all_src:
                self.add_program_line(f":- {tag}({r}, {c}, {r}, {c1}), {tag}({r1}, {c1}, {r}, {c1}).")
                self.add_program_line(f":- {tag}({r1}, {c1}, {r1}, {c}), {tag}({r}, {c}, {r1}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_rect_size(num, (r, c), color="gray", adj_type=4))

            all_src.append((r, c))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program

    def refine(self, solution: Puzzle) -> Puzzle:
        """Refine the solution by adding edges around shaded cells."""

        for (r, c, _, _), color in solution.surface.items():
            if color in Color.DARK and solution.surface.get(Point(r - 1, c)) not in Color.DARK:
                solution.edge[Point(r, c, Direction.TOP)] = True

            if color in Color.DARK and solution.surface.get(Point(r + 1, c)) not in Color.DARK:
                solution.edge[Point(r + 1, c, Direction.TOP)] = True

            if color in Color.DARK and solution.surface.get(Point(r, c - 1)) not in Color.DARK:
                solution.edge[Point(r, c, Direction.LEFT)] = True

            if color in Color.DARK and solution.surface.get(Point(r, c + 1)) not in Color.DARK:
                solution.edge[Point(r, c + 1, Direction.LEFT)] = True

        return solution
