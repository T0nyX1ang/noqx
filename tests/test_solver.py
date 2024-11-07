"""Test all solvers in Noqx."""

import unittest

from starlette.config import environ
from starlette.testclient import TestClient

from noqx import app
from noqx.manager import list_solver_metadata
from noqx.rule.neighbor import adjacent
from noqx.rule.shape import all_shapes, count_shape, general_shape, get_neighbor
from noqx.solution import Config
from solver.binairo import unique_linecolor
from solver.yajikazu import yajikazu_count
from solver.yajilin import yajilin_count

environ["DEBUG"] = "TRUE"
metadata = list_solver_metadata()


with open("static/index.html", encoding="utf-8") as f:
    index_page = f.read()


class TestSolver(unittest.TestCase):
    """Test all solvers in Noqx."""

    @classmethod
    def setUpClass(cls):
        """Initialize the test client."""
        cls.client = TestClient(app)

    def test_root(self):
        """Test root page redirection."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, index_page)

    def test_list_solver_metadata(self):
        """Test list solver metadata API."""
        response = self.client.get("/api/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), metadata)

    def test_solver_assertion_error(self):
        """Test solver assertion error."""
        payload = "m=edit&p=7VZBz5pAEL3zK8ye58CKCu5NrX4Xi22xsWZDCCp+mkqwIM2XJfx3Z4dtuNg07cG2CVl4eTszj33s7mGKb2WcJ+DY9HhgA9eDu54Bl48asM1Yn2+XRPRgUt5OWY4EYLVYwDG+FIklTVVoVWos1ATUi5CMM2B9fDkLQX0UlXovlA8qwBQDjrFlU9RHOm/phvKazZogt5H7hiPdIt3FN/RTnM7XaNpEPwip1sD0WlP6gqYszb4nzHjR832W7s460H7AZIrykH0tTS0Pa1CTxnLwwLLTWta0sazZA8v6T55geRzWNW7/JzQdCan9f26p19JAVIi+qBi3vaEWf0E3dEoY55TdEi4I+4RrFINyCN8R2oRDwiXVzAk3hDPCAeGIaly9/G8ZfIId6Zqb/0dj2Gk7bafttJ220/7f2tCSLCjzY7xPsLmYH16Tnp/laXzBmV+muyT/Mccer7bYG6NXOigedG3fX2779FHY/1pv9Qs7EndYd6CgVsCuZRRH+wxvG+7gTzNP/wNsEEPrDg=="
        response = self.client.post(
            "/api/solve/",
            json={"puzzle_type": "aqre", "puzzle": payload, "param": {}},
        )
        self.assertEqual(response.status_code, 400)

    def test_solver_timeout_error(self):
        """Test solver assertion error."""
        Config.time_limit = 0.5
        payload = "m=edit&p=7VVNa9tAEL3rV5Q9z0Gzu9bXzXXjXtz0wy4hCBEcVyEiNnL1UYqM/3tmRiIrQ2gphdYHI/R4sztv9GZ3JdXf23WVA4aABkwEPiBdQWRhYjQNR3L7w7Uqmm2evIFp2zyWFRGAj/M5PKy3de6lQ1bmHbo46abQvU9ShQqUphtVBt3n5NB9SNSm3N0XCrolzStAmlj0mZrolaM3Ms9s1g+iT/x64ERviW6KarPN7xb9yKck7Vag+GFvRc1U7cofuRrMcNwboIH7dUMd1Y/Ffpip22/lUzvkYnaEbvobz8Z5Ztp7ZvaKZ27l7z1v9+VrbuPseKSl/0J+75KUrX91NHJ0mRwIr5ODspakIQT97igbUWhfwommUAcuDk6mA59C9F/iiNV0dIYwZrUTxyxGN40+y50aNcuNiw3rxwLDFWIXWy6gRxWkm5EhDLmEM4whV3DtYiQdOI8YcQUn0CgenEKjdDHK0FzCVdBaPOjRwGlbWhbRdaX7VRwPnO6JDrjAqGC/kO6RRhYyGsVcwK2C8U931fRNDTEdBJTjcCs4F9SCKzot0BnBd4K+4ERwITlXgjeCM0ErGEhOyOftj07kP7CTWiufuF9dk0vGOWZkXqqWbfWw3uT0/ZuVu31ZF02u6Idz9NRPJTe9bAj28g/6j/8g3gb/3N77c7NDXyL11FZl05Qq854B"
        response = self.client.post(
            "/api/solve/",
            json={"puzzle_type": "kurotto", "puzzle": payload, "param": {}},
        )
        self.assertEqual(response.status_code, 504)
        Config.time_limit = 30

    def test_solver_api(self):
        """Test all available solvers. The tests should only return a unique solution."""
        for puzzle_type, puzzle_metadata in metadata.items():
            default_params = puzzle_metadata.get("parameters", {})

            for puzzle_example in puzzle_metadata.get("examples", []):
                if puzzle_example.get("test") is False or puzzle_example.get("url"):
                    continue  # ignore test cases with url option or test flag is set to False

                # replace default values with actual configuration values
                puzzle_config = puzzle_example.get("config", {})
                params = {k: v["default"] if k not in puzzle_config else puzzle_config[k] for k, v in default_params.items()}

                for k, v in params.items():
                    v_str = str(v)
                    if v_str.isdigit():
                        params[k] = v_str

                response = self.client.post(
                    "/api/solve/",
                    json={"puzzle_type": puzzle_type, "puzzle": puzzle_example["data"], "param": params},
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.json()["url"]), 1)

    def test_nonogram_edge_case(self):
        """Test nonogram edge case."""
        payload = "m=edit&p=7ZJBb7JAEIbv/Aqz5znsgvbTvVmrvVhai40xhBikGEkh9ANpmiX8d2cGjGnSSw9tPTTrvnmZnXWfnZ3yfxUWMdg4nCFIUDRUn+dA0u80lskhjXUPxtVhnxdoAO5nM9iFaRlbvuK9MrBqM9JmAeZW+0IJEDZOJQIwC12bO21cMB4uCXAwNm+TbLTTs13xOrlJG1QSvdt5tGu0UVJEabyZt5EH7ZslCDrnmneTFVn+FouOg76jPNsmFNiGB7xMuU9eu5Wyes5fqi5XBQ2YcYvrnXDplA6XyDtcsi0uuU9w6RbfjDsKmgbL/ojAG+0T+9PZDs/W0zWqq2uhBrRVIkv7NsKWHwKYpjh5zTpjtVmX+F9gHNYbVsk6YJ1zzpR1xTph7bNecc4/ovkS7w/g+LYKLF94VbELoxir7FbZNi56bl5kYSqwrRtLvAuevoNl6v91+i91Oj2BvLT+uTQc7OjAOgI="

        response = self.client.post(
            "/api/solve/",
            json={"puzzle_type": "nonogram", "puzzle": payload, "param": {}},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["url"]), 1)


class TestExtraFunction(unittest.TestCase):
    """Test extra functions in solvers."""

    def test_neighbor_adjacent(self):
        """Test neighbor adjacent."""
        self.assertRaises(AssertionError, adjacent, "unknown")
        self.assertRaises(AssertionError, adjacent, 1000)

    def test_shape_functions(self):
        """Test shape functions."""
        self.assertRaises(AssertionError, all_shapes, "test", "black", "unknown")
        self.assertRaises(AssertionError, count_shape, 0, "test", None, "black", "unknown")
        self.assertRaises(AssertionError, general_shape, "test", 0, [(0, 0)], "black", "unknown", 4, False)
        self.assertRaises(AssertionError, general_shape, "test", 0, None, "black", "grid", 4, False)
        self.assertRaises(AssertionError, get_neighbor, 0, 0, "unknown")
        self.assertRaises(AssertionError, get_neighbor, 0, 0, 1000)

    def test_binairo_unique_linecolor(self):
        """Test binairo unique linecolor."""
        self.assertRaises(AssertionError, unique_linecolor, ["color1", "color2"], "unknown")

    def test_yajilin_yajikazu_count(self):
        """Test yajilin count and yajikazu count."""
        self.assertRaises(AssertionError, yajilin_count, 0, (0, 0), 5, "black")
        self.assertRaises(AssertionError, yajilin_count, 0, (0, 0), -1, "black")
        self.assertRaises(AssertionError, yajikazu_count, 0, (0, 0), 5, "black")
        self.assertRaises(AssertionError, yajikazu_count, 0, (0, 0), -1, "black")
