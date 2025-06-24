"""Test all solvers in Noqx."""

import logging
import pkgutil
import unittest

from noqx.clingo import Config, run_solver
from noqx.manager import list_solver_metadata, load_solver
from noqx.puzzle import Direction
from noqx.rule.common import count, fill_num, unique_num
from noqx.rule.helper import fail_false, validate_direction, validate_type
from noqx.rule.neighbor import adjacent
from noqx.rule.reachable import count_reachable_src
from noqx.rule.shape import all_rect, all_shapes, count_shape, general_shape, get_neighbor
from noqx.rule.variety import yaji_count
from solver.binairo import unique_linecolor
from solver.castle import wall_length
from solver.heyawake import limit_border
from solver.nagare import nagare_wind

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.CRITICAL)

for module_info in pkgutil.iter_modules(["solver"]):
    load_solver("solver", module_info.name)

metadata = list_solver_metadata()


class TestSolver(unittest.TestCase):
    """Test all solvers in Noqx."""

    def test_solver_timeout_error(self):
        """Test solver assertion error."""
        Config.time_limit = 0.5
        payload = "m=edit&p=7VVNa9tAEL3rV5Q9z0Gzu9bXzXXjXtz0wy4hCBEcVyEiNnL1UYqM/3tmRiIrQ2gphdYHI/R4sztv9GZ3JdXf23WVA4aABkwEPiBdQWRhYjQNR3L7w7Uqmm2evIFp2zyWFRGAj/M5PKy3de6lQ1bmHbo46abQvU9ShQqUphtVBt3n5NB9SNSm3N0XCrolzStAmlj0mZrolaM3Ms9s1g+iT/x64ERviW6KarPN7xb9yKck7Vag+GFvRc1U7cofuRrMcNwboIH7dUMd1Y/Ffpip22/lUzvkYnaEbvobz8Z5Ztp7ZvaKZ27l7z1v9+VrbuPseKSl/0J+75KUrX91NHJ0mRwIr5ODspakIQT97igbUWhfwommUAcuDk6mA59C9F/iiNV0dIYwZrUTxyxGN40+y50aNcuNiw3rxwLDFWIXWy6gRxWkm5EhDLmEM4whV3DtYiQdOI8YcQUn0CgenEKjdDHK0FzCVdBaPOjRwGlbWhbRdaX7VRwPnO6JDrjAqGC/kO6RRhYyGsVcwK2C8U931fRNDTEdBJTjcCs4F9SCKzot0BnBd4K+4ERwITlXgjeCM0ErGEhOyOftj07kP7CTWiufuF9dk0vGOWZkXqqWbfWw3uT0/ZuVu31ZF02u6Idz9NRPJTe9bAj28g/6j/8g3gb/3N77c7NDXyL11FZl05Qq854B"
        self.assertRaises(TimeoutError, run_solver, "kurotto", payload, {})
        Config.time_limit = 30

    def test_solver_api(self):
        """Test all available solvers. The tests should only return a unique solution."""
        for puzzle_name, puzzle_metadata in metadata.items():
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

                response = run_solver(puzzle_name, puzzle_example["data"], params)
                self.assertEqual(len(response["url"]), 1)

    def test_nonogram_edge_case(self):
        """Test nonogram edge case."""
        payload = "m=edit&p=7ZJBb7JAEIbv/Aqz5znsgvbTvVmrvVhai40xhBikGEkh9ANpmiX8d2cGjGnSSw9tPTTrvnmZnXWfnZ3yfxUWMdg4nCFIUDRUn+dA0u80lskhjXUPxtVhnxdoAO5nM9iFaRlbvuK9MrBqM9JmAeZW+0IJEDZOJQIwC12bO21cMB4uCXAwNm+TbLTTs13xOrlJG1QSvdt5tGu0UVJEabyZt5EH7ZslCDrnmneTFVn+FouOg76jPNsmFNiGB7xMuU9eu5Wyes5fqi5XBQ2YcYvrnXDplA6XyDtcsi0uuU9w6RbfjDsKmgbL/ojAG+0T+9PZDs/W0zWqq2uhBrRVIkv7NsKWHwKYpjh5zTpjtVmX+F9gHNYbVsk6YJ1zzpR1xTph7bNecc4/ovkS7w/g+LYKLF94VbELoxir7FbZNi56bl5kYSqwrRtLvAuevoNl6v91+i91Oj2BvLT+uTQc7OjAOgI="
        response = run_solver("nonogram", payload, {})
        self.assertEqual(len(response["url"]), 1)

    def test_nurimisaki_edge_case(self):
        """Test nurimisaki edge case."""
        payload = "m=edit&p=7ZLNb7JAEIfv/BVmznNgwfqxN2u1F0s/sDFmQwzyYiRCsSBNs4b/3dmBhIvprW96MMCTx5kx/NhM+VmFRYyCLneENstwYG7hmNtur2VySmPZw0l12ucFCeLzfI67MC1jS7VTgXXWY6knqB+lAgEIDj0CAtSv8qyfpPZQ+9QC7FNt0Qw5pLNOV9w3Nm2Kwib3Gh+QrkmjpIjSeLOgLlVepNJLBPOee/63UcjyrxjaHOZ3lGfbxBS24Yk+ptwnx7ZTVv/yQ9XOiqBGPWni+lfiul1co01cY78WNz3m14KOg7qmA3+jqBupTOr3Tked+vJM9JiCuWbOmQ5zSaOoXeYD02beMRc8M2OumFNmnzngmaF52V+Lo4QTWAr8qtiFUUyH6FXZNi56Xl5kYQq0r7UF38CPcmn1+7cV/u8rbA7fvi3yz3Fol+GjKpIsKcNDAoF1AQ=="
        response = run_solver("nurimisaki", payload, {})
        self.assertEqual(len(response["url"]), 1)

    def test_statuepark_all_shapes(self):
        """Test statuepark all shapes."""
        for shapeset in ["tetro", "pento", "double_tetro", "others"]:
            payload = "m=edit&p=7ZLNb7JAEIfv/BVmznNgwfqxN2u1F0s/sDFmQwzyYiRCsSBNs4b/3dmBhIvprW96MMCTx5kx/NhM+VmFRYyCLneENstwYG7hmNtur2VySmPZw0l12ucFCeLzfI67MC1jS7VTgXXWY6knqB+lAgEIDj0CAtSv8qyfpPZQ+9QC7FNt0Qw5pLNOV9w3Nm2Kwib3Gh+QrkmjpIjSeLOgLlVepNJLBPOee/63UcjyrxjaHOZ3lGfbxBS24Yk+ptwnx7ZTVv/yQ9XOiqBGPWni+lfiul1co01cY78WNz3m14KOg7qmA3+jqBupTOr3Tked+vJM9JiCuWbOmQ5zSaOoXeYD02beMRc8M2OumFNmnzngmaF52V+Lo4QTWAr8qtiFUUyH6FXZNi56Xl5kYQq0r7UF38CPcmn1+7cV/u8rbA7fvi3yz3Fol+GjKpIsKcNDAoF1AQ=="

            if shapeset == "others":
                self.assertRaises(ValueError, run_solver, "statuepark", payload, {"shapeset": shapeset})
                continue

            response = run_solver("statuepark", payload, {"shapeset": shapeset})
            self.assertEqual(len(response["url"]), 0)


class TestExtraFunction(unittest.TestCase):
    """Test extra functions in solvers."""

    def test_neighbor_adjacent(self):
        """Test neighbor adjacent."""
        self.assertRaises(ValueError, adjacent, "unknown")
        self.assertRaises(ValueError, adjacent, 1000)

    def test_shape_functions(self):
        """Test shape functions."""
        self.assertRaises(ValueError, all_rect, "not black", False)
        self.assertRaises(ValueError, all_shapes, "test", "black", "unknown")
        self.assertRaises(ValueError, count_shape, 0, "test", None, "black", "unknown")
        self.assertRaises(ValueError, general_shape, "test", 0, [(0, 0)], "black", "unknown", 4, False)
        self.assertRaises(ValueError, general_shape, "test", 0, None, "black", "grid", 4, False)
        self.assertRaises(ValueError, get_neighbor, 0, 0, "unknown")
        self.assertRaises(ValueError, get_neighbor, 0, 0, 1000)

    def test_binairo_unique_linecolor(self):
        """Test binairo unique linecolor."""
        self.assertRaises(ValueError, unique_linecolor, ["color1", "color2"], "unknown")

    def test_yaji_yajikazu_count(self):
        """Test yajilin count and yajikazu count."""
        self.assertRaises(ValueError, yaji_count, 0, (0, 0), 5, "black")
        self.assertRaises(ValueError, yaji_count, 0, (0, 0), -1, "black")

    def test_heyawake_limit_border(self):
        """Test heyawake limit border."""
        self.assertRaises(ValueError, limit_border, 0, [(0, 0)], None, "unknown")

    def test_castle_wall_length(self):
        """Test castle wall length."""
        self.assertRaises(ValueError, wall_length, 0, 0, 4, 1)

    def test_nagare_wind(self):
        """Test nagare wind."""
        self.assertRaises(ValueError, nagare_wind, 0, 0, "unknown", None)

    def test_validation(self):
        """Test validation functions in helper."""
        self.assertRaises(ValueError, validate_direction, 0, 0, Direction.LEFT)
        self.assertRaises(ValueError, validate_direction, 0, 0, Direction.CENTER, Direction.LEFT)
        self.assertRaises(ValueError, validate_type, None, "any")
        self.assertRaises(ValueError, validate_type, "unknown", "known")
        self.assertRaises(ValueError, validate_type, "unknown", ("known", "something", "other"))
        self.assertRaises(ValueError, fail_false, isinstance("?", int), "This is not an integer.")

    def test_common_rules(self):
        """Test common rules."""
        self.assertRaises(ValueError, fill_num, [0], "unknown", 0, "unknown")
        self.assertRaises(ValueError, unique_num, "black", "unknown")
        self.assertRaises(ValueError, count, 0, "black", "unknown", None)

    def test_reachable_rules(self):
        """Test reachable rules."""
        self.assertRaises(ValueError, count_reachable_src, 0, (0, 0), "unknown")
