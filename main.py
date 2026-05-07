"""Entry point for the noqx project."""

import argparse
import json
import logging
import os
import pkgutil
import shutil
import sys
import traceback
from typing import Any, Dict

from noqx.clingo import Config, run_solver
from noqx.manager import list_solver_metadata, load_solver

# argument parser
parser = argparse.ArgumentParser(description="Noqx startup settings.")
parser.add_argument("-H", "--host", default="127.0.0.1", type=str, help="the host to run the server on.")
parser.add_argument("-p", "--port", default=8000, type=int, help="the port to run the server on.")
parser.add_argument("-d", "--debug", action="store_true", help="whether to enable debug mode with auto-reloading.")
parser.add_argument("-tl", "--time-limit", default=Config.time_limit, type=int, help="time limit in seconds.")
parser.add_argument("-pt", "--parallel-threads", default=Config.parallel_threads, type=int, help="parallel threads.")
parser.add_argument("-B", "--build-document", action="store_true", help="build the documentation site.")
parser.add_argument("-D", "--deployment-mode", action="store_true", help="enable deployment mode for static sites.")
parser.add_argument("-O", "--offline-mode", action="store_true", help="enable offline mode.")
args = parser.parse_args()
Config.time_limit = args.time_limit
Config.parallel_threads = args.parallel_threads

# logging setup
log_level = "DEBUG" if args.debug else "INFO"
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=log_level)

if not os.path.exists("./penpa-edit/js/config.js"):
    logging.info("Creating default configuration.")
    with open("./penpa-edit/js/config.js", "w", encoding="utf-8", newline="\n") as f:
        f.write("const DEPLOYMENT_MODE = false;\n")
        f.write("const OFFLINE_MODE = true;")

if __name__ == "main" or (__name__ == "__main__" and args.deployment_mode):
    if args.build_document:
        # build the documentation site
        try:
            from mkdocs.commands import build
            from mkdocs.config import load_config
        except ImportError:
            logging.error("mkdocs is not installed. Please install the 'docs' optional dependencies.")
            sys.exit(1)

        config = load_config()
        build.build(config)
    else:
        # build an empty redirect page
        shutil.rmtree("./site", ignore_errors=True)
        os.makedirs("./site", exist_ok=True)
        with open("./site/index.html", "w", encoding="utf-8", newline="\n") as f:
            f.write('<html><head><meta http-equiv="refresh" content="0; url=./penpa-edit/"></head><body></body></html>')

    if args.offline_mode:
        # fetch penpa-edit core resources for offline usage
        with open("./penpa-edit/js/penpa_loader.js", encoding="utf-8", newline="\n") as f:
            penpa_loader_content = f.read()
            penpa_hash_index = penpa_loader_content.find("penpa_edit_hash = ")

            if penpa_hash_index == -1:
                logging.error("Failed to find the penpa-edit hash in penpa_loader.js.")
                sys.exit(1)

            from urllib.request import urlopen

            penpa_hash_start = penpa_hash_index + len("penpa_edit_hash = ")
            penpa_hash_end = penpa_loader_content.find(";", penpa_hash_start)
            penpa_edit_hash = penpa_loader_content[penpa_hash_start:penpa_hash_end].strip().strip('"').strip("'")
            penpa_edit_url = f"https://github.com/swaroopg92/penpa-edit/archive/{penpa_edit_hash}.zip"
            os.makedirs("./build/", exist_ok=True)

            if os.path.exists(f"./build/penpa-edit-{penpa_edit_hash}/"):
                logging.debug("Penpa-edit resources already exist. Skipping download.")
            else:
                logging.debug(f"Fetching penpa-edit repository at {penpa_edit_hash[:7]} ...")
                try:
                    with urlopen(penpa_edit_url) as response, open("./build/penpa-edit.zip", "wb") as out_file:
                        shutil.copyfileobj(response, out_file)
                    shutil.unpack_archive("./build/penpa-edit.zip", "./build/")
                    os.remove("./build/penpa-edit.zip")
                except Exception as e:
                    logging.error(f"Failed to fetch penpa-edit resources: {e}")
                    sys.exit(1)

            os.makedirs("./penpa-edit/core", exist_ok=True)
            existing_hash = None
            if os.path.exists("./penpa-edit/core/.hash"):
                with open("./penpa-edit/core/.hash", encoding="utf-8", newline="\n") as f:
                    existing_hash = f.read().strip()

            if existing_hash == penpa_edit_hash:
                logging.debug("Penpa-edit resources are up to date. Skipping copy.")
            else:
                logging.debug("Copying penpa-edit resources...")
                penpa_css_index = penpa_loader_content.find("penpa_style_sources = ")
                if penpa_css_index == -1:
                    logging.error("Failed to find the penpa-edit style sources in penpa_loader.js.")
                    sys.exit(1)

                penpa_css_start = penpa_css_index + len("penpa_style_sources = ")
                penpa_css_end = penpa_loader_content.find(";", penpa_css_start)
                penpa_style_sources_str = penpa_loader_content[penpa_css_start:penpa_css_end].strip("[").strip("]").strip()
                penpa_style_sources = [
                    s.strip().strip('"').strip("'") for s in penpa_style_sources_str.split(",") if s.strip()
                ]
                os.makedirs("./penpa-edit/core/css", exist_ok=True)

                for css_file in penpa_style_sources:
                    source_path = f"./build/penpa-edit-{penpa_edit_hash}/docs/{css_file}"
                    target_path = f"./penpa-edit/core/{css_file}"
                    shutil.copy(source_path, target_path)

                penpa_js_index = penpa_loader_content.find("penpa_script_sources = ")
                if penpa_js_index == -1:
                    logging.error("Failed to find the penpa-edit script sources in penpa_loader.js.")
                    sys.exit(1)

                penpa_js_start = penpa_js_index + len("penpa_script_sources = ")
                penpa_js_end = penpa_loader_content.find(";", penpa_js_start)
                penpa_script_sources_str = penpa_loader_content[penpa_js_start:penpa_js_end].strip("[").strip("]").strip()
                penpa_script_sources = [
                    s.strip().strip('"').strip("'") for s in penpa_script_sources_str.split(",") if s.strip()
                ]
                os.makedirs("./penpa-edit/core/js", exist_ok=True)
                os.makedirs("./penpa-edit/core/js/libs", exist_ok=True)

                for js_file in penpa_script_sources:
                    source_path = f"./build/penpa-edit-{penpa_edit_hash}/docs/{js_file}"
                    target_path = f"./penpa-edit/core/{js_file}"
                    shutil.copy(source_path, target_path)

                with open("./penpa-edit/core/.hash", "w", encoding="utf-8", newline="\n") as f:
                    f.write(penpa_edit_hash)

        with open("./penpa-edit/js/config.js", encoding="utf-8", newline="\n") as f:
            fin = f.read()

        with open("./penpa-edit/js/config.js", "w", encoding="utf-8", newline="\n") as f:
            f.write(fin.replace("OFFLINE_MODE = false", "OFFLINE_MODE = true"))
    else:
        with open("./penpa-edit/js/config.js", encoding="utf-8", newline="\n") as f:
            fin = f.read()

        with open("./penpa-edit/js/config.js", "w", encoding="utf-8", newline="\n") as f:
            f.write(fin.replace("OFFLINE_MODE = true", "OFFLINE_MODE = false"))

    # load the solvers
    logging.debug("Loading solvers...")
    for module_info in pkgutil.iter_modules(["solver"]):
        load_solver("solver", module_info.name)

    with open("penpa-edit/js/solver_metadata.js", "w", encoding="utf-8", newline="\n") as f:
        # dump the metadata to a javascript file for further import
        logging.debug("Dumping solver metadata...")
        f.write(f"const solver_metadata = {json.dumps(list_solver_metadata(), indent=2)};")
        f.write("window.puzzle_list = Object.keys(solver_metadata);")

    with open("./penpa-edit/js/config.js", encoding="utf-8", newline="\n") as f:
        fin = f.read()

    with open("./penpa-edit/js/config.js", "w", encoding="utf-8", newline="\n") as f:
        f.write(fin.replace("DEPLOYMENT_MODE = true", "DEPLOYMENT_MODE = false"))

if args.deployment_mode:
    # generate files if needed
    shutil.rmtree("./dist/page", ignore_errors=True)
    os.makedirs("./dist/page/penpa-edit", exist_ok=True)

    target_dirs = ["noqx", "noqx/puzzle", "noqx/rule", "solver"]
    for dirname in target_dirs:
        os.makedirs(f"dist/page/penpa-edit/py/{dirname}", exist_ok=True)

    pyscript_config = {
        "files": {},
        "plugins": ["!codemirror", "!deprecation-manager", "!donkey", "!error", "!py-editor", "!py-game", "!py-terminal"],
    }
    for dirname in ["noqx", "noqx/puzzle", "noqx/rule", "solver"]:
        for filename in os.listdir(dirname):
            if filename.endswith(".py") and filename != "clingo.py":
                pyscript_config["files"][f"./py/{dirname}/{filename}"] = f"{dirname}/{filename}"
                shutil.copy(f"./{dirname}/{filename}", f"./dist/page/penpa-edit/py/{dirname}/{filename}")

    with open("pyscript.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(pyscript_config, f, indent=2)

    with open("./penpa-edit/js/config.js", "w", encoding="utf-8", newline="\n") as f:
        f.write(fin.replace("DEPLOYMENT_MODE = false", "DEPLOYMENT_MODE = true"))

    shutil.copy("./pyscript.json", "./dist/page/penpa-edit/pyscript.json")
    shutil.copy("./main_deploy.py", "./dist/page/penpa-edit/py/main_deploy.py")
    shutil.copytree("./penpa-edit/", "./dist/page/penpa-edit/", dirs_exist_ok=True)
    shutil.copytree("./site/", "./dist/page/", dirs_exist_ok=True)
else:
    # starlette app setup
    try:
        import uvicorn
        from starlette.applications import Starlette
        from starlette.config import environ
        from starlette.requests import Request
        from starlette.responses import JSONResponse
        from starlette.routing import Mount, Route
        from starlette.staticfiles import StaticFiles
    except ImportError:
        logging.error("starlette or uvicorn is not installed. Please install the 'web' optional dependencies.")
        sys.exit(1)

    async def solver_api(request: Request) -> JSONResponse:
        """The solver endpoint of the server."""
        try:
            body = await request.json()
            puzzle_name: str = body["puzzle_name"]
            puzzle: str = body["puzzle"]
            param: Dict[str, Any] = body["param"]
            result = run_solver(puzzle_name, puzzle, param)
            return JSONResponse(result)
        except ValueError as err:
            logging.error(traceback.format_exc())
            return JSONResponse({"detail": str(err)}, status_code=400)
        except TimeoutError as err:
            return JSONResponse({"detail": str(err)}, status_code=504)
        except Exception:  # pragma: no cover
            logging.error(traceback.format_exc())
            return JSONResponse({"detail": "Unknown error."}, status_code=500)

    routes = [
        Mount(
            "/api",
            name="api",
            routes=[Route("/solve/", endpoint=solver_api, methods=["POST"])],
        ),
        Mount("/penpa-edit/", StaticFiles(directory="penpa-edit", html=True), name="penpa-edit"),
        Mount("/", StaticFiles(directory="site", html=True), name="docs"),
    ]
    app = Starlette(routes=routes)
    environ["DEBUG"] = "TRUE" if args.debug else "FALSE"

    # start the server
    if __name__ == "__main__":
        UVICORN_LOGGING_CONFIG = {
            "version": 1,
            "disable_existing_loggers": True,
            "handlers": {"default": {"class": "logging.NullHandler", "level": log_level}},
            "loggers": {
                "uvicorn.error": {"handlers": ["default"], "level": log_level},
                "uvicorn.access": {"handlers": ["default"], "level": log_level},
            },
        }

        uvicorn.run(
            app="main:app",
            host=args.host,
            port=args.port,
            reload=args.debug,
            log_level=log_level.lower(),
            log_config=UVICORN_LOGGING_CONFIG,
        )
