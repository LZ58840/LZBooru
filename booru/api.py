from prawcore import NotFound
from api import praw_api


def subreddit_exists(subreddit_name):
    try:
        praw_api.subreddits.search_by_name(subreddit_name, exact=True)
    except NotFound:
        return False
    return True


def get_subreddit_created(subreddit_name):
    """Assume subreddit exists."""
    subreddit = praw_api.subreddit(subreddit_name)
    return int(subreddit.created_utc)
