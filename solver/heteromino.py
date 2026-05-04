"""The Heteromino solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, edge, grid
from noqx.rule.helper import fail_false
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import OMINOES, all_shapes, avoid_same_omino_adjacent, general_shape


class HeterominoSolver(Solver):
    """The Heteromino solver."""

    name = "Heteromino"
    category = "region"
    examples = [
        {
            "data": "m=edit&p=7VVNa9tAEL37V4Q5z0H7IVnWzU3tXtykrV1CEMIoitKIyiiVrVLW+L93dmaxKTW00Da0UOR973n2842Y1fbTUPY1qsj/TIrE9FiVctNpwi0Kz6rZtXV2gdNh99j1JBCv53N8KNttjaM8DCtGezfJ3BTdqywHDchNQYHubbZ3rzO3RLekLkBLsQUpBahJzk7yhvu9upSgikhfBU3ylmTV9FVbrxcSeZPlboXg93nBs72ETfe5BpnG/6tuc9f4wF25Izfbx+Yp9GyH++7jAMctYDO0u6bq2q4HXk8VB3RTsTA7Y8GcLJijBXPegv7zFibnLRzo9bwjE+ss937en2R6kstsDzaGzCLYMVMcCSkhLTRhSiSYJExjI2SFZJVxKiQTUllMqTiw7KF0iGsVWAeWacqEuLGBZUdlTeAQD0dXVnZVfPiDT/6eUDHeMs4ZNeOKvKMzjC8ZI8aYccFjZow3jJeMljHhMWOfvZ/M7+86DmWfXE5SKjNlUGtKpfnhEXMjlf7tE/97sWKUw3LoH8qqphqY3X+oL666flO2QNfQYQRfgFtOmfGD/99Mf/XN5F9V9Mz186vlnFPGj6WH7hrhaViXa7IG9C1E300V+l3Hs7ugoi9GXwE=",
        },
        {
            "data": "m=edit&p=7Zffb9s2EMff/VcUeuaDxDseJb9lXdKXtN2WFEVhGIHrumtQB26deBgU+H8fRX60PMzBtnbrMMCwxTvxfvC+dydSuv28W2xXzofhL62rXZN+XdvmS32dr/F3eX23Xk2fuJPd3YfNNjHOvTw7c+8X69vVZIbWfHLfd9P+xPXPprPKVy5fTTV3/Y/T+/75tL9w/UUSVU7T3Hnimsr5xJ4+sK+zfOCelsmmTvwL+MS+Sezyertcr67Oy8wP01l/6aphne+y9cBWN5tfVlUxy/fLzc3b62Hi7eIugbn9cP0Jye3u3ebjrhqX2Lv+pIR7eiBceQhXfg9XDofr//1wu/l+n9L+Uwr4ajobYn/1wLYP7MX0vrK2mqqrrMskNoX4QqQQzaQrsq7IupBJUxu0OGiaGlrUGs+9b6DjvEDx41sofgQ7wU5YR2KhilzHe+yCQvEbsAvoGf6MOIw4DDsS0UTsInG16HfFj6/LvG8Myjx4vVdogBa/XrgHhxfm1UMFij34vLJeaKDog9eD0wf0wOMN+0hc4PGRdVvk1NN3RS51A/XQ4k+oqzQCHefL+kJ9BfziIxS/glywF/TIi5APob6ixAFOoY4CTqGeQj3FiAPcQn8LnS00s4BfWtZpiYd8SItdx3yHHXlS8qN1kSt5UfKhTbFX8qF+vC/rKnlQcKqO9/ij/qqsRx8ofa4BO/pcqb+SDwW/0s/KI62R+RY9+lrBr/R3qGtoCy1+As93oP4BvKEJUPS8Qbmn3oE6B/o/gDco+tQ5UOcAnkB9g2EPvkA9Q2QeHKFlXbarAC4Dl7FvGXUz8Bg4jPoZ9TP62NiXjL406mbgMOpmPK/Gc2oBObjM8AM+Yx+yOFL8UC+jX416GX1q4LOODZx+jHWRR/BF8EWe08g+FalPBFekTpE6RSk4IjijjmeCQkc5fsaDJO+f++HUu09jk8c3eTzLo8/jZTqIXC95/D6PdR5DHs+zzmkeX+fxaR41j5Z14nCU/cXD7p8KJ50GQ/t0bd5fQ+E6E9cN1ZDEdz7xKVPyp5HPrLxk/Z1fOFocLY4WR4v/h8V8Mqsudtv3i+Uqfa2cvvt59eTFZnuzWFfp43A/qX6t8jWTpKzH78X/6HtxKEH9jQ/Srz3XZym76dOuS0doSJ+nrn/pqk+7q8XVcrOuXEriqJC60NIbz2EFkbp+VNI87vTrVk0KbTd4+GKFL4p7fE15TMyby2Hx8LZzWDK8Ef1B8s27Jb1OzSe/AQ==",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false((puzzle.row * puzzle.col - len(puzzle.surface)) % 3 == 0, "The grid cannot be divided into 3-ominoes!")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(edge(puzzle.row, puzzle.col))
        self.add_program_line(adjacent(_type="edge"))
        self.add_program_line(all_shapes("omino_3", color="grid"))
        self.add_program_line(avoid_same_omino_adjacent(3, color="grid", adj_type="edge", allow_isometry=False))

        for i, o_shape in enumerate(OMINOES[3].values()):
            self.add_program_line(general_shape("omino_3", i, o_shape, color="grid", adj_type="edge"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

            for r1, c1, r2, c2 in ((r, c - 1, r, c), (r, c + 1, r, c + 1), (r - 1, c, r, c), (r + 1, c, r + 1, c)):
                prefix = "not " if (Point(r1, c1), color) in puzzle.surface.items() else ""
                d = Direction.LEFT if c1 != c else Direction.TOP
                self.add_program_line(f'{prefix}edge({r2}, {c2}, "{d}").')

        for (r, c, d, _), draw in puzzle.edge.items():
            self.add_program_line(f':-{" not" * draw} edge({r}, {c}, "{d}").')

        self.add_program_line(display(item="edge", size=3))

        return self.program
