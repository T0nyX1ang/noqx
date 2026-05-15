"""The Icebarn solver."""

from typing import List, Tuple

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, full_bfs
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.route import count_area_pass, crossing_route_connected, directed_route
from noqx.rule.variety import straight_at_ice

dir_dict = {"1": Direction.LEFT, "3": Direction.TOP, "5": Direction.RIGHT, "7": Direction.BOTTOM}


class IcebarnSolver(Solver):
    """The Icebarn solver."""

    name = "Icebarn"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VdNb+M2EL3nVyx4noP4TfmWTdNe0mzbpCgMwQi8ibcx6tSpY/dDgf97H8lR1DSSXGW3BVoUhjlP84ZDDociRw8/7eabBUlLUpIOVJDEzxWBjHUkjUr/gn+Xy+1qMXlDx7vt7XoDQPTunD7MVw8LOqpk6itnR491OamPqf5iUgklKP2lmFH99eSx/nJST6m+ACXIzkjc7Vbb5fV6td6IpJOwOwOSghTgaQu/S3xEJ1kpC+BzYJe7TQHnm836l6vzq7dZ9dWkqi9JxMHfpu4Rirv1zwuRfaTn6/Xd+2VUvJ9vEeHD7fJekAbxsLtZ/7BjUznbU32cQuAeTRxyOA7dxqGf4tAdcXCgHx/Havnj4ma56QiinO33SNA3CONqUsWIvm1haOHF5FGEQkwsiSCzUFm4LHwWIYsyiTJ3KPOTLAqWkqVmmTtJ2Ui2V2yvFEu2V4alzVJzP8N+Ddsbtjd5itKyX8d+Hds7tnfs17Ffx/08Sw5cBvYb2D6wfcnPZfPM/UrPMs9TFYqlZhn77WPKH9HK1E6x3k7CQeXpT8kXTvfoHQao9Eu99936mJgOP16abr1VnX586PZTyjiufKmPCazsS31MZJfeddtjI6keQvcRaYleTkkWvugjXIcrZOjzlCeV2ku8JFTr1H6W2iK1NrVnyeYUGdXGko7RKBKQOGF1xkGTidsCGBJYM4ZesV5Brxq9eY4Ly35ci52Hf5exCRjXM4beBMYOuNFjbibbG1uS8aHF8ZWJ2Mjn2PDccCmY+DpF7KIN613U8zwdYuHYIclw7CaoP2D0Ddw3FMDs02MOgcf1uIx8yePCp2GfBj6NZWyBORbEaBzrHfSu0fsWK/jkdTAFxlKhxZLHVdG/brFin4V7wjrAZ8Fr7rDmwbfYlYxL6Hn9Q7RhfYC+zGNBAkvG8mkO2uJW9ow9bDzb+KhXjBUw7yuv4Yf1JfRlozfPsef545JvMfaD5VgsbGyjh0/Le9jCp9Xt3CznDtWD0c26lc8x7z1IrD+vOfaq4b2a+srGD/aG5j2go0/Wa+gt6zGu8c3eiHuG9wbWtsXRP48b35GUl328e+OreZJak1qXXlkfb72/eC92ndxxblUggXsXFdVquf0tXeU4+op8VD4nxh4nuAKQjDLkY+VgHJXLdVzXz/+3mNlRJS52mw/z6wWKoNOb7xdvztebu/kKTxe38/uoPVnf3a8fltuFQG26PxK/ivTHzab+L1f/BeVqTFbx6pfzdVf3x54VVX1GqOeofkfifnc1v8JaC8LKDRI4GAlX1ycncQ3i5ntFT5w73QQOtpHE4CR6xpl+OmIgFlF6Qq3eRwZC3dxHlhQ/c3pYUBS/fnppHGCoAnto1IgDLCoqFFF9pCZUXn2kwlIMkKF3wkEejFb2LhUoip9ufbQOJK1/LX3A+fDUhuMaXJLhxRzK0XB6D+yNwQQf2HbDe3Z4uw+8KCVqxjHEdDQRXfUdR93EdDSBYwL15RhiOpqAK99zSPYQ09HEOWptQmmEKzpXM50G49LSG2fvIvfGOfb6mI4m/vZE/uMFB+r62dHv",
        },
        {
            "data": "m=edit&p=7VVNb9NAEL3nV1R73sN+2bv2rS2FSwkfKUKVZVVu69KIBBcnAeQo/71vd6e1Sy1AIKEiocQzz+OZ2Xmz6/Hq86Zqay6F/2vHofEz0oVLuTRcgn4n8/Wizvf4/mZ93bQAnL+a8qtqsar5pJAhVpaTbZfl3T7vXuQFU4yHS7KSd2/ybfcy7055N8MjxpOSs+VmsZ5fNIumZcEm4XcMJBlXgEc9fB+ee3QYjVIAT4HTGHYKWLVt8/VsenYQTa/zojvhzC9+EMI9ZMvmS81ijnB/0SzP595wXq3BcHU9v2Fc48Fqc9l83JCrLHe82w8UKOKOh/wxD93z0Pc89AgPIvrnPBbzT/XlvB0hkZW7HTboLWic5YVn9K6HroezfMtMxvKEs1REJaPSUSVBWRuUI+WCymKAFAlpSzo+lpK0Jj+tSBvSFGdS6J1vzRZSBnmKuhKBwgrNv2sSSkNgkYzYsSCO5yO7pzTmn9pxf5uN2q1Qo3msJzxml2LcPlo/SD8P1FWQJ9gf3ukgnwUpgkyCPA4+R2iSMpKrBAkVXsAkAU4J451ObMRGD7DiuCeMWKMiTjEH0oxwxpUVEVuB2WAidnqAkcfFPFpKrlWsARo4JbsaYPhIRT6WayPJruFDtWUZfHSPRawBGnZD/gb+jvI45KGc0q+bkR2xmmI1YvXdWnaAU+S0faykvjnkFJRToH5BHAXqFObeRznqlUOvMuoVZuiDmoUkux1gP2uJr0X/He2dS/wMJrsaYPhY2iNwUYZqMAZ76mivXe/jYy31MMl6bPzZoJq133da16CelOpPkT+lOo0dYPgYX/POjzV/9A6DNEGm4UhaP1B+ceQ8ftl/7/T/tJwCrOWDn/279+WkYLNNe1Vd1BjeR5cf6r1p0y6rBe5m19WNtx42y5tmNV/XDN/U3YR9Y+HC5FP/P7P/wGfWb5Z4aif/qZWDd7Gc3AI=",
        },
        {
            "data": "m=edit&p=7VVdb9MwFH3vr5j87IfYju04b1sZvIzy0SE0RdGUbRmNaMlIW0Cp+t937NwtEY0AAQ9DQm6uT66P770nzm3Wn7dFU3KHoRIecYGhkihcSex/EY3zarMs0yN+vN0s6gaA81czflss1yWfZCLsFPlk17q0PebtizRjkvFwCZbz9k26a1+m7QVv51hiXOecrbbLTXVdL+uGBZ8A7wxIMC4BT3v4Pqx7NO2cIgKeAZtu2wVg0TT118vZ5Unnep1m7TlnPvlJ2O4hW9VfStbFCPfX9eqq8o6rYgOF60V1x7jCwnp7U3/cElXke94eBwm040GH+LEO1etQjzrUiA4S+uc6ltWn8qZqRkS4fL/HAb2FjMs084re9TDp4TzdsThmqeZMuzDZKExOh0lEEc3dqpCCZkWz5+29rh2sCPYCQfFWoRTFv1PIYoFAmT30KzvOj+0434hRvo4T+MWhX0Nlpg/9oc4RvlMjfIh7HiTKYM/xEHmrgn0WbBSsDvYscE7xMIRzXArJUokuERJYdTiKeixiLqXtsLTACfn1AIMjNHHgV+RHQ0vlyG8G2O81HdbIZSiXUcAx+cUAg6MFcZDLUj0W9VjKZfQAg2OoHou8CeVNoNdF/d5HbAYxUbOjXA41OHo+1g0wOPYhJmpzVL9D/Y5qTsQAg5NQTI06temxeagZMQ3F1Ibw3verP65psHGwJhyj9Z3yi7102Ai/98b8tJwsllwMhv37d/kkY/Ntc1tcl/jfOb35UB7N6mZVLHE3XxR33jutV3f1utqUDJ+D/YR9Y+FCX8r/X4h/4AvhDyt6au/2UysH3ZZP7gE=",
        },
        {
            "data": "m=edit&p=7VVdb9MwFH3vr5j87IfYTmwnb9sYvIzy0SE0RdGUbRmLaMlIW0Cp+t93bN/iwiJAIKEhoTa+xzf33uPj3DjLj+u6b7hI3F9ZDotfKqy/pNX+Suh31q7mTXHAD9er264H4PzFlN/U82XDJ6XwuaKabIa8GA758KwomWTcX4JVfHhVbIbnxXDOhxluMZ5VnC3W81V71c27nnmfQNwpkGBcAp5E+Nbfd+g4OEUCPAXWIe0csO777vPF9OIouF4W5XDGmSM/8ukOskX3qWGhhp9fdYvL1jku6xUULm/bO8YVbizX1937NYWKasuHQy+BMnY6xI91qKhDfdWhRnSQ0D/XMW8/NNdtPyIir7ZbPKDXkHFRlE7RmwhthLNiw9KMFRlnqQ7GeKNVMGkwIcSEmaFZSMhlMCEhDyEiEWQl2XBbiDxYmZClOEVztZtTXmrJUl7m4rZuHzcYhR/PnQgJ4lLx73YUOlAAPfvA7wqO+bUe9zvRI36TpON+J2DUP7YeiHjqpUg/nuHh8EH58YkfEz9mfjz1MScQLdOEyxQ7JvH2pQJYEpbAKmCZR5ymXGY24AwvfpYTRoxOAtaoqXc1zR7GIeGaw+MMWMearoV8HbNXH/EZxWeIz3TEmng1eA3xGvAa4jLQYmRc5w4b5BqqY8BriNco4DRiS7wW67G0HusOOuK14M13vDpii5qWalpXh2pa7KelPbRYQ051cruHwZUTV+5qmpibhzWrBKevCDVhgTPCGTDFCA1sKF7tYclVoggLYBlrJoJy1V59xAuKF4gXMmJJvBK8kngleCVxSQNs4zp3WCFXUR0FXkW86DGlkoip32CBaT3oE0V9AgtMvEoS3roz07X2sR9TP2rf8sadVr94nj08HH7v7frpckqoEN/8zN+dV5OSzdb9TX3V4Mtwcv2uOZh2/aKeYza7re+c97hb3HXLdtUwfLC3E/aF+Qsnpfz/Df8HvuHuYSWPrfMf23LwLlaTew==",
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

        start_point: List[Tuple[int, int]] = []
        end_point: List[Tuple[int, int]] = []

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            symbol_dir = dir_dict.get(symbol_name.split("__")[1])

            if symbol_name.startswith("arrow_N") and d == Direction.TOP:
                if symbol_dir == Direction.TOP:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.TOP}").')

                    if r == 0:
                        end_point.append((r - 1, c))

                    if r == puzzle.row:
                        start_point.append((r, c))

                if symbol_dir == Direction.BOTTOM:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.TOP}").')

                    if r == 0:
                        start_point.append((r - 1, c))

                    if r == puzzle.row:
                        end_point.append((r, c))

            if symbol_name.startswith("arrow_N") and d == Direction.LEFT:
                if symbol_dir == Direction.LEFT:
                    self.add_program_line(f':- not line_out({r}, {c}, "{Direction.LEFT}").')

                    if c == 0:
                        end_point.append((r, c - 1))

                    if c == puzzle.col:
                        start_point.append((r, c))

                if symbol_dir == Direction.RIGHT:
                    self.add_program_line(f':- not line_in({r}, {c}, "{Direction.LEFT}").')

                    if c == 0:
                        start_point.append((r, c - 1))

                    if c == puzzle.col:
                        end_point.append((r, c))

        fail_false(len(start_point) == 1, "There must be exactly one start point.")
        fail_false(len(end_point) == 1, "There must be exactly one end point.")
        self.add_program_line(f"path_start({start_point[0][0]}, {start_point[0][1]}).")
        self.add_program_line(f"grid({start_point[0][0]}, {start_point[0][1]}).")
        self.add_program_line(f"path_end({end_point[0][0]}, {end_point[0][1]}).")
        self.add_program_line(f"grid({end_point[0][0]}, {end_point[0][1]}).")

        for (r, c, d, label), draw in puzzle.line.items():
            if label == "normal" and not draw:
                self.add_program_line(f':- line_in({r}, {c}, "{d}").')
                self.add_program_line(f':- line_out({r}, {c}, "{d}").')

            if label in ["in", "out"] and draw:
                self.add_program_line(f':-{" not" * draw} line_{label}({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_in", size=3))
        self.add_program_line(display(item="line_out", size=3))

        return self.program
