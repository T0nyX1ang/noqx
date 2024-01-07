"""The Slitherlink solver."""

from typing import List

from . import utils
from .utils.claspy import set_max_val
from .utils.borders import RectangularGridBorderSolver
from .utils.encoding import Encoding


def encode(string: str) -> Encoding:
    return utils.encode(string, clue_encoder=lambda s: s)


def solve(E: Encoding) -> List:
    number_clues, inside_clues, outside_clues = {}, set(), set()
    for clue, value in E.clues.items():
        if value.isnumeric():
            number_clues[clue] = int(value)
        elif value == "s":
            inside_clues.add(clue)
        elif value == "w":
            outside_clues.add(clue)
        else:
            raise ValueError("Clues must be numbers, s, or w.")

    set_max_val(max(number_clues.values()) if number_clues else 0)

    bs = RectangularGridBorderSolver(E.R, E.C)
    bs.loop()
    bs.clues(number_clues)
    bs.inside_loop(inside_clues)
    bs.outside_loop(outside_clues)
    return bs.solutions()


def decode(solutions: List[Encoding]) -> str:
    return utils.decode(solutions)
