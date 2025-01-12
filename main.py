"""Entry point for the noqx project."""

import argparse
import sys
import traceback
from typing import Any, Dict

import uvicorn
from starlette.applications import Starlette
from starlette.config import environ
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from noqx.logging import logger
from noqx.manager import list_solver_metadata, load_solvers, run_solver
from noqx.solution import Config


async def root_redirect(_: Request) -> RedirectResponse:
    """Redirect root page to penpa-edit page."""
    return RedirectResponse(url="/penpa-edit/")


async def list_puzzles_api(_: Request) -> JSONResponse:
    """List the available puzzles."""
    return JSONResponse(list_solver_metadata())


async def solver_api(request: Request) -> JSONResponse:
    """The solver endpoint of the server."""
    try:
        body = await request.json()
        puzzle_type: str = body["puzzle_type"]
        puzzle: str = body["puzzle"]
        param: Dict[str, Any] = body["param"]
        return JSONResponse(run_solver(puzzle_type, puzzle, param))
    except ValueError as err:
        logger.error(traceback.format_exc())
        return JSONResponse({"detail": str(err)}, status_code=400)
    except TimeoutError as err:
        return JSONResponse({"detail": str(err)}, status_code=504)
    except Exception as err:  # pylint: disable=broad-except  # pragma: no cover
        logger.error(traceback.format_exc())
        return JSONResponse({"detail": "Unknown error."}, status_code=500)


# load default solver directory
load_solvers("solver")

# argument parser
parser = argparse.ArgumentParser(description="noqx startup settings.")
parser.add_argument("-H", "--host", default="127.0.0.1", type=str, help="the host to run the server on.")
parser.add_argument("-p", "--port", default=8000, type=int, help="the port to run the server on.")
parser.add_argument("-d", "--debug", action="store_true", help="whether to enable debug mode with auto-reloading.")
parser.add_argument("-tl", "--time_limit", default=Config.time_limit, type=int, help="time limit in seconds.")
parser.add_argument("-pt", "--parallel_threads", default=Config.parallel_threads, type=int, help="parallel threads.")
args = parser.parse_args()
Config.time_limit = args.time_limit
Config.parallel_threads = args.parallel_threads

# logging setup
log_level = "DEBUG" if args.debug else "INFO"
log_format = "<g>{time:MM-DD HH:mm:ss}</g> | <lvl>{level}</lvl> | {message}"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"default": {"class": "noqx.logging.LoguruHandler", "level": log_level}},
    "loggers": {
        "uvicorn.error": {"handlers": ["default"], "level": log_level},
        "uvicorn.access": {"handlers": ["default"], "level": log_level},
    },
}
logger.remove()
logger.add(sys.stdout, level=log_level, diagnose=False, format=log_format)

# starlette app setup
routes = [
    Mount(
        "/api",
        name="api",
        routes=[
            Route("/list/", endpoint=list_puzzles_api, methods=["GET"]),
            Route("/solve/", endpoint=solver_api, methods=["POST"]),
        ],
    ),
    Mount("/penpa-edit/", StaticFiles(directory="static", html=True), name="static"),
    Route("/", root_redirect),
]
app = Starlette(routes=routes)
environ["DEBUG"] = "TRUE" if args.debug else "FALSE"

# start the server
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level=log_level.lower(),
        log_config=LOGGING_CONFIG,
    )
