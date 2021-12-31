from greg.api import get_subreddits, post_submissions, post_links
from greg.proc import format_links, format_submissions, get_submissions


REFRESH_DELAY = 60


def GregDaemon(local_handler):
    subreddits = get_subreddits()
    submissions = get_submissions(subreddits)
    formatted_submissions = format_submissions(submissions)
    formatted_links = format_links(submissions)
    post_submissions(formatted_submissions)
    post_links(formatted_links)
    local_handler.enter(REFRESH_DELAY, 1, GregDaemon, (local_handler,))