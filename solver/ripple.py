"""The Ripple Effect solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import area, display, fill_num, grid, unique_num
from noqx.rule.helper import full_bfs, validate_direction, validate_type


def ripple_constraint() -> str:
    """A constraint for the 'ripples'."""
    row = ":- grid(R, C1), grid(R, C2), number(R, C1, N), number(R, C2, N), (C2 - C1) * (C2 - C1 - N - 1) < 0."
    col = ":- grid(R1, C), grid(R2, C), number(R1, C, N), number(R2, C, N), (R2 - R1) * (R2 - R1 - N - 1) < 0."
    return row + "\n" + col


class RippleSolver(Solver):
    """The Ripple Effect solver."""

    name = "Ripple Effect"
    category = "num"
    aliases = ["rippleeffect"]
    examples = [
        {
            "data": "m=edit&p=7ZdBb9tGE4bv/hUGz3sQubPkUjc3jXtx/bV1iiAQhMB2ZcSoDaey9aGQ4f+eZ5bvij2kKFCgbQ6BJPIVNZwZad95SD3+trvcbkIb/RlzWISWR4pdebVm5bXQ483t091meRxOdk8fHraIEP53ehpuLu8eN0crRa2Pnvfjcn8S9t8tV03bhKbj1TbrsP9x+bz/frk/D/sLPmpCy7GzKahDvp7l2/K5q1fTwXaBPpdGvkNe326v7zbvz6YjPyxX+zeh8TrflLNdNvcP/9806sPfXz/cX936gavLJ77M44fbj/rkcffLw687xbbrl7A/+fN249yuy6ldV59p17/FP9zuuH554Wf/iYbfL1fe+8+zzLO8WD6zPS/btmzfle1p2XZl+4bQsI9l+23ZLso2le1ZiXm9fG7iIofYpWbZhSa2LTpL9yHGKD2i+0l3HDcd7zjXdG5HjCkm4sK0kE7oTppzk861Dj1KW4h9K01MX2MGtEmTv1f+RJ+9+kzUGlQrETMopl+gB2lqDarVUyurVk9vWb311Mqq1ZMnK89Anqw8AzGjYga++6jvnokZFZPpbVRvmbqj6mYLtlDdnNCqm3u0vm8e0Mo/Et8qfiS+VfxITFtjMnrqgdzoqS650VNdcgfrpt+H3OgpJ7nRiocaFhXTEhNrDHXjVNda6sapLvnQ0/clH1p58IPJD4YfTH4gH1oxkfxJ+fGDyQ+GB0weIAdadfGDyQ+GH0x+IB9atfCGyRvkRqtW4nfo9TvgE5NPLJF/UH68YfIGdYJlxeATk0+og67x9JPVD54xeYY6aPWAZ0yesYF+svoZqJVVC/+Y/ENNtOLxjMkz5A5JniEfWrXyiFYtvJHkDRt7tHrDG0neSHggyQNpQXw3xXMeeqpFrF8sJs36Jq0vsWh5uGNeuj9woJPnO+aicsOZoJyFCfIVe7T8jB+iarGfOePckMfYozVfRrwp3rlR+ePcqPxxbpj6cW7Ib+zRlTP0U7mU6Ec+hE8zl5wblUW9c6bygZjKJXxy4JLzRD6ET+jKHOrKe3Hgd6tcGoipXHKGVC45QyqXnBvyGPuZS/gBdhwYcmAUDDkwCp9E+S2Ozh/lGclT2YU3KpcKB6p/8AMsmJkgzpTZr2zhWnDgCR4weYD9zBOf/coT1v3AE+dA5Qnrblp39jNbnAmVLdGZo5xGjNXZ53jliXNA61tmX9eaMvuVLT77Secm54/mzjmQNEes+4E/rPuBPz7vWtMy75UtPteVIT7LlSGDc0DfnWvBgRs+15UbrOmBG87/ygrnf2WFM3+sM85xXVN8rg98GJ0Dda6ZWbGCPVqzzLWA+Z85IIYUDogh7NGad9Y9ad3ZzwxxPrSK594gtTUeLskb7NGVJ/RWmeM80XWHvfjDDcjbchvyqmytbPtyezL4fc6/fCf0l+2scKbfVn/ukb5+8nc+WR+tmovd9ubyesP98Pnu/mqzPT5/2N5f3vH+otwb1/f8IXk5an5vymvFP51gX/+j/Ef/UXwJFl/afH5p7UCMZnv78ePd5nhzc7O5fmrWR58A",
        },
        {
            "data": "m=edit&p=7VZdbyo3EH3nV0T77Ie1vfZ696VK06QvKf0g1VWEUETI0osKIuWjqhbx3++Z8bgo3itVV1XVVKoAcxjGM4c5Z83ufzvOd53SJT1tUHjHo9KBXyZ4fpXyeFgd1l17pa6Ph4/bHYBS39/dqeV8ve9GU8majU590/bXqv+2nRa6UIXBSxcz1f/Ynvrv2n6s+gm+KpRG7D4mGcDbC/zA3xO6iUFdAo8FAz4CLla7xbp7uo+RH9pp/6AK6vM17yZYbLa/d4XwoM+L7eZ5RYHn+QE/Zv9x9Srf7I8v21+PkqtnZ9VfR7qTz9C1F7oEI11Cn6FLv+IfptvMzmeM/ScQfmqnxP3nCwwXOGlPWMftqbAlbf0KXKI2hdV5wOQBmwd8HqjzQMgDTRaoqjzg8gAVJVfGjy6n5XJaLm/qc1p1XiPkP17rnJc2eR9t8kZ6MABd5a10NahTUR1/+exybbQb8HP57LUb9B4MQrt8/NoP+PkBPz+YhX8rEjyl2VmPvN7xanh9gPFUb3n9hteSV8frPefcwo9GO2UM6BmcF7pWhvxI2ABXCeNIooESthoYNBgbYAyEsQXGKAhXpTIO5Bkj30l+hRwaF2MccR4DZ4z6NBDCrgLGABkjp5YchxzyD2GP+rXU96hfS30PPrXw8XSMSn6N/CD5NXKC5NToFaRXAG4S9sqW0jcEYKnT4KwupU6DHC05TQ0ss2qQr2M+agDHfNQAjn1RAzj2Qg1ljeRoCxzng33AKQf1RRfsA5b6xgFH7awBnyrywT5gyYFeVvSy0MKKFhZa2KQFaS29WOvkB9JaerHWdBIlfZM3KvJAipMHku6YZ/JJRV5KmsJvdBElfRMHhxy6cJLWdMkwbi4+Id299PXITz6pUTPpXpNnpGYgrYVbALfkAdI6CLeAvckP/Leb9qL+n94gLwmfAD5N0h17G9kLDyT/sL6lzJn0FW/AF8CRD2udvEFa65QPTZNPNHlM/GDID5JDWiefkL7JD7a5eAAaQW/B6Csase6iEd7FGzgMPvCRcMNrxavno6Kmf7Av+o/7+6fSX9KZ2njD9Pbh/nux2WhaTI675XzR4f7i9uWX7mq83W3ma3waHzfP3S59xu3deVT8UfBraulu8f87vn/pjo8kKN/bNfHe6OAqLXar19d1d9Utl93iUMxGnwA=",
        },
    ]

    def program(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))

        flag = False
        for (r, c, d, pos), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(pos, "normal")
            if isinstance(num, int):
                self.add_program_line(f"number({r}, {c}, {num}).")
            else:
                flag = True
                self.add_program_line(f"black({r}, {c}).")

        areas = full_bfs(puzzle.row, puzzle.col, puzzle.edge)
        for i, ar in enumerate(areas):
            self.add_program_line(area(_id=i, src_cells=ar))
            if flag:
                self.add_program_line(f"{{ number(R, C, (1..{len(ar)})) }} = 1 :- area({i}, R, C), not black(R, C).")
            else:
                self.add_program_line(fill_num(_range=range(1, len(ar) + 1), _type="area", _id=i))

        self.add_program_line(unique_num(color="not black" if flag else "grid", _type="area"))
        self.add_program_line(ripple_constraint())
        self.add_program_line(display(item="number", size=3))

        return self.asp_program
