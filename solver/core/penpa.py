"""Encoding for penpa-edit frontend."""

import json

from base64 import b64decode
from enum import Enum
from functools import reduce
from typing import Optional, Tuple
from zlib import decompress


Direction = Enum("Direction", "LEFT TOP")
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
        self.cols: int = 0
        self.rows: int = 0
        self.top_rows: int = 0
        self.bottom_rows: int = 0
        self.left_cols: int = 0
        self.right_cols: int = 0
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
            self.top_rows, self.bottom_rows, self.left_cols, self.right_cols = json.loads(self.__parts[1])
            self.rows = int(header[2]) - self.top_rows - self.bottom_rows
            self.cols = int(header[1]) - self.left_cols - self.right_cols
        else:
            raise ValueError("Unsupported cell shape. Current only supported square shape.")

        margin = (self.top_rows, self.bottom_rows, self.left_cols, self.right_cols)
        print(f"Puzzle size initialized. Size: {self.rows}x{self.cols}. Margin: {margin}.")

    def _init_board(self):
        """Initialize the content of the puzzle."""
        board = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.__parts[3]))

        self.surface = {}
        for index, _ in board["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            self.surface[coord] = "gray"  # fix color to gray
        print(self.surface)

        self.number = {}
        for index, num_data in board["number"].items():
            coord, _ = self.index_to_coord(int(index))
            # num_data: number, color, subtype
            if num_data[2] == "4":  # for tapa-like puzzles
                self.number[coord] = list(map(int, list(num_data[0])))
            elif num_data[2] != "7":  # neglect candidates
                self.number[coord] = int(num_data[0])
            # TODO: handle non-number texts
        print(self.number)

        self.edge = set()
        for r in range(self.rows):  # initialize border edges
            self.edge.add((r, 0, Direction.LEFT))
            self.edge.add((r, self.cols, Direction.LEFT))
        for c in range(self.cols):  # initialize border edges
            self.edge.add((0, c, Direction.TOP))
            self.edge.add((self.rows, c, Direction.TOP))
        for index, _ in board["edge"].items():
            if "," not in index:  # helper(x) edges
                # TODO handle helper(x) edges
                continue

            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, _ = self.index_to_coord(index_2)
            if coord_1[0] == coord_2[0]:  # row equal, horizontal line
                self.edge.add((coord_2[0] + 1, coord_2[1], Direction.TOP))
            elif coord_1[1] == coord_2[1]:  # col equal, vertical line
                self.edge.add((coord_2[0], coord_2[1] + 1, Direction.LEFT))
        print(self.edge)

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the penpa index to coordinate."""
        real_rows = self.rows + self.top_rows + self.bottom_rows + 4
        real_cols = self.cols + self.left_cols + self.right_cols + 4
        category, index = divmod(index, real_rows * real_cols)
        return (index // real_rows - 2, index % real_cols - 2), category

    def coord_to_index(self):
        """Convert the coordinate to penpa index."""
        return


def encode(data: str):
    """Encode the given data."""
    puzzle = Puzzle(data)
    return puzzle
