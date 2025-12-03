"""Encoding for [Penpa+](https://swaroopg92.github.io/penpa-edit/) frontend."""

import json
from base64 import b64decode, b64encode
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple, Union
from zlib import compress, decompress

from noqx.puzzle import Color, Direction, Point, Puzzle

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
    ('"d"', "zD"),
    ('"squareframe"', "z0"),
    ('"polygon"', "z5"),
    ('"deleteedge"', "z4"),
    ('"killercages"', "z6"),
    ('"nobulbthermo"', "z7"),
    ('"__a"', "z_"),
    ("null", "zO"),
]


def _int_or_str(data: Union[int, str]) -> Union[int, str]:
    """Convert the string to integer if possible.

    * Since [Penpa+](https://swaroopg92.github.io/penpa-edit/) is a JavaScript-based application,
    the clues are not strictly typed when exported. This function helps to convert the string data
    to integer if it is actually an integer.

    * This function uses `str.isdigit()` to check if the string can be converted to an integer.

    Args:
        data: The data to be converted.

    Returns:
        The converted integer or the original string.
    """
    return int(data) if isinstance(data, int) or data.isdigit() else data


def _style_convert(style: List[int]) -> int:
    """Convert a boolean list of style to integer format.

    * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), there are basically two types of symbol styles:
    the **integer** style (for single symbols), and the **boolean list** style (for cascaded multiple symbols).
    To unify these styles, this function **binarized** the boolean list to a single integer.

    Args:
        style: The style list to be converted.

    Returns:
        The converted integer style.
    """
    return int("".join(map(str, style)), 2)


def _category_to_direction(r: int, c: int, category: int) -> Tuple[int, int, str]:
    """Convert the coordination with category to standard direction.

    * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the relative directions of a cell is hard-coded
    as a `category` code with a different placement in `noqx`. This function helps to convert the category code
    to the standard direction format in `noqx`.

    Args:
        r: The row index of the cell.
        c: The column index of the cell.
        category: The category code of the direction (allowed values: 0, 1, 2, 3).

    Returns:
        A tuple representing the converted coordination with stardard direction.

    Raises:
        ValueError: If the category code is invalid.
    """
    if category == 0:
        return (r, c, Direction.CENTER)

    if category == 1:
        return (r + 1, c + 1, Direction.TOP_LEFT)

    if category == 2:
        return (r + 1, c, Direction.TOP)

    if category == 3:
        return (r, c + 1, Direction.LEFT)

    raise ValueError("Invalid category type.")


class PenpaPuzzle(Puzzle):
    """The encoding for general puzzles.

    * The general process is decoding the raw format, unpacking the board, running the solver, packing the board,
    and encoding back to the raw format.
    """

    def __init__(self, name: str, content: str, param: Optional[Dict[str, Any]] = None):
        """Initialize the encoding of the puzzle.

        * To facilitate the interoperability with [Penpa+](https://swaroopg92.github.io/penpa-edit/), four extra
        variables are included in this class:

            * `cell_shape`: The shape of the cell, currently only `square` shape is supported.
            * `parts`: The decompressed parts of the [Penpa+](https://swaroopg92.github.io/penpa-edit/) content
                       with a more readable format.
            * `problem`: The problem board extracted from `parts`.
            * `solution`: The solution board to be written into `parts`.

        Args:
            name: The name of the puzzle.
            content: The raw content of the puzzle in [Penpa+](https://swaroopg92.github.io/penpa-edit/) format.
            param: Optional parameters for the puzzle.
        """
        super().__init__(name, content, param)

        self.cell_shape: Optional[str] = None
        self.parts: List[str] = []
        self.problem: Dict[str, Any] = {}
        self.solution: Dict[str, Any] = {}

    def decode(self):
        """Decode the Penpa+ content into the puzzle elements.

        * The process involves decompressing the base64-encoded content, parsing the JSON data,
        initializing the puzzle size, and unpacking the board elements into the respective attributes.
        """
        self.parts = decompress(b64decode(self.content[len(PENPA_PREFIX) :]), -15).decode().split("\n")
        self._init_size()
        self._unpack_board()

    def _init_size(self):
        """Initialize the size of the puzzle."""
        header = self.parts[0].split(",")

        if header[0] in ("square", "sudoku", "kakuro"):
            self.cell_shape = "square"
            self.margin = json.loads(self.parts[1])
            top_margin, bottom_margin, left_margin, right_margin = self.margin

            self.row = int(header[2]) - top_margin - bottom_margin
            self.col = int(header[1]) - left_margin - right_margin
        else:
            raise NotImplementedError("Unsupported cell shape. Current only square shape is supported.")

    def _unpack_surface(self):
        """Unpack the surface element from the board."""
        for index, color_code in self.problem["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            point = Point(*coord)

            if color_code in [1, 3, 8]:
                self.surface[point] = Color.GRAY

            if color_code == 4:
                self.surface[point] = Color.BLACK

            if color_code == 2:
                self.surface[point] = Color.GREEN

    def _unpack_text(self):
        """Unpack the number/text element from the board."""
        for index, num_data in self.problem["number"].items():
            (r, c), category = self.index_to_coord(int(index))
            coord = _category_to_direction(r, c, category)
            # num_data: number, color, subtype

            if num_data[2] == "4":  # for tapa-like puzzles, convert to List[int]
                for i, data in enumerate(map(_int_or_str, list(num_data[0]))):
                    self.text[Point(*coord, f"tapa_{i}")] = data
            elif num_data[2] != "7":  # neglect candidates, convert to Union[int, str]
                self.text[Point(*coord, "normal")] = _int_or_str(num_data[0])

    def _unpack_sudoku(self):
        """Unpack the sudoku element from the board."""
        for index, num_data in self.problem["sudoku"].items():
            (r, c), category = self.index_to_coord(int(index) // 4)
            coord = _category_to_direction(r, c, 0)
            num_direction = (category - 1) * 4 + int(index) % 4
            self.text[Point(*coord, f"sudoku_{num_direction}")] = _int_or_str(num_data[0])

    def _unpack_symbol(self):
        """Unpack the text element from the board."""
        for index, (style, shape, _) in self.problem["symbol"].items():
            (r, c), category = self.index_to_coord(int(index))
            if isinstance(style, list):
                symbol_name = f"{shape}__{_style_convert(style)}"
                self.symbol[Point(*_category_to_direction(r, c, category), "multiple")] = symbol_name
            else:
                symbol_name = f"{shape}__{style}"
                # special case for nondango (which problem/solution symbols are on the same coordinates)
                label = "nondango_mark" if self.puzzle_name == "nondango" and symbol_name == "circle_M__4" else "normal"
                self.symbol[Point(*_category_to_direction(r, c, category), label)] = symbol_name

    def _unpack_edge(self):
        """Unpack the edge/helper_x element from the board."""
        for index, _ in self.problem["edge"].items():
            if "," not in index:  # helper(x) edges
                coord, category = self.index_to_coord(int(index))
                if category == 2:
                    self.edge[Point(coord[0] + 1, coord[1], Direction.TOP)] = False

                if category == 3:
                    self.edge[Point(coord[0], coord[1] + 1, Direction.LEFT)] = False

                continue

            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, _ = self.index_to_coord(index_2)
            if coord_1[0] == coord_2[0]:  # row equal, horizontal line
                self.edge[Point(coord_2[0] + 1, coord_2[1], Direction.TOP)] = True
            elif coord_1[1] == coord_2[1]:  # col equal, vertical line
                self.edge[Point(coord_2[0], coord_2[1] + 1, Direction.LEFT)] = True
            elif coord_1[0] - coord_2[0] == 1 and coord_2[1] - coord_1[1] == 1:  # upwards diagonal line
                self.edge[Point(coord_2[0], coord_2[1], Direction.DIAG_UP)] = True
            elif coord_2[0] - coord_1[0] == 1 and coord_1[1] - coord_2[1] == 1:  # downwards diagonal line
                self.edge[Point(coord_2[0], coord_2[1], Direction.DIAG_DOWN)] = True

        for index, _ in self.problem["deleteedge"].items():  # edge deletion mark, stronger than helper_x
            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, _ = self.index_to_coord(index_2)
            if coord_1[0] == coord_2[0]:  # row equal, horizontal line, set label to `delete` as indicator
                self.edge[Point(coord_2[0] + 1, coord_2[1], Direction.TOP, "delete")] = False
            elif coord_1[1] == coord_2[1]:  # col equal, vertical line, set label to `delete` as indicator
                self.edge[Point(coord_2[0], coord_2[1] + 1, Direction.LEFT, "delete")] = False

    def _unpack_line(self):
        """Unpack the line element from the board."""
        for index, data in self.problem["line"].items():
            if "," not in index:  # helper(x) lines
                coord, category = self.index_to_coord(int(index))
                if category == 2:
                    self.line[Point(coord[0], coord[1], label="d")] = False
                    self.line[Point(coord[0] + 1, coord[1], label="u")] = False

                if category == 3:
                    self.line[Point(coord[0], coord[1], label="r")] = False
                    self.line[Point(coord[0], coord[1] + 1, label="l")] = False

                continue

            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, category = self.index_to_coord(index_2)

            hashi_num = (self.puzzle_name == "hashi") * ("_2" if data == 30 else "_1")  # hashi has two types of lines
            if category == 0:
                dd = "rl" if coord_1[0] == coord_2[0] else "du"
                self.line[Point(*coord_1, label=f"{dd[0]}{hashi_num}")] = True
                self.line[Point(*coord_2, label=f"{dd[1]}{hashi_num}")] = True
            else:
                eqxy = coord_1 == coord_2
                d = ("d" if eqxy else "u") if category == 2 else ("r" if eqxy else "l")
                self.line[Point(*coord_1, label=f"{d}{hashi_num}")] = True

    def _unpack_board(self):
        """Initialize the content of the puzzle."""
        for p in (4, 3):  # must unpack solution board first, then edit board to keep consistency
            self.problem = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[p]))
            self._unpack_surface()
            self._unpack_text()
            self._unpack_sudoku()
            self._unpack_symbol()
            self._unpack_edge()
            self._unpack_line()

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the penpa index to coordinate.

        * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the coordination (with margins) and category of a cell is encoded
        as a single integer index. This function helps to convert the index back to the ((`row`, `column`), `category`) format.

        Args:
            index: The penpa index to be converted.

        Returns:
            A cascaded tuple representing the converted coordination (in tuple) and category.
        """
        top_margin, bottom_margin, left_margin, right_margin = self.margin
        real_row = self.row + top_margin + bottom_margin + 4
        real_col = self.col + left_margin + right_margin + 4
        category, index = divmod(index, real_row * real_col)
        return (index // real_col - 2 - top_margin, index % real_col - 2 - left_margin), category

    def encode(self) -> str:
        """Encode the puzzle into Penpa+ format.

        * The process involves packing the puzzle elements into the solution dictionary,
        updating the relevant part of the Penpa+ content, and compressing it into a base64-encoded string.

        Returns:
            The encoded Penpa+ content.
        """
        self.solution = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[4]))
        self._pack_board()
        self.parts[4] = reduce(lambda s, abbr: s.replace(abbr[0], abbr[1]), PENPA_ABBREVIATIONS, json.dumps(self.solution))
        return PENPA_PREFIX + b64encode(compress("\n".join(self.parts).encode())[2:-4]).decode()

    def _pack_surface(self):
        """Pack the surface element into the board."""
        for (r, c, _, _), color in self.surface.items():
            coord = (r, c)
            index = self.coord_to_index(coord)

            color_code = None
            if color == Color.BLACK:
                color_code = 4

            if color == Color.GRAY:
                color_code = 8

            if color_code and not self.problem["surface"].get(f"{index}"):  # avoid overwriting the original stuff
                self.solution["surface"][f"{index}"] = color_code

    def _pack_text(self):
        """Pack the text/number element into the board."""
        for (r, c, _, _), data in self.text.items():
            coord = (r, c)
            index = self.coord_to_index(coord, category=0)  # currently the packing of texts are all in the center
            if not self.problem["number"].get(f"{index}"):  # avoid overwriting the original stuff
                self.solution["number"][f"{index}"] = [str(data), 2, "1"]

    def _pack_symbol(self):
        """Pack the symbol element into the board."""
        for (r, c, _, _), symbol_name in self.symbol.items():
            shape, style = symbol_name.split("__")
            coord = (r, c)
            index = self.coord_to_index(coord, category=0)  # currently the packing of symbols are all in the center
            if self.puzzle_name == "nondango":
                self.solution["symbol"][f"{index}"] = [int(style), shape, 1]
            elif not self.problem["symbol"].get(f"{index}"):  # avoid overwriting the original stuff
                self.solution["symbol"][f"{index}"] = [int(style), shape, 1]

    def _pack_edge(self):
        """Pack the edge element into the board."""
        for r, c, d, _ in self.edge:
            coord_1 = (r - 1, c - 1)
            coord_2 = (r - 1, c - 1)
            if d == Direction.TOP:
                coord_2 = (r - 1, c)
            if d == Direction.LEFT:
                coord_2 = (r, c - 1)
            if d == Direction.DIAG_UP:
                coord_1 = (r, c - 1)
                coord_2 = (r - 1, c)
            if d == Direction.DIAG_DOWN:
                coord_2 = (r, c)

            index_1 = self.coord_to_index(coord_1, category=1)
            index_2 = self.coord_to_index(coord_2, category=1)
            if not self.problem["edge"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.solution["edge"][f"{index_1},{index_2}"] = 3

    def _pack_line(self):
        """Pack the line element into the board."""
        for r, c, _, label in self.line:
            index_1 = self.coord_to_index((r, c), category=0)
            if label.startswith("r"):
                index_2 = self.coord_to_index((r, c), category=3)
            elif label.startswith("d"):
                index_2 = self.coord_to_index((r, c), category=2)
            elif label.startswith("l"):
                index_2 = self.coord_to_index((r, c - 1), category=3)
            elif label.startswith("u"):
                index_2 = self.coord_to_index((r - 1, c), category=2)
            else:
                raise ValueError("Unsupported line direction.")

            if self.puzzle_name == "hashi":
                self.solution["line"][f"{index_1},{index_2}"] = 3 if label.endswith("_1") else 30
            elif not self.problem["line"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.solution["line"][f"{index_1},{index_2}"] = 3

    def _pack_board(self):
        """Pack the solution into penpa format."""
        self._pack_surface()
        self._pack_text()
        self._pack_symbol()
        self._pack_edge()
        self._pack_line()

    def coord_to_index(self, coord: Tuple[int, int], category: int = 0) -> int:
        """Convert the coordinate to penpa index.

        * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the coordination (with margins) and category of a cell is encoded
        as a single integer index. This function helps to convert the ((`row`, `column`), `category`) format back to the index.

        Args:
            coord: The coordination to be converted.
            category: The category code of the direction (default is 0).

        Returns:
            The converted penpa index.
        """
        top_margin, bottom_margin, left_margin, right_margin = self.margin
        real_row = self.row + top_margin + bottom_margin + 4
        real_col = self.col + left_margin + right_margin + 4
        return (category * real_row * real_col) + (coord[0] + 2 + top_margin) * real_col + coord[1] + 2 + left_margin
