"""Definitions of the base encodings."""

from typing import Any, Dict, Optional, Tuple, Union


class Color:
    """Enumeration for colors.

    * Currently, only one color can be shaded on a single cell. Each cell can be categorized into
    two types, **shaded** or **unshaded**. The unshaded cells are represented by the **green** color, while
    the shaded cells can be either **gray** or **black** to distinguish region edges.

    * For compatiblity issue with the web version, the enumeration class is altered to a simple class.

    Attributes:
        GREEN: Represents the green color on shaded cells or unshaded cells.
        GRAY: Represents the gray color on shaded cells.
        BLACK: Represents the black color on shaded cells.
        DARK: A tuple representing dark colors (gray and black).
    """

    GREEN: int = 0
    GRAY: int = 1
    BLACK: int = 2
    DARK: Tuple[int, int] = (GRAY, BLACK)


class Direction:
    """Enumeration for directions.

    * This `Direction` enumeration only involves with the direction of **adjacent** cells. For the directions
    inside a cell, please refer to the `label` descriptor instead. According to symmetry, only 3 directions are needed
    in the program: the top, left, and top-left directions.

    * For edge visualizations, two additional directions are included in this enumeration, which are the upwards-diagonal
    and downwards-diagonal directions. These two directions should be only used for edge visualizations.

    * For compatiblity issue with the web version, the enumeration class is altered to a simple class.

    Attributes:
        CENTER: The center direction. This is the default direction for most cells.
                Using this direction will not have effects on visualizations.
        TOP: The top direction. This indicates the adjacent cell is on the **top** side of a cell.
             Also, this direction is used for **horizontal** edge visualizations.
        LEFT: The left direction. This indicates the adjacent cell is on the **left** side of a cell.
              Also, this direction is used for **vertical** edge visualizations.
        TOP_LEFT: The top-left direction. This indicates the adjacent cell is on the **top-left** side of a cell.
                  Using this direction will not have effects on visualizations.
        DIAG_UP: The downwards-diagonal direction. This is only used for edges that goes from **bottom-left** to **top-right**.
        DIAG_DOWN: The upwards-diagonal direction. This is only used for edges that goes from **top-left** to **bottom-right**.
    """

    CENTER: str = "center"
    TOP: str = "top"
    LEFT: str = "left"
    TOP_LEFT: str = "top_left"
    DIAG_UP: str = "diag_up"
    DIAG_DOWN: str = "diag_down"


def Point(r: int, c: int, d: str = Direction.CENTER, label: str = "normal") -> Tuple[int, int, str, str]:
    """A factory function to create a point tuple.

    * For compatiblity issue with the web version, the NamedTuple class is altered to a factory function.

    * The label descriptor is used for elements **inside** an cell. Common labels include:

        * `normal`: The normal label. This is the default label for most elements.
                    Using this direction will not have effects on visualizations.
        * `l/u/r/d`: The left, up, right, and down labels. These labels are often used for
                     **arrows**, **lines**, etc. to indicate their directions.
        * `tapa_x`: The tapa label with index x (x = 0 ~ 3). This label is often used for
                    **tapa-like** clues to indicate their positions inside a cell.
        * `sudoku_x`: The sudoku label with index x (x = 0 ~ 7). This label is often used for
                      **sudoku-like** clues to indicate their positions inside a cell.
        * `multiple`: The symbol label with style x (x = 0 ~ n). This label is often
                      used for indicating **mulitple symbols** inside a cell.
        * `delete`: The delete label. This label is often used for **erased** edges.
        * other labels may be defined in specific puzzles, such as `hashi` and `nondango`.

    Args:
        r: The row index of the point.
        c: The column index of the point.
        d: The direction of the point (default is `Direction.CENTER`).
        label: The label of the point (default is `"normal"`).
    """
    return (r, c, d, label)


class Puzzle:
    """Base class for puzzle encodings.

    * The `decode` and `encode` method should be implemented in an inherited class,
    such as the `PenpaPuzzle`.
    """

    def __init__(self, name: str, content: str, param: Optional[Dict[str, Any]] = None):
        """Initialize the puzzle.

        * The atom element of a puzzle is a cell, and the data structures are all crafted around a cell.
        In detail, a puzzle has the following elements:

            * `puzzle_name`: the name of the puzzle, should be the same as the filename of the solver.
            * `param`: the parameters of the puzzle.
            * `row`: the number of rows in the puzzle.
            * `col`: the number of columns in the puzzle.
            * `margin`: the margin of the puzzle, the order is a tuple of
                        (`top-margin`, `bottom-margin`, `left-margin`, `right-margin`).
            * `surface`: the shaded cells in the puzzle stored in a dictionary.
            * `text`: the text clues in the puzzle stored in a dictionary.
            * `symbol`: the symbols in the puzzle stored in a dictionary.
            * `edge`: the borders in the puzzle stored in a dictionary.
            * `line`: the lines in the puzzle stored in a dictionary.

        Args:
            name: The name of the puzzle.
            content: The content of the puzzle.
            param: Optional parameters for the puzzle.
        """
        self.puzzle_name = name
        self.param = param if param is not None else {}
        self.content = content

        self.col: int = 0
        self.row: int = 0
        self.margin: Tuple[int, int, int, int] = (0, 0, 0, 0)  # top, bottom, left, right

        self.surface: Dict[Tuple[int, int, str, str], int] = {}
        self.text: Dict[Tuple[int, int, str, str], Union[int, str]] = {}
        self.symbol: Dict[Tuple[int, int, str, str], str] = {}
        self.edge: Dict[Tuple[int, int, str, str], bool] = {}
        self.line: Dict[Tuple[int, int, str, str], bool] = {}

    def clear(self):
        """Clear the puzzle structure.

        * This function is often used before initializating a new solver instance.
        """
        self.surface.clear()
        self.text.clear()
        self.symbol.clear()
        self.edge.clear()
        self.line.clear()

    def decode(self):  # pragma: no cover
        """Decode the source content to a puzzle object.

        Raises:
            NotImplementedError: If this method is not implemented.
        """
        raise NotImplementedError

    def encode(self) -> str:  # pragma: no cover
        """Encode the puzzle object to the target content.

        Raises:
            NotImplementedError: If this method is not implemented.
        """
        raise NotImplementedError
