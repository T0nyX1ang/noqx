"""The Hakoiri-masashi solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, count, display, grid, shade_cc
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_color_adjacent
from noqx.rule.reachable import grid_color_connected


class HakoiriSolver(Solver):
    """The Hakoiri-masashi solver."""

    name = "Hakoiri-masashi"
    category = "var"
    aliases = ["hakoirimasashi"]
    examples = [
        {
            "data": "m=edit&p=7Vbfb9MwEH7vXzH52Q+xz47tvG2j42VswIbQVFVVtxVW0aqjPxBK1f+dz86lXkelSUNDgFAb58vlfP7uy/mSxdfVcD6Sqoh/8hJn/Izy6dC+TEfBv8vxcjKqDuThank3mwNIeX5yIj8NJ4uR7PTYrd9Z16GqD2X9uuoJJaTQOJToy/pdta7fVHVX1he4JaSH7bRx0oDdDD+m+xEdN0ZVAJ8xBrwCnH0fHDVXb6tefSlFXOMozYxQTGffRoI5xOub2fR6HA3XwyUyWdyN7/nOYnU7+7IS2/BiuposxzezyWwuUjzV38j6sKF/tYc+Zfq0pU/76etMv/sC9MN++hs8lvdIYFD1Yi4fMvQZXlTrTeQZR5XGq2otqEAUJbPewmpY6KGltLDohxal/eNpisxPpscTseZJWlmn8RLEZE1pfJXGIo02jafJpwuOmoLUBkQRSutyF2vXYEUZW2BrGBtgy9gClw02OmON/WA0Y4c4Ptt1YAwOxOtSAawYK2CeS4hJxBgciDkQOFDLAZxtyxNrOZXjG55rMNfwXBP5Mx8LPo7Xcirj6GM4vkGOps0xauUynxYbrGs4pkHMkuOU4O94rsPcwPkGNJCi4YMzsM18LOtjwb9k/xL6OObvwM2xv7M5fvR3nK8DN8/cPLh55uZjn+L4PmQ+TsfexfYSfArmBp6KeSrwVJbtaotjfFxv41Oh2UcDE2OCv+M48FeeMfxVyHauAUI9bDGeI3GdEOqHuH4IdUVcV4S6Jd3Gx7q6zFixJiHsYs4x1XDJmpTQxLOPh4bBZexZfw/9fZu7zboF6BxY5xDz4hrw+kFM1Jhne8Dc0M4Ff8U5xpeLZs01NNesuVJbHNfCNftY6MOaYF+TpawJ72ucYTdZQ96bOMNeZs15j+AMO2uL+ieuyYRN6693cdqnm9jOY5s5TqNJY5naj4td8xf6qtq2vuZFICJZ7qutJbZHny3Pa49P5tCj5tW/+7N/n63f6Ynu7efRwdlsPh1O8IK8uBvejwS+SjYd8V2kAxLjK+f/h8of+qESH1Hx7G31QjvkCTo9qI3XfH0uxf1qMBwgJ4FvYRntaD377fafs//2p4LW1e/8AA==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(colors=["ox_E__1", "ox_E__2", "ox_E__3", "white"]))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__1", adj_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__2", adj_type=8))
        self.add_program_line(avoid_same_color_adjacent(color="ox_E__3", adj_type=8))
        self.add_program_line(grid_color_connected(color="not white", grid_size=(puzzle.row, puzzle.col)))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(count(1, color="ox_E__1", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__2", _type="area", _id=i))
            self.add_program_line(count(1, color="ox_E__3", _type="area", _id=i))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            symbol, style = symbol_name.split("__")
            validate_type(symbol, ("ox_B", "ox_E"))
            fail_false(style in ["1", "2", "3", "4", "7", "8"], f"Invalid symbol at ({r}, {c}).")
            if style in ["1", "2", "3"]:
                self.add_program_line(f"ox_E__{style}({r}, {c}).")
            else:
                self.add_program_line(f"white({r}, {c}).")

        self.add_program_line(display(item="ox_E__1"))
        self.add_program_line(display(item="ox_E__2"))
        self.add_program_line(display(item="ox_E__3"))

        return self.program
