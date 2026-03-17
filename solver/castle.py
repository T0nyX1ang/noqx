"""The Castle Wall solver."""

from noqx.manager import Solver
from noqx.puzzle import Color, Direction, Point, Puzzle
from noqx.rule.common import defined, display, fill_line, grid, shade_c
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import separate_item_from_route, single_route


def wall_length(r: int, c: int, d: str, num: int) -> str:
    """Constrain the castle length."""
    if d == Direction.TOP:
        return f':- #count{{ R: line_io(R, {c}, "{Direction.BOTTOM}"), R < {r} }} != {num}.'
    if d == Direction.LEFT:
        return f':- #count{{ C: line_io({r}, C, "{Direction.RIGHT}"), C < {c} }} != {num}.'
    if d == Direction.RIGHT:
        return f':- #count{{ C: line_io({r}, C, "{Direction.RIGHT}"), C > {c} }} != {num}.'
    if d == Direction.BOTTOM:
        return f':- #count{{ R: line_io(R, {c}, "{Direction.BOTTOM}"), R > {r} }} != {num}.'

    raise ValueError("Invalid direction.")


class CastleSolver(Solver):
    """The Castle Wall solver."""

    name = "Castle Wall"
    category = "route"
    aliases = ["castlewall"]
    examples = [
        {
            "data": "m=edit&p=7ZZNbxs3EIbv/hUBzzzwe8m9uWnci+q0tYuiWAiCrCqIULlKZasI1tB/7zvk7HIV20iQAD4F0nLffWZIDoe7JO/+PSz3a6kt/W2USmr8vDX50s7lS/HvenO/Xbev5Pnh/v1uDyHl24sL+W65vVufdew1P3voU9ufy/6nthNaSGFwaTGX/a/tQ/9z21/K/gomIR3YrDgZyDdV/pHtpF4XqBX0JbQp1f6EXG32q+16MYMV5Je266+loH5+yLVJitvdf2vBcdDzand7syFws7zHYO7ebz6w5e7w1+7vA/vq+VH25yXc2RCuruHaGq4dw7VPhMvj+eZwt5t/1h+fijTNj0dk/DfEumg7Cvv3KmOVV+2DsEG0Tgpn8q0pt6jyLRWbtrHcfcE6FS+jCje6+BnHd0/2Iw22tN8Jt7BCNjTt89JXJ5opajKaPDdjLc2IYuqEndZKj9vWFFOemBGkT4DxBMy0bW11aVxPWSxhmknrXp3GqX0ONJDTWDFYYn6hJqxJhU07KCPSJ4EkU5iqfZgyJHvCtD4dVZ4DHsHo5EIZ6WQEeW5OOsA86fbhSO8jlRe5NLm8xmsie5vLH3OpculzOcs+b2iOVSOtcaI1EjpCe9bgFD1p4yqnhcUq1uCU/oFrbseqyh14YH+sPTZMuGP/oCYcMQTuyyXoULlL7O8r9xqa4/QGOlVOCcv+sfKAcUVXefSVD+1EV3mDGFKoOvJYItpPgz/ijxx/aipPQTptR+44P2BVKwOdWIMbVbmy7J8mnHRgrqCbyjX7mFC50dLZyBpt2lS5KfmBfcKhnWeNNl2o3LCP85VbJ53XrMG9qdxyOx5xhqbqwR85d5xz1IPm9jEvVSMnnHMX0GbUlQfOIfI/csyR4/nKPDWVD+3QvAw8ot/EfUUrvVKVR85/ShPeQA/9Rmg/cjxnDfvIvYa/dazhbydcsz9yNXKDGJxiDe505fydws78SHsVfcqvc+nog6aXkQanyws4aCS9JHvQNFEalUJeERraVr5w4ynbw7csPtg0MEUp0u7RsHB2EK4IjenWtBRY0h46sA7QqGbLGvY4CZ+MqrMhn4Oe+vnvlq+xzM86cXXYv1uu1jjFzHCaeXW5298ut3i6PNzerPfDM86PxzPxUeSrw8EU573vR8oXP1JS9tWLfd9f+GF+JpwOiR1XAdm/leLDYbFcrHZ4y5A9NpeF4VlzWSueNmMVesaA08kzNZrnarhHhhdPJ5a6+dn/",
        },
        {
            "data": "m=edit&p=7ZdNbxs3EIbv/hXBnnngx/Brb24a9+K6H3ZRFIJg2K6CGLXrVraKQIb+e1+SszuU4CAFDBQ5BILJlw+Hw+HsUF49/r25Wq+UCcoY5ZLSyuATKCjyYJpyazR/Lm6f7lbjG3W8efrwsIZQ6oeTE/X+6u5xdbRgq+XR8zaP22O1/W5cDGZQg8WfGZZq+9P4vP1+3J6r7TmmBkVgp83IQr4T+WudL+ptg0ZDn0Hbtuw3yJvb9c3d6vIUsyA/jovthRrKPt/U1UUO9w//rAaOo4xvHu6vbwu4vnrCYR4/3P7FM4+b3x/+2LCtWe7U9riFezqFayRcJ+G6OVz3Qrh8nleHe3f75+rjS5Hm5W6HjP+MWC/HRQn7F5FJ5Pn4PFAaRqeGQMNI6HIdxVi77GpndBsaY7gn7pnbXBcbF9qYQht7yz3bs1uT2mYmpdZn3fi0X/a1t6b5s5bHTnNvW0/c+2K3K8lt50FFXJaElzJbtrMV5AYVJ5RnNFlFX5DrF5Z460PmcQrNxAoqISPnParpKmad85q6Yqd7Ri/YHWxpbDXSfVg133zG6UA19wfh1+dQnM1G5YGUhbpnvEF/gnZwv+cs0YGzlA5AeYx7sbfk7MeU/b6R1aFlpjOqD34x0B6z/Hx0z9KBM6cPgT0AZJvr3o2v20XZDrVkxudduaOlPamtre0Fro7autp+W1tdW1/b02rzDnXobFSOkEeroBN0Yg1uWVMUTk654FgTNAkn1sF1HD7DtDZDZ+HEOiThHj4jr/Ue2gv3rCN1PEAH1ogzRuGedQzCA3wmXhvAUxAeWCcvPFrlsmWNc2UnPLLOVnjCfyA9+YnQceYYV4154VkrMpq1gTYzx7jZG91xBz3tS9A0c4zZ3nUcexmOJyMeE2eOMduHmZPGWutYw78l4Zq1dR1P0Il1hs7CNWubhBuvyHnZ1wXhHCfmhVtoYnsLe+q4ZU1euEMOPefNWWgr3LH2puM4i+fzOpzXk3DH2jvhqCvieiPUG3FdVc71hnnhuAuU2H+A/0TC+Y5gvuPwOdUJ7gWlJJzvEZW6mjlynji3EXWStfDIOmXhqFvieibUM3HdVs71jPmOI+apriLynL1wvoNU6nDiuDteTzpAh5kT3ynMC8/QZvIDeyMc42Zv/Mw9atJz7VU/1gvnfTHf8QgdWSfoJFyztrHjGTrzvlp5p4XzPcW8cLx+emdYW2gr3LB2RriFJra3sKeOW9ZkhOMueP7e8w758UE43xHMM9+V97ny1f62tlTbUL/yY3mX+o9vW+0d5fX/XT4bzoJsfW//9Md/nX/N/PJoMZxv1u+vblZ4Az/Fm/ibs4f1/dUdRmeb++vVehrjt8/uaPg41L+Fw2L6+nPo//85VLKvv7Rr+qWFgy+O5dG/",
        },
        {
            "url": "https://puzz.link/p?castle/10/10/f00.g231g141d141b022d042g241d212b112d141g042d022b241d241g131g00.f",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(defined(item="black_clue"))
        self.add_program_line(defined(item="white_clue"))
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(separate_item_from_route(inside_item="white_clue", outside_item="black_clue"))

        for (r, c, d, label), clue in puzzle.text.items():
            validate_direction(r, c, d)
            if Point(r, c) not in puzzle.surface:
                self.add_program_line(f"white_clue({r}, {c}).")
                self.add_program_line(f"not white({r}, {c}).")

            if isinstance(clue, str) and (len(clue) == 0 or clue.isspace()):  # empty clue for compatibility
                continue

            fail_false(isinstance(clue, int) and label.startswith("arrow"), "Please set all NUMBER to arrow sub.")
            arrow_direction = label.split("_")[1]
            self.add_program_line(wall_length(r, c, arrow_direction, int(clue)))

        for (r, c, _, _), color in puzzle.surface.items():
            self.add_program_line(f"not white({r}, {c}).")
            if color == Color.BLACK:
                self.add_program_line(f"black_clue({r}, {c}).")

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
