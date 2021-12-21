from prawcore import NotFound
from booru.api import reddit


def subreddit_exists(subreddit_name):
    try:
        reddit.subreddits.search_by_name(subreddit_name, exact=True)
    except NotFound:
        return False
    return True


def get_subreddit_created(subreddit_name):
    """Assume subreddit exists."""
    subreddit = reddit.subreddit(subreddit_name)
    return int(subreddit.created_utc)
