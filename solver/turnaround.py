"""The Turnaround solver."""

from noqx.manager import Solver
from noqx.puzzle import Puzzle
from noqx.rule.common import display, fill_line, grid, shade_c, shade_cc
from noqx.rule.helper import validate_direction, validate_type
from noqx.rule.neighbor import adjacent, count_adjacent
from noqx.rule.reachable import grid_color_connected
from noqx.rule.route import route_turning, single_route


class TurnaroundSolver(Solver):
    """The Turnaround solver."""

    name = "Turnaround"
    category = "route"
    examples = [
        {
            "data": "m=edit&p=7VZdb5swFH3Pr6j87Ad/AAFerKxr9sLSbU1VVQhFacY0NBgbCVPlKP991xdYWpuHVO1DJ1XEN4fja/vYvjpi+7tdNznlzPxkSOEfHo+H2EQYYGP9syx2ZR6f0Vm7+143ACi9nM/pt3W5zekk7dOyyV5HsZ5R/SFOiSAUGycZ1Z/jvf4Y6wXVV9BFqAQuAcQJFQAvjvAG+w0670jOAC96DPAW4KZoNmW+SjrmU5zqJSVmnXc42kBS1X9y0g3D901d3RWGKIuf+X1Pbtuv9Y+W/JudVG25KzZ1WTcEp+LZgepZpz4ZUS979bBTfpQvx+WLF5QvbfXRuPoDXMoX0L+KU7OV6yMMj/Aq3h+Myj2RzIxUMLS7OSLFcDoDIUm/34EI7IypleHbQwJmE9wQ7AEh7AycQz4g7FWmttIwsDIiYc0R2cI4s1M4sxfmLLIZ4eSI0J7ZOUjunCSXnnUMXPp2jmefDPedtfzIZgJn9eDx6nD/HKvgFuMco8C4hCKhWmJ8j5Fh9DEmmHOB8QbjOUYPY4A5U1NmTyrE58ghnrmPKDRFIzogweSgxCQiD05Znqg5lZ0zPn78/4/LJilJwDrOFnVTrUtwlUVb3eXN8A7mfZiQe4ItleDn0Zufv0o/NxfEnubqnc8px+eU43PK8Tnl+JxyfE6d4FjKcSzlOJZyHEs5jqVej2OlUEK9tVB9ScmvdrVewXUR+BaiQye4zXgnuNR4B7iW0/Fi5njqzsH6sslf",
        },
        {
            "data": "m=edit&p=7VNNa8JAEL3nV8ic57DZ9TM3a7WXNP3QIhKCqE1paNLQaIps8L93dhIbql4KRTyUZR5v33692d1Zf+SLLMQuNdVFgTY11ZQcUvQ4RNUm0SYOnQb2881rmhFBvBuN8GURr0O0/GpaYBW65+g+6hvHBwnIYUOA+sEp9K2jPdRjGgJUpLnEbEBJdFjTKY8bNihFWxD3Kk50RnQVZas4nLulcu/4eoJgzrni1YZCkn6GUC7j/ipNlpER4ug93FbiOn9O33L43h2SPN5EqzROM+Ct7GCHul+6d0+4V5V7ytSu7avT9uUf2leH7nun3e/oUR7J/9zxTSpPNe3WdOwUO+OyANmDKpvy5aDZOhDaan9dldDpGEHUgi3EkSKPlOaPbeh4m03MGEeMknFCHlErxmtGwdhidHnOkHHKOGBsMrZ5Tsdk+at7OIMdX7a55urWOm8/sHxw6TM1vDRLFjH9My9PlmG271M57yzYAoevUJol/xV+gRVuHkhc2v++NDtUcYH1BQ==",
            "config": {"visit_all": True},
        },
    ]
    parameters = {"visit_all": {"name": "Visit all cells", "type": "checkbox", "default": False}}

    def solve(self, puzzle: Puzzle) -> str:
        self.reset()
        self.add_program_line(grid(puzzle.row, puzzle.col))
        self.add_program_line(shade_cc(["white"]) if puzzle.param["visit_all"] else shade_c(color="white"))
        self.add_program_line(fill_line(color="white"))
        self.add_program_line(adjacent(_type="line"))
        self.add_program_line(grid_color_connected(color="white", adj_type="line"))
        self.add_program_line(single_route(color="white"))
        self.add_program_line(route_turning(color="white"))

        for (r, c, d, label), num in puzzle.text.items():
            validate_direction(r, c, d)
            validate_type(label, "normal")
            self.add_program_line(f"white({r}, {c}).")

            if isinstance(num, int):
                self.add_program_line(count_adjacent(num, (r, c), color="turning", adj_type="line", include_self=True))

        for (r, c, d, label), draw in puzzle.line.items():
            validate_type(label, "normal")
            self.add_program_line(f':-{" not" * draw} line_io({r}, {c}, "{d}").')

        self.add_program_line(display(item="line_io", size=3))

        return self.program
