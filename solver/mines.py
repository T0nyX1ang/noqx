"""The Minesweeper solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import count, display, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent


class MinesSolver(Solver):
    """The Minesweeper solver."""

    name = "Minesweeper"
    category = "var"
    aliases = ["minesweeper"]
    examples = [
        {
            "data": "m=edit&p=7VRLb5tAEL7zK6I972EfmNfNTeNeXOdhV5GFEMIulVHBOGCiaC3+e2YHCtnKhzZSnUu12k/zzQzMt7OP+qlJqpR6MKRHGeUwpC1wCubjZP1YZcc8Da7otDnuygoMSm9nM/ojyevUCvusyDopP1BTqr4EIeGEEgGTk4iq++CkvgZqQdUSQoRy8M27JAHmzWg+Ylxb152TM7AXvQ3mGsxtVm3zNJ53nrsgVCtKdJ1P+LU2SVE+p6TXofm2LDaZdmySIyym3mWHPlI338ufDflVoqVq2sldn5ErR7lykCvPyxW93LrZx0VZ7t8lt8j2aX1OqR+1LXT8AbTGQahlfxtNbzSXwanVkk5EuPCp3mjcFCI9oHygNjOpMJJt26COMJId26Tmn11d1x6pjk4G6um6YqC+MKk06vqeGfWByoFyxoxKnInfuKmTc278nXP5Jg5d49i7NeIMUSCuoLVUScTPiAxxgjjHnBvER8RrRBvRwRxXb85fbd9bOcT1cWHG0fpHGkPh4NswjslleWSFZNEUm7S6WpRVkeRwG5a75JASeHFai7wQnHgO7P+P0OUfId199u6z/DFXK4TGOpKqW0oOTZzE2zLHzpz1s87v+n/sv/hq4Z5G1is=",
            "config": {"mine_count": 10},
        },
        {
            "data": "m=edit&p=7VZNj9owEL3zK1Y+++CxHcfOjW6XXij9gNUKRQgBTQUqIVsgVRXEf68zYQlj0UN7WHFYBY/mecaeNzOOye5nOdtmHKL6pywXHPxjhMUBVuB4eUar/TpL7ni33C+LrVc4/9Tr8e+z9S7rpCevSedQuaTq8upDkjJgnEk/gE149SU5VB+TasCroTcxDn6u3zhJrz606hPaa+2+mQTh9cFJ9+rYq4vVdrHOpv1m5nOSViPO6jjvcHWtsrz4lbETjxoviny+qifms71PZrdcPZ8su/Jb8aNkLyGOvOo2dMdX6KqWrjrTVdfpyhPdXbmZ5kWx+S+6+WqT7a4xdZPj0Vf8q+c6TdKa9mOr2lYdJodjTenAtPRLfcObpjBtPFQttB7CGUbCQ9lCRdZGzkN9hoZajaHWmMC43tm00BIaVhJnq4jVUauzJC4IIGYQmqwGYQJMYwMIuh/EFEsdYFoGUBHdTwX8NC0M6Jj6R8H6iFYODC0dYN3jCxzkZyxpIsQ6wIF/HORjdYADvtgOcYE1OUPggnxdUG/nCB8Z9E8KemIl0PhSAYknlaL7YT8u1gf9kBpI/aSm9ZQRUP+I5iMNzUfGKsAmwLSfMqi3tCLAgb8Dup8L4jkd+Afxsd5tPkrQ86QE7YeCy/fH3yKAd8kYZQ+lRDnyVw2vFMr3KAXKCGUffR5QPqG8R6lRGvSJ68vqn66zV6CT6uZv8W9P9Ga9deukk7JBmc+z7d2g2Oaztf8rHS5nzxnznyvHDvvNcOAh129fMK//BVNXX9zai39rdPxVNOn8AQ==",
        },
    ]
    parameters = {"mine_count": {"name": "Mines", "type": "number", "default": ""}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="sun_moon__4"))
        self.add_program_line(adjacent(_type=8))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            self.add_program_line(f"not sun_moon__4({r}, {c}).")
            self.add_program_line(count_adjacent(int(num), (r, c), color="sun_moon__4", adj_type=8))

        mine_count = puzzle.param["mine_count"]
        if mine_count:
            fail_false(isinstance(mine_count, str) and mine_count.isdigit(), "Please provide a valid mine count.")
            self.add_program_line(count(int(mine_count), color="sun_moon__4", _type="grid"))

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "sun_moon__4")
            self.add_program_line(f"sun_moon__4({r}, {c}).")

        self.add_program_line(display(item="sun_moon__4"))

        return self.program
