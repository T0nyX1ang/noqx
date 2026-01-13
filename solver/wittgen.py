"""The Wittgenstein Briquet solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, edge, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import OMINOES, all_shapes, general_shape


def edge_around_shade(color: str = "gray") -> str:
    """Generate constraints to ensure shaded cells are surrounded by edges."""
    rule = f':- {color}(R, C), not edge(R, C, "{Direction.TOP}").\n'
    rule += f':- {color}(R, C), not edge(R, C, "{Direction.LEFT}").\n'
    rule += f':- {color}(R, C), not edge(R + 1, C, "{Direction.TOP}").\n'
    rule += f':- {color}(R, C), not edge(R, C + 1, "{Direction.LEFT}").'
    return rule


class WittgensteinBriquetSolver(Solver):
    """The Wittgenstein Briquet solver."""

    name = "Wittgenstein Briquet"
    category = "var"
    aliases = ["wittgensteinbriquet"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb9pIEH7nr6j2tSud1z/AtnSqSGp67SUECigXLIQMcRInNpszNukZ8b93dgxlvXbaVJXu7iEyOxp/Mzs7s2N9w/rvPEhDynTxM2yqUQaP6Zi4jI6FS9s/4yiLQ/cN7ebZHU9BofSi16M3QbwO6aeru7NT3n163/1rY2fTKfug5R+1y/ve/dvPyZ8fIyNlvb49OB+cR/pt94/Tk2Hbe9se5OtJFm6GCTu5n0zHN4PLW0f/x+tPzWJ6oVmfpje/bbqT31v+PodZa1s4bjGkxQfXJ4xQosNiZEaLobstzt2iT4sRmAi1Z5QkeZxFSx7zlCDGwO+s3KiD6h3VS7QL7bQEmQZ6f6+DegXqMkqXcTg/K5GB6xdjSsTZJ7hbqCThm1AcJnIT70ueLCIBLIIMrm99Fz0SaoBhnV/zh3zvymY7WnTLCrwXVgBBDhUItaxAaA0ViMJ+vYL4kTfk7sx2O2jLZ8h+7vqikMlRtY/qyN2C7LtbYphiqwZJlL0jhiMAaOUBMK3DxewBq6MAbVsAxhHoqFtsQwEcXTmFaYhIQZiGUWSEYbJSGKZjYCl9ZmAc2cdkKmJpamQL48hIGxE5w04tso1xZB9bvRvm4OVIPjrDXVLOOmsru3SGXXgnITpW8W0XtI9hE69Q9lDqKMfQY1oYKN+j1FBaKM/Qx0N5ifIUpYmyjT4d8ZW88DsiBrTJhq8CqrLLj+rXcyO2aL4DYfWOTXUH+m78MF/fMJEz64/1iotn1vLJKE9vgmUIfOJd34Zv+jxNghje+nmyCNPDO3A7WfN4vi695+GXYJkRtxwvsqWCrTBGBYo5f4yjVVOEg6kCRrcrnoaNJgGGkPMzoYSpIdSCp9dKTk9BHFdrwdFbgUpyrkBZCswrvQdpyp8qSBJkdxVAmjOVSOFKucwsqKYYPATKacnxOnYt8oXg8g0KfxdeB/H/dBCLFmk/NY7/e1b3ixEFHi0uKHnM58EcrhnvpRGHG/SLq5fjcE0ijsWa/Bvwg7/W5O+J4WDCcICZWDVDj39ohmqsptM8CqOnOZ6ttX/S8G161cz/eteRRHj6HUY/GlW4gdcB/Q61S9Ym/BkWl6wqXqNskWydtQFtIG5AVe4GqE7fANYYHLBnSFxEVXlcZKVSuTiqxubiKJnQfbLK0+ghWIRk1voK",
        }
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(general_shape("omino_3", 0, OMINOES[3]["I"], color="not gray", _type="grid", adj_type="edge"))
        self.add_program_line(all_shapes("omino_3", color="not gray", _type="grid"))
        self.add_program_line(edge_around_shade(color="gray"))
        self.add_program_line(grid_color_connected(color="gray", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"gray({r}, {c}).")
            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="not gray", adj_type=4))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"gray({r}, {c}).")

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="gray", size=2))
        self.add_program_line(display(item="edge", size=3))

        return self.program
