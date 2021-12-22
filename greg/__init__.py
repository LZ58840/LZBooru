from greg.api import get_subreddits
from greg.proc import get_submissions


def GregDaemon(local_handler):
    booru_subreddits_json = get_subreddits()
    pushshift_submissions_json = get_submissions(booru_subreddits_json)
    local_handler.enter(60, 1, GregDaemon, (local_handler,))