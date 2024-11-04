"""Initialization for the Noqx application."""

import traceback
from typing import Any, Dict

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from .logging import logger
from .manager import list_solver_metadata, run_solver


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
    except AssertionError as err:
        logger.error(traceback.format_exc())
        return JSONResponse({"detail": str(err)}, status_code=400)
    except TimeoutError as err:
        return JSONResponse({"detail": str(err)}, status_code=504)


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
