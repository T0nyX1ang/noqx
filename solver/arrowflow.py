"""The Arrow Flow solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, shade_cc
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected


def arrow_flow_adjacent() -> str:
    """Generate a rule to define the adjacency for arrow flow."""

    # the definition is designed to be compatible with the reachable propagation
    rule = "adj_line_directed(R, C, R, C + 1) :- grid_all(R, C), grid_all(R, C + 1), arrow_N_W__5(R, C).\n"
    rule += "adj_line_directed(R, C, R, C - 1) :- grid_all(R, C), grid_all(R, C - 1), arrow_N_W__1(R, C).\n"
    rule += "adj_line_directed(R, C, R + 1, C) :- grid_all(R, C), grid_all(R + 1, C), arrow_N_W__7(R, C).\n"
    rule += "adj_line_directed(R, C, R - 1, C) :- grid_all(R, C), grid_all(R - 1, C), arrow_N_W__3(R, C)."
    return rule


class ArrowFlowSolver(Solver):
    """The Arrow Flow solver."""

    name = "ArrowFlow"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7Vb/b6pIEP/dv+Jlf+0mx4JSJLlc1Kfv+q6l+tR4SoxBi0oLrodg32H839/MooVF2jRN7ltyQYaZzwyzM7Pwwd0fsRO6lCn40wwKVziqzBCnaujiVE7HwIt81/xEG3G05iEolN53OnTp+DuXfh2vb1u88fy58fveiCYT9kWJb5TRY+fx6lvw242nhaxjGd277p2nrhq/tpo9vX2ld+PdMHL3vYA1H4eTwbI7WtXVP9vWpJpM7pXa18nyp31j+HPFPtUwrRySupn0aPLFtAkjlKhwMjKlSc88JHdmYtGkDy5Cq1NKgtiPvAX3eUgExiDuNr1RBbWdqSPhR62VgkwB3TrpoI5BdcKQP8+sWTOFuqadDCjBxZvidlRJwPcurobFob3gwdxDYO5EML/d2tsSqoFjFz/wp/gUyqZHmjTSFsbnFmCRt1qAJOcWUE1bQK2kBews38LoYy34W15SfH16PMLGfIPyZ6aNnQwz1cjUvnkgBiNmlZK6ll6q4sJqOlwhwoIIDSLsKjyHYl+JBiG2lpnXYBovpq5IwTqkzQXrGIxP98k2YJmc26iDef1i1lXJyxRMpuZsvFsM9gXBBAzfmROgGgDUMlvDlLkUWg1T/JJLUcM79MzW5e6Zju2fV4AJMfMAcoyTxNYBl55K8HVEhCrkAAZPE03Iz0IqQtaEvBUxbSFHQraErAqpi5hr3Lp3bm66gVKRGhZZy4oUz91fVKStpfwlH7gb/zFsWrFJPw6XzsKFN9CKg7kbfrJ4GDg+2P21s3UJMCHZcX+2S+Nm7ndnEREzJeO8R8I2IpcE+ZxvfW9TluHskkBvteGhW+pC0H1YvZYKXSWp5jx8KNT07Pi+3Iv4UEnQwgsXvgxFIbBUzhYPnYQETrSWgBwpS5ncTWGYkSOX6Dw5hdWCbBzHCvlOxAl8Aq///5+tf+1nCzdJ+TC//TN0a8OsgeuSe0q28cyZwZwJ/DeiiMNX6v2Ov70v8aLw8A3WypxFuIS7AH2DvnLeMvwVpsp5i/gFLWGxl8wEaAk5AVrkJ4AuKQrAC5YC7BWiwqxFrsKqinSFS10wFi6VJy2bbOLQm/OYTCs/AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(shade_cc(colors=["arrow_N_W__1", "arrow_N_W__3", "arrow_N_W__5", "arrow_N_W__7"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(arrow_flow_adjacent())
        self.add_program_line(avoid_unknown_src(adj_type="line_directed", color="grid"))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__1", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__3", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__5", adj_type=4))
        self.add_program_line(avoid_same_color_adjacent(color="arrow_N_W__7", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(grid_src_color_connected((r, c), adj_type="line_directed", color="grid"))
            self.add_program_line(f"hole({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), adj_type="line_directed", color="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            fail_false(
                symbol_name.startswith("arrow_N") and symbol_name.split("__")[1] in ["1", "3", "5", "7"],
                f"Invalid symbol at ({r}, {c}).",
            )
            self.add_program_line(f"{symbol_name.replace('B', 'W')}({r}, {c}).")

        self.add_program_line(display(item="arrow_N_W__1", size=2))
        self.add_program_line(display(item="arrow_N_W__3", size=2))
        self.add_program_line(display(item="arrow_N_W__5", size=2))
        self.add_program_line(display(item="arrow_N_W__7", size=2))

        return self.program
