"""The Statue Park solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.helper import validate_direction
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import all_shapes, count_shape, general_shape, parse_shapeset


class StatueParkSolver(Solver):
    """The Statue Park solver."""

    name = "Statue Park"
    category = "var"
    examples = [
        {
            "data": "m=edit&p=7VZNa9tAEL3rV5Q5z0Gzqy/r5rpxL07T1i4hCGEcVSGmMkptqy1r/N87O5YrSOZQCkmhFLGP56fx6M0w2tXua7fa1kiEFKLNMERmGMUJRpRhTKmssL8W631T569w3O3v2y0TxKvpFO9Wza4Oij6qDA5ulLsxurd5AQQIhhdBie5DfnCXOVTt5nYN6OZ8H5D4xuwUaZheDPRa7ns2OYkUMn/Xc6Y3TKv1tmrq5eykvM8Lt0DwD3st//YUNu23Gnoz/vfJAAu3zff7Xtt1n9svHZyTH9GNxa2bn41mg1E7GLW/jFrdqHlOo6PyeOR+f2Sry7zwrj8NNBvoPD8cvSOPJHiTHyC2nIbwbO1SrEGcaGqaampGqqrmzWJV9U8zj9WRUVU9VnU2yrRYCkNdNloOCtXURGrVRGrZRGrdRKnqxKiVk9Fzm0iPVhtFRu+J1Xti9Sr1oSFtanjMpjJsRnDBs4jOCr4RDAVjwZnEXAheC04EI8FEYlI/zb857xBxg7mqhP1mT4f/mbwV1sgW+viK/wW1DAqYd9u7VVXzZjRpNw/tbr2vgbf8YwA/QFZh/Qny/xR46VPA9z7847Pg77yqBfc1StFdITx0y9WyahvgLwj0emKf6C/unt/nMvgJ",
            # "config": {"shapeset": "double_tetro"},
        },
        {
            "url": "https://puzz.link/p?statuepark/12/12/3g3g6000515100003ala0i003g3a0060515160003g3g0000//p",
            # "config": {"shapeset": "pento"},
            "test": False,
        },
    ]
    parameters = {
        "shapeset": {
            "name": "Shape Set",
            "type": "shapeset",
            "default": [],
            "presets": ["tetro", "double_tetro", "pento"],
        },
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="gray"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not gray", grid_size=(puzzle.row, puzzle.col)))
        self.add_program_line(all_shapes("omino_statue", color="gray"))

        shapeset = parse_shapeset(puzzle.param["shapeset"])
        for i, (o_shape, o_count) in enumerate(shapeset.items()):
            self.add_program_line(general_shape("omino_statue", i, o_shape, color="gray", adj_type=4))
            self.add_program_line(count_shape(o_count, name="omino_statue", _id=i, color="gray"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            if symbol_name == "circle_M__2":
                self.add_program_line(f"gray({r}, {c}).")
            if symbol_name == "circle_M__1":
                self.add_program_line(f"not gray({r}, {c}).")

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} gray({r}, {c}).")

        self.add_program_line(display(item="gray"))

        return self.program
