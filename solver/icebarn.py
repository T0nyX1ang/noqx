"""The Icebarn solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.route import count_area_pass, crossing_route_connected, directed_route
from noqx.rule.variety import straight_at_ice


class IcebarnSolver(Solver):
    """The Icebarn solver."""

    name = "Icebarn"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VjvT9tIE/7OX1Ht1650Xnv9K9J9CJT22qOBFhAHURQZMJA2wZyT0NaI/73P7E6a2LHNhVanV69OUbKPn9mdnZmd3R1n+vc8yVOpfKmU9CLpSIVP4ERS+4FU2jVfhz9Ho9k47byQ3fnsJssBpNzvyatkPE3lu9ObvZ2s++VV96/7aHZ2pt4487fOyafXn15+nPz5duTl6nUvOnh/8H7kXnf/2Nn+EOy+DA7m0+NZev9horY/HZ8dXR2cXMfut93emS7O9h3/3dnVb/fd49+3+mQWPoOthyLuFF1ZvOn0hSuk+SoxkMWHzkPxvlP0ZHEIkZD+QIrJfDwbXWTjLBeGU+i3B6SEdAF3l/DEyAntWFI5wD3gyA47BUzyPPsy7A23LXXQ6RdHUtDk22Y4QTHJ7lOaDTrM80U2OR8RcZ7MEL7pzehOSA+C6fwy+zznrmrwKIuucYFHLPzATG1+QNPCD4LWD0JVP9jRn/djPLpNL0d5jRPx4PERC/QRbgw7ffLoeAmjJTzsPIjIER1fikjZxrVNYJvQNpFtYtPEdkBsn5RjH5VjFSjH49YOUmrRcn+X+7t2JuVyf1dz69vW43Ga9Wrur7m/tiYqn/UGrDfg/gH3D1hvwHoDHhdyy46riPVG3D/i/jE/x4tnHhfb2KjY2uk6dj6X/XcdGocY9xBjsrUv3vawzAgjLaJL7vXF/vHRgkNX1XnA7ykGBIpGhLKSISLwGviA1HnrfAgr63havRo9oYLVdbwP72r0hJQTNf1jRfPCsSpPq9xHeKq8CUcNT6tXwyPbyKA6gdckMCFaN0k5ITKnXkDBrqrCCr026+Sa3yPsJFl45veV+XXMr29+90yfXayop33pkTeuFGhxxiNPCEee1JQ7wGiBLY9WatojhF3wtE8Mr8vYQV4aPcESByH0w3jCOsK8WA2DwWuEweAAeMHDNspR0unHUoe2j8G0rwhrVca0Hw2GbbTnCAfUh/mAeLYzgC/sO1qp2Xcdoc8PjLF0+hjsALPOEDbQGWUwrsMQGWfmhU7NOjV0aus7WmD2BT5q2vdmXvC09w0fLrELnRwH7WAul30nrHhel/SznYTpjDJ9oJ+xF0GnwzEPEHM6Oxc4sDajBc/xj6gP8xF4OlYJxw6w9R3tDxs8H3UBZSrhEH1C7hMSb+OGFpjzKvSgh/kYfLzgkXurOGT7UWYsMfLBZ1989PEXPHT6nMM+dPqsh2yjE4JigvpFe4u4IYarmHMPLeLPMUeuas5VM5Y2tsHIDY9zwCOdzHvgfeYxr+aYoIUezg3EdolJP89Le8SsCzblidmaO+ZXm9/AbNmQrsZ/eHna4710csd0v9GJiMsZNd14NPtG9/2mpwZOesQ8juzp8aS5/cAWjHWf8P9LMtjqi8N5fpVcpCiIdi+v0xe9LJ8kYzz15pPzNF8+H94kd9RrJ5vcZdPRLBWoW8U0Gw+nVsMw/ZpczETHls6rkhJ3a/SWqHGW3VEBVqNhISqRo+vbLE9rRUSm8KNBFYlqVJ1n+WXFpi/JeFz2xbxVlKiLUX4xLlOzHOXkyrO57krMJJndlIiVErqkKb2tBHOWlE1MPieV2SbLcDxuia/CfFFq4I3nv5eM//mXDFos59mn5fNqqZ89vPvFnkSBLYt9Ke7mw2SIWAuJyLUKcFNJ1BK/XIi6BKXIM0bihqgX4AraUNBqRMM8p79O0OKLiEOJN6wmYSTxItMkjLEdnCYpRBAjjZvEuGpQljeIUbS3SFHioqptEnoSpXCT0EUoWoQoipssInvbvcUbeJNYIVZ4BWsS4w8p5YfPFT+hvN20dr9aQ9IezLY1al/eJ3KjdYGfSLv2nG1P95aNEqOI30RwurGAVDUdR/UCUrWZAMcECv5NBDhxNhRAFV4kNhFA1YaCHl5+JIpYXNG2mqntsNmyNPrZGORGPze9PjDHJoJ/vRgwVWaWt5T8S2GVrin8wbbU/ivSOr6hzF+RVvm1mp6MXS/rwdZU9mCrxT2o9foe5FqJD66hyiet1UKfrKrW+jTVWrlPU61W/P3B1nc=",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white", directed=True))
        self.add_program_line(adjacent(_type="line_directed"))
        self.add_program_line(directed_route(color="white", path=True, crossing=True))
        self.add_program_line(crossing_route_connected(color="white", directed=True))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color == Color.BLUE, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"ice({r}, {c}).")

        self.add_program_line(shade_c(color="crossing", _from="ice"))
        self.add_program_line(straight_at_ice(color="white", directed=True))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(rooms):
            if len(tuple((r, c) for r, c in ar if puzzle.surface.get(Point(r, c)) == Color.BLUE)) != len(ar):
                continue  # filter ice rooms

            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(("gt", 0), _id=i, directed=True))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if clue.upper() == "IN":
                self.add_program_line(f"path_start({r}, {c}).")
                self.add_program_line(f"grid({r}, {c}).")

            if clue.upper() == "OUT":
                self.add_program_line(f"path_end({r}, {c}).")
                self.add_program_line(f"grid({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            dir_dict = {"1": Direction.LEFT, "3": Direction.TOP, "5": Direction.RIGHT, "7": Direction.BOTTOM}
            dir_value = symbol_name.split("__")[1]

            if symbol_name.startswith("arrow_N") and d == Direction.TOP:
                if dir_dict.get(dir_value) == Direction.TOP:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.TOP}").')

                if dir_dict.get(dir_value) == Direction.BOTTOM:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.TOP}").')

            if symbol_name.startswith("arrow_N") and d == Direction.LEFT:
                if dir_dict.get(dir_value) == Direction.LEFT:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.LEFT}").')

                if dir_dict.get(dir_value) == Direction.RIGHT:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.LEFT}").')

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
