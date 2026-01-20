"""Encodings for [Penpa+](https://swaroopg92.github.io/penpa-edit/) frontend."""

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

    * Since [Penpa+](https://swaroopg92.github.io/penpa-edit/) is a JavaScript-based application, the clues are not strictly typed when exported. This function helps to convert the string data to integer if it is actually an integer.

    * This function uses `str.isdigit()` to check if the string can be converted to an integer.

    Args:
        data: The data to be converted.
    """
    if isinstance(data, int):
        return data

    data = data.strip()  # strip whitespace
    return int(data) if data.isdigit() else data


def _style_convert(style: List[int]) -> int:
    """Convert a boolean list of style to integer format.

    * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), there are basically two types of symbol styles: the **integer** style (for single symbols), and the **boolean list** style (for cascaded multiple symbols). To unify these styles, this function **binarized** the boolean list to a single integer.

    Args:
        style: The style list to be converted.
    """
    return int("".join(map(str, style)), 2)


def _category_to_direction(r: int, c: int, category: int) -> Tuple[int, int, str]:
    """Convert the coordination with category to standard direction.

    * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the relative directions of a cell is hard-coded as a `category` code with a different placement in `noqx`. This function helps to convert the category code to the standard direction format in `noqx`.

    Args:
        r: The row index of the cell.
        c: The column index of the cell.
        category: The category code of the direction (allowed values: 0, 1, 2, 3).

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
    """The encodings for [Penpa+](https://swaroopg92.github.io/penpa-edit/) puzzles.

    * The general process is decoding the raw [Penpa+](https://swaroopg92.github.io/penpa-edit/) format, unpacking the board, running the solver, packing the board, and encoding back to the raw [Penpa+](https://swaroopg92.github.io/penpa-edit/) format.
    """

    def __init__(self, name: str, content: str, param: Optional[Dict[str, Any]] = None):
        """Initialize the [Penpa+](https://swaroopg92.github.io/penpa-edit/) puzzle.

        * To facilitate the interoperability with [Penpa+](https://swaroopg92.github.io/penpa-edit/), four extra variables are included in this class:

            * `cell_shape`: The shape of the cell, currently only `square` shape is supported.
            * `parts`: The decompressed parts of the [Penpa+](https://swaroopg92.github.io/penpa-edit/) content with a more readable format.
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
        """Decode the [Penpa+](https://swaroopg92.github.io/penpa-edit/) content into the puzzle elements.

        * The process involves decompressing the base64-encoded content, parsing the JSON data, initializing the puzzle size, and unpacking the board elements into the respective attributes.
        """
        self.parts = decompress(b64decode(self.content[len(PENPA_PREFIX) :]), -15).decode().split("\n")
        self._init_size()
        self._unpack_board()

    def _init_size(self):
        """Initialize the size of the puzzle.

        * This is usually the first step while parsing a puzzle from [Penpa+](https://swaroopg92.github.io/penpa-edit/). The following attributes are set during the initialization:
            * `cell_shape`: The shape of the cell, currently only `square` shape is supported. Equivalent shape types include `sudoku` and `kakuro` in [Penpa+](https://swaroopg92.github.io/penpa-edit/).
            * `margin`: The margins of the puzzle in the order of (`top`, `bottom`, `left`, `right`).
            * `row`: The number of rows in the puzzle (excluding margins).
            * `col`: The number of columns in the puzzle (excluding margins).

        * These attributes are essential for correctly interpreting the puzzle elements and their positions on the board. For any grid puzzle, `(0, 0)` always refers to the top-left cell.

        Raises:
            NotImplementedError: If the `cell_shape` is other than `square`, `sudoku` and `kakuro`.
        """
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
        """Unpack surface elements from the board.

        * Store the `color_code` in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Surface` mode into the `surface` attribute with `Color` enumeration.

        * Multicolor surfaces are **not supported** currently. These surfaces won't be unpacked.
        """
        for index, color_code in self.problem["surface"].items():
            coord, _ = self.index_to_coord(int(index))
            point = Point(*coord)

            if color_code in [1, 3, 8]:
                self.surface[point] = Color.GRAY

            if color_code == 4:
                self.surface[point] = Color.BLACK

            if color_code == 2:
                self.surface[point] = Color.WHITE

    def _unpack_text(self):
        """Unpack number/text elements from the board.

        * Store the numbers or texts in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Number` mode into the `text` attribute.

        * For **tapa-like** puzzles, the numbers are separately stored with the label `tapa_x`. Single numbers will be converted to the `tapa_0` label automatically.

        * For **yaji-like** puzzles, the numbers are separately stored with the label `arrow_x`. The direction `x` is translated by a conversion table.

        * The **Candidates** submode in sudoku-like puzzles are neglected during unpacking.
        """
        for index, num_data in self.problem["number"].items():
            (r, c), category = self.index_to_coord(int(index))
            coord = _category_to_direction(r, c, category)
            # num_data: number, color, submode

            if num_data[2] == "4" or self.puzzle_name in ["tapa", "tapaloop"]:  # for tapa-like puzzles, convert to List[int]
                for i, data in enumerate(map(_int_or_str, list(num_data[0]))):
                    self.text[Point(*coord, f"tapa_{i}")] = data
            elif num_data[2] != "7":  # neglect candidates, convert to Union[int, str]
                if str(num_data[0]).endswith(
                    ("_0", "_1", "_2", "_3")
                ):  # for arrow-like puzzles, the label is set with arrow direction
                    data, arrow_dir = num_data[0].split("_")
                    arrow_dir_convert = {"0": Direction.TOP, "1": Direction.LEFT, "2": Direction.RIGHT, "3": Direction.BOTTOM}
                    self.text[Point(*coord, f"arrow_{arrow_dir_convert[arrow_dir]}")] = _int_or_str(data)
                else:
                    self.text[Point(*coord, "normal")] = _int_or_str(num_data[0])

    def _unpack_sudoku(self):
        """Unpack sudoku elements from the board.

        * Store the numbers or texts in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Number` mode, `Sudoku` submode into the `text` attribute.

        * The numbers are stored with `corner_x` labels indicating their direction in the cell. The direction `x` is translated by a conversion table.
        """
        corner_convert = {
            0: Direction.TOP_LEFT,
            1: Direction.TOP_RIGHT,
            2: Direction.BOTTOM_LEFT,
            3: Direction.BOTTOM_RIGHT,
            4: Direction.TOP,
            5: Direction.RIGHT,
            6: Direction.LEFT,
            7: Direction.BOTTOM,
        }
        for index, num_data in self.problem["sudoku"].items():
            (r, c), category = self.index_to_coord(int(index) // 4)
            coord = _category_to_direction(r, c, 0)
            corner_direction = corner_convert[(category - 1) * 4 + int(index) % 4]
            self.text[Point(*coord, f"corner_{corner_direction}")] = _int_or_str(num_data[0])

    def _unpack_symbol(self):
        """Unpack symbol elements from the board.

        * Store the symbols in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Shape` mode and `Composite` mode into the `symbol` attribute. Moreover, all the symbols are stored with the format `shape__style`,

        * For multiple symbols in a single cell, the symbols are stored as a boolean list, which are converted to a single integer for easier processing.

        Warning:
            Since the `symbol` and `style` is hard-coded, the solvers must be very careful of these labels. For example, a medium-sized circle is not a large circle. The shape and style must be correctly identified. The label might be encoded more conveniently in future versions.

        Warning:
            Since the handling for directed lines are defined in the `inequality` shape (with style = 5 ~ 8) in [Penpa+](https://swaroopg92.github.io/penpa-edit/), these symbols are converted to directed lines in the `line` attribute during unpacking. Please be careful of using these `inequality` shapes for other purposes for compatibility.
        """
        for index, (style, shape, _) in self.problem["symbol"].items():
            (r, c), category = self.index_to_coord(int(index))
            if isinstance(style, list):
                cvt_style = _style_convert(style)
                symbol_name = f"{shape}__{cvt_style}"
                self.symbol[Point(*_category_to_direction(r, c, category), "multiple")] = symbol_name

                if (
                    self.puzzle_name in ["castle", "tetrochain", "yajilin", "yajikazu", "yajitatami"]
                    and shape == "arrow_fouredge_B"
                    and self.text.get(Point(*_category_to_direction(r, c, category), "normal")) is not None
                ):  # compatible with older Penpa+ versions
                    num = self.text.pop(Point(*_category_to_direction(r, c, category), "normal"))
                    if cvt_style in [4, 16]:
                        self.text[Point(*_category_to_direction(r, c, category), f"arrow_{Direction.TOP}")] = num

                    if cvt_style in [1, 64]:
                        self.text[Point(*_category_to_direction(r, c, category), f"arrow_{Direction.BOTTOM}")] = num

                    if cvt_style in [8, 32]:
                        self.text[Point(*_category_to_direction(r, c, category), f"arrow_{Direction.LEFT}")] = num

                    if cvt_style in [2, 128]:
                        self.text[Point(*_category_to_direction(r, c, category), f"arrow_{Direction.RIGHT}")] = num
            else:
                symbol_name = f"{shape}__{style}"
                # special case for nondango (which problem/solution symbols are on the same coordinates)
                label = "nondango_mark" if self.puzzle_name == "nondango" and symbol_name == "circle_M__4" else "normal"
                self.symbol[Point(*_category_to_direction(r, c, category), label)] = symbol_name

                if shape == "inequality":  # convert inequality to arrow for directed line
                    if style == 6:
                        self.line[Point(r, c, Direction.BOTTOM, "in")] = True
                        self.line[Point(r + 1, c, Direction.TOP, "out")] = True

                    if style == 8:
                        self.line[Point(r, c, Direction.BOTTOM, "out")] = True
                        self.line[Point(r + 1, c, Direction.TOP, "in")] = True

                    if style == 5:
                        self.line[Point(r, c, Direction.RIGHT, "in")] = True
                        self.line[Point(r, c + 1, Direction.LEFT, "out")] = True

                    if style == 7:
                        self.line[Point(r, c, Direction.RIGHT, "out")] = True
                        self.line[Point(r, c + 1, Direction.LEFT, "in")] = True

    def _unpack_edge(self):
        """Unpack edge elements from the board.

        * Store the edges in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Edge` mode into the `edge` attribute. Supported submodes are `Normal`, `Diagonal`, `Helper (x)` and `Erase`.
        """
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

            if coord_1[0] == coord_2[0] and coord_2[1] - coord_1[1] == 1:  # row equal, horizontal line
                self.edge[Point(coord_2[0] + 1, coord_2[1], Direction.TOP)] = True
            if coord_1[1] == coord_2[1] and coord_2[0] - coord_1[0] == 1:  # col equal, vertical line
                self.edge[Point(coord_2[0], coord_2[1] + 1, Direction.LEFT)] = True
            if coord_2[0] - coord_1[0] == 1 and coord_2[1] - coord_1[1] == 1:  # upwards diagonal line
                self.edge[Point(coord_2[0], coord_2[1], Direction.TOP_LEFT)] = True
            if coord_2[0] - coord_1[0] == 1 and coord_1[1] - coord_2[1] == 1:  # downwards diagonal line
                self.edge[Point(coord_2[0], coord_1[1], Direction.TOP_RIGHT)] = True

        for index, _ in self.problem["deleteedge"].items():  # edge deletion mark, stronger than helper_x
            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, _ = self.index_to_coord(index_2)
            if coord_1[0] == coord_2[0]:  # row equal, horizontal line, set label to `delete` as indicator
                self.edge[Point(coord_2[0] + 1, coord_2[1], Direction.TOP, "delete")] = False
            elif coord_1[1] == coord_2[1]:  # col equal, vertical line, set label to `delete` as indicator
                self.edge[Point(coord_2[0], coord_2[1] + 1, Direction.LEFT, "delete")] = False

    def _unpack_line(self):
        """Unpack line elements from the board.

        * Store the lines in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Line` mode into the `line` attribute. Supported submodes are `Normal`, `Middle`, and `Helper (x)`.

        * For **hashi** puzzles, there are two types of lines: single lines and double lines. Double lines are stored with the `double` label.

        * For directed lines (such as in `nagare` puzzles), the lines are stored with the `in` and `out` labels in the `_unpack_symbol` process.
        """
        for index, data in self.problem["line"].items():
            if "," not in index:  # helper(x) lines
                coord, category = self.index_to_coord(int(index))
                if category == 2:
                    self.line[Point(coord[0], coord[1], f"{Direction.BOTTOM}")] = False
                    self.line[Point(coord[0] + 1, coord[1], f"{Direction.TOP}")] = False

                if category == 3:
                    self.line[Point(coord[0], coord[1], f"{Direction.RIGHT}")] = False
                    self.line[Point(coord[0], coord[1] + 1, f"{Direction.LEFT}")] = False

                continue

            index_1, index_2 = map(int, index.split(","))
            coord_1, _ = self.index_to_coord(index_1)
            coord_2, category = self.index_to_coord(index_2)

            line_type = "double" if self.puzzle_name == "hashi" and data == 30 else "normal"  # hashi has two types of lines
            if category == 0:
                dd = (Direction.RIGHT, Direction.LEFT) if coord_1[0] == coord_2[0] else (Direction.BOTTOM, Direction.TOP)
                self.line[Point(*coord_1, dd[0], label=line_type)] = True
                self.line[Point(*coord_2, dd[1], label=line_type)] = True
            else:
                eqxy = coord_1 == coord_2
                d = (
                    (f"{Direction.BOTTOM}" if eqxy else f"{Direction.TOP}")
                    if category == 2
                    else (f"{Direction.RIGHT}" if eqxy else f"{Direction.LEFT}")
                )
                self.line[Point(*coord_1, d, label=line_type)] = True

    def _unpack_board(self):
        """Initialize the content of the puzzle.

        * The unpacking order is `surface`, `text`, `sudoku`, `symbol`, `edge`, and `line`.
        """
        for p in (4, 3):  # must unpack solution board first, then edit board to keep consistency
            self.problem = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[p]))
            self._unpack_surface()
            self._unpack_text()
            self._unpack_sudoku()
            self._unpack_symbol()
            self._unpack_edge()
            self._unpack_line()

    def index_to_coord(self, index: int) -> Tuple[Tuple[int, int], int]:
        """Convert the [Penpa+](https://swaroopg92.github.io/penpa-edit/) index to coordinate.

        * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the coordination (with margins) and category of a cell is encoded as a single integer index. This function helps to convert the index back to the ((`row`, `col`), `category`) format.

        Args:
            index: The [Penpa+](https://swaroopg92.github.io/penpa-edit/) index to be converted.
        """
        top_margin, bottom_margin, left_margin, right_margin = self.margin
        real_row = self.row + top_margin + bottom_margin + 4
        real_col = self.col + left_margin + right_margin + 4
        category, index = divmod(index, real_row * real_col)
        return (index // real_col - 2 - top_margin, index % real_col - 2 - left_margin), category

    def encode(self) -> str:
        """Encode the puzzle into [Penpa+](https://swaroopg92.github.io/penpa-edit/) format.

        * The process involves packing the puzzle elements into the solution dictionary, updating the relevant part of the [Penpa+](https://swaroopg92.github.io/penpa-edit/) content, and compressing it into a base64-encoded string.
        """
        self.solution = json.loads(reduce(lambda s, abbr: s.replace(abbr[1], abbr[0]), PENPA_ABBREVIATIONS, self.parts[4]))
        self._pack_board()
        self.parts[4] = reduce(lambda s, abbr: s.replace(abbr[0], abbr[1]), PENPA_ABBREVIATIONS, json.dumps(self.solution))
        return PENPA_PREFIX + b64encode(compress("\n".join(self.parts).encode())[2:-4]).decode()

    def _pack_surface(self):
        """Pack surface elements into the board.

        * Store the `Color` enumeration in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Surface` mode with decicated `color_code`. The `GRAY` color will be converted to `color_code = 8` only, but the original surfaces won't be overwritten.

        * Multicolor surfaces are **not supported** currently. These surfaces won't be packed.
        """
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
        """Pack text/number elements into the board.

        * Store the numbers or texts in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Number` mode from the `text` attribute.

        * Currently all the solution texts are placed in the center with `Normal` submode, the original texts won't be overwritten.
        """
        for (r, c, _, _), data in self.text.items():
            coord = (r, c)
            index = self.coord_to_index(coord, category=0)  # currently the packing of texts are all in the center
            if not self.problem["number"].get(f"{index}"):  # avoid overwriting the original stuff
                self.solution["number"][f"{index}"] = [str(data), 2, "1"]

    def _pack_symbol(self):
        """Pack symbol elements into the board.

        * Store the symbols in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Shape` mode from the `symbol` attribute.

        * Currently all the solution symbols are placed in the center without any submodes, the original symbols won't be overwritten.
        """
        for (r, c, _, _), symbol_name in self.symbol.items():
            shape, style = symbol_name.split("__")
            coord = (r, c)
            index = self.coord_to_index(coord, category=0)  # currently the packing of symbols are all in the center
            if self.puzzle_name == "nondango":
                self.solution["symbol"][f"{index}"] = [int(style), shape, 1]
            elif not self.problem["symbol"].get(f"{index}"):  # avoid overwriting the original stuff
                self.solution["symbol"][f"{index}"] = [int(style), shape, 1]

    def _pack_edge(self):
        """Pack edge elements into the board.

        * Store the edges in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Edge` mode from the `edge` attribute. Supported submodes are `Normal` and `Diagonal`, and the original edges won't be overwritten.
        """
        for r, c, d, _ in self.edge:
            coord_1 = (r - 1, c - 1)
            coord_2 = (r - 1, c - 1)
            if d == Direction.TOP:
                coord_2 = (r - 1, c)
            if d == Direction.LEFT:
                coord_2 = (r, c - 1)
            if d == Direction.TOP_RIGHT:
                coord_1 = (r, c - 1)
                coord_2 = (r - 1, c)
            if d == Direction.TOP_LEFT:
                coord_2 = (r, c)

            index_1 = self.coord_to_index(coord_1, category=1)
            index_2 = self.coord_to_index(coord_2, category=1)
            if not self.problem["edge"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.solution["edge"][f"{index_1},{index_2}"] = 3

    def _pack_line(self):
        """Pack line elements into the board.

        * Store the lines in [Penpa+](https://swaroopg92.github.io/penpa-edit/) `Line` mode from the `line` attribute. Only `Normal` submode is supported, and the original lines won't be overwritten.
        """
        for r, c, d, label in self.line:
            coord_1 = (r, c)
            coord_2 = (r, c)
            category = 0

            if d == Direction.RIGHT:
                coord_2, category = (r, c), 3
            if d == Direction.BOTTOM:
                coord_2, category = (r, c), 2
            if d == Direction.LEFT:
                coord_2, category = (r, c - 1), 3
            if d == Direction.TOP:
                coord_2, category = (r - 1, c), 2

            index_1 = self.coord_to_index(coord_1, 0)
            index_2 = self.coord_to_index(coord_2, category)
            if self.puzzle_name == "hashi" and label == "double":
                self.solution["line"][f"{index_1},{index_2}"] = 30
            elif not self.problem["line"].get(f"{index_1},{index_2}"):  # avoid overwriting the original stuff
                self.solution["line"][f"{index_1},{index_2}"] = 3

    def _pack_board(self):
        """Pack the solution into penpa format.

        * The packing order is `surface`, `text`, `symbol`, `edge`, and `line`.
        """
        self._pack_surface()
        self._pack_text()
        self._pack_symbol()
        self._pack_edge()
        self._pack_line()

    def coord_to_index(self, coord: Tuple[int, int], category: int = 0) -> int:
        """Convert the coordinate to [Penpa+](https://swaroopg92.github.io/penpa-edit/) index.

        * In [Penpa+](https://swaroopg92.github.io/penpa-edit/), the coordination (with margins) and category of a cell is encoded as a single integer index. This function helps to convert the ((`row`, `col`), `category`) format back to the index.

        Args:
            coord: The coordination to be converted.
            category: The category code of the direction (default is 0).
        """
        top_margin, bottom_margin, left_margin, right_margin = self.margin
        real_row = self.row + top_margin + bottom_margin + 4
        real_col = self.col + left_margin + right_margin + 4
        return (category * real_row * real_col) + (coord[0] + 2 + top_margin) * real_col + coord[1] + 2 + left_margin
