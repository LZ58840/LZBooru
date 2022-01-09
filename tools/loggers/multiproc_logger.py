import logging
from logging.handlers import QueueHandler
from time import sleep
from dotenv import dotenv_values
from tools.loggers import LOG_LEVEL


config = dotenv_values(".env")


def listener_config():
    root = logging.getLogger()
    if len(root.handlers) > 0:
        root.handlers.clear()
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt=config["LOG_FMT"], datefmt=config["LOG_DATEFMT"])
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)
    root.setLevel(LOG_LEVEL[config["LOG_LEVEL"]])


def listener_process(queue):
    listener_config()
    while True:
        while not queue.empty():
            record = queue.get()
            logger = logging.getLogger(record.name)
            logger.handle(record)
        sleep(1)


def worker_config(queue):
    h = QueueHandler(queue)
    root = logging.getLogger()
    if len(root.handlers) > 0:
        root.handlers.clear()
    root.addHandler(h)
    root.setLevel(LOG_LEVEL[config["LOG_LEVEL"]])
