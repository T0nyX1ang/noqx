"""Encoding for penpa-edit frontend."""

import json
from base64 import b64decode, b64encode
from functools import reduce
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from zlib import compress, decompress

from .logging import logger
from .rule.helper import Direction

PENPA_PREFIX = "m=edit&p="
PENPA_ABBREVIATIONS = [
    ('"qa"', "z9"),
    ('"pu_q"', "zQ"),
    ('"pu_a"', "zA"),
    ('"grid"', "zG"),
    ('"edit_mode"', "zM"),
    ('"surface"', "zS"),
    ('"line"', "zL"),
    ('"edge"', "zE"),
    ('"wall"', "zW"),
    ('"cage"', "zC"),
    ('"number"', "zN"),
    ('"sudoku"', "z1"),
    ('"symbol"', "zY"),
    ('"special"', "zP"),
    ('"board"', "zB"),
    ('"command_redo"', "zR"),
    ('"command_undo"', "zU"),
    ('"command_replay"', "z8"),
    ('"freeline"', "zF"),
    ('"freeedge"', "z2"),
    ('"thermo"', "zT"),
    ('"arrows"', "z3"),
    ('"direction"', "zD"),
    ('"squareframe"', "z0"),
    ('"polygon"', "z5"),
    ('"deleteedge"', "z4"),
    ('"killercages"', "z6"),
    ('"nobulbthermo"', "z7"),
    ('"__a"', "z_"),
    ("null", "zO"),
]


def int_or_str(data: Union[int, str]) -> Union[int, str]:
    """Convert the string to integer if possible."""
    return int(data) if isinstance(data, int) or data.isdigit() else data


class Puzzle:
    """The encoding for general puzzles."""

    def __init__(self, _type: str, content: str, param: Optional[Dict[str, Any]] = None):
        """Initialize the encoding of the puzzle."""
        self.puzzle_type = _type
        self.param = param if param is not None else {}
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
        self.text: Dict[Tuple[int, int], Union[int, str, List[Union[int, str]]]] = {}
        self.sudoku: Dict[Tuple[int, int], Dict[int, Union[int, str]]] = {}
        self.symbol: Dict[Tuple[int, int], str] = {}
        self.edge: Set[Tuple[int, int, Direction]] = set()
        self.helper_x: Set[Tuple[int, int, Direction]] = set()
        self.line: Set[Tuple[int, int, str]] = set()
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
            raise NotImplementedError("Unsupported cell shape. Current only supported square shape.")

        margin = (self.top_row, self.bottom_row, self.left_col, self.right_col)
        logger.debug(f"[Puzzle] Board initialized. Size: {self.row}x{self.col}. Margin: {margin}.")

    def _unpack_surface(self):
        """Unpack the surface element from the board."""
        for index, color in self.board["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            self.surface[coord] = int(color)

    def _unpack_text(self):
        """Unpack the number/text element from the board."""
        for index, num_data in self.board["number"].items():
            coord, _ = self.index_to_coord(int(index))
            # num_data: number, color, subtype
            if num_data[2] == "4":  # for tapa-like puzzles, convert to List[int]
                self.text[coord] = list(map(int_or_str, list(num_data[0])))
            elif num_data[2] != "7":  # neglect candidates, convert to Union[int, str]
                self.text[coord] = int_or_str(num_data[0])

    def _unpack_sudoku(self):
        """Unpack the sudoku element from the board."""
        for index, num_data in self.board["sudoku"].items():
            coord, category = self.index_to_coord(int(index) // 4)
            num_direction = (category - 1) * 4 + int(index) % 4
            if self.sudoku.get(coord) is None:
                self.sudoku[coord] = {}
                self.sudoku[coord][num_direction] = int_or_str(num_data[0])
            else:
                self.sudoku[coord][num_direction] = int_or_str(num_data[0])

        for indices in self.board["killercages"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.cage.append(coord_indices)

        for indices in self.board["arrows"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.arrows.append(coord_indices)

        for indices in self.board["thermo"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.thermo.append(coord_indices)

        for indices in self.board["nobulbthermo"]:
            coord_indices = list(map(lambda x: self.index_to_coord(x)[0], indices))
            self.nobulbthermo.append(coord_indices)

    def _unpack_symbol(self):
        """Unpack the text element from the board."""
        for index, (style, shape, _) in self.board["symbol"].items():
            coord, category = self.index_to_coord(int(index))
            symbol_name = f"{shape}__{style}__{category}"
            self.symbol[coord] = symbol_name

    def _unpack_edge(self):
        """Unpack the edge/helper_x element from the board."""
        for index, _ in self.board["edge"].items():
            if "," not in index:  # helper(x) edges
                coord, category = self.index_to_coord(int(index))
                if category == 2:
                    self.helper_x.add((coord[0] + 1, coord[1], Direction.TOP))
                elif category == 3:
                    self.helper_x.add((coord[0], coord[1] + 1, Direction.LEFT))
                continue

            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, _ = self.index_to_coord(index_2)
            if coord_1[0] == coord_2[0]:  # row equal, horizontal line
                self.edge.add((coord_2[0] + 1, coord_2[1], Direction.TOP))
            elif coord_1[1] == coord_2[1]:  # col equal, vertical line
                self.edge.add((coord_2[0], coord_2[1] + 1, Direction.LEFT))
            elif coord_1[0] - coord_2[0] == 1 and coord_2[1] - coord_1[1] == 1:  # upwards diagonal line
                self.edge.add((coord_2[0], coord_2[1], Direction.DIAG_UP))
            elif coord_2[0] - coord_1[0] == 1 and coord_1[1] - coord_2[1] == 1:  # downwards diagonal line
                self.edge.add((coord_2[0], coord_2[1] + 1, Direction.DIAG_DOWN))

    def _unpack_line(self):
        """Unpack the line element from the board."""
        for index, _ in self.board["line"].items():
            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, d = self.index_to_coord(index_2)
            eqxy = coord_1 == coord_2
            d = ("d" if eqxy else "u") if d == 2 else ("r" if eqxy else "l")
            self.line.add((*coord_1, d))

    def _unpack_board(self):
        """Initialize the content of the puzzle."""
        for p in (4, 3):  # must unpack solution board first, then edit board to keep consistency
            self.board = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[p]))
            self._unpack_surface()
            self._unpack_text()
            self._unpack_sudoku()
            self._unpack_symbol()
            self._unpack_edge()
            self._unpack_line()
        logger.debug("[Puzzle] Board unpacked.")

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the penpa index to coordinate."""
        real_row = self.row + self.top_row + self.bottom_row + 4
        real_col = self.col + self.left_col + self.right_col + 4
        category, index = divmod(index, real_row * real_col)
        return (index // real_col - 2 - self.top_row, index % real_col - 2 - self.left_col), category


class Solution:
    """Solution of a puzzle."""

    def __init__(self, puzzle: Puzzle):
        """Initialize the solution."""
        self.puzzle: Puzzle = puzzle
        self.parts = puzzle.parts
        self.board = {
            "surface": {},
            "number": {},
            "sudoku": {},
            "symbol": {},
            "squareframe": [],
            "line": {},
            "edge": {},
        }

        self.surface: Dict[Tuple[int, int], int] = {}
        self.text: Dict[Tuple[int, int], Union[int, str]] = {}
        self.symbol: Dict[Tuple[int, int], str] = {}
        self.edge: Set[Tuple[int, int, Direction]] = set()
        self.line: Set[Tuple[int, int, str]] = set()

    def __str__(self):
        """Return the solution as a string."""
        self._pack_board()
        self.parts[4] = reduce(lambda s, abbr: s.replace(abbr[0], abbr[1]), PENPA_ABBREVIATIONS, json.dumps(self.board))
        return PENPA_PREFIX + b64encode(compress("\n".join(self.parts).encode())[2:-4]).decode()

    def _pack_surface(self):
        """Pack the surface element into the board."""
        for coord, color in self.surface.items():
            index = self.coord_to_index(coord)
            if not self.puzzle.board["surface"].get(f"{index}"):  # avoid overwriting the original stuff
                self.board["surface"][f"{index}"] = color

    def _pack_text(self):
        """Pack the text/number element into the board."""
        for coord, text in self.text.items():
            index = self.coord_to_index(coord)
            if not self.puzzle.board["number"].get(f"{index}"):  # avoid overwriting the original stuff
                self.board["number"][f"{index}"] = [str(text), 2, "1"]

    def _pack_symbol(self):
        """Pack the symbol element into the board."""
        for coord, symbol_name in self.symbol.items():
            shape, style, category = symbol_name.split("__")
            index = self.coord_to_index(coord, category=int(category))
            if not self.puzzle.board["symbol"].get(f"{index}"):  # avoid overwriting the original stuff
                self.board["symbol"][f"{index}"] = [int(style), shape, 1]

    def _pack_edge(self):
        """Pack the edge element into the board."""
        for r, c, direction in self.edge:
            coord_1 = (r - 1, c - 1)
            coord_2 = (r - 1, c - 1)
            if direction == Direction.TOP:
                coord_2 = (r - 1, c)
            if direction == Direction.LEFT:
                coord_2 = (r, c - 1)
            if direction == Direction.DIAG_UP:
                coord_1 = (r, c - 1)
                coord_2 = (r - 1, c)
            if direction == Direction.DIAG_DOWN:
                coord_2 = (r, c)

            index_1 = self.coord_to_index(coord_1, category=1)
            index_2 = self.coord_to_index(coord_2, category=1)
            if not self.puzzle.board["edge"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.board["edge"][f"{index_1},{index_2}"] = 3

    def _pack_line(self):
        """Pack the line element into the board."""
        for r, c, direction in self.line:
            index_1 = self.coord_to_index((r, c), category=0)
            if direction.startswith("r"):
                index_2 = self.coord_to_index((r, c), category=3)
            elif direction.startswith("d"):
                index_2 = self.coord_to_index((r, c), category=2)
            elif direction.startswith("l"):
                index_2 = self.coord_to_index((r, c - 1), category=3)
            elif direction.startswith("u"):
                index_2 = self.coord_to_index((r - 1, c), category=2)
            else:
                raise AssertionError("Unsupported line direction.")

            if self.puzzle.puzzle_type == "hashi":
                self.board["line"][f"{index_1},{index_2}"] = 3 if direction.endswith("_1") else 30
            elif not self.puzzle.board["line"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.board["line"][f"{index_1},{index_2}"] = 3

    def _pack_board(self):
        """Pack the solution into penpa format."""
        self._pack_surface()
        self._pack_text()
        self._pack_symbol()
        self._pack_edge()
        self._pack_line()
        logger.debug("[Solution] Board packed.")

    def coord_to_index(self, coord: Tuple[int, int], category: int = 0) -> int:
        """Convert the coordinate to penpa index."""
        puzzle = self.puzzle
        real_row = puzzle.row + puzzle.top_row + puzzle.bottom_row + 4
        real_col = puzzle.col + puzzle.left_col + puzzle.right_col + 4
        return (category * real_row * real_col) + (coord[0] + 2 + puzzle.top_row) * real_col + coord[1] + 2 + puzzle.left_col
