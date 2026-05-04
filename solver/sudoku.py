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
        cage_cells = tuple(puzzle.index_to_coord(index)[0] for index in cage)
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
        arrow_cells = tuple(puzzle.index_to_coord(index)[0] for index in arrow)
        arrows[arrow_cells[1:]] = arrow_cells[0]

    rule = ""
    for _id, (arrow_cells, (r0, c0)) in enumerate(arrows.items()):
        rule += "\n".join(f"arrow_num({_id}, {r}, {c})." for r, c in arrow_cells) + "\n"
        rule += f":- number({r0}, {c0}, N0), #sum {{ N, R, C: arrow_num({_id}, R, C), number(R, C, N) }} != N0.\n"

    return rule.strip()


def generate_thermo_rule(puzzle: Puzzle) -> str:
    """Generate thermo rules from the given puzzle."""

    # Thermo definition (only supported in Penpa+). The format is not standardized yet.
    rule = ""
    for thermo in puzzle.problem["thermo"]:
        i = 0
        while i < len(thermo) - 1:
            r1, c1 = puzzle.index_to_coord(thermo[i])[0]
            r2, c2 = puzzle.index_to_coord(thermo[i + 1])[0]
            rule += f":- number({r1}, {c1}, N1), number({r2}, {c2}, N2), N1 >= N2.\n"
            i += 1

    return rule.strip()


class SudokuSolver(Solver):
    """The Sudoku solver."""

    name = "Sudoku"
    category = "num"
    examples = [
        {
            "data": "m=edit&p=7VVNi9swEL3nVyw66yCNpLHkW7rd9JJuP5KlLMYs2TRlQxNS8lGKg/97R/JsHJXCUkohh6J48kYf7z1JlrU7fN58PchAxXippKZivEqPt/GnuEyX+9WivJLDw/5psyUg5bvRSH6ZrXaLQcW96sGxCWUzlM2bshJaSAH0aFHL5kN5bN6WYpcEhWwm1EFITS3jrisQvOnhp9Qe0XVXqRXhW8YE7wnOl9v5avEw7mrel1UzlSKqvUqjIxTrzfeFYDcxn2/Wj8tY8Tjb05R2T8tv3MLeniVa2QxfMm160+Zk2vzeNPx701C3LW3BR7L9UFZxBnc99D2clMc2+joKY2ho3PW0S8JYSs0ptUgp9GlBaXFKXexs+9TlrXEs9mnImFFRGvo0Mvs+9ZkuxrHulIaQddZKZT600tmctMrZtAqZttaQ0WttMqta21wPfuEHyNvTIp7xG3e2ErTuOq3+fYqjFCHFKW2ObEyKr1NUKboUx6nPDe2Z9kQWFwGIMQQJcQKE6V8CuA6Dk2B8h+log9MddloC2g6jlVAUHS4KCUF1ONAHQJmO3xO/Yn5F/Jr5NfED8wPxW+a3xO+Y3xE/Mj8Sv2d++rhAMKxlSAuZJ/rnejCEmQdsPi947o+EmR+K3A8ExuTfsK4hXcM+Ma4DzwtJF1kXTb4+yLpIusi6iPm8kHWRdJF1kXSLqNvGz0LcuusUbYqYtrSIp/GPzuvfvz0v2qnAp2vgvLjLqqkHlZik797V7Wa7nq0EXTztQPwQ6Uln1/6/iy7gLorboS7tDb80O3Tm6sFP",
        },
        {
            "data": "m=edit&p=7VVNi9swEL3nVyw66yCNrJHkW7rd9JJuP5JSFmOWbJqyoQkp+SjFwf+9I3k2XoXCUkohh6J48p4+3htJlrw7fNl8O8hAxXippKZivEqPL+JPcZku96tFeSWHh/3jZktAynejkfw6W+0Wg4p71YNjE8pmKJs3ZSW0kALo0aKWzYfy2LwtxS4ZCtlMqIOQmlrGXVcgeNPDz6k9ouuuUivCt4wJ3hGcL7fz1eJ+3NW8L6tmKkV0e5VGRyjWmx8LwdlEPt+sH5ax4mG2pyntHpffuYVze7JoZTN8KWnTJ21OSZvfJw3/Pmmo25a24COlfV9WcQafeuh7OCmPbczrKIymoXHX0y4JY4niiRaxFXoKRENPHdGip56oO1EbpUxPQyaFIevsVObr4lh7osHkNBr5nuZSWp1xnY/WoM64zmalAbMl0eAyO23MGXfPxtOy6rS4dymOUoQUp7T2sjEpvk5RpWhTHKc+N7Ql2tNCxEkBKYYgQUPC9C8BbIfBSjC+w3RyweoOWy0Biw5jIcG5DjsnIagOBzrfynT6nvQV6yvS16yvSR9YH0i/YP2C9C3rW9JH1kfS96xPdwcEw16GvJB1Yv5cD4Yw60CRzwue+iNh1geX5wOBMeVv2NeQr+E8Ma4DzwvJF9kXTb4+yL5Ivsi+iPm8kH2RfJF9kXzjSwttPPVx665TLFLEtKUuHrY/Oo5///a8mE4FPt3yz4u9rJp6UIlJutaubjfb9Wwl6LvSDsRPkZ50qRT/PzUX8KmJ26Eu7Q2/tHTozNWDXw==",
            "config": {"diagonal": True},
        },
        {
            "data": "m=edit&p=7VTLittAELz7K5Y5z0HToxk9bs5mnYuzedghLMIsXsdhTWwc/AhBRv+e6lbvyoLAEkLAhyCrXT1qVVVrHvvjl+23oy1w+dwm1uHyeSJ3nvIv0Wu6OqyX5ZUdHg+P2x2Ate9GI/t1vt4vB5VWzQanuijroa3flJVxxhrC7czM1h/KU/22NHsRNLaeoMBYhyfjtpQAbzr4WZ4zum4HXQJ8qxjwDnCx2i3Wy/txO/K+rOqpNaz2St5maDbbH0ujbjhfbDcPKx54mB/Q0v5x9V2fqLcnicbWw5dM+860fzbtf2+a/r1pmjUNpuAjbN+XFXfwqYN5ByflqWFfJ+MdXiXMusyS8QGpe05Tj9R3adYrDlycdmnRK3YJ57HLHZOFLieWzs7y0K/3XJ+f5dlZPew7aeJO4kgiSZyiR1t7ia8lJhKDxLHU3KB1l0OsgEkCY1FYciQY/5bYDGMKlnzeYuwQCq7FwVmKaYtjainLWpxlloqkxQX2UeJb/hz8ifIn4HfK78BPyk/gT5U/BX9Q/gD+qPwR/LnyY49S4VXLQysqD/vXcfLAykNpvy96qo/Ayk9Z3w8ViuHfq66Hrlefkb+D9hWhG1U3+v73iaoboRtVN8Z+X1F1I3Sj6kboZqzb8O7iqbuWmEqMMqUZL+o/WvZ/v3petFNRLqfp+RUua2Q2qMxEjo+r2+1uM18bnN/NwPw0csteTv8f6RdwpPN0JJe2wi/NDvbcbPAL",
            "config": {"untouch": True, "antiknight": True},
        },
        {
            "data": "m=edit&p=7ZdLb+NGDMfv+RSBznMQ5z2+pdtNL2n62BRFYRiLJHWxQR24yKMoFPi798+ZISUHe1ksCuRQOFb4G1J8jUTJj8+/7/98NgUfl81oCB+Xx/rNnv/G/rm6e9ptV6fm7Pnp0/4BgjE/nJ+bP653j1tzsu5mm5OXqaymMzN9t1oPNJjB4kvDxkw/rV6m71fTpZk+QDUY2pjh/nn3dHe73+0fBlmbLtqJFuL7Wfy16ll61xZphHzZZYi/Qby9e7jdbT9etJUfV+vpygwc+5t6NovD/f7v7dBzY77d39/c8cLN9RMqfPx099dgHBSPtTWDRDiY6ezLKnBzBU4rcJ+vwP7nFZTN4YDN+Rk1fFytuZxfZjHP4ofVy4HTehlc4FMDUmk7OHh6tRASL5R5ITlecPNCee2DqDrJixVbvfjFinPS9rqCfAj5pBJ5ObXGZ7JL8p7p1PrOMTd2nUu1jo2K9ZIEhxt9PsJg27nUF2jMUmfF47MpdXPbF+xCf+Bt5Yae16Otxyt02kyuHr+tx7EeQz1eVJv3KJhyNFTKsLLwWoqxXDJk/DfWhibbYKzLTcYtbAM1OZCx0Tc5emNTanJKxpaxyQU3+uia/wz/Y/c/wj91/wT/tvu38O+7fw//ofsP8B+7/wj/ufvHELHF9VgOsWL3w/n3detMbViV/XFdVuwj5O7fpuN8bOky8nc9rkNc1/OM3IdeV0Tc2ONGd9yf2ONGxI09bozHdcUeNyJu7HEj4iaOe+BbnLfuXbtWTSowp9F0SALJ5HEUKAArkGFWGsAEGhIggBOwC/A8pOMSgkAAZAEEDaNAhCYJZIAE9Ugn9HQyrqDMO9wA6QRJJyCDIBkEB5CguBJmKDArfglyDi6GXCTrgkSlVbAHqAMkKn2DYIr0LaNvRfqGk2HWS4AJNCRAACdgZ+B7HgNYWtJR+sASa0kQ1WMKqDE6AxQtFIxWsWqdol0ihgt79sc4ax1jUPR87mwcGIN6rtqoWLVJEcODwqxNjKoNVZsVq7Yo5iMcGWk8wnHWFtZqN4i7EdWYuBtRtbFqtVexarVXuEGpTrmOjlG0PPZw8IpVGxT9EjGV4Tn5Y9RAyTFqcxK3Lmk3Ejc2za64V0lbl7hXWQtMXH7WnBM3J2lzMtebtfzM9WZNI9sl8vyjOvSWqAViIlIdfR2RRp14HSNrk2JmLIqFjSUNHpALJA5EGrejls9xSeMSxyWNSxyXNC5xXNK4xHHJaXMcl+90UzgNmtNw3A2nzXG8R07TcH6BeL6bnMYFRJlhGMg5yaRKmAZWzBKmgZXRYFljBVgjcwJPp5JU4wCiSazxAqwJAn4B6F+RbjZQTQAkgYhz1AzTTS4xrAKyAGtkuuHqUsAbkMlyOzSQ+YpbI8utABN0R80wbKM2kTUyhiNrZNjiyVdINciAJDdijeRGrJHcKAvgIejrozCu1nil4T9staMmemu8M95DxHzDTAsRYuHJVwXsMw8ri9fjdZ012B3sPlO9I/g2YENysHKZJapXDr5shVGOsZJYxDxJgaN7gydgHDd4v0r8nvtFb8Lt/fNrXuWW7wbL5mg6a75vXn3C21rZnKyHy+f7m+3D6eX+4f56N+DH3uFk+Geo3zXep9jo/99/b/j3H2/U+Nau/beWDu7Gzcm/",
        },
        {
            "data": "m=edit&p=7VVNbxMxEL3nV1Q+z8Ee27P23kppuZRQKAhVq1XVhqBGJNoqHwhtlP/O2J6wDUJQDkg5oM16X97ab+Z5dnZXm0/dlw1EPmwADYYPG3Q+g0s/Lcf72Xo+rU/gdLN+6JYMAN5cXMDnu/lqCqNGprWjbR/r/hT6V3WjjAKFfBrVQv+23vav6/4K+mu+pcC0oBab+Xo26ebdUu25/rIsRIbnA/yY7yd0VkijGY8FM7xhOJktJ/Pp7WVhruqmt6BS7Bd5dYJq0X2dKskt/Z90i/tZIu7v1uxw9TB7VGD5xipvjdpH2EF/WhyMn+nADg7sDwf21w7wnzuI7W7HxXnHHm7rJtn5MMAwwOt6u0tpbZWnvflSQeVDInAgSCfCDkTARIQnRNZwA2F0FqmeMCar0FMmy/g9w/mYnNVNHi/yiHl8z0lDb+um4Ue1MuBDCxkikC4weAhUYAzA2oIrxjIlEhdDVgYLQaZUGnxaaR04KtKuAh/5aozjJbooG2MhZha5f3RGvMYgSgjvgEKR9R4otpzzy5y5zqPP42V2dM47bwInFKOqkf3HCJg2hDFfAdEXjB7QhoK5d9Gbgr0BJFcwOcCqKriqAKMuOHKHa1v0A+tr0desb0TfsD6KPrK+E33H+l702RiS6BPrB9HntwdGK7EsxyLRSfkLj5ax6KA79IX7+cRY9LE6zAejYM7fSlzLca3kSWkfxBdxXJK4ZA/3hyQucVySuESHvkjichWRJC5x3CrF3aXeTqU7y6PLI+WSVqmn/qrrnvOs//7p+WM6De+e+enwx8W0o0aNN4v76fJk3C0Xd3N+1V0/TiczRvyJ2Y3UN5XPhouZpv//6hzxVycVSh9bFxxbOtyX7eg7",
        },
        {
            "data": "m=edit&p=7VXLbtswELz7KwKe90AuyaWom5smvaTuIwmKQBCC2HURozYU+FEUMvzvXVLryg6KtjkU8KGgRQ+H1MzuUpRWm8/N1w1EbrYADYabLXS+Cpd+WtrNbD2flmcw3KwfmyUDgHeXl/DlYb6awqCSZfVg28ayHUL7pqyUUaCQL6NqaD+U2/Zt2Y6gveYpBaYGtdjM17NJM2+Was+1V92NyPCih5/yfELnHWk045FghncMJ7PlZD69v+qY92XV3oBK3q/y3QmqRfNtqiS2NJ40i/EsEeOHNWe4epw9KbA8scqlUXuHHbTDl2Vg+wzszwzsrzPAf55BrHc73pyPnMN9WaV0bntY9PC63O5SWFuFxT75bgeVNYnAA8IlwvVE8Zww3RJ/yITE0AHjdGLCnmF7k4O4y/1l7jH3N2VVOQsOwXvwBD5A0ECxhio4CBYCz0RwBC6AK4C4ilW0XGoCY2I/iA6iT0PmdQSD2A9igFjw0GC6yUKMBwOjTc3bYblY0L7Ovc69z/1VDvOCq2cKviFGVSInFSOgwYz5HxB9h9ED2qLDfP7Qmw57A0iuw+QAQ+hwCIBRdzjyKdW20y9YX4u+Zn0j+ob1UfSR9Z3oO9b3ou9Zn0SfWL8QfX4DYLTiZdmLRCfFLzxaxqKD7jgv3K8nxqKP4TgejII5fiu+ln2txEmpDpIXsS+JL9nj+pD4EvuS+BId50XiS+xL4kvsG5LvLp3PtHXnuXe5p7ylIZ2LF52c3z/Af/P0/DGciqtnnjV/Wkw9qNRosxhPl2ejZrl4mPPr6vppOpkx4s/EbqC+q3xVvJlp+f8vxwl/OdJG6VM7BacWDp/LevAD",
        },
        {
            "data": "m=edit&p=7VZLbxMxEL7nV1Q+++AZe7323kppuZTwaBGqVlGVlqBGJNqSB0Ib5b8z43VIs0yphEDqAW3WmXye/b552PEu15+aL2sd6bJBGw102WDSHRx/TL4up6vZpDrSx+vVXbMgQ+s3Z2f683i2nOhBnd1Gg00bq/ZYt6+qWoHSCukGNdLtu2rTvq7aK91e0JTSQNh552TJPO1MJPNjmmfwpPM0ZA67eX7qiszl1/V4Mbk+75C3Vd1easUyL9IjbKp5822ichj8+7aZ30wZuBmvKJnl3fQ+zyxTGdRPCTVfz1bT22bWLFQOdqvb4y6D4e8zsE9kgL9kgH87A5Qz2FJz3lMO11XN6XzYmxfVZssBbhQGdi/Iv2ubsoaB+ACwDPg94JCB8AAoehwuMlDugcL1gZIBtwd8esTugQAM4B6IdtevDAC43jMAfRZA30sHbOhJgzMH8VNlINXniupjOQxLnZgubme79acsdujBqlTWS6izIuokXhcktChEVFTzRkRLERXVSpGhRNG3kHyDyBCciJYSbxAji15EZd8oqYERQwMjdhlMEL1B9gaxRABi/wGN6I2PeIvFAxRXBsjLE+wj3mJZwQprhjbFWdoamMZL+jfRrU3jyzSaNBZpPE8+p7SJIHgN3BEk3hg1cqnIpm+NnAPbWGjkvck2nU1YQGcXoNG7zvZOY1l2dllqjKazI51gxnb8gfhN5jfED5kfiB8zPxK/y/yO+IvMXxC/z/ye+EPmp9MRo81alrR85uH4M46W7MyD7jAv3Pl7sjM/lofxYMw2xW+zriVdm+P0XIeclyddn3W9PayPz7qedH3W9f4wL591Pen6rOtJl/c+bvk849adpNGl0aeWlmkMu4Pk8QMmCGfNw//VP1tIT0S2HdRUSOhdxfNCRoNaDdfzm8niaNgs5uMZHegXd+P7iaJ3qe1AfVfprrnDOv5/v3rW71fcKfP0W9Y/X/nPeU/Soq5Hgx8=",
        },
        {
            "data": "m=edit&p=7VbbattAEH33V4R9nofdWWm10luapn1J04tTShAmOK5LTG0UfClFxv/emdE4tlWJ0kIhhSJrOT5anTMX7Uqrzefq6wZyOnwEC44OH62cMeGf1eNmtp5PizM436wfqiUBgLfX8GU8X01hUOqs0WBb50V9DvXrojTOgEE6nRlB/b7Y1m+K+hbqIV0y4Ii7aiYhwcsD/CTXGV00pLOErxUTvCW4ksCn60lDvSvK+gYMG72Q2xmaRfVtajQQ/j+pFvczJu7Ha8pm9TB71CuNnHnyMIvNfD2bVPNqaTTcHdTnksN+ckcm/pCJf8rEd2eCmslktpzMp3dXfyER7E5kR136QKncFSVn9fEA4wEOi+2OY90ajHwnNdI1rTQe94VSImkTWcJEekSkTIQDES0T+RGRMRGPCLHNDkQeWzOcbYs4xJaxQ89McswkLWGHoZWhQ4nGHzG+nYHz4ac5easOLrEn7lRRJ3W9pbq6nKc7aD3LBi328L6HT7p516Pjsm4ee/SxRx/THj5280mPfuiJM/T4Zj2+scc39tQ5dz18lz417ZW0DmW8oVUCtZfxpYxWxlTGK5lzyU2OAaTRCNxwkKagNAekgCiFBPSxwbQNY+oanDqQIqAUAzDLGpxlgLltcE6bNT8YrB9J36q+JX2n+o70UfWR9BPVT0g/Vf2U9IPqB9KPqk8vAsy9ennyCqrD8SuPHuQhEZyc5oX7+YGw6mN2Gg/miil+r76efL3GGbgOmlcg36C+wZ/WJ6hvIN+gviGc5hXUN5BvUN9Avhn77njP5tZdyJjIGKSlGW+Lv7VxHi/2P3t6fhlOSdVzrSN9XsxoUJqhLKSz62q5GM/pRTV8GD9ODX0s7Abmu5GzpFby5P/fD//C9wN3zD63xfDcwqHlORr8AA==",
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
        self.add_program_line(generate_thermo_rule(puzzle))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, ("normal", f"corner_{Direction.TOP_LEFT}"))
            fail_false(isinstance(num, int), f"Clue at ({r}, {c}) must be an integer.")
            if label == "normal":
                self.add_program_line(f"number({r}, {c}, {num}).")

        for (r, c, d, _), symbol_name in puzzle.symbol.items():
            if d == Direction.CENTER and symbol_name == "circle_L__3":
                self.add_program_line(f":- number({r}, {c}, N), N \\ 2 != 1.")

            if d == Direction.CENTER and symbol_name == "square_L__3":
                self.add_program_line(f":- number({r}, {c}, N), N \\ 2 != 0.")

            if d == Direction.TOP_LEFT and symbol_name == "sudokuetc__1":
                self.add_program_line(f":- number({r}, {c}, N1), number({r - 1}, {c - 1}, N2), (N1 - N2) \\ 2 != 0.")
                self.add_program_line(f":- number({r - 1}, {c}, N1), number({r}, {c - 1}, N2), (N1 - N2) \\ 2 != 0.")
                self.add_program_line(f":- number({r}, {c}, N1), number({r}, {c - 1}, N2), (N1 - N2) \\ 2 = 0.")

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
