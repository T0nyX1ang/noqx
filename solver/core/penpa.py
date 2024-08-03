"""Encoding for penpa-edit frontend."""

import copy
import json
from base64 import b64encode, b64decode
from enum import Enum
from functools import reduce
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from zlib import compress, decompress

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
    ['"self.board"', "zB"],
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
        self.parts = decompress(b64decode(content[len(PENPA_PREFIX) :]), -15).decode().split("\n")

        self.cell_shape: Optional[str] = None
        self.col: int = 0
        self.row: int = 0
        self.top_row: int = 0
        self.bottom_row: int = 0
        self.left_col: int = 0
        self.right_col: int = 0
        self._init_size()

        self.board: Dict[str, Any] = {}
        self.surface: Dict[Tuple[int, int], int] = {}
        self.number: Dict[Tuple[int, int], Union[int, List[int]]] = {}
        self.edge: Set[Tuple[int, int, Direction]] = set()
        self.cage: List[List[Tuple[int, int]]] = []
        self.arrows: List[List[Tuple[int, int]]] = []
        self.thermo: List[List[Tuple[int, int]]] = []
        self.nobulbthermo: List[List[Tuple[int, int]]] = []
        self._unpack_board()

    def _init_size(self):
        """Initialize the size of the puzzle."""
        header = self.parts[0].split(",")

        if header[0] in ("square", "sudoku", "kakuro"):
            self.cell_shape = "square"
            self.top_row, self.bottom_row, self.left_col, self.right_col = json.loads(self.parts[1])
            self.row = int(header[2]) - self.top_row - self.bottom_row
            self.col = int(header[1]) - self.left_col - self.right_col
        else:
            raise ValueError("Unsupported cell shape. Current only supported square shape.")

        margin = (self.top_row, self.bottom_row, self.left_col, self.right_col)
        print(f"[Puzzle] Size initialized. Size: {self.row}x{self.col}. Margin: {margin}.")

    def _unpack_board(self):
        """Initialize the content of the puzzle."""
        self.board = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[3]))

        self.surface = {}
        for index, color in self.board["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            self.surface[coord] = int(color)
        print("[Puzzle] Surface unpacked.")

        self.number = {}
        for index, num_data in self.board["number"].items():
            coord, _ = self.index_to_coord(int(index))
            # num_data: number, color, subtype
            if num_data[2] == "4":  # for tapa-like puzzles
                self.number[coord] = list(map(int, list(num_data[0])))
            elif num_data[2] != "7":  # neglect candidates
                self.number[coord] = int(num_data[0])
            # TODO: handle non-number texts
        print("[Puzzle] Number unpacked.")

        self.edge = set()
        for index, _ in self.board["edge"].items():
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
        print("[Puzzle] Edge unpacked.")

        self.cage = []
        for indices in self.board["killercages"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.cage.append(coord_indices)

        self.arrows = []
        for indices in self.board["arrows"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.arrows.append(coord_indices)

        self.thermo = []
        for indices in self.board["thermo"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.thermo.append(coord_indices)

        self.nobulbthermo = []
        for indices in self.board["nobulbthermo"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.nobulbthermo.append(coord_indices)
        print("[Puzzle] Sudoku unpacked.")

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the penpa index to coordinate."""
        real_row = self.row + self.top_row + self.bottom_row + 4
        real_col = self.col + self.left_col + self.right_col + 4
        category, index = divmod(index, real_row * real_col)
        return (index // real_row - 2 - self.top_row, index % real_col - 2 - self.left_col), category


class Solution:
    """Solution of a puzzle."""

    def __init__(self, puzzle: Puzzle):
        """Initialize the solution."""
        self.puzzle: Puzzle = puzzle
        self.parts = puzzle.parts
        self.board = copy.deepcopy(puzzle.board)

        self.surface: Dict[Tuple[int, int], int] = {}
        self.number: Dict[Tuple[int, int], Union[int, List[int]]] = {}
        self.edge: Set[Tuple[int, int, Direction]] = set()

    def __str__(self):
        """Return the solution as a string."""
        self._pack_board()
        self.parts[4] = reduce(lambda s, abbr: s.replace(abbr[0], abbr[1]), PENPA_ABBREVIATIONS, json.dumps(self.board))
        return PENPA_PREFIX + b64encode(compress("\n".join(self.parts).encode())[2:-4]).decode()

    def _pack_board(self):
        """Pack the solution into penpa format."""
        for coord, color in self.surface.items():
            index = self.coord_to_index(coord)
            self.board["surface"][f"{index}"] = color
        print("[Solution] Surface packed.")

    def coord_to_index(self, coord: Tuple[int, int], category: int = 0) -> int:
        """Convert the coordinate to penpa index."""
        puzzle = self.puzzle
        real_row = puzzle.row + puzzle.top_row + puzzle.bottom_row + 4
        real_col = puzzle.col + puzzle.left_col + puzzle.right_col + 4
        return (category * real_row * real_col) + (coord[0] + 2 + puzzle.top_row) * real_col + coord[1] + 2 + puzzle.left_col
