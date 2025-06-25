"""Initializations of the base encodings."""

from typing import Any, Dict, Optional, Tuple, Union


class Color:
    """Enumeration for colors."""

    GREEN: int = 0
    GRAY: int = 1
    BLACK: int = 2
    DARK: Tuple[int, int] = (GRAY, BLACK)


class Direction:
    """Enumeration for directions."""

    CENTER: str = "center"
    TOP: str = "top"
    LEFT: str = "left"
    TOP_LEFT: str = "top_left"
    DIAG_UP: str = "diag_up"
    DIAG_DOWN: str = "diag_down"


def Point(r: int, c: int, d: str = Direction.CENTER, label: str = "normal") -> Tuple[int, int, str, str]:
    """Create a point tuple with row, column, direction, and label."""
    return (r, c, d, label)


class Puzzle:
    """Base class for puzzle encodings."""

    def __init__(self, name: str, content: str, param: Optional[Dict[str, Any]] = None):
        """Initialize the puzzle."""
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
        """Clear the puzzle structure."""
        self.surface.clear()
        self.text.clear()
        self.symbol.clear()
        self.edge.clear()
        self.line.clear()

    def decode(self):  # pragma: no cover
        """Decode the source content to a puzzle object."""
        raise NotImplementedError

    def encode(self) -> str:  # pragma: no cover
        """Encode the puzzle object to the target content."""
        raise NotImplementedError
