import logging
from time import time, sleep
from sched import scheduler
from greg import greg_daemon
from tools.loggers.singleproc_logger import log_config


log_config()
handler = scheduler(time, sleep)
handler.enter(0, 1, greg_daemon, (handler,))
logging.info("Starting Aggregator...")
handler.run()
