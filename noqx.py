"""Main file for the noqx project."""

import argparse

import uvicorn
from starlette.config import environ

from noqx.manager import load_solvers
from noqx.solution import Config

load_solvers("solver")  # default solver directory

parser = argparse.ArgumentParser(description="noqx startup settings.")
parser.add_argument("-H", "--host", default="127.0.0.1", type=str, help="the host to run the server on.")
parser.add_argument("-p", "--port", default=8000, type=int, help="the port to run the server on.")
parser.add_argument("-d", "--debug", action="store_true", help="whether to enable debug mode with auto-reloading.")
parser.add_argument("-tl", "--time_limit", default=Config.time_limit, type=int, help="time limit in seconds.")
parser.add_argument("-pt", "--parallel_threads", default=Config.parallel_threads, type=int, help="parallel threads.")
args = parser.parse_args()
Config.time_limit = args.time_limit
Config.parallel_threads = args.parallel_threads

if __name__ == "__main__":
    environ["DEBUG"] = "TRUE" if args.debug else "FALSE"
    uvicorn.run(app="noqx:app", host=args.host, port=args.port, reload=args.debug, log_level="debug" if args.debug else "info")
