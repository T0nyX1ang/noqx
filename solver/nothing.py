"""The All or Nothing solver."""

from typing import List

from noqx.penpa import Puzzle, Solution
from noqx.rule.common import area, direction, display, fill_path, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.loop import pass_area_once, single_loop
from noqx.rule.neighbor import adjacent, avoid_area_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.shape import area_same_color
from noqx.solution import solver


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))
    solver.add_program_line(direction("lurd"))
    solver.add_program_line(shade_c(color="anything"))
    solver.add_program_line(fill_path(color="anything"))
    solver.add_program_line(adjacent(_type=4))
    solver.add_program_line(adjacent(_type="loop"))
    solver.add_program_line(grid_color_connected(color="anything", adj_type="loop"))
    solver.add_program_line(single_loop(color="anything"))
    solver.add_program_line(area_same_color(color="anything"))
    solver.add_program_line(avoid_area_adjacent(color="not anything"))
    solver.add_program_line("nothing(A) :- area(A, R, C), not anything(R, C).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, (ar, _) in enumerate(areas.items()):
        solver.add_program_line(area(_id=i, src_cells=ar))
        solver.add_program_line(pass_area_once(ar).replace(":-", f":- not nothing({i}),"))

    solver.add_program_line(display(item="grid_direction", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "All or Nothing",
    "category": "loop",
    "aliases": ["allornothing"],
    "examples": [
        {
            "data": "m=edit&p=7ZhPj9PIE4bv8ymQzz7Edlfbzo1l4Xdh2T+wQigaoWE2iNEOhJ0/K5TRfHee6n7LvrDisNJvOaAk7jdJuapsv/20k+u/bs+u9m1n/hymdtN2PPJmKq9u4j2veLy4uLncbx+0D29v3h2uEG3785Mn7duzy+v9yU5Rpyd3x3l7fNge/7fdNX3TllfXnLbHX7d3x5+2zfnh/ZuLpj0+5/um7fjiKapr2h75eJUvy/euHtUPuw36mTTyFfL84ur8cv/6af3kl+3u+KJtvNgPZW+XzfvD3/um7lbe1wb44M3ZDUd0/e7io765vv3j8OetYrvT+/b48Cs9D2vPLmvPrr7Qsx/Kv+758uLD/tOX2p1P7+8597/R8Ovtznv/fZXTKp9v79g+K9uubF+V7ZOy7cv2BaHtcSjbH8t2U7ZWtk9LzOPtXTNMQ5s2fbPtW3RCD9IZbdIjOktP6LHqeYOepfs2dZ00eTrlmQ2dik6brk39Rpr4vsZTE117SBv27eu+1EfHvvTT136oj679pI4e+toD9ds0KH9HzkE5O3IOytkTPyi+Jz4pvqefpH564lPEz+ip6oF4U/xAflP+gRhTTCK/KX8iZ1bORM6snInjyjquxLFkHUsiT1YeY99R+xrnfKznPGXyj8qfiZkUk8k/KX8m/6T8mfyT8mfyT8o/ciyzjmUk/6z8IzGzYiBHmlVr6lvbqBaeMXkmTYZWLXxi8gl10Mo5zWjlxDMmz1CztU7xM/Gd4mfiuxpvG+K7Gk/91uQfwzMmz1AfXY/d8IzJM/SCrp6hF3StZaDSBsV0xAyK6YgZIoZ+htoP9dHqB/+Y/GP4x+Qf6qPVD/4x+Yf6aNXqqZVUq6dWUq2BeFP8QIwpBp6bqQd8ZfKVJepm1U3UzaqLr0y+Mnxl8pUZ+UflN2JGxRi1RtXCYyaPkRutWplak2plak2qhcdMHqMOWnlGYmbFjHw+x+f0M6sf/GbyG3XQOrf4zeQ3m3wVU128l+U9w3tZ3rOZmE4x8CeLP9REq7c5o9UDfsvyGzXR6gG/ZfmNmujaQ8ZjWR7LeCzLY9REKwYvZXmJfOian3zomp/92ixvsB9ateBJFk8yPMniCTnQtecMW7LYkrnuWdedfOh6vBluZHEjGzGjYoyco3JyrbOuNfnQ6o1rnYMnHDuMXlkdc9yZrLWgsDfmMncYwX9GOB/sJY+uRWFyFxz2NSK46vwP7cxXfubLwnbmS+rFBOZL6lW3p24wf3Ceq5bzOZg/kD+YzzxamO98Ds5zPmH0yupgvrNa87SwWvOUEa1+EjlT5HT+69jN+R/c9vVC+Z3nmuOF57FGmDNf+zrbY71wtsd64WzP6oe5BtOlyZNjLSCPrjvjunYw7+D7yvNYL5hfMH1h+7J2+P1ArB1+P6B57Zxf1hG/N5iC7fQwBc+J0RxnXNaUwvCYv87wmL/cA8DxleHyGGvFskYwwn/Nced2zF9ncqwFzuFYC/DVshY4k2MtcPbKS4W98hIjWrUGXxeCyb4WKIY5uHDe2Rucd/YG2/EGzF3ZqzluXPeF7cxHWLxy2ILPxGuOFw4H5/HGwnnncHDeORycxxuweGVvsH10zgdvyS8PFPYG2529wXb8sLDd1/dgOx5Y2O5rvTxgvo7PwVv2FfPh9MJnRrSY6SzVfUJhqa41zIa3iocPWXxgXBheGKvrzrhwG07DYbGOdTnrfpJx5bbzVveEjGjFOHvFCka06jqHg+esy1n3Bowr253PwXZ8kuUTRrTWBee2PMOIDlZTN9YCGAK7xWRixI3C8FgL8A8cX3ku/zCuawRegu8r2+UfxnW9wD+5+Icb/5fl9v9R2aayzeVnwei/L/7Pv0C+2s6Os+e/af/pwS/f799+29+enuya57dXb8/O9/zufXR4//FwfXGzb/in4f6k+dSU124gNH3/8+G//PPBr8PmWwPAt9YOSOL8Hj48OFw9uL790JyefAY=",
        }
    ],
}
