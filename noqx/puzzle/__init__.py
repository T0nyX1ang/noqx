"""Initializations of the base encodings."""

from enum import Enum, Flag, auto
from typing import Any, Dict, NamedTuple, Optional, Tuple, Union


class Color(Flag):
    """Enumeration for colors."""

    GREEN = auto()
    GRAY = auto()
    BLACK = auto()
    DARK = GRAY | BLACK


class Direction(Enum):
    """Enumeration for directions."""

    CENTER = "center"
    TOP = "top"
    LEFT = "left"
    TOP_LEFT = "top_left"
    DIAG_UP = "diag_up"
    DIAG_DOWN = "diag_down"


class Point(NamedTuple):
    """A point with row number, column number, direction and inner position."""

    r: int
    c: int
    d: Direction = Direction.CENTER
    pos: str = "normal"


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

        self.surface: Dict[Point, Color] = {}
        self.text: Dict[Point, Union[int, str]] = {}
        self.symbol: Dict[Point, str] = {}
        self.edge: Dict[Point, bool] = {}
        self.line: Dict[Point, bool] = {}

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
