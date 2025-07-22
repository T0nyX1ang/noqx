"""The Yajilin solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, direction, display, fill_path, grid
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent, avoid_adjacent_color
from noqx.rule.reachable import grid_color_connected
from noqx.rule.variety import yaji_count


class YajilinSolver(Solver):
    """The Yajilin solver."""

    name = "Yajilin"
    category = "loop"
    aliases = ["yajirin"]
    examples = [
        {
            "data": "m=edit&p=7ZZ9T/o6FMf/51WY/msTNzZwLDE3PJoYRLng5epClgJFhoXqHpTfiO/d0xbuHhhGY3IfkhvY4exz2rNz2uxbgpeI+BTrmvgaFoZf+Ji6Ja+yVZWXtvsMvZBR+wTXo3DBfXAwvul08JywgOKr+2Wj9VR/a9f/PKs8GMZdb366bPXvlrPRH3pf8858rces9fVtq8FOL+OH60X9lbZp9Tbg0wWjZEbih9HVhq071uNirjevFk1rTtZa8GINa6+N/sVFydkVMi5t45od13F8aTuojLC8dDTGcd/extd23MPxAEIIW8C64OkIl8FtJ+5IxoXXVFDXwO+phDq49+BOPX/KqNtV5NZ24iFG4jkNOVu4aMVfKVIp5P2UryaeABMSwnoFC+95FwmiGX+KdmMhIVpFLPSmnHFfQMHecVxXLXT3LZhJC0bSgnBVC8IraEF09uMWmLemm6Lqa8XVv8PO/A71u7YjWrlLXCtxB/YWbM/eIkMTM3+DqWILIWVFl/ld0csOVQ2BDNdIkCWn6WlUK6tRqYm6JmeWXbGfe6ZXDpmxm6ulmGmqcWlWlXP/qhZ60GUn99J2pC1LO4RGcWxI25JWk7YibVeOaUs7krYprSltVY45F0v1xcVEZhXZplrSnxSFzDKsRM2CNdct5ZgmNqFrAyMDZEF4X6zcMZSUZD+V/x4blxw0iPw5mVJ4D7rwPpz0uL8iDO560WpC/f09qBIKOHMDNdqlGzINka3UMR3JsLXMkUGM82fx4hVk2Icy0Htcc58WhgSks8djqUSoINWE+7NcTW+EsWwv8uTIIKU0GRT6ICOpe+L7/C1DViRcZEBKNTOZ6Dq3mCHJlkieSO5pq2Q53ktog+TlGOKE+/8I+fceIWKXtG8dJP+8FDvxAJtVHN9g9By5xIWeEPxRwZ/y8yPc+iY/lqfwud29qh8JKqEvDsK5UByAk+Mg8LfvkHznuf+JACfBPC6QYaCfKHEqWsSPiG4qmucHCiuKPRRZoAU6CzQvtYAO1RbggeACO6K5ImtedkVVeeUVjzoQX/GotP466BdZerBeaFz6AA==",
        },
        {
            "url": "https://puzz.link/p?yajilin/19/13/g24g33f45o23d30g32z43k41y11a11a42zo33a14a12b11d31a32c21e11t36g31e21y",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="gray"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line("{ black(R, C); white(R, C) } = 1 :- grid(R, C), not gray(R, C).")
        self.add_program_line(fill_path(color="white"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(avoid_adjacent_color(color="black", adj_type=4))
        self.add_program_line(grid_color_connected(color="white", adj_type="loop"))
        self.add_program_line(single_loop(color="white"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")

            # empty clue or space or question mark clue (for compatibility)
            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace() or clue == "?"):
                continue

            fail_false(isinstance(clue, str) and "_" in clue, "Please set all NUMBER to arrow sub and draw arrows.")
            num, d = clue.split("_")
            fail_false(num.isdigit() and d.isdigit(), f"Invalid arrow or number clue at ({r}, {c}).")
            self.add_program_line(yaji_count(int(num), (r, c), int(d), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"black({r}, {c}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} grid_direction({r}, {c}, "{d}").')

        self.add_program_line(display(item="black"))
        self.add_program_line(display(item="grid_direction", size=3))

        return self.program
