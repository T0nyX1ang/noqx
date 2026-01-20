"""The Anglers solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Puzzle
from noqx.rule.common import defined, display, fill_line, grid
from noqx.rule.helper import fail_false, tag_encode, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import avoid_unknown_src, count_reachable_src, grid_src_color_connected
from noqx.rule.route import single_route


class AnglersSolver(Solver):
    """The Anglers solver."""

    name = "Anglers"
    category = "route"
    aliases = ["anglerfish"]
    examples = [
        {
            "data": "m=edit&p=7ZVvb6JKFMbf+ymaedtJCiIKJM3Gv00aa+tqr9cSY0YdCy2K5U/bYPrde86gAQS7vc3dZl9sCJNnfgfmnDkjj/5TyDxONbgUjUpUhkuplMVdlnRxS7traAcON05oPQws1wNB6XWnQ5fM8Tm9HD80Wo/1l3b93zP1TlFue8vTh1b/9mEx+kfuS/aZJ/UcbX1102o4pxfR3ZVVf+ZtXr3x3bnlcLZg0d3o8tVZd7R7ayk3L62mtmRryX/Shvpzo39+XjKxOLgmpW2kG1GdRheGScqEilsmExr1jW10ZURjGg0gRGgFWBeUTGgZZDuRIxFH1YyhLIHu7TTIMciArwM/nt4YZjSkBJM0xKsoycp95iR+R8zn7mpmI9i9KaAfLtzHcPcYrEVWoRPYc9dxPYTI3mhUj0vv7kvHpFh6hVAlKR1lXDqqgtJxR1j63PbmDp92v1T9jAVw1L5lb4q2oBdv4Q2O5SdsYmqYuJ/bRGqJHBhbolaIUQHdQy3v+xKfIKlCUBzqHtRqCJQE6BICaMseyJKCRE0RuYrkx55AMtnYwjiGlIoOMYWmDpeouEAWVfOopuaRlkMa1ptGkLYjkpfFOIRG0EgRY0uMkhhVMXbFM20xjsTYFGNFjFXxTA1b+clmx21O7/+/lkOUMuxI1yipaNATIXToBApVptgn5ZMlm4oef8Hiqn1dT0omGYTeks05/EC79pqf9FxvxRyY9cLVjHvJfGCxDSfgGcR3nakfvzXlr2weECP2rnQkw9ZirQxyXHfjQMKCFfahDLTv167HC0MI+eL+2FIYKlhq5nqLg5pemONk9yJcPYNiP8igwIOPPTVnnue+ZMiKBVYGpIwhsxL81rMFBCxbIntkB9lWSTveSuSViBs+HBlM+6/B/5kGj0ckfZvz/D9GaELHwfMp/NPQ6JqSTThlU9gYodDUXwdji/tK8PfkBDcuDoA7Hwnoai7w7WckPnnX+8B/k+AhLnBhoB8YcSpaxI94bip6yHMGi8XmPRZogc0CPXRaQHmzBZjzW2BHLBdXPXRdrOrQeDFVznsxVdp+zUnpHQ==",
        },
        {
            "data": "m=edit&p=7ZV/a+IwGMf/91WM/LvAmlZnLYzDn4PhvHm685yIRI1rt2i2tm6jsve+J6nDJu0Gd3Cwg6P24ennaZ5809hvo8ctDRkmtvw5LrYwgaNcK6vTqVbUae2PYRBz5h3h+jb2RQgJxt87HbyiPGL4YnzXaN3Xn9v1XyeVG8e57q2O71r967vl6CfpW8FJaPW4u7m8ajX48Xlyc+nXn1ibnV5FYuFzRpc0uRldvPBNx731V6R54TfdFd1Y0aM7rD01+mdnpYkUB8e0tEtqXlLHybk3QTbC6iRoipO+t0suvWSMkwGUEC4D60JGELYhbR/SkarLrJlCYkHe2+eQjiGN2SaO0ssrb5IMMZKTNNRQmaK1eGIoHaOuF2I9DyTYj1Qw2i7F/XZ/G/RC6y2Pg4XgIpRQslec1FPp3XfpctK9dOcgXaapdJkVSJcrktIXQbjgbNb9I/VzGsNWR37wULSEWvESXmFbfsAiZt5Eruf6kLqHdODtIPa8HXJcOfIbDE33DpVtA7gmIHbFJOVTk1TNvsStGcQm+ihQRJSuMeiqlKHm4Mzeo4psqSPXyaEaySFi55uRmpxcZ7ZlFTBzChDYUTJtFYfwRHHiqNhS0VKxomJX3dNWcaRiU8Wyiqfqnqrck9/ateyT+ktyJpX9a64d1X+PTUsTNNiGK7pg8BZ1gw076olwTTlc9bbrOQsP1wOfPjAExoYiwWdROmrGXugiRl5qsNmKxjaql4a4EA8cJizo8F7SYHC7ESErLEnIlrcftZKlglZzES4NTc+Uc30t6uOjodS0NBSH4EiZaxqG4lkjaxr7Gsi4l9YJ3iNdQEx1ifSeGrOtD4/jtYRekDrhpYSP5P+v0Bf9Csktsr6aq301OerfLcJPrOZQNHGB4QD9xHMy1SL+gb1kqibPeYkUm7cToAWOAtQ0FUB5XwGYsxZgH7iL7GoajFRleoycKmczcqqs00ympTc=",
        },
        {
            "data": "m=edit&p=7ZVtT+pKEMff8ynMvnUT+wACTXzBo4lBrlzwcrAhZIHFVhdWt62aEr+7M1tMH6gm9yQ38SQ3pZPZ33RnZrv0v8FzxBSnpoU/u0ENasJVbVb1bddr+jYO18QPBXdOaCsKPanAofSvfp9umAg4vZo9tLuPrdde69dZ7c62b4eb04fu6PZhPf3HHBn+mTKGorG7vum2xellfHfttV54j5/fBHLlCc7WLL6bXr2JXb9x723MzpXXaWzYzgieG5PmS3t0cVFxsTm45pV93HTiFo0vHZdYhOrbJHMaj5x9fO3EMxqPIURoFdgAPJNQC9xe6k51HL1OAk0D/OHBB3cGbsh3YZAMbxw3nlCCRdp6KrpkK184Sebo8Upulz6Cw0wNg2gtH6PDY5CLbCMR+isppEKI7J3GraT1wWfrWPTQup22jm7SOnolreOKsPWVr1aCLwa/1f2ShbDVgec/lS2hWb6Ed9iWv2ERC8fF9dymbiN1x84e7NDZE7uJMy0D5iabR6pWkZi2cYSq50VkmXYeQQVT15lBnQbWsWlmL4lpYI4CszFJgdWwfIHViwzq9HU1S9sJLJTGtrZdbQ1ta9oO9DM9bafadrStanuun6njq/pXLzO74P+oHbd2+PpyV/3PY/OKS8aR2rAVhz/3wN/xk6FUWyZgNIy2S67S8dhjT5yA3pBAikWQzFrwN7YKiZPoXjaSYzudK4eElE8CCpZk+AzloH+/k4qXhhDy9f1XqTBUkmop1brQ0ysTIr8WfSbkUKIlORQqEIrMmCklX3Nky0IvBzKikssE31G+gZDlW2SPrFBtm76O9wp5I/qGjxLOrv8Phx96OOAWGT9N1X5aO/rfLdU3UpMGi7hEcIB+ozmZaBn/Ql4y0SI/0hJs9lhOgJYoCtCiqAA61hWAR9IC7At1waxFgcGuihqDpY5kBktllcadVz4A",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(len(puzzle.symbol) > 0, "No clues found.")
        fail_false(len(puzzle.text) == len(puzzle.symbol), "Unmatched clues.")
        self.add_program_line(defined(item="hole"))
        self.add_program_line(grid(puzzle.row, puzzle.col, with_holes=True))
        self.add_program_line(fill_line(color="grid"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(single_route(color="grid", path=True))
        self.add_program_line(avoid_unknown_src(color="grid", adj_type="line"))

        for (r, c, _, _), color in puzzle.surface.items():
            fail_false(color in Color.DARK, f"Invalid color at ({r}, {c}).")
            self.add_program_line(f"hole({r}, {c}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            validate_direction(r, c, d)
            validate_type(symbol_name, "tents__3")
            self.add_program_line(f"dead_end({r}, {c}).")

        tag = tag_encode("reachable", "grid", "src", "adj", "line", "grid")
        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            if not (0 <= r < puzzle.row and 0 <= c < puzzle.col):  # coordinations out of bounds
                self.add_program_line(f"grid({r}, {c}).")

            self.add_program_line(f"dead_end({r}, {c}).")
            self.add_program_line(grid_src_color_connected((r, c), color="grid", adj_type="line"))

            if isinstance(num, int):
                self.add_program_line(count_reachable_src(num + 1, (r, c), color="grid", adj_type="line"))

            for (r1, c1, _, _), _ in puzzle.text.items():
                if (r1, c1) != (r, c):
                    self.add_program_line(f":- {tag}({r}, {c}, {r1}, {c1}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
