from time import time, sleep
from sched import scheduler
from parsa import ParsaImgurDaemon, ParsaRedditDaemon, ParsaGenericDaemon


handler = scheduler(time, sleep)
handler.enter(0, 1, ParsaImgurDaemon, (handler,))
handler.enter(0, 1, ParsaRedditDaemon, (handler,))
handler.enter(0, 1, ParsaGenericDaemon, (handler,))
handler.run()