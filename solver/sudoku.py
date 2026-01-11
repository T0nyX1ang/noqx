"""The Sudoku solver."""

from typing import Dict, Tuple, Union

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent, avoid_same_number_adjacent


def generate_killer_cage_rule(puzzle: Puzzle) -> str:
    """Generate killer cage rules from the given puzzle."""

    # Killer cages definition (only supported in Penpa+). The format is not standardized yet.
    cages: Dict[Tuple[Tuple[int, int], ...], Union[int, str]] = {}
    for cage in puzzle.problem["killercages"]:
        cage_cells = tuple(puzzle.index_to_coord(coord)[0] for coord in cage)
        for r, c in cage_cells:
            if puzzle.text.get(Point(r, c, label=f"corner_{Direction.TOP_LEFT}")):
                clue = puzzle.text[Point(r, c, label=f"corner_{Direction.TOP_LEFT}")]
                fail_false(cage_cells not in cages or cages[cage_cells] == clue, "Conflicting killer cage clues found.")
                cages[cage_cells] = clue

    rule = ""
    for _id, (cage_cells, clue) in enumerate(cages.items()):
        rule += "\n".join(f"cage_num({_id}, {r}, {c})." for r, c in cage_cells) + "\n"
        rule += f":- #sum {{ N, R, C: cage_num({_id}, R, C), number(R, C, N) }} != {clue}.\n"

    return rule.strip()


def generate_arrow_rule(puzzle: Puzzle) -> str:
    """Generate arrow rules from the given puzzle."""

    # Arrows definition (only supported in Penpa+). The format is not standardized yet.
    arrows: Dict[Tuple[Tuple[int, int], ...], Tuple[int, int]] = {}
    for arrow in puzzle.problem["arrows"]:
        arrow_cells = tuple(puzzle.index_to_coord(coord)[0] for coord in arrow)
        arrows[arrow_cells[1:]] = arrow_cells[0]

    rule = ""
    for _id, (arrow_cells, (r0, c0)) in enumerate(arrows.items()):
        rule += "\n".join(f"arrow_num({_id}, {r}, {c})." for r, c in arrow_cells) + "\n"
        rule += f":- number({r0}, {c0}, N0), #sum {{ N, R, C: arrow_num({_id}, R, C), number(R, C, N) }} != N0.\n"

    return rule.strip()


class SudokuSolver(Solver):
    """The Sudoku solver."""

    name = "Sudoku"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VVLi9s8FN3nVwxaayFd2fJjl04n3aTpIynDYMKQSVMmNCElj4/ikP8+514rkV0+GEopZFEc35xrSefch2TvDl833w+6wOVybbTF5XIjd57wz4RrstyvFuWN7h/2z5stgNYfBgP9bbbaLXpVmDXtHeuirPu6fldWyiqtCLdVU11/Ko/1+1I1gkrXY0xQ2mJk2EwlwLsI72Wc0W3z0BrgUcCAD4Dz5Xa+WjwOmycfy6qeaMVqb2Q1Q7Xe/LdQIRr255v105IfPM32SGn3vPwRRkJsZ4mTrvuvBe1i0AyboBn9T9Ccy18OmqanE1rwGWE/lhVn8CXCPMJxeYQdlUflHJZy16VLyiVw3cVNPFyKbgY3u7gpT06im3ZHea2PbtFh9gZuEV1mzqObd3Q9r00vbsFunGwNc8U4rLGdnKzpslnD66O2tdSht5ZrEkO1lvNs6dEv/MTrW+NSxBa/48KcK4G6W6n+g9iBWBI7QXN07cS+FWvEpmKHMucOPbM5yLgIBMai0MQJAONfE0GMMaWaHBJnjKNNKYJmnFpNHgEy9ommDJVnnGWaChSScYEXgEERmD8Hvwn8Bvw28FvwU+An8CeBPwE/bwzRAj93VrTAnwd+vFyoaPjxDy1sFeHh+MNzcsCBh8DTzovO8z1w4Cfwt+Ohpj74Rx2CroOuC3F6rkPIy0PXB10P3XZ9fND10PVB10O3nRdvV8HQ5b0qGLoZ66Jp99K6W7GJWC8tzfg0/tZ5/fPd82o4FarHm7t98eG4oifTXqXG8t67GW2269lK4cNz6qmfSm45u8m/b9EVfIu4Hebadvi1hYMzp+ar2W63nKtp7wU=",
        },
        {
            "data": "m=edit&p=7VVda9swFH3Pryh61oN0Zcsfb1nX7CXLPpJRigklzVIalpCRjzEc8t977rUa2WNQxhjkYTi+OVeWzrkfkr07fN18O+gCl8u10RaXy43cecI/E67Jcr9alFe6f9g/bbYAWn8YDPTjbLVb9Kowa9o71kVZ93X9rqyUVVoRbqumuv5UHuv3pWoEla7HmKC0xZNhM5UAbyK8leeMrptBa4BHAQPeAc6X2/lqcT9sRj6WVT3RitXeyGqGar35sVAhGvbnm/XDkgceZnuktHtafg9PQmwvEidd918L2sWgGTZBM/pN0JzLPw6apqcTWvAZYd+XFWfwJcI8wnF5hB2VR+UslnLXpUvKpXD92U34KUWX4BbRzeAm0c3hZmc3ZSoX3aJD5dmNkzPT0c14bXp2C9d1WSiPbpfKml98211tibXaPicZs7LkOyWxxGlGOeuYr+3z85f1KKuV4t6JHYglsRPUXtdO7FuxRmwqdihzbtASm6MQnBSBsSg0WZQdGP+aCJVhTKkmhzowxsmlFEkwTq0mnzTYJ5oyBMc4yzQVSJxxgfNtkATz5+A3gd+A3wZ+C34K/AR+3gmME/CngT8Fvw/8Hvx54Me7g7hlouWghYIKD8cfxskBBx4CTzsvboBgDxz4CfzteKipD/5Rh6DroMv7WeLhOoS8PHR90PXQbdfHB10PXR90PXTbefmg66HL+1YwdHnTEpp2K627FpuI9dLSjA/bHx3Hv989r4ZToXq8udsXH4YLGpn2KjWW19rVaLNdz1YK35VTT/1UcstLJfn/qbmATw23w1zaDr+0cHDm1Hw12+2WczXtPQM=",
            "config": {"diagonal": True},
        },
        {
            "data": "m=edit&p=7VRNa9tAEL37V4Q972F3Vlp93Nw07sV1P5ISgjDBcV1iauNiO6XI+L/nzewYKVAIpRR8KLJGb1bj997sh3ZPXzffn2yFK5TWWY8rlE7uMuOf0+tmuV8t6gs7fNo/brYA1n4Yjey32Wq3GDRaNR0c2qpuh7Z9VzfGG2sItzdT236qD+372iRBY9trFBjr8WacSgnwqoO38p7RZRr0DniiGPAOcL7czleL+3Ea+Vg37Y01rPZG/s3QrDc/F0bdcD7frB+WPPAw26Ol3ePyh75RbyeJo22Hr5kOnWmGyTSj35jmXv6xaZoej1iCz7B9XzfcwZcOlh28rg+Ik/pggsdfCasuq2RCjpQ3QUqzgDR0afGiOOfirEurF8XecR673DNZ3uXE0kUvZ7pefeD6spez+qke9r00cSdxJJEk3qBH2waJbyU6ibnEsdRcoXVfQqyCSQJjVVnyJBhPS2yGMeWWQpkwTgjlMM0495ZilnDMLBUwx7goLFUu4QrnyKEJ5i/B75Tfgd8rvwc/KT+BP1P+DPy58ufgj8ofwV8qP84oVYkfT2hF5WH/Ok4BWHkIPP2+6FQfgZWfwN/3Q2l+8MQ8qG6ALu8b8cPzoH1F6EbVjdDtz09U3QjdqLoRuv2+oupG6EbVjdAtWBeLditLdykxkxhlSQve1H+07f9+97xqp8Hs8UHqX7z5z2hkOmjMtXw+Liab7Xq2Mvh+Hwfml5FbznL2/5N+Bp90Xg53bjv83OzgzJn5arbbLedmOngG",
            "config": {"untouch": True, "antiknight": True},
        },
        {
            "data": "m=edit&p=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",
        },
        {
            "data": "m=edit&p=7VZdT9tIFH3Pr6j82iutZ2yPx5b2IVDSbQtpKCCWWBEywYCpg1nHga4R/71nPqLYSWC7DyvxsHIyPjnXc+7HeO5kvrgsvy8owuVJconh8qSrv9JXH9dex3ldZPE76i/qm7ICIPo6GNBVWswz+nx2s79b9h8/9P98kPV4zD66i0/u6e3g9v232ZdPuVexwVCODkYHOb/u/7G7cyj23ovRYn5SZw+HM7ZzezI+vhqdXkf8773h2G/GX93g8/jqt4f+ye+9xMYw6T01Udz0qfkYJw5zyOH4MmdCzWH81BzEzYiaI5gcYhNyZouizqdlUVbOkmv2zUQOuLeCp9qu0K4hmQs8tBjwDHCaV9MiO983zChOGo8c5XtHz1bQmZUPmXKmYlO/p+XsIlfERVqjfPOb/N4hDwZTd/somzxT0zcZDH8xA4gsM1DQZKDQlgxUYv9tBtHk+RmL8w05nMeJSudkBeUKHsVPGIfxkxOIZfJmBZ1AKgILuiSEqwhvRUiuCNkitIa/IpirRcIWw7SKaDNaJlgyiIfpqM70ONAj1+MxgqbGi5ME+yBkFMgJachJoLwKyoCkMDCSBG2LQ2D7SCSwGHam9EjaR0KXAjXT88kXRtoPKYhwZ8zHFGxAZWfMo0izHJvT1QhzGOfWReCTkEY2CEhEE8T8QUfu6jHQ477OaA+VZxIBRZETc+QfRcRVQYBxJ84Dg3lA3EMxFUZj4AEzOGDEhW+w8ImHocFhSDxCqRWO0D5cz+hL6LtW34U+s/oM+tzqc+j7Vt+HfmD1kRgXVl9AX1p9tCYeGX3c4QuvgdZR8Vuee8BWh0OnnRdfPi+ArT6HfjsebuqDO+pg/Xrw69k4haqDzUvAr7B+Bfy26yOsXwG/wvoV8NvOS1i/WEUurF8Bv6Hyi0U71Uu3q0dfj0Ivaaj21L/adb/yrr/+9vxjOAmqpw6R9hW8LWbSS5zhYnaRVe+GZTVLC7S6o/tsmgPhiHHmZXE+X1RX6TQ7z36k09qJzSnXtnS4O63WoYqyvC/yu20KS1OHzK/vyirbalJkdnn9kpQybZG6KKvLtZge06Lo5vLXIq26k80Z0aHqCgdA63daVeVjh5ml9U2HaB0WHaXsbq2YddoNMf2ernmbrcrx3HN+OPqbYJuphfz//8Ab/j+gFsp9a/3prYWj3/GyeqXhrIzr9Ja2A/aVztOybuNfaDIt6zq/0VFUsJtNBeyWvgJ2vbWA2uwuIDcaDLgXeoxSXW8zKqr1TqNcbTQb5ardb5JJ7yc=",
        },
    ]
    parameters = {
        "diagonal": {"name": "Diagonal", "type": "checkbox", "default": False},
        "untouch": {"name": "Untouch", "type": "checkbox", "default": False},
        "antiknight": {"name": "Antiknight", "type": "checkbox", "default": False},
    }

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        fail_false(puzzle.row == puzzle.col, "This puzzle must be square.")

        n = puzzle.row
        sep = {9: (3, 3), 8: (2, 4), 6: (2, 3), 4: (2, 2)}
        fail_false(n in sep, "Invalid sudoku board size.")

        self.add_program_line(grid(n, n))
        self.add_program_line(adjacent(_type="x"))

        seg_i, seg_j = sep[n]
        for i in range(n):
            for j in range(n):
                area_id = (i // seg_i) * (n // seg_j) + (j // seg_j)
                self.add_program_line(area(area_id, [(i, j)]))

        self.add_program_line(fill_num(_range=range(1, n + 1)))
        self.add_program_line(unique_num(_type="row", color="grid"))
        self.add_program_line(unique_num(_type="col", color="grid"))
        self.add_program_line(unique_num(_type="area", color="grid"))
        self.add_program_line(generate_killer_cage_rule(puzzle))
        self.add_program_line(generate_arrow_rule(puzzle))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, ("normal", f"corner_{Direction.TOP_LEFT}"))
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            if label == "normal":
                self.add_program_line(f"number({r}, {c}, {num}).")

        if puzzle.param["diagonal"]:  # diagonal rule
            for i in range(n):
                self.add_program_line(f"area({n + 1}, {i}, {i}).")
                self.add_program_line(f"area({n + 2}, {i}, {8 - i}).")

        if puzzle.param["untouch"]:  # untouch rule
            self.add_program_line(avoid_same_number_adjacent(adj_type="x"))

        if puzzle.param["antiknight"]:  # antiknight rule
            self.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 2, |C - C1| = 1.")
            self.add_program_line("adj_knight(R, C, R1, C1) :- grid(R, C), grid(R1, C1), |R - R1| = 1, |C - C1| = 2.")
            self.add_program_line(avoid_same_number_adjacent(adj_type="knight"))

        self.add_program_line(display(item="number", size=3))

        return self.program
