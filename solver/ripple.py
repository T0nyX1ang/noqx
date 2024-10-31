"""The Ripple Effect solver."""

from typing import List

from .core.common import area, display, fill_num, grid, unique_num
from .core.helper import full_bfs
from .core.penpa import Puzzle, Solution
from .core.solution import solver


def ripple_constraint() -> str:
    """A constraint for the 'ripples'."""
    row = ":- grid(R, C1), grid(R, C2), number(R, C1, N), number(R, C2, N), (C2 - C1) * (C2 - C1 - N - 1) < 0."
    col = ":- grid(R1, C), grid(R2, C), number(R1, C, N), number(R2, C, N), (R2 - R1) * (R2 - R1 - N - 1) < 0."
    return row + "\n" + col


def solve(puzzle: Puzzle) -> List[Solution]:
    solver.reset()
    solver.register_puzzle(puzzle)
    solver.add_program_line(grid(puzzle.row, puzzle.col))

    flag = False
    for (r, c), num in puzzle.text.items():
        if num == "?":
            solver.add_program_line(f"black({r}, {c}).")
            flag = True
            continue

        assert isinstance(num, int), "Clue should be integer."
        solver.add_program_line(f"number({r}, {c}, {num}).")

    areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
    for i, ar in enumerate(areas):
        solver.add_program_line(area(_id=i, src_cells=ar))
        if flag:
            solver.add_program_line(f"{{ number(R, C, (1..{len(ar)})) }} = 1 :- area({i}, R, C), not black(R, C).")
        else:
            solver.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

    solver.add_program_line(unique_num(color="not black" if flag else "grid", _type="area"))
    solver.add_program_line(ripple_constraint())
    solver.add_program_line(display(item="number", size=3))
    solver.solve()

    return solver.solutions


__metadata__ = {
    "name": "Ripple Effect",
    "category": "num",
    "aliases": ["rippleeffect"],
    "examples": [
        {
            "url": "https://puzz.link/p?ripple/13/13/i2aonbatddnfdjqt6qafrlvfl9egl450fvjbt3t9lfu2072jfj8pvgojecbvcvu0zzzzzzzzo",
            "test": False,
        },
        {
            "data": "m=edit&p=7VZdbyo3EH3nV0T77Ie1vfZ696VK06QvKf0g1VWEUETI0osKIuWjqhbx3++Z8bgo3itVV1XVVKoAcxjGM4c5Z83ufzvOd53SJT1tUHjHo9KBXyZ4fpXyeFgd1l17pa6Ph4/bHYBS39/dqeV8ve9GU8majU590/bXqv+2nRa6UIXBSxcz1f/Ynvrv2n6s+gm+KpRG7D4mGcDbC/zA3xO6iUFdAo8FAz4CLla7xbp7uo+RH9pp/6AK6vM17yZYbLa/d4XwoM+L7eZ5RYHn+QE/Zv9x9Srf7I8v21+PkqtnZ9VfR7qTz9C1F7oEI11Cn6FLv+IfptvMzmeM/ScQfmqnxP3nCwwXOGlPWMftqbAlbf0KXKI2hdV5wOQBmwd8HqjzQMgDTRaoqjzg8gAVJVfGjy6n5XJaLm/qc1p1XiPkP17rnJc2eR9t8kZ6MABd5a10NahTUR1/+exybbQb8HP57LUb9B4MQrt8/NoP+PkBPz+YhX8rEjyl2VmPvN7xanh9gPFUb3n9hteSV8frPefcwo9GO2UM6BmcF7pWhvxI2ABXCeNIooESthoYNBgbYAyEsQXGKAhXpTIO5Bkj30l+hRwaF2MccR4DZ4z6NBDCrgLGABkjp5YchxzyD2GP+rXU96hfS30PPrXw8XSMSn6N/CD5NXKC5NToFaRXAG4S9sqW0jcEYKnT4KwupU6DHC05TQ0ss2qQr2M+agDHfNQAjn1RAzj2Qg1ljeRoCxzng33AKQf1RRfsA5b6xgFH7awBnyrywT5gyYFeVvSy0MKKFhZa2KQFaS29WOvkB9JaerHWdBIlfZM3KvJAipMHku6YZ/JJRV5KmsJvdBElfRMHhxy6cJLWdMkwbi4+Id299PXITz6pUTPpXpNnpGYgrYVbALfkAdI6CLeAvckP/Leb9qL+n94gLwmfAD5N0h17G9kLDyT/sL6lzJn0FW/AF8CRD2udvEFa65QPTZNPNHlM/GDID5JDWiefkL7JD7a5eAAaQW/B6Csase6iEd7FGzgMPvCRcMNrxavno6Kmf7Av+o/7+6fSX9KZ2njD9Pbh/nux2WhaTI675XzR4f7i9uWX7mq83W3ma3waHzfP3S59xu3deVT8UfBraulu8f87vn/pjo8kKN/bNfHe6OAqLXar19d1d9Utl93iUMxGnwA=",
        },
    ],
}
