from greg.api import get_subreddits, post_submissions, update_subreddits
from greg.proc import format_submissions, get_submissions


def GregDaemon(local_handler):
    subreddits = get_subreddits()
    submissions = get_submissions(subreddits)
    formatted_submissions = format_submissions(submissions)
    post_submissions(formatted_submissions)
    update_subreddits(subreddits)
    local_handler.enter(60, 1, GregDaemon, (local_handler,))