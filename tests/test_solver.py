"""Test all solvers in Noqx."""

from starlette.testclient import TestClient

from solver import list_solver_metadata

metadata = list_solver_metadata()


with open("static/index.html", encoding="utf-8") as f:
    index_page = f.read()


def test_root(client: TestClient):
    """Test root page redirection."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == index_page


def test_list_solver_metadata(client: TestClient):
    """Test list solver metadata API."""
    response = client.get("/api/list/")
    assert response.status_code == 200
    assert response.json() == metadata


def test_solver_api(client: TestClient):
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

            response = client.post(
                "/api/solve/",
                json={"puzzle_type": puzzle_type, "puzzle": puzzle_example["data"], "param": params},
            )

            assert response.status_code == 200
            assert len(response.json()["url"]) == 1
