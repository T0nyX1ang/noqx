"""The Inaba's Island solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, grid, invert_c, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src, grid_color_connected, grid_src_color_connected


class InabasIslandSolver(Solver):
    """The Inaba's Island solver."""

    name = "Inaba's Island"
    category = "shade"
    aliases = ["inabasisland"]
    examples = [
        {
            "data": "m=edit&p=7Vbfj9pGEH7nr4j2NSvVa4x/SVXFEUiTcj4ugChYFjKcAd/ZLDU2lxrxv2d2jWOvbaL0oWkeKsNo5vt259eaHY5/JW7kYQOeto4lTOBp6xL/6gr7SNdn4seBZ77B3STe0QgUjB8GA7xxg6OHP853wx7tvr7r/nnS48WCvJeSD9LsefD89lP4xwe/HZGBpY/uR/e+vO3+3rt7VPtv1VFynMbe6TEkd8/TxWQzmm0N+e++tVDSxYPU+bjY/HLqTn9t2dccnNY5Ncy0i9P3po0IwkiGL0EOTh/Nc3pvphZOx0AhrDgYhUkQ+2sa0AhxjMC6YbZRBrVfqDPOM62XgUQC3cp0FdQ5qGs/Wgfecpg5Gpl2OsGIxb7ju5mKQnryWDCWG7PXNFz5DFi5MbTvuPMPCLeBOCZP9CW5LiXOBafdrILxd1YATvIKmJpVwLR/rYLgQBtyN5zLBY7lE2S/NG1WyLRQ9UIdm2eQlnlGigxbZaxmJ4cUBUxSmKpo6oKpMrP91dQkgdVEzxrzXCw2mFmwhhjIED0TibnWCpswG/0GzcwRmSFqyWbRiVQCWMCSC5lFzENAMwhvyZzLAZcylxPoGE7bXL7jUuKyw+WQr+lzOeOyx6XCpcrXaKzn33kqkJeGTAWSUqAgOTukH5CdLev8tik/nZ8LcVo2GifRxl178GuwknDlRW8sGoVugOAuQkcaLI8Zv/Q+u+sYmdl1WGYEbM99CFBA6SHw900eckoA/e2eRl4jxUDvaXvLFaMaXK1o9FTJ6dUNArEWPiYEKLtMBCiO4KYo2W4U0VcBCd14JwCle1Hw5O0rzYxdMUX3xa1EC4t2XFroM+Jf+L3J7CD/Hxw/5eBgRyT9o/Hx39+bNrQaxgFOHzA6JEt3CX3m70AzAYXb6fwWYTUQcADNO6D5PIZyK7isNcUAotOuEPCSNLvq3NoB70IWo1MhtCsB/x9FQs8Jo0IYeQy5WiAvvSkIyWuvRSF58bUw5Gv1tTg3yycd54e/bvz2otE3RklBVuGGgQLoN2ZKiW3Cb4yPElvFa7OCJVsfF4A2TAxAq0MDoPrcALA2OgC7MT2Y1+oAYVlVZwgLVRsjLFR5ktjoJYloHFPktL4A",
        },
        {"url": "https://pzplus.tck.mn/p.html?island/4/5/k0i6i0j6g", "test": False},
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(defined("clue"))
        self.add_program_line(invert_c(color="clue", invert="clueless"))
        self.add_program_line(shade_c(color="black", _from="clueless"))
        self.add_program_line(invert_c(color="black", invert="white", _from="clueless"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="not white", grid_size=(puzzle.row, puzzle.col)))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"clue({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(grid_src_color_connected((r, c), color="black"))
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="black"))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"{'not' * (color not in Color.DARK)} black({r}, {c}).")

        self.add_program_line(display(item="black"))

        return self.program
