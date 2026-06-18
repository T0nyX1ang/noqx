"""Direct JSON-based puzzle encoding for local tools and benchmarks."""

import json
from base64 import b64decode, b64encode
from zlib import compress, decompress

from noqx.puzzle import Puzzle

DIRECT_PREFIX = "direct:"
DIRECT_FORMAT = "noqx-direct-puzzle"
DIRECT_VERSION = 1


def _encode_point_map(data):
    return [[r, c, d, label, value] for (r, c, d, label), value in sorted(data.items())]


def _decode_point_map(data):
    return {(r, c, d, label): value for r, c, d, label, value in data}


class DirectPuzzle(Puzzle):
    """A compact direct encoding of the internal :class:`Puzzle` fields."""

    def decode(self):
        """Decode a direct puzzle string into the puzzle fields."""
        if not self.content.startswith(DIRECT_PREFIX):
            raise ValueError("Invalid direct puzzle encoding.")

        data = json.loads(decompress(b64decode(self.content[len(DIRECT_PREFIX) :]), wbits=-15).decode())
        if data.get("format") != DIRECT_FORMAT:
            raise ValueError("Invalid direct puzzle format.")
        if data.get("version") != DIRECT_VERSION:
            raise ValueError("Unsupported direct puzzle version.")

        self.puzzle_name = data["puzzle_name"]
        self.param = data.get("param", {})
        self.row = data["row"]
        self.col = data["col"]
        self.margin = tuple(data.get("margin", (0, 0, 0, 0)))
        self.surface = _decode_point_map(data.get("surface", []))
        self.text = _decode_point_map(data.get("text", []))
        self.symbol = _decode_point_map(data.get("symbol", []))
        self.edge = _decode_point_map(data.get("edge", []))
        self.line = _decode_point_map(data.get("line", []))

    def encode(self) -> str:
        """Encode the current puzzle fields into a direct puzzle string."""
        data = {
            "format": DIRECT_FORMAT,
            "version": DIRECT_VERSION,
            "puzzle_name": self.puzzle_name,
            "param": self.param,
            "row": self.row,
            "col": self.col,
            "margin": list(self.margin),
            "surface": _encode_point_map(self.surface),
            "text": _encode_point_map(self.text),
            "symbol": _encode_point_map(self.symbol),
            "edge": _encode_point_map(self.edge),
            "line": _encode_point_map(self.line),
        }
        raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode()
        return DIRECT_PREFIX + b64encode(compress(raw)[2:-4]).decode()


def from_puzzle(puzzle: Puzzle) -> DirectPuzzle:
    """Copy any puzzle object into a direct puzzle object."""
    result = DirectPuzzle(puzzle.puzzle_name, "", dict(puzzle.param))
    result.row = puzzle.row
    result.col = puzzle.col
    result.margin = tuple(puzzle.margin)
    result.surface = dict(puzzle.surface)
    result.text = dict(puzzle.text)
    result.symbol = dict(puzzle.symbol)
    result.edge = dict(puzzle.edge)
    result.line = dict(puzzle.line)
    result.content = result.encode()
    return result
