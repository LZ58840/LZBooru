from greg.api import get_booru_subreddits


def GregDaemon(local_handler):
    get_booru_subreddits()
    local_handler.enter(60, 1, GregDaemon, (local_handler,))