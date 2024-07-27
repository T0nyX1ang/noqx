"""Encoding for penpa-edit frontend."""

import json

from base64 import b64decode
from typing import Optional
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
    ['"lineE"', "zE"],
    ['"wall"', "zW"],
    ['"cage"', "zC"],
    ['"number"', "zN"],
    ['"symbol"', "zY"],
    ['"special"', "zP"],
    ['"board"', "zB"],
    ['"command_redo"', "zR"],
    ['"command_undo"', "zU"],
    ['"command_replay"', "z8"],
    ['"numberS"', "z1"],
    ['"freeline"', "zF"],
    ['"freelineE"', "z2"],
    ['"thermo"', "zT"],
    ['"arrows"', "z3"],
    ['"direction"', "zD"],
    ['"squareframe"', "z0"],
    ['"polygon"', "z5"],
    ['"deletelineE"', "z4"],
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

        self.cell_shape: Optional[str] = None
        self.width: int = 0
        self.height: int = 0
        self.top_space: int = 0
        self.bottom_space: int = 0
        self.left_space: int = 0
        self.right_space: int = 0
        self._init_size()

    def __str__(self) -> str:
        """Return the encoded puzzle."""
        return self.content  # TODO encode the puzzle dynamically

    def _init_size(self):
        """Initialize the size of the puzzle"""
        parts = decompress(b64decode(self.content[len(PENPA_PREFIX) :]), -15).decode().split("\n")
        header = parts[0].split(",")

        if header[0] in ("square", "sudoku", "kakuro"):
            self.cell_shape = "square"
            self.top_space, self.bottom_space, self.left_space, self.right_space = json.loads(parts[1])
            self.width = int(header[1]) - self.left_space - self.right_space
            self.height = int(header[2]) - self.top_space - self.bottom_space
        else:
            raise ValueError("Unsupported cell shape. Current only supported square shape.")

        margin = (self.top_space, self.bottom_space, self.left_space, self.right_space)
        print(f"Puzzle size initialized. Size: {self.width}x{self.height}. Margin: {margin}.")

    def index_to_coord(self):
        """Convert the penpa index to coordinate."""
        return

    def coord_to_index(self):
        """Convert the coordinate to penpa index."""
        return


def encode(data: str):
    """Encode the given data."""
    puzzle = Puzzle(data)
    print(puzzle)
