"""Entry point for the noqx project."""

import argparse
import sys

import uvicorn
from starlette.config import environ

from noqx.logging import logger
from noqx.manager import load_solvers
from noqx.solution import Config

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
logger.add(sys.stdout, level=log_level, diagnose=False, format=log_format)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"default": {"class": "noqx.logging.LoguruHandler", "level": log_level}},
    "loggers": {
        "uvicorn.error": {"handlers": ["default"], "level": log_level},
        "uvicorn.access": {
            "handlers": ["default"],
            "level": log_level,
        },
    },
}

if __name__ == "__main__":
    environ["DEBUG"] = "TRUE" if args.debug else "FALSE"
    uvicorn.run(
        app="noqx:app",
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level=log_level.lower(),
        log_config=LOGGING_CONFIG,
    )
