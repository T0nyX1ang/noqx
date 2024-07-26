"""Main file for the noqx project."""

import argparse
import traceback

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from solver import run_solver

app = FastAPI(title="noqx", description="An extended logic puzzle solver.")

app.mount("/penpa-edit", StaticFiles(directory="penpa-edit/docs", html=True), name="penpa-edit")
app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/solver/", response_class=HTMLResponse)
def solver(puzzle_type: str, puzzle: str):  # clingo might be incompatible with asyncio
    """The solver endpoint of the server."""
    try:
        return run_solver(puzzle_type, puzzle)
    except ValueError as err:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(err)) from err


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="noqx startup settings.")
    parser.add_argument("-H", "--host", default="127.0.0.1", type=str, help="The host to run the server on.")
    parser.add_argument("-p", "--port", default=8000, type=int, help="The port to run the server on.")
    parser.add_argument("-r", "--reload", action="store_true", help="Whether to reload the server on changes.")
    parser.add_argument("-l", "--log-level", default="info", type=str, help="The log level of the server.")
    args = parser.parse_args()

    uvicorn.run(app="noqx:app", host=args.host, port=args.port, reload=args.reload, log_level=args.log_level)
