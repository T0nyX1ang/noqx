"""The Simple Loop solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import single_route


class SimpleLoopSolver(Solver):
    """The Simple Loop solver."""

    name = "Simple Loop"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZLbxoxEL7zKyKf5+Dnvm40Db3QpC1EUbRCaEM3CurSTYGtIiP+e8czphxK1EiJuAQZz/d5ZmyPbe0Mq19dtaxBy/AzGUhQ2NI8o545RV3GNp6vm7o4g363fmiXSACuBgO4r5pV3Suj16S38Xnh++A/FaXQAqgrMQH/tdj4z4UfgR+hSYBF3RCZEqCRXuzpDdkDO2elksgvI0d6i3Q2X86aejpkzZei9GMQYZ8PNDtQsWh/14Kn0XjWLu7mQXFXrfEwq4f5Y7Ssuu/tj07sttiC73O4wwPhmn245m+45nC4+i3CbeY/66dDkeaT7RZv/BvGOi3KEPb1nmZ7Oio2wllRWBAuI0g0Qa4IlJSMyjFqHTGObc6YxHFqGLOoz6M+57GWKiL76bieTngfE+1GpoyG5xkX9S5hzHbIfjbOs4b3s47XtYmJGP3S6JfyfJvx4W3Op3cyolYRdcSw7ja83galInlLckBSkxzjrYI3JD+SlCQdySH5XJC8IXlO0pJMyCcN7/LCl3t9OPhOKR4MP2qBPbyRQZaD0oYoInJLPLUQLsm88Ail46zx/+ZOfie/9+c36ZVi1C3vq1mNGXyImfzssl0uqkZgrdz2xJOgXuIXiDXmVD6PXj7D7cujpeK3qQwlXmxM5eCvQDx202o6axuB/8CAjZzdn7HuEv4zZq4Bh42hlPxjOfr1YOGZ9P4A",
        },
        {"url": "https://puzz.link/p?simpleloop/15/15/124000400000a0004g0002008h12000482008400004i1", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="grid", adj_type="line"))
        self.add_program_line(single_route(color="grid"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
