"""
Main file for the noqx project.

execute "uvicorn noqx:app" to start the server.
"""


import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from solvers.utilsx import run
from solvers.utilsx.consts import CATEGORIES, PUZZLE_TYPES

app = FastAPI(title="noqx", description="An extended logic puzzle solver.")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    """The root endpoint of the server."""
    context = {"types": PUZZLE_TYPES, "cats": CATEGORIES}
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/{puzzle_type}", response_class=HTMLResponse)
async def puzzle_page(request: Request, puzzle_type: str):
    """The puzzle endpoint of the server."""
    for _pt_dict in PUZZLE_TYPES:
        if _pt_dict["value"] == puzzle_type:
            context = {"name": _pt_dict["name"], "value": _pt_dict["value"]}
            return templates.TemplateResponse(request=request, name="noq.html", context=context)

        if "aliases" in _pt_dict and puzzle_type in _pt_dict["aliases"]:
            return RedirectResponse(url=f"/{_pt_dict['value']}")


@app.get("/solver/", response_class=HTMLResponse)
def solver(puzzle_type: str, puzzle: str):  # clingo might be incompatible with asyncio
    """The solver endpoint of the server."""
    try:
        return run(puzzle_type, puzzle)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


if __name__ == "__main__":
    uvicorn.run(app="noqx:app", host="127.0.0.1", port=8000, reload=False)
