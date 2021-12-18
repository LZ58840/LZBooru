from time import time, sleep
from sched import scheduler
from greg import GregDaemon


handler = scheduler(time, sleep)
handler.enter(0, 1, GregDaemon, (handler,))
handler.run()
