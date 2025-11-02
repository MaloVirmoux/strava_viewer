"""Module used to setup the env and the parser logging level"""

import argparse
import logging
import os

os.environ["running_env"] = "container"


def setup_env():
    """Setup the parser logging level in the Flask app"""
    logging_levels = {
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "DEBUG": logging.DEBUG,
    }
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--loglevel", choices=list(logging_levels.keys()), default="INFO"
    )
    parser.add_argument(
        "--env", choices=["local", "container"], default=os.environ["running_env"]
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging_levels[args.loglevel])

    os.environ["running_env"] = args.env
