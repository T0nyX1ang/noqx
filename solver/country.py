"""The Country Road solver."""

from noqx.manager import Solver
from noqx.puzzle import Direction, Point, Puzzle
from noqx.rule.common import area, count, direction, display, fill_line, grid, shade_c
from noqx.rule.helper import full_bfs
from noqx.rule.neighbor import adjacent, area_border
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import count_area_pass, single_loop


class CountrySolver(Solver):
    """The Country Road solver."""

    name = "Country Road"
    category = "loop"
    aliases = ["countryroad"]
    examples = [
        {
            "data": "m=edit&p=7ZZPbxs3EMXv/hTGnnnYXf5dXQo3tXtxnbZxEQSCYMi22gi1o1S2inQNf/f8hhxKQWMjNYIml0AQ9UiOdh7J94Z789dmvl6YrjddMDaZ1nR83OBMcMG4CObb6ud0eXu1mOybg83t69UaYMzzoyPz+/zqZrE31ajZ3t04TMYDM/44mTZdY5qeb9fMzPjL5G78aTIemvEFU43pGDsuQT3wcAdf5nlBz8pg14JPFANfAS+W64urxdlxGfl5Mh1PTSN5vs//Fthcr/5eNMpD+her6/OlDJzPb1nMzevlW5252Vyu/txobDe7N+NBoXv8AF27oyuw0BX0AF1ZxWfTvVq+WazePUR1mN3fs+W/QvZsMhXev+1g2sEXkzvak8ld45389Tt4lHNpfPjXQIgMRLft971E2A/6A32/61tLX6RT+55+0D5pu5z8VW6Pctvn9hRuZrS5/SG3bW59bo9zzCGULdq0wrs3jXUdGIYZ9+Ck2IIhlrEzNrSKIxiCgr03NnaKkXzsFRMTawy5oubyA5jFCA4tmI3IGA5ROQQ4ROUQyJs0byQ+aXwkJmlMJNeguRIxg8YkHNcqnwHntfr8oQfrfwdiuhJDLLiMM2ZcX/FgnByA4D4a50ouZ51xvnBz7I/T/WEMXDgwhuMrJlfSXNFTFcq+MQ/W8WTBZc9dGoxvNe/QgvU58PfK3w3J+K7srW+J6UqMb53xfeHDM8AlF/8Da3zHuNVx1uh1jfwPrM/pLbjwIdZ4V/bQWzi4wsFbYlyNIa/uCc8D6/NtAJc1ehvBZQ89OvSqQ+/IK9bJmPig8ejNq97ICdZ4Dx9xVsbwCcrHwycoHw+fqHzQqletkgeszw/ER41Hb1715gPxSeM5O69nR06w8gnwSconsIdJ9xCtetUqecDKDX161adP0YS2egSde/WF+Kj6UTwS1F/ii+o7OOONnS+qB7ldth6MxFTfobet18Qv1V8Jbyb1OHqzg3oNveGZrV+qv/DQ1jt4Bb+oVsUX1S/ii+oXagje2HnE6bjov/oi4TXdT9E8Wt9qfusR8WzlMJBrqPoXj1Sdc3bqF7wCVm3AufoFr+ARjRH9V79wXftO4zvitQ7wC1Zt9OitVw30nGmvGhCPVE/14qOqf/FR1T/xUtSrR6rXxCPVa+IRW/1F3q3veKbTZzpw9ZdoWHWStao1x3O+Xs+X3522RXtVz+z5VsPUnK2Gk+hfuSXRf9Wq6F9zoduiZy6Tl/lKeZZbl9uQr5ool+STrtHPudWaKPtPLWy6VqqzIFwqC7QZSWkQlIwsFMQ6ZZmCrJGCC0JLnWjJlkvyk6ubcpByR3/8kZv82/j/Pj7bmzbHvMjtn6zW1/Mr3uYOL//4oHeyuT5frGufF+n7veZdk7/55ct9e7f+Cu/Wsv3tFysN/9HLn6AzZWe1opjxuWnebs7mZxcrRMbm1UmKzMOTkbeup01IGXvqjFa3RyZLwXtsMtfARya1LD6VDiX5o4kvfqoUaXS5eXO7/md/vZpfNrO99w==",
        },
        {"url": "https://puzz.link/p?country/10/12/d4ibeqt5abl75ajb6m94i80400vvvvk5vvufvv9h7sci34h21h21t6j6h", "test": False},
        {
            "url": "https://puzz.link/p?country/17/17/4si5d6t8fa2heg0ch42pfar88vioeikf7s4665a6g69g2bo2rc2qk0g5jrmll2p6kk62qsfhflvrakghu0pq13l87qg5huhgj407o09p0557vg4g4j-19o-362k2q1g",
            "test": False,
        },
    ]

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(direction("lurd"))
        self.add_program_line(shade_c(color="country_road"))
        self.add_program_line(fill_line(color="country_road"))
        self.add_program_line(adjacent(_type=4))
        self.add_program_line(adjacent(_type="loop"))
        self.add_program_line(grid_color_connected(color="country_road", adj_type="loop"))
        self.add_program_line(single_loop(color="country_road"))

        rooms = full_bfs(puzzle.row, puzzle.col, puzzle.edge, puzzle.text)
        for i, (ar, rc) in enumerate(rooms.items()):
            self.add_program_line(area(_id=i, src_cells=ar))
            self.add_program_line(area_border(_id=i, src_cells=ar, edge=puzzle.edge))
            self.add_program_line(count_area_pass(1, _id=i))
            if rc:
                num = puzzle.text[Point(*rc, Direction.CENTER, "normal")]
                if isinstance(num, int):
                    self.add_program_line(count(num, color="country_road", _type="area", _id=i))

        for (r, c, d, _), draw in puzzle.edge.items():
            if d == Direction.TOP and r > 0 and draw:
                self.add_program_line(f":- not country_road({r}, {c}), not country_road({r - 1}, {c}).")

            if d == Direction.LEFT and c > 0 and draw:
                self.add_program_line(f":- not country_road({r}, {c}), not country_road({r}, {c - 1}).")

        for (r, c, _, d), draw in puzzle.line.items():
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
