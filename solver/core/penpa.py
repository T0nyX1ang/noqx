"""Encoding for penpa-edit frontend."""

import json

from base64 import b64decode
from functools import reduce
from typing import Optional, Tuple
from zlib import decompress


PENPA_PREFIX = "m=edit&p="
PENPA_ABBREVIATIONS = [
    ['"qa"', "z9"],
    ['"pu_q"', "zQ"],
    ['"pu_a"', "zA"],
    ['"grid"', "zG"],
    ['"edit_mode"', "zM"],
    ['"surface"', "zS"],
    ['"line"', "zL"],
    ['"edge"', "zE"],
    ['"wall"', "zW"],
    ['"cage"', "zC"],
    ['"number"', "zN"],
    ['"symbol"', "zY"],
    ['"special"', "zP"],
    ['"board"', "zB"],
    ['"command_redo"', "zR"],
    ['"command_undo"', "zU"],
    ['"command_replay"', "z8"],
    ['"sudoku"', "z1"],
    ['"freeline"', "zF"],
    ['"freeedge"', "z2"],
    ['"thermo"', "zT"],
    ['"arrows"', "z3"],
    ['"direction"', "zD"],
    ['"squareframe"', "z0"],
    ['"polygon"', "z5"],
    ['"deleteedge"', "z4"],
    ['"killercages"', "z6"],
    ['"nobulbthermo"', "z7"],
    ['"__a"', "z_"],
    ["null", "zO"],
]


class Puzzle:
    """The encoding for general puzzles."""

    def __init__(self, content: str):
        """Initialize the encoding of the puzzle."""
        self.content = content
        self.__parts = decompress(b64decode(self.content[len(PENPA_PREFIX) :]), -15).decode().split("\n")

        self.cell_shape: Optional[str] = None
        self.width: int = 0
        self.height: int = 0
        self.top_space: int = 0
        self.bottom_space: int = 0
        self.left_space: int = 0
        self.right_space: int = 0
        self._init_size()

        self._init_board()

    def __str__(self) -> str:
        """Return the encoded puzzle."""
        return self.content  # TODO encode the puzzle dynamically

    def _init_size(self):
        """Initialize the size of the puzzle."""
        header = self.__parts[0].split(",")

        if header[0] in ("square", "sudoku", "kakuro"):
            self.cell_shape = "square"
            self.top_space, self.bottom_space, self.left_space, self.right_space = json.loads(self.__parts[1])
            self.width = int(header[1]) - self.left_space - self.right_space
            self.height = int(header[2]) - self.top_space - self.bottom_space
        else:
            raise ValueError("Unsupported cell shape. Current only supported square shape.")

        margin = (self.top_space, self.bottom_space, self.left_space, self.right_space)
        print(f"Puzzle size initialized. Size: {self.width}x{self.height}. Margin: {margin}.")

    def _init_board(self):
        """Initialize the content of the puzzle."""
        board = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.__parts[3]))

        self.surface = {}
        for index, _ in board["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            self.surface[coord] = "gray"  # fix color to gray

        self.number = {}
        for index, num_data in board["number"].items():
            coord, _ = self.index_to_coord(int(index))
            # num_data: number, color, subtype
            if num_data[2] == "4":  # for tapa-like puzzles
                self.number[coord] = list(map(int, list(num_data[0])))
            elif num_data[2] != "7":  # neglect candidates
                self.number[coord] = int(num_data[0])

            # TODO: handle non-number texts

        print(board)

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the penpa index to coordinate."""
        real_width = self.width + self.left_space + self.right_space + 4
        real_height = self.height + self.top_space + self.bottom_space + 4
        category = index // (real_width * real_height)
        index = index % (real_width * real_height)
        return (index // real_height - 2, index % real_width - 2), category

    def coord_to_index(self):
        """Convert the coordinate to penpa index."""
        return


def encode(data: str):
    """Encode the given data."""
    puzzle = Puzzle(data)
    return puzzle
