"""The Pipe Link solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.route import crossing_route_connected, route_crossing, single_route
from noqx.rule.variety import straight_at_ice


class PipeLinkSolver(Solver):
    """The Pipe Link solver."""

    name = "Pipe Link"
    category = "route"
    aliases = ["pipelinkr", "pipelinkreturns"]
    examples = [
        {
            "data": "m=edit&p=7ZbrT+M4EMC/969Y+etaOtuxnYd0HwpL93avlLIL6tEIVaEECJsQLk1gL4j/fcePKkkf6Fhx1Z10SjP9dcYZz0xcjxd/VlERY0rUx/EwfMPFqadv5kl9E3udJGUaB+9wvypv8gIA46PBAF9F6SLGn89uhvt5//FD/48Hr5xO6UdSfSKT28Ht+y/Z758Sp6CDkTc+HB8m7Lr/2/7esTx4L8fV4rSMH44zund7Oj25Gk+uffbXwWjK6+kREZ+nV7889E9/7YU2hvPeU+0HdR/XH4MQMYT1TdE5ro+Dp/owqIe4/gomhCnohkACYQZ4AEgNTrRd0b5RUgI8sgx4BjhPinkaz4ZGMw7C+gQjNc+eflohyvKHGJnH9O95nl0kSnERlVCqxU1yby2L6jL/Vtmx4BBlVVom8zzNC6VUumdc97en4DQpKDQpKNqQgsrsH07B35zCM7yeL5DELAhVPqcNeg1+DZ5AjrSkWp5pOdCSaXkCQ3HtaPlBS6Kl0HIYPCFHYMkcFDCskDNXI/c7yOkSpSMbtAMkoPGgkWsUFNBfIudmgJSAZgCgFFbLsORmrEJBNLocS8mWyKWZ2HOxdI0HjWKJXDboGmeUEGCvYd+4o8zHLjX+DJtMFAvSYmbyppxj12mz9QMsWIttcagk2OXWD7BwbAxQnza7tlaUujCvjRnYJSYVSiBv3/oEljZ+HwoqzXBAabN1PaiXeRCQC/OcDy/VNWVW6NmoCAz2l7MoXs4CT3oNC2LeBWUwpW8jBHaJzcJxsMvsGM3LKkFV7fpQLPQKggV5oJflRMt9LbmWUi9IV63s3a19zqD+vvc3wwods613L/Hf0533QjRM7uJ3o7zIohRBM0CLPJ0tquIqmsez+Hs0L1Fg+lHb0tHdVdlFDFtWS5Xm+X0Kjjd4WJo6yuT6Li/ijSaljC+vt7lSpg2uLvLiciWmxyhNu7noXt1RmQ2+oyoL2L1bv6OiyB87miwqbzqK1k7f8RTfrRSzjLohRt+ildmyphzPPfQd6Tt01Jni/879L+/c6lWRne1hb7OlhlBx2AxxfYTRfTWLZpAUglMifnODeLVhF1E5rzTAIeeVhjcMF8FJg8Mf4meMcAKQuzeq4+FLVtjBtibz89aXPW+Jaud/TL3f58ULzbcxrqo3tGDQvtCFW9ZN+i0Nt2Vd1a91VxXseoMF7YYeC9rVNguq9U4LyrVmC7ot/VZ5XW25KqrVrqumWmu8aqp27w3Pez8A",
        },
        {
            "data": "m=edit&p=7Zbfb6NGEMff/Vec9vVWKgvL8kPqg5OLr3d1fE7iyI1RFBGHxOQgpBicK1b+95vZhRrw+tRWqpRKlc364+8OszOz68Hr38swjygz8G25FD7hxZkrL9MV8jLq1ywuksh/R4dlscpyAEq/jEb0PkzWEf18tRofZ8OXD8PfNm6xWLCPRvnJmD+OHt+fp79+iq2cjSbu9HR6GpsPw1+Oj87EyXsxLdeXRbQ5S9nR4+Vidj+dP3jmHyeTBa8WXwz78+L+p83w8udBUMdwPdhWnl8NafXRD4hJqLwYuabVmb+tTv1qTKsLmCKUgTYGsgk1AU8AmcK5nEc6ViIzgCc1A14BLuN8mUQ3Y6VM/aCaUYLrHMm7EUmabSKibpPfl1l6G6NwGxZQqvUqfq5n1uVd9rWsbcEhScukiJdZkuUoovZKq+HhFKxdCogqBSRNCpjZv5yCp0/hFbbnHJK48QPM53KH7g4v/C2MEzkyOV75W+Jw8MIggHbQxLG1qqtVPZ3qOjrVY1pVGwMztMbMOGCtDY4xoZe14THT0MuaSKB+I1lFU44zKDKtLDl+kKMhR1uOY6g0t6mwLOKbFJFbEAGiAypk1CAUHlAwKjgkpJDb6jbHAoRQFAqhkBkmFS5sQsMeJIFsMeow5URxbQNsGy02lXfGLeDaJ7BjNSyAGxtkFS7jLrCKF9k2odTSJ9g0PiXX9oYHsdU2wDbur2TIG4/An1z7BOZui70mRwE2tX/Jzb0C7Fvsqdw9k3JHlQSxtnCxrMohoqP82VA+S6mAnCtbG3bDUs4k1gZwm7lDrjwI2COuEgMUNi4Mx+NEHpK5HI/lyOUo5PFw8Bf6j3/Df/ck/sVwAks9lrov+7+nXQ8CMo6foneTLE/DBPrqxSp8jgg81Mg6S27WZX4fLqOb6Fu4LIivnqvtmY72VKa3EbTelpRk2XMCC2g8NFMdMX54yvJIO4VidPdwyBVOaVzdZvldL6aXMEm6ucj/HB1JtbOOVOTwFGp9D/M8e+koaVisOkLridXxFD31ilmE3RDDr2FvtXRXjtcB+UbkFVjUxE38/x/Im/4HgltlvLUe9tbCkac8y3/QcnaTfVnTeED9Qe9pzer0A22mNdvX93oKBrvfVkDVdBZQ+80FpP3+AuJeiwHtQJdBr/1Gg1H1ew0utdducKl2xwmuB98B",
            "config": {"pipelinkr": True},
        },
    ]
    parameters = {
        "pipelinkr": {"name": "Pipelink Returns", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", crossing=True))
        self.add_program_line(crossing_route_connected(color="grid"))

        if puzzle.param["pipelinkr"]:
            for (r, c, d, label), symbol_name in puzzle.symbol.items():
                validate_direction(r, c, d)
                validate_type(label, "normal")
                validate_type(symbol_name, "circle_L__1")
                self.add_program_line(f"ice({r}, {c}).")

            self.add_program_line(shade_c(color="crossing", _from="ice"))
            self.add_program_line(straight_at_ice(color="grid"))
        else:
            self.add_program_line(route_crossing(color="grid"))

        crossing_points = set()
        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")

            if not draw:
                self.add_program_line(f':- line_io({r}, {c}, "{d}").')

            else:
                cnt = 0
                for d in (Direction.TOP, Direction.LEFT, Direction.BOTTOM, Direction.RIGHT):
                    if puzzle.line.get(Point(r, c, d)) is True:
                        self.add_program_line(f'line_io({r}, {c}, "{d}").')
                        cnt += 1
                    else:
                        self.add_program_line(f'not line_io({r}, {c}, "{d}").')

                if cnt == 4 and (r, c) not in crossing_points and puzzle.param["pipelinkr"]:
                    self.add_program_line(f"crossing({r}, {c}).")
                    crossing_points.add((r, c))

        self.add_program_line(display(item="line_io", size=3))

        return self.program
