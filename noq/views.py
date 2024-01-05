"""The view for the Noq(x) website."""

import json
import traceback
from typing import Any, Mapping

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.urls import URLPattern, path
from django.views.generic.base import RedirectView

from solvers import *
from solvers.claspy import reset
from static.consts import cats as CATS
from static.consts import types as PUZZLE_TYPES


def create_view(pt_map: Mapping[str, Any]):
    """Create a view for a puzzle type."""
    return lambda request: render(request, "./noq.html", pt_map)


def redirect_view(red_url: URLPattern):
    """Create a redirect view."""
    return RedirectView.as_view(url=red_url)


urlpatterns = []

# index page
types_by_cat = {}

for pt_dict in PUZZLE_TYPES:
    cat = pt_dict["cat"]
    if cat not in types_by_cat:
        types_by_cat[cat] = []
    types_by_cat[cat].append(pt_dict)

for cat in types_by_cat:
    types_by_cat[cat] = sorted(types_by_cat[cat], key=lambda d: d["name"])

urlpatterns.append(
    path(
        route="",
        view=lambda request: render(
            request, "./index.html", {"types": types_by_cat, "cats": CATS}
        ),
    )
)

# solver pages
for pt_dict in PUZZLE_TYPES:
    value = pt_dict["value"]
    name = pt_dict["name"]

    urlpatterns.append(
        path(route=value, view=create_view(pt_dict), name=f"{name} solver - Noq")
    )  # we have to use another function here because of closures

    if "aliases" in pt_dict:
        for alias in pt_dict["aliases"]:
            urlpatterns.append(path(route=alias, view=redirect_view(pt_dict["value"])))


# internal/custom views
def solver(request):
    """Solver view."""
    try:
        reset()
        module = globals()[request.GET["puzzle_type"]]
        puzzle_encoding = module.encode(request.GET["puzzle"])
        solutions_encoded = module.solve(puzzle_encoding)
        solutions_decoded = module.decode(solutions_encoded)
        return HttpResponse(solutions_decoded)
    # show error messages
    except ValueError as err:
        print(traceback.print_exc(), flush=True)
        return HttpResponseBadRequest(json.dumps({"message": str(err)}))
    except Exception as exc:
        print(traceback.print_exc(), flush=True)
        return HttpResponseServerError(json.dumps({"message": str(exc)}))


# append internal urlpatterns
urlpatterns += [
    path("solver", solver, name="solver"),
]
