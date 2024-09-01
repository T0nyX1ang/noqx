"""Main file for the noqx project."""

import argparse
import traceback
from typing import Any, Dict

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from solver import run_solver
from solver.core.const import PUZZLE_TYPES, logger


async def list_puzzles_api(_: Request) -> JSONResponse:
    """List the available puzzles."""
    return JSONResponse(PUZZLE_TYPES)


async def solver_api(request: Request) -> JSONResponse:
    """The solver endpoint of the server."""
    try:
        body = await request.json()
        puzzle_type: str = body["puzzle_type"]
        puzzle: str = body["puzzle"]
        param: Dict[str, Any] = body["param"]
        return JSONResponse(run_solver(puzzle_type, puzzle, param))
    except AssertionError as err:
        logger.error(traceback.format_exc())
        return JSONResponse({"detail": str(err)}, status_code=400)
    except TimeoutError as err:
        return JSONResponse({"detail": str(err)}, status_code=504)


parser = argparse.ArgumentParser(description="noqx startup settings.")
parser.add_argument("-H", "--host", default="127.0.0.1", type=str, help="the host to run the server on.")
parser.add_argument("-p", "--port", default=8000, type=int, help="the port to run the server on.")
parser.add_argument("-d", "--debug", action="store_true", help="whether to enable debug mode with auto-reloading.")
args = parser.parse_args()

routes = [
    Mount("/penpa-edit", StaticFiles(directory="penpa-edit/docs", html=True), name="penpa-edit"),
    Mount(
        "/api",
        name="api",
        routes=[
            Route("/list/", endpoint=list_puzzles_api, methods=["GET"]),
            Route("/solve/", endpoint=solver_api, methods=["POST"]),
        ],
    ),
    Mount("/", StaticFiles(directory="static", html=True), name="static"),
]

app = Starlette(debug=args.debug, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app="noqx:app", host=args.host, port=args.port, reload=args.debug, log_level="debug" if args.debug else "info")
