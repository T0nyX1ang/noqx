"""The Rail Pool solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, direction, display, fill_path, grid
from noqx.rule.helper import full_bfs
from noqx.rule.loop import single_loop
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.solution import solver


def len_segment_area(color: str = "grid") -> str:
    """
    Generate a rule to get the length of segments.
    """
    rule = 'nth_horizontal(R, C, 0) :- grid_direction(R, C, "r"), not grid_direction(R, C, "l").\n'
    rule += 'nth_horizontal(R, C, N) :- grid_direction(R, C, "l"), nth_horizontal(R, C - 1, N - 1).\n'
    rule += 'nth_vertical(R, C, 0) :- grid_direction(R, C, "d"), not grid_direction(R, C, "u").\n'
    rule += 'nth_vertical(R, C, N) :- grid_direction(R, C, "u"), nth_vertical(R - 1, C, N - 1).\n'

    rule += f'len_horizontal(R, C, N) :- nth_horizontal(R, C, 0), {color}(R, C + N), nth_horizontal(R, C + N, N), not grid_direction(R, C + N, "r").\n'
    rule += f'len_vertical(R, C, N) :- nth_vertical(R, C, 0), {color}(R + N, C), nth_vertical(R + N, C, N), not grid_direction(R + N, C, "d").\n'
    rule += f"len_horizontal(R, C, L) :- {color}(R, C), nth_horizontal(R, C, N), len_horizontal(R, C - N, L).\n"
    rule += f"len_vertical(R, C, L) :- {color}(R, C), nth_vertical(R, C, N), len_vertical(R - N, C, L).\n"

    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_horizontal(R, C, L).\n"
    rule += f"area_len(A, L) :- {color}(R, C), area(A, R, C), len_vertical(R, C, L).\n"
    return rule.strip()


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line("railpool(R, C) :- grid(R, C).")
    solver.add_program_line(fill_path(color="railpool"))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="railpool", adj_type="loop"))
    solver.add_program_line(single_loop(color="railpool"))
    solver.add_program_line(len_segment_area(color="railpool"))

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
    for i, (ar, rc) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if rc:
            data = puzzle.text[rc]
            if not isinstance(data, list):
                data = [data]
            for num in data:
                if num != "?":
                    solver.add_program_line(f":- not area_len({i}, {num}).")
            solver.add_program_line(f":- #count{{ N: area_len({i}, N) }} != {len(data)}.")

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Rail Pool",
    "category": "loop",
    "examples": [
        {
            "data": "m=edit&p=7ZRPa9tMEMbv/hRlz3vYnV3r3yWkadyL6zaNX0IQIjiuQ0zt+m0clyLj755nZseVW1JKCYQcitDop0czu8+OVlp/3UzuZrbAEQrrrMcRIslJrpTT6TGe3y9m1St7vLm/Xd0BrH0/GNibyWI969Wa1fS2bVm1Z7Z9W9XGG2sIpzeNbc+qbfuuake2PccjYwtow5REwNMOL+Q500kSvQOPwBEMvARO53fTxexqmJQPVd2OreF5Xks1o1muvs2M+uD76Wp5PWfhy2Z5s1Bxvfm0+rzRNN/sbHv8e6fhMacs/upUE57s9Hpyj7avb+f/P2a3bHY7dPwjDF9VNXv/r8Oiw/NqiziqtoYyLg3wkl6LCUGEoyORIkvRs5QEycmizJeqJKUsuhQRvJMiTwdJ3uesdRI8eHFyKXEgkSSOYdS2QeIbiU5iX+JQck7h32el9bkzFWH8ftFxTtYX8MlcRHBfuQ/GoiWH9T0H1Go+1+boA3OGnHyfkyEfK5VxMFdRJi75y0jz4mrJU2LvD5h19ETyC7D6LHOLe2WMX6JHwvBZ6rxgcknHFbVpXvI8jrLLwGkc4cN8t9eRT+qT4IeSH1zB6pPwpeMN/fCvLGtU/0TgoOMEjBO1lv8S/dRDCuCoHCM49R9XcFoXBdb3HDDmQS3vQ8mH50znYo7a8wz9yXmN2AgXsh1OJEaJmWyTnHf7X30PT9+Rf7RTE97yTwdW8pz3Ta/Gb3nXM9+NnDV2vo3//tTP/6fm7ruXtj9fmh18MU3vAQ==",
        },
        {
            "data": "m=edit&p=7VZdT9tKEH3Pr6j8vA/77Y83yoW+UHopVAhZEQKaiqigtIRUlaP8d87snsURVKqurqrygBzvHo9nzp4Zjzdefl9d3M2UsfJzjdLK4PCtT6erQzo1j5P5/c2se6N2VvfXizsApT7s76svFzfL2aSn13SyHtpuOFLDu66vTKUqi9NUUzUcdevhfTccquEYtyplYDvIThZwb4Sn6b6g3Ww0GvgQ2OewM8Cr+d3Vzez8IFv+7frhRFWyztsULbC6XfyYVdQh11eL28u5GC4v7pHM8nr+jXeWq8+Lryv6mulGDTtZ7vEv5LpRrsAsV9BTucznD8ttp5sNyv4Rgs+7XrR/GmEzwuNujfGwW1chpFDrpJ4KVQVlrZPNbVlc9hotTbZs+RhNp20qYz2NWzY4JNu2n69LxYslmOd0Vtuny1rzTK3FxRO51pKtmJC+SUU4S+N+Gm0aT1AjNbg0/pNGncaQxoPks4fSeeeUl1wsGB3elAAlgoMGxnoJ4y2KyC1hC9zQP8IHyRTs6ONq4OLTALfErfKe/B78nvwe/J48HvyBsQGxNbUFxNZ4zgXHwgPN29jTRzhD0Sw6Cw7AkVjyLZyoQyhrAUdq1tBjsh7XgEceHrFrMidm4OIDzZo8GvyW2gw0P2L4GPJb8JdaafBb8reoj846Bbs21wozcPFBrC6x4JQ+TZxSh7yWC9AmnS+4dtCZ18UMHvqAx7X0aeHTZh7MwLk+mIGppxE9xBE+DXkiYiNjIzgjOSM0R2qOiI3MBc8R18SNwvWomT2Qdu2Se9rBuW6N+tesfy050l/WLRi99Mgj2FOPh05PneiZRw3oVcdexQwf2tGrjr2KGZi5SCz7zVnxJzbgt+SRvyJ5lRNGLN7ejMFpyKkRKztAwtCgGauRF5+vQ2/gesSlT9A/0E0sesgj2BZtqJtl3azEkkf0FCwa6G/luVOPYMsewAyceTAzF2wkp2k72U2jT2NM20wtG/V/2sr//472Wzk9djn5Lnh+hFe7HNNJj8+ezaT6WaWzd/IV9fol9Je+hOQR6Jf2Er00OXitp5MH",
        },
        {
            # This example has extra rules, which is not implemented by the current solver
            # https://brokensign.com/puzzle/2022/08/04/rail-pool-forgetful.html
            "data": "m=edit&p=7Zddbxs3E4Xv/SuKvebF8ms/dFOkadwb120aF0EgCIHjuohRB27juChk+L/nGfJQWsgBihdF3+YikLRzRJGcM2dmuKvbP+7O3186n+wdJ9c7zyuPffmkcSifXq+zqw/Xl6uv3JO7D29v3gOc++H42P16fn17ebTWrM3R/XZebZ+77Xerdec71wU+vtu47fPV/fb71fbUbV/wU+c8Yyd1UgA+28OX5XdDT+ug78Gn4FSXvQJeXL2/uL58fVJHflytt2euMz/flNUGu3c3f1524mHfL27evbmygTfnHwjm9u3V7/rl9u6Xm9/uNNdvHtz2SaX74hN0456uwUrX0CFdxfMv0503Dw/I/hOEX6/Wxv3nPZz28MXqnuvp6r5Lviz9GjIOTdkwxRZ7G5gOp+T5YMowHAxMfV2zWDTXfRcj3qeDZT7WkeWk9HgrP2SNLQdHTVwMTXXeYmQOByOhr9wXy0L/KOLgpdNyLI6PWYSkCJZjo+guh+raxchUme0mkSBf0vSqXI/LNZTrGVl021iu35ZrX665XE/KnGckN6bBxQFCwXVYGhsfhufZpR65Cp4c33c4efQAY12ydBiOCUwQBWdwncN+u32wrEW4spZ9NAfrUtY+mX3GygHr0qy1M+eMiQ7GuhzqWqzLJqjhlFwe6lqsy1ZihifWzvI7+sX+dm6RtYYnzZnY33JefLF/TyYKHvccUlz4xZf1RMOD/A52Nmr+yJ6zNDGdrT4LzuA2brmovrDguhYLlv7D7KKVsWE4R/HHgpU7NNxhNIzSEEsuFCMapr7lFE0aHiPztWeG21jjKvOlOdYlxY51SZpj0VD5QvPUNKdmsmoG67JqButyVr4yuimuck9RLrBuaLmgTrJ1VMOqGSxrtQ/xZsWLBddY6n1KOJO7hqlVvosb+VUNF56++koT+qj+0xCJUTWTqPNB+hhO0oeeSuopLPOlD72QWy/QXw2X+tSeWLBisfmTuE1wnhTvRLx2bhUM/0n6THCepM9ELNKw1Jj2wZJr8e+JyysuT79LWyz9qF6mBlKrAWojSU8s/OtaLP0ovwG/SdzQJEsf7C7GUquT6m2yc0Z+6a8U5DeYnk1b/A7yO1j/ivPI2llrZ/z6ljv8RvmN+M0t73BWH2F3WkU0jNIQC27j8OnFp4dPEJ8AH7srFm7wsZtd0Qo+dmoXbqydtXaGj281Bp/Yag8+SXwSfNT72F1+jVvqWw/iN8hvwG+U34jfLL8Zv3YzKRxYa/fUwgG/docqHPAb5DfgN8lvwq/OJeyu9kptBNVtoK8bB54C9xzwG1u/W7+o5mc7wxV7sHO7+cVX0HzTM6hfAv3SaoDzc5d307adq6ahPRgUTC+0vEf6ZZd3YozqI9M2a22m11QPRTd7dih5xFfLqek2qpfLc630Md289vT4Uk5jsvNZ9cM51s5n699h1+MDWDHaOdz6yOq5nZ/UcD0zuTm/LLfop+WaynUot+7RHs/+pwe4f/6U8Ld01lSC/Rv49Ct/+e3/9dvmaM2fqoej7q+ufNaR0fTlf9Z/9D/LUtB/bs36udHh+NgcfQQ=",
        },
    ],
}
