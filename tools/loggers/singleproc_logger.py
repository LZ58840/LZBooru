import logging
from dotenv import dotenv_values
from tools.loggers import LOG_LEVEL


config = dotenv_values(".env")


def log_config():
    """Configures logger with given formatting."""

    root = logging.getLogger()
    if len(root.handlers) > 0:
        root.handlers.clear()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt=config["LOG_FMT"], datefmt=config["LOG_DATEFMT"])
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    root.setLevel(LOG_LEVEL[config["LOG_LEVEL"]])