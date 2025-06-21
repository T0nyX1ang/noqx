"""The Coral solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Puzzle
from noqx.rule.common import display, grid, shade_c
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import border_color_connected, grid_color_connected
from noqx.rule.shape import avoid_rect


def len_segment(color: str = "black") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = f"nth_horizontal(R, C, 1) :- {color}(R, C), not {color}(R, C - 1).\n"
    rule += f"nth_horizontal(R, C, N) :- {color}(R, C), nth_horizontal(R, C - 1, N - 1).\n"
    rule += f"nth_vertical(R, C, 1) :- {color}(R, C), not {color}(R - 1, C).\n"
    rule += f"nth_vertical(R, C, N) :- {color}(R, C), nth_vertical(R - 1, C, N - 1).\n"

    rule += f"len_horizontal(R, C, N) :- nth_horizontal(R, C, 1), nth_horizontal(R, C + N - 1, N), not {color}(R, C + N).\n"
    rule += f"len_vertical(R, C, N) :- nth_vertical(R, C, 1), nth_vertical(R + N - 1, C, N), not {color}(R + N, C).\n"

    return rule.strip()


class CoralSolver(Solver):
    """The Coral solver."""

    name = "Coral"
    category = "shade"
    examples = [
        {
            "data": "m=edit&p=7VZdb+M2EHz3rwj4vA+kRMqS3tL00pfU19YpgoNhGI7r9Izap9SOi0KG/3tmlnRktQGuRYAABQrD3Bl9cGd2KUq73/fz7VJcEJdLXooVh19hSwl5Jq4Aw9+m3+3qab2sL+Ry//S52QKIfLy+lof5erccTHJcEcROB4e2qttLab+rJ8YZMRn+zkyl/bE+tN/X7UjaMU4Z8Th2Ey/KAD908E7PE13Fg84CjxIG/AS4WG0X6+XsJh75oZ60t2KY5xu9m9Bsmj+WJukgXzSb+xUP3M+fYGb3efWYzuz2vzS/7dO1bnqU9jLKHb8iN+/kEka5RK/IpYu3y10/Nq8JrabHIwr+E6TO6glV/9zBsoPj+oBxVB+Mr3Aru6w9MSHr0cL3aQDFQjjRok/LHh060PyFlnlvqpIzdxeX/ZnLYe/eyvYpZ/Yd5cXdzBVlnNG+QWc51znnZF1mV/Utu4rKzjlNd1oyrVgnJgv0ecaH/XyZluWcn9+PpjhtzScdr3XMdLxF56TNdfxWR6tj0PFGr/mAhua+lLxASTIxiHiMIZi4LMRbmAFGFJ/BKHHmxXuIJva5+AKCiItMfAmxxKWTwMIBI0pwKCqxq7AzoN7E2C9CiHkRJQxjXkQJLCI1BGwrNIztxQBIzlYqqZx4hwwkAJCHFEqyCvqQQwnMeZpTAnee7pTAXqA9EgAJ9KcEBgMNKoHDQIdKYDHQohJ4LOhR5QQUcZiKOEQR2XXiCkV0qYjYJn2eipijiOw8MUx6miSGR0+PxLAYaFELhyLSITEMBhokhr+QmocIdamIcFe8NA/V4apVjLLZlMsil00aLDTYpM1C23njbZwTETjmQgSOGhCBozbE2Bb1i7wu5XVsV8rrkNelvCiedymvQ95TrSrkZQ21VSwiH9pIkJmPbCRIzQc2EtTl1BBddTQdCZfjqYmwHWg7ErSXviNB43tLgs4j4WJJCgBAkgIAkKQAIHZMSQUFqZWIwNE+InC0jwgc7SO+rHtE4NRKuA90rxipaV4xMtO74iquRWBE4JgXETjmRQSOeRGBY17EtFSwIdzptnClo9ex0O1iyNfAP3xRYItERo/9KaOK+N54+0b1VXUT5NXvj7/84kfJf/LgdDAx4/32Yb5Y4u092m/ul9uLUbPdzNcGH0rHgfnT6F9fMP7/b6d3/3Zi8e2/+oJ6hyfhK3ImqCuflfajmMf9bD5bNGuDL2/RE5n724l314+H2XxpvjS/bucbMx08Aw==",
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        top_clues = {}
        for c in range(puzzle.col):
            top_clues[c] = tuple(
                clue
                for (r1, c1, d1, pos1), clue in puzzle.text.items()
                if r1 <= -1 and c1 == c and d1 == Direction.CENTER and pos1 == "normal"
            )

        left_clues = {}
        for r in range(puzzle.row):
            left_clues[r] = tuple(
                clue
                for (r1, c1, d1, pos1), clue in puzzle.text.items()
                if r1 == r and c1 <= -1 and d1 == Direction.CENTER and pos1 == "normal"
            )

        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="black"))
        self.add_program_line(adjacent())
        self.add_program_line(grid_color_connected(color="black"))
        self.add_program_line(border_color_connected(rows=puzzle.row, cols=puzzle.col, color="not black"))
        self.add_program_line(avoid_rect(2, 2, color="black"))
        self.add_program_line(len_segment(color="black"))

        for r, clue in left_clues.items():
            if clue:
                count_dict = {}  # Replace collections.Counter with manual counting
                for num in clue:
                    count_dict[num] = count_dict.get(num, 0) + 1

                for num, count in count_dict.items():
                    self.add_program_line(f":- #count{{ C: grid({r}, C), len_horizontal({r}, C, {num}) }} != {count}.")

                forbidden_len = ",".join([f"N != {x}" for x in count_dict])
                self.add_program_line(f":- grid({r}, C), len_horizontal({r}, C, N), {forbidden_len}.")

        for c, clue in top_clues.items():
            if clue:
                count_dict = {}  # Replace collections.Counter with manual counting
                for num in clue:
                    count_dict[num] = count_dict.get(num, 0) + 1

                for num, count in count_dict.items():
                    self.add_program_line(f":- #count{{ R: grid(R, {c}), len_vertical(R, {c}, {num}) }} != {count}.")

                forbidden_len = ",".join([f"N != {x}" for x in count_dict])
                self.add_program_line(f":- grid(R, {c}), len_vertical(R, {c}, N), {forbidden_len}.")

        for (r, c, _, _), color in puzzle.surface.items():
            if color in Color.DARK:
                self.add_program_line(f"black({r}, {c}).")
            else:
                self.add_program_line(f"not black({r}, {c}).")

        self.add_program_line(display())

        return self.program
